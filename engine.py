from math import ceil
from PIL import Image, ImageFile
import os
import zipfile
import shutil
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import tempfile
import img2pdf
import numpy as np
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

# Register AVIF opener at module level so it is available to ALL functions
# (including get_image_size_fast for the fast-dimension pass).
# Without this, get_image_size_fast returns (0,0) for AVIF files, causing
# them to be silently skipped in normal (non-AI-enhance) mode.
try:
    from pillow_heif import register_avif_opener
    register_avif_opener()
except ImportError:
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass

IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "avif", "psd"}

# WebP cannot encode an image taller or wider than this. Any slice that exceeds
# it fails to save (silently aborting the worker thread), so for WebP output the
# cut points are capped to guarantee every slice stays within the limit.
WEBP_MAX_DIMENSION = 16383


# Watermark cache to avoid loading and resizing from disk repeatedly
_WATERMARK_CACHE = {}
_RESIZED_WM_CACHE = {}


def _get_cached_watermark(watermark_path):
    global _WATERMARK_CACHE
    if watermark_path in _WATERMARK_CACHE:
        return _WATERMARK_CACHE[watermark_path]
    try:
        with Image.open(watermark_path) as wm_orig:
            if wm_orig.mode != 'RGBA':
                loaded = wm_orig.convert('RGBA')
            else:
                loaded = wm_orig.copy()
            _WATERMARK_CACHE[watermark_path] = loaded
            return loaded
    except Exception as e:
        print(f"Error loading watermark {watermark_path}: {e}")
        return None


def _get_resized_watermark(watermark_path, target_w, target_h):
    global _RESIZED_WM_CACHE
    cache_key = (watermark_path, target_w, target_h)
    if cache_key in _RESIZED_WM_CACHE:
        return _RESIZED_WM_CACHE[cache_key]
    wm_orig = _get_cached_watermark(watermark_path)
    if wm_orig is None:
        return None
    try:
        resized = wm_orig.resize((target_w, target_h), Image.Resampling.LANCZOS)
        _RESIZED_WM_CACHE[cache_key] = resized
        return resized
    except Exception as e:
        print(f"Error resizing watermark: {e}")
        return None


def _prepare_watermark_for_canvas(watermark_path, canvas_w, canvas_h, count):
    """
    Loads the watermark and scales it to fit a canvas of the given size:
    never wider than the canvas, and never taller than 80% of one of the
    `count` vertical segments. Returns the resized RGBA watermark, or None
    if the watermark cannot be loaded.
    """
    wm_orig = _get_cached_watermark(watermark_path)
    if wm_orig is None:
        return None

    orig_w, orig_h = wm_orig.size
    wm_w, wm_h = orig_w, orig_h

    # Scale down if it exceeds the page width
    if wm_w > canvas_w:
        wm_w = canvas_w
        wm_h = int((wm_w / float(orig_w)) * orig_h)
        if wm_h < 5: wm_h = 5

    # If the watermark is taller than the image segment itself, scale it down
    max_allowed_h = int(canvas_h / float(count))
    if wm_h > max_allowed_h * 0.8:
        wm_h = int(max_allowed_h * 0.8)
        if wm_h < 5: wm_h = 5
        wm_w = int((wm_h / float(orig_h)) * orig_w)
        if wm_w < 10: wm_w = 10

    return _get_resized_watermark(watermark_path, wm_w, wm_h)


def _default_watermark_placements(canvas_size, wm_size, count, edge, margin=15):
    """
    Deterministic fallback positions used when the content-aware placement
    search is unavailable or fails: one watermark per vertical segment,
    vertically centered in the segment, hugging the requested edge. Uses no
    numpy so it cannot fail the way the detector can.
    """
    W, H = canvas_size
    wm_w, wm_h = wm_size

    if edge == 'left':
        x_pos = min(margin, max(0, W - wm_w))
    else:
        x_pos = max(0, W - margin - wm_w)

    placements = []
    segment_height = H / float(count)
    for i in range(count):
        seg_start = int(i * segment_height)
        seg_end = int((i + 1) * segment_height)
        y_pos = seg_start + max(0, (seg_end - seg_start - wm_h) // 2)
        y_pos = max(0, min(y_pos, H - wm_h))
        if not placements or y_pos > placements[-1][1]:
            placements.append((x_pos, y_pos))
    return placements


def extract_images_from_zip(zip_path, extract_base_dir):
    """
    Extracts all images from a ZIP archive (including nested ZIPs).
    Returns: Path to the temporary directory containing extracted images.
    """
    folder_name = Path(zip_path).stem
    output_dir = os.path.join(extract_base_dir, folder_name)
    os.makedirs(output_dir, exist_ok=True)

    def _extract_zip_recursive(zf, target_dir):
        """
        Recursively inspects ZIP files and extracts embedded images.
        """
        for member in zf.namelist():
            member_lower = member.lower()
            
            # Unpack nested ZIP files recursively
            if member_lower.endswith('.zip'):
                inner_zip_data = zf.read(member)
                import io
                with zipfile.ZipFile(io.BytesIO(inner_zip_data)) as inner_zf:
                    _extract_zip_recursive(inner_zf, target_dir)
            
            # Extract image files
            elif any(member_lower.endswith(f'.{ext}') for ext in IMAGE_EXTENSIONS):
                # Extract filename without internal archive folder structure
                filename = os.path.basename(member)
                if not filename:
                    continue
                
                # Prevent filename collisions
                dest_path = os.path.join(target_dir, filename)
                counter = 0
                stem, suffix = os.path.splitext(filename)
                while os.path.exists(dest_path):
                    counter += 1
                    dest_path = os.path.join(target_dir, f"{stem}_{counter}{suffix}")
                
                with zf.open(member) as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            _extract_zip_recursive(zf, output_dir)
    except (zipfile.BadZipFile, Exception) as e:
        print(f"Error extracting ZIP {zip_path}: {e}")
        return None

    # Check if any valid images were extracted
    extracted_images = [
        f for f in os.listdir(output_dir)
        if os.path.splitext(f)[1][1:].lower() in IMAGE_EXTENSIONS
    ]
    if not extracted_images:
        return None

    return output_dir


def extract_images_from_pdf(pdf_path, extract_base_dir):
    """
    Extracts all embedded images from a PDF file.
    If no embedded images are found, renders pages to PNG files.
    Returns: Path to temporary directory containing extracted images.
    """
    try:
        #import fitz  # PyMuPDF
        from fitz import open as fitz_open, Matrix as fitz_Matrix
    except ImportError:
        print("PyMuPDF not installed. Cannot extract from PDF.")
        return None

    folder_name = Path(pdf_path).stem
    output_dir = os.path.join(extract_base_dir, folder_name)
    os.makedirs(output_dir, exist_ok=True)

    try:
        doc = fitz_open(pdf_path)
        image_count = 0

        # Method 1: Extract embedded images
        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                filename = f"{str(page_index + 1).zfill(4)}_{str(img_index + 1).zfill(3)}.{image_ext}"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                image_count += 1

        # Method 2: Fallback - Render pages if no embedded images found
        if image_count == 0:
            for page_index in range(len(doc)):
                page = doc[page_index]
                # High quality render (zoom=2 -> 144 DPI)
                mat = fitz_Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)
                filename = f"{str(page_index + 1).zfill(4)}.png"
                filepath = os.path.join(output_dir, filename)
                pix.save(filepath)
                image_count += 1

        doc.close()

    except Exception as e:
        print(f"Error extracting PDF {pdf_path}: {e}")
        return None

    if image_count == 0:
        return None

    return output_dir



def open_image_robust(path):
    
    file_ext = os.path.splitext(path)[1].lower()

    if file_ext == '.psd':
        # Import PSD tools ONLY here
        try:
            from psd_tools import PSDImage
            psd = PSDImage.open(path)
            return psd.composite()
        except ImportError as e:
            print(e)
            print("Warning: psd-tools not installed.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        # For standard formats like JPG, PNG, WEBP, etc.
        try:
            img = Image.open(path)
            # .load() forces the image data to be read from the file into memory
            img.load() 
            return img
        except Exception as e:
            print(f"Warning: Could not open image file {path}. Skipping. Error: {e}")
            return None


def get_image_size_fast(path):
    """
    Gets image dimensions without loading pixel data into memory (Lazy Read).
    Significant speedup for the first pass.
    """
    file_ext = os.path.splitext(path)[1].lower()
    if file_ext == '.psd':
        # PSD tools reads header efficiently usually
        try:
            from psd_tools import PSDImage
            psd = PSDImage.open(path)
            return psd.width, psd.height
        except:
            return (0, 0)
            
    try:
        # For standard images, Image.open reads only headers initially
        with Image.open(path) as img:
            return img.width, img.height
    except:
        return (0, 0)


def any_image_exceeds_webp_limit(images, is_custom_width, new_width):
    """
    Checks if any image in no-stitch mode exceeds WebP's maximum height limit after optional resizing.
    Uses fast header inspection without decoding full pixel data.
    """
    for path in images:
        w, h = get_image_size_fast(path)
        if w <= 0 or h <= 0:
            continue
        if is_custom_width and new_width and new_width > 0:
            eff_h = int((new_width / float(w)) * h)
        else:
            eff_h = h
        if eff_h > WEBP_MAX_DIMENSION:
            return True
    return False


def process_and_resize(args):
    """
    Worker function to open and resize an image in a separate thread.
    """
    path, target_width, target_height = args
    img = open_image_robust(path)
    if img:
        try:
            if img.size != (target_width, target_height):
                # Optimization: Bicubic is much faster than Lanczos and quality is sufficient for Webtoons
                resized = img.resize((target_width, target_height), resample=Image.Resampling.BICUBIC)
                img.close()
                return resized
            return img
        except Exception as e:
            print(f"Error resizing {path}: {e}")
            img.close()
    return None


def get_concat_v_optimized(image_paths, new_width, is_custom_width, max_workers=4):
    """
    Multi-threaded Stitcher:
    1. Fast-scans dimensions (Lazy Load).
    2. Resizes images in parallel threads (Speed Boost).
    3. Pastes them sequentially.
    """
    if not image_paths:
        return None

    # --- Pass 1: Calculate Dimensions (Fast) ---
    dimensions = []
    max_w = 0
    
    for path in image_paths:
        w, h = get_image_size_fast(path)
        if w > 0 and h > 0:
            dimensions.append((w, h))
            if w > max_w: max_w = w
        else:
            # Treat broken images as 0x0 to skip later
            dimensions.append((0, 0))

    target_width = new_width if is_custom_width else max_w
    if target_width <= 0:
        return None

    # Calculate final heights
    final_heights = []
    valid_indices = [] 
    
    for i, (w, h) in enumerate(dimensions):
        if w > 0:
            new_h = int((target_width / float(w)) * h)
            final_heights.append(new_h)
            valid_indices.append(i)
    
    total_height = sum(final_heights)
    if total_height <= 0:
        return None

    # Create the final canvas
    try:
        dst = Image.new('RGB', (target_width, total_height))
    except Exception as e:
        print(f"Memory Error creating canvas: {e}")
        return None

    # --- Pass 2: Parallel Resize & Sequential Paste ---
    current_height = 0
    
    # Prepare tasks
    tasks = []
    for i, h in zip(valid_indices, final_heights):
        tasks.append((image_paths[i], target_width, h))

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # executor.map yields results in order, which is crucial for stitching
        results = executor.map(process_and_resize, tasks)
        
        for img in results:
            if img:
                dst.paste(img, (0, current_height))
                current_height += img.height
                img.close()
            
    return dst


def find_safe_cut_points(image, slices_count):
    """
    Modified with vertical context check to avoid cutting through balloons.
    """
    gray_img = image.convert('L')
    combined_img = np.array(gray_img)
    
    height, width = combined_img.shape
    if height == 0 or slices_count <= 0:
        return []
    
    split_height = int(height / slices_count)
    
    if split_height < 50:
        even_cuts = []
        for i in range(1, int(slices_count)):
            cut_point = int((height * i) / slices_count)
            even_cuts.append(cut_point)
        even_cuts.append(height)
        return even_cuts
    
    scan_step = 5
    ignorable_pixels = 0
    sensitivity = 90
    threshold = int(255 * (1 - (sensitivity / 100)))
    last_row = height
    
    # --- Vertical context check offsets (rows above and below candidate cut point) ---
    vertical_check_offsets = [-25, -15, -8, 8, 15, 25]
    
    slice_locations = [0]
    row = split_height
    move_up = True
    
    while row < last_row:
        if row >= last_row:
            break
            
        # Step 1: Check row uniformity
        can_slice = _is_row_uniform(combined_img, row, width, ignorable_pixels, threshold)
        
        # Step 2: Check vertical neighborhood to verify clean gap
        if can_slice:
            for offset in vertical_check_offsets:
                check_row = row + offset
                if 0 <= check_row < last_row:
                    if not _is_row_uniform(combined_img, check_row, width, 
                                            ignorable_pixels, threshold):
                        can_slice = False
                        break
        # ────────────────────────────────────────────────────────────
        
        if can_slice:
            slice_locations.append(row)
            row += split_height
            move_up = True
            continue
            
        if row - slice_locations[-1] <= 0.4 * split_height:
            row = slice_locations[-1] + split_height
            move_up = False
            
        if move_up:
            row -= scan_step
            if row <= slice_locations[-1]:
                row = slice_locations[-1] + scan_step
                move_up = False
            continue
            
        row += scan_step
    
    if slice_locations[-1] != last_row:
        slice_locations.append(last_row)
    
    slice_locations = sorted(list(set(slice_locations)))
    
    min_height = 10
    validated_cuts = [slice_locations[0]]
    for i in range(1, len(slice_locations)):
        if slice_locations[i] - validated_cuts[-1] >= min_height:
            validated_cuts.append(slice_locations[i])
    
    if validated_cuts[-1] != height:
        validated_cuts[-1] = height
    
    return validated_cuts[1:]


def _is_row_uniform(img_array, row, width, ignorable_pixels, threshold):
    """Checks horizontal row uniformity for content detection."""
    row_pixels = img_array[row]
    
    if len(row_pixels) <= ignorable_pixels * 2 + 1:
        return False
    
    for index in range(ignorable_pixels + 1, width - ignorable_pixels):
        prev_pixel = int(row_pixels[index - 1])
        next_pixel = int(row_pixels[index])
        value_diff = next_pixel - prev_pixel
        
        if value_diff > threshold or value_diff < -threshold:
            return False
    
    return True


def _cap_slice_gaps(cut_points, max_height):
    """
    Ensures the gap between any two consecutive cut points does not exceed `max_height`.
    Adds forced cut points if a safe gap overshoots the maximum format limit (e.g. WebP).
    `cut_points`: Sorted list starting at 0 and ending at total height.
    """
    if not max_height or max_height <= 0 or not cut_points:
        return cut_points

    capped = [cut_points[0]]
    for cp in cut_points[1:]:
        prev = capped[-1]
        while cp - prev > max_height:
            prev += max_height
            capped.append(prev)
        capped.append(cp)
    return capped


def format_filename(pattern, number, digits, extension, folder_name="", total=1):
    """Replace placeholders in pattern with dynamic values (number, folder name, date, total count)."""
    import datetime
    padded = str(number).zfill(max(1, min(digits, 6)))
    name = pattern
    if '[number]' in name:
        name = name.replace('[number]', padded)
    else:
        name = f"{name}_{padded}"
        
    if '[folder]' in name:
        name = name.replace('[folder]', folder_name)
    if '[date]' in name:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        name = name.replace('[date]', today)
    if '[total]' in name:
        name = name.replace('[total]', str(total))
        
    # Clean invalid filename characters
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    return f"{name}.{extension.lower()}"


def slicer(image, saveFormat, slicesCount, saveQuality, mode, current_date, saveDirectory=None, isZip=False, isPdf=False, isCbz=False, progress_callback=None, output_base="./Results", max_workers=4, filename_pattern="[number]", filename_digits=3, watermark_enabled=False, watermark_path="", watermark_count=1, watermark_edge="right", watermark_width_percent=12):
    def process_slice(start, end, image_file, index, save_path):
        width, _ = image_file.size
        res = image_file.crop((0, start, width, end))
        is_psd = saveFormat.lower() == "psd"
        # For PSD output the watermark goes in as a separate layer (inside
        # save_psd_layered) instead of being baked into the pixels, so the
        # user can reposition it later in Photoshop.
        if watermark_enabled and not is_psd:
            res = apply_watermark(res, watermark_path, watermark_count, watermark_edge, watermark_width_percent)
        filename = format_filename(filename_pattern, index, filename_digits, saveFormat, folder_name=os.path.basename(save_path), total=len(cut_points) - 1)
        filepath = os.path.join(save_path, filename)
        if saveFormat.lower() == "webp":
            res.save(filepath, format="webp", quality=saveQuality, method=6)
        elif is_psd:
            save_psd_layered(res, filepath, watermark_enabled, watermark_path, watermark_count, watermark_edge, watermark_width_percent)
        else:
            res.save(filepath, quality=saveQuality, optimize=True, progressive=True)
        res.close()

    image_file = image
    base_folder = output_base
    if mode == 'single':
        folderName = saveDirectory or "folderName"
        save_path = os.path.join(base_folder, folderName)
    elif mode == 'multi':
        folderName = saveDirectory or current_date
        save_path = os.path.join(base_folder, current_date, folderName)
    else:
        raise ValueError("Invalid mode.")

    counter = 0
    original_save_path = save_path
    while os.path.exists(save_path) or os.path.exists(f"{save_path}.zip") or os.path.exists(f"{save_path}.cbz"):
        counter += 1
        save_path = f"{original_save_path} ({counter})"
    os.makedirs(save_path, exist_ok=True)
    
    cut_points = find_safe_cut_points(image_file, slicesCount)
    cut_points = [0] + cut_points

    # Safety net: WebP can't encode slices taller than WEBP_MAX_DIMENSION. The
    # safe-cut search can overshoot the requested limit, so cap the gaps to make
    # sure every slice stays saveable (otherwise the save would crash silently).
    if saveFormat.lower() == "webp":
        cut_points = _cap_slice_gaps(cut_points, WEBP_MAX_DIMENSION)

    # --- Slicing Logic with Progress ---
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(1, len(cut_points)):
            start, end = cut_points[i - 1], cut_points[i]
            futures.append(executor.submit(process_slice, start, end, image_file, i, save_path))
        
        # Track progress
        completed_count = 0
        total_count = len(futures)
        
        for future in as_completed(futures):
            future.result() # Wait for completion
            completed_count += 1
            if progress_callback:
                percent = (completed_count / total_count) * 100
                progress_callback(percent)
    # -----------------------------------
    
    if isZip:
        zipFilePath = ""
        folderName = os.path.basename(save_path)
        if mode == 'single':
            zipFilePath = os.path.join(os.path.dirname(save_path), f"{folderName}.zip")
        elif mode == 'multi':
            zipFilePath = os.path.join(output_base, current_date, f"{folderName}.zip")

        with zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in os.listdir(save_path):
                file_path = os.path.join(save_path, file)
                if os.path.isfile(file_path):
                    zip_file.write(file_path, arcname=file)
        shutil.rmtree(save_path)
        
    elif isCbz:
        cbzFilePath = ""
        folderName = os.path.basename(save_path)
        if mode == 'single':
            cbzFilePath = os.path.join(os.path.dirname(save_path), f"{folderName}.cbz")
        elif mode == 'multi':
            cbzFilePath = os.path.join(output_base, current_date, f"{folderName}.cbz")

        with zipfile.ZipFile(cbzFilePath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in os.listdir(save_path):
                file_path = os.path.join(save_path, file)
                if os.path.isfile(file_path):
                    zip_file.write(file_path, arcname=file)
        shutil.rmtree(save_path)
        
    elif isPdf:
        pdfFilePath = ""
        folderName = os.path.basename(save_path)
        if mode == 'single':
            pdfFilePath = os.path.join(os.path.dirname(save_path), f"{folderName}.pdf")
        elif mode == 'multi':
            # Ensure target directory exists
            results_dir = os.path.join(output_base, current_date)
            os.makedirs(results_dir, exist_ok=True)
            pdfFilePath = os.path.join(results_dir, f"{folderName}.pdf")

        # Collect image files for PDF generation
        image_files = sorted([os.path.join(save_path, f) for f in os.listdir(save_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
        
        if image_files:
            try:
                # Convert image files into PDF
                with open(pdfFilePath, "wb") as f:
                    f.write(img2pdf.convert(image_files))
                
                print(f"PDF successfully created at: {pdfFilePath}")
                
                # Delete uncompressed directory after successful PDF creation
                shutil.rmtree(save_path)

            except Exception as e:
                print(f"Failed to create PDF or delete folder for '{save_path}': {e}")
        else:
            # Remove empty directory if no images were found
            print(f"No images found in '{save_path}', removing the empty directory.")
            os.rmdir(save_path)


# Global list of temporary extraction directories
_temp_extraction_dirs = []


def fast_scandir(dirname):
    """
    Scans subdirectories and extracts ZIP/CBZ/PDF files into temporary directories.
    Returns: List of paths (original folders + extracted temporary folders).
    """
    global _temp_extraction_dirs
    
    result = []
    
    # Common temporary folder for all extractions in this run
    extraction_temp = tempfile.mkdtemp(prefix="photoslicer_extract_")
    _temp_extraction_dirs.append(extraction_temp)

    for entry in os.scandir(dirname):
        if entry.is_dir():
            result.append(entry.path)
        
        elif entry.is_file():
            ext = os.path.splitext(entry.name)[1].lower()
            
            if ext in ('.zip', '.cbz'):
                extracted = extract_images_from_zip(entry.path, extraction_temp)
                if extracted:
                    result.append(extracted)
            
            elif ext == '.pdf':
                extracted = extract_images_from_pdf(entry.path, extraction_temp)
                if extracted:
                    result.append(extracted)

    return result


def cleanup_extraction_temps():
    """Cleans up temporary extraction directories after processing."""
    global _temp_extraction_dirs
    for temp_dir in _temp_extraction_dirs:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Warning: Could not cleanup temp dir {temp_dir}: {e}")
    _temp_extraction_dirs = []



def getAllImagesDirectory(imagesPath):
    path = Path(imagesPath)
    if not path.is_dir():
        raise ValueError(f"Path {imagesPath} does not exist or is not a directory")
    
    extensions = {"jpg", "jpeg", "png", "webp", "avif", "psd"}
    
    imagesLocations = [
        p for p in path.iterdir()
        if p.is_file() and not p.name.startswith('.') and p.suffix[1:].lower() in extensions
    ]
    
    def sort_key_improved(filepath):
        basename = os.path.basename(filepath)
        match_double = re.search(r'(\d+)__(\d+)', basename)
        if match_double:
            return (0, int(match_double.group(1)), int(match_double.group(2)))
        parts = re.split(r'(\d+)', basename)
        parts = [int(p) if p.isdigit() else p.lower() for p in parts]
        return (1, parts)

    return sorted([str(p) for p in imagesLocations], key=sort_key_improved)


def process_batch_no_stitch(images, save_path, newWidth, isChecked, saveFormat, SaveQuality, is_zip, isPdf, isCbz, current_date, mode, progress_callback=None, output_base="./Results", max_workers=4, filename_pattern="[number]", filename_digits=3, watermark_enabled=False, watermark_path="", watermark_count=1, watermark_edge="right", watermark_width_percent=12):
    """
    Processes images individually without stitching.
    Handles optional resizing, watermarking, saving, and ZIP/PDF/CBZ archiving.
    """
    os.makedirs(save_path, exist_ok=True)

    def worker_save_single(args):
        img_path, idx = args
        try:
            img = open_image_robust(img_path)
            if not img: return None

            # Resize only if custom width is enabled
            if isChecked:
                w_percent = (newWidth / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                img = img.resize((newWidth, h_size), Image.Resampling.BICUBIC)

            is_psd = saveFormat.lower() == "psd"
            # For PSD output the watermark goes in as a separate layer (inside
            # save_psd_layered) instead of being baked into the pixels, so the
            # user can reposition it later in Photoshop.
            if watermark_enabled and not is_psd:
                img = apply_watermark(img, watermark_path, watermark_count, watermark_edge, watermark_width_percent)

            filename = format_filename(filename_pattern, idx + 1, filename_digits, saveFormat, folder_name=os.path.basename(save_path), total=len(images))
            filepath = os.path.join(save_path, filename)

            if saveFormat.lower() == "webp":
                img.save(filepath, format="webp", quality=SaveQuality, method=6)
            elif is_psd:
                save_psd_layered(img, filepath, watermark_enabled, watermark_path, watermark_count, watermark_edge, watermark_width_percent)
            else:
                img.save(filepath, quality=SaveQuality, optimize=True, progressive=True)
            
            img.close()
            return True
        except Exception as e:
            print(f"Error in no-stitch mode for {img_path}: {e}")
            return False

    # Parallel processing
    tasks = [(path, i) for i, path in enumerate(images)]
    completed_count = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker_save_single, t) for t in tasks]
        for future in as_completed(futures):
            future.result()
            completed_count += 1
            if progress_callback:
                percent = (completed_count / len(images)) * 100
                progress_callback(percent)

    # Handle archive and PDF outputs
    folderNameBase = os.path.basename(save_path)
    
    if is_zip:
        zipFilePath = ""
        if mode == 'single':
            zipFilePath = os.path.join(os.path.dirname(save_path), f"{folderNameBase}.zip")
        elif mode == 'multi':
            zipFilePath = os.path.join(output_base, current_date, f"{folderNameBase}.zip")

        with zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in os.listdir(save_path):
                file_path = os.path.join(save_path, file)
                if os.path.isfile(file_path):
                    zip_file.write(file_path, arcname=file)
        shutil.rmtree(save_path)

    elif isPdf:
        pdfFilePath = ""
        if mode == 'single':
            pdfFilePath = os.path.join(os.path.dirname(save_path), f"{folderNameBase}.pdf")
        elif mode == 'multi':
            pdfFilePath = os.path.join(output_base, current_date, f"{folderNameBase}.pdf")

        output_images = sorted([os.path.join(save_path, f) for f in os.listdir(save_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
        
        if output_images:
            img1 = Image.open(output_images[0]).convert("RGB")
            other_images = [Image.open(f).convert("RGB") for f in output_images[1:]]
            img1.save(pdfFilePath, "PDF", resolution=100.0, save_all=True, append_images=other_images)
            img1.close()
            for img in other_images: img.close()
        
        shutil.rmtree(save_path)

    elif isCbz:
        cbzFilePath = ""
        if mode == 'single':
            cbzFilePath = os.path.join(os.path.dirname(save_path), f"{folderNameBase}.cbz")
        elif mode == 'multi':
            cbzFilePath = os.path.join(output_base, current_date, f"{folderNameBase}.cbz")

        with zipfile.ZipFile(cbzFilePath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in os.listdir(save_path):
                file_path = os.path.join(save_path, file)
                if os.path.isfile(file_path):
                    zip_file.write(file_path, arcname=file)
        shutil.rmtree(save_path)

    return True


class ContentAwarePanelDetector:
    """
    Content-Aware Panel Detection with Speech Bubble Avoidance.
    """
    
    # Thresholds
    WHITE_THRESHOLD = 230
    BLACK_THRESHOLD = 25
    BUBBLE_WHITE_THRESHOLD = 235  # Very white = likely speech bubble
    MIN_GUTTER_HEIGHT = 8
    MIN_GUTTER_COVERAGE = 0.65
    EDGE_MARGIN = 80
    
    # Adjustment parameters
    ADJUSTMENT_STEP = 15      # Pixels to move each iteration (fine enough to clear bubble corners)
    MAX_ADJUSTMENT = 300      # Maximum adjustment distance
    MIN_SAFE_SCORE = 20       # Minimum score to consider "safe"

    # Bubble-mask parameters
    BUBBLE_MASK_SCALE = 4     # Downscale factor for the whole-image bubble mask
    MASK_CLEARANCE = 24       # Extra pixels above/below the footprint checked against the mask
    
    @staticmethod
    def to_grayscale(img_array):
        if len(img_array.shape) == 2:
            return img_array
        if img_array.shape[2] >= 3:
            return ((img_array[:, :, 0].astype(np.uint16) * 77 +
                     img_array[:, :, 1].astype(np.uint16) * 150 +
                     img_array[:, :, 2].astype(np.uint16) * 29) >> 8).astype(np.uint8)
        return img_array[:, :, 0]
    
    @staticmethod
    def get_saturation(img_array):
        # Saturation is kept as uint8 (0-255, same scale as PIL's HSV "S"
        # channel) instead of float32: 4x less memory and no full-image
        # float division. All threshold comparisons scale by 255 accordingly.
        if len(img_array.shape) != 3 or img_array.shape[2] < 3:
            return np.zeros(img_array.shape[:2], dtype=np.uint8)

        r = img_array[:, :, 0]
        g = img_array[:, :, 1]
        b = img_array[:, :, 2]

        max_val = np.maximum(np.maximum(r, g), b)
        min_val = np.minimum(np.minimum(r, g), b)

        diff = (max_val - min_val).astype(np.uint16) * 255
        saturation = (diff // np.maximum(max_val, 1)).astype(np.uint8)

        return saturation

    @staticmethod
    def build_bubble_mask(gray, saturation, scale=None):
        """
        Whole-image speech-bubble mask, downscaled by `scale`.

        Bubble interiors are near-white, unsaturated regions containing text.
        The mask is seeded from text-bearing tiles and grown through the
        connected white area, so it follows the full bubble outline INCLUDING
        its tail — which whole-region statistics and per-cell checks miss.
        The growth stops at the bubble's dark outline (min-pooled cells keep
        thin outlines intact), so it does not leak into page background.

        Returns a boolean array of shape (H//scale, W//scale); mask[y, x]
        covers original pixels [y*scale:(y+1)*scale, x*scale:(x+1)*scale].
        """
        if scale is None:
            scale = ContentAwarePanelDetector.BUBBLE_MASK_SCALE
        H, W = gray.shape
        hh, ww = (H // scale) * scale, (W // scale) * scale
        h, w = hh // scale, ww // scale
        if h < 8 or w < 8:
            return np.zeros((max(h, 1), max(w, 1)), dtype=bool)

        blocks = gray[:hh, :ww].reshape(h, scale, w, scale)
        g_mean = blocks.mean(axis=(1, 3))
        g_min = blocks.min(axis=(1, 3))

        if saturation is not None:
            s_mean = saturation[:hh, :ww].reshape(h, scale, w, scale).mean(axis=(1, 3))
        else:
            s_mean = np.zeros((h, w), dtype=np.float32)

        # White bubble-interior cells; g_min keeps cells crossed by a dark
        # outline out of the mask so the outline acts as a growth barrier.
        # (saturation is uint8 0-255, so thresholds are scaled by 255)
        white = (g_mean > 220) & (g_min > 160) & (s_mean < 0.22 * 255)
        # Cells containing dark (potential text/outline) pixels
        dark = g_min < 100

        # --- Text seeds: mostly-white tiles with many short dark runs ---
        tile = max(6, 48 // scale)
        th, tw = h // tile, w // tile
        if th < 1 or tw < 1:
            return np.zeros((h, w), dtype=bool)

        dk = dark[:th * tile, :tw * tile].reshape(th, tile, tw, tile)
        wh = white[:th * tile, :tw * tile].reshape(th, tile, tw, tile)
        dark_cells = dk.mean(axis=(1, 3))
        white_cells = wh.mean(axis=(1, 3))
        # Horizontal dark/light alternation inside the tile: text produces many
        # short runs; a single art stroke or an empty region produces few.
        trans = (dk[:, :, :, 1:] != dk[:, :, :, :-1]).mean(axis=(1, 3))
        text_tile = (white_cells > 0.4) & (dark_cells > 0.08) & (dark_cells < 0.5) & (trans > 0.12)
        # A dark run spanning the tile's full height or width is a panel border
        # or an art stroke, never text — a white page margin next to a panel
        # border would otherwise be seeded and flood the whole margin strip.
        border_col = dk.all(axis=1).any(axis=-1)
        border_row = dk.all(axis=3).any(axis=1)
        text_tile &= ~border_col & ~border_row

        seeds = np.zeros((h, w), dtype=bool)
        seeds[:th * tile, :tw * tile] = np.repeat(np.repeat(text_tile, tile, axis=0), tile, axis=1)
        seeds &= white
        if not seeds.any():
            return np.zeros((h, w), dtype=bool)

        # --- Grow seeds through the connected white area (bubble + tail) ---
        # Frontier-based BFS: identical result to repeated 4-neighbour
        # dilation (one BFS level == one dilation pass, same max_iters cap),
        # but each cell is visited once instead of re-scanning the whole
        # mask on every iteration.
        mask = np.ascontiguousarray(seeds)
        white_flat = np.ascontiguousarray(white).ravel()
        mask_flat = mask.ravel()
        frontier = np.flatnonzero(mask_flat)
        max_iters = max(24, 480 // scale)
        for _ in range(max_iters):
            if frontier.size == 0:
                break
            up = frontier[frontier >= w] - w
            down = frontier[frontier < (h - 1) * w] + w
            left = frontier[frontier % w != 0] - 1
            right = frontier[frontier % w != w - 1] + 1
            cand = np.concatenate((up, down, left, right))
            cand = cand[white_flat[cand] & ~mask_flat[cand]]
            if cand.size == 0:
                break
            cand = np.unique(cand)
            mask_flat[cand] = True
            frontier = cand

        # Safety valve: if the mask swallowed most of the image the seeding
        # misfired (e.g. an all-text credits page) — better to fall back to
        # the local heuristics than to poison every candidate's score.
        if mask.mean() > 0.5:
            return np.zeros((h, w), dtype=bool)

        return mask

    @staticmethod
    def detect_text_pattern(gray_region):
        """
        Detect if a region likely contains text (speech bubble interior).
        Text appears as dark pixels scattered within a mostly white region.
        """
        if gray_region.size == 0:
            return False, 0
        
        n = gray_region.size
        very_white = np.count_nonzero(gray_region > 235) / n

        if very_white < 0.15:
            return False, 0

        # Look for dark pixels (text) within the region
        dark_pixels = (gray_region < 80) & (gray_region > 10)
        dark_ratio = np.count_nonzero(dark_pixels) / n

        # Also check for medium-dark (anti-aliased text edges)
        medium_dark = (gray_region >= 80) & (gray_region < 150)
        medium_ratio = np.count_nonzero(medium_dark) / n
        
        # Text pattern: some dark pixels but not too many
        has_text = (0.02 < dark_ratio < 0.25) or (dark_ratio > 0.01 and medium_ratio > 0.05)
        
        # Calculate text confidence
        text_confidence = min(1.0, dark_ratio * 10) if has_text else 0
        
        return has_text, text_confidence
    
    @staticmethod
    def detect_face_region(gray_region, sat_region):
        """
        Detect if a region might contain a character face.
        """
        if gray_region.size == 0:
            return False, 0
        
        # Check for high local variance (detail)
        variance = np.var(gray_region)
        
        # Check for edge density
        if gray_region.shape[0] > 2 and gray_region.shape[1] > 2:
            g16 = gray_region.astype(np.int16)
            gy = np.abs(np.diff(g16, axis=0))
            gx = np.abs(np.diff(g16, axis=1))
            edge_density = (np.count_nonzero(gy > 20) / gy.size + np.count_nonzero(gx > 20) / gx.size) / 2
        else:
            edge_density = 0
        
        # High detail with moderate saturation suggests character art
        # (saturation is uint8 0-255; normalize the scalar mean back to 0-1)
        mean_sat = np.mean(sat_region) / 255.0 if sat_region is not None else 0
        
        is_face_like = (variance > 1500 and edge_density > 0.15 and 0.1 < mean_sat < 0.5)
        confidence = min(1.0, edge_density * 3) if is_face_like else 0
        
        return is_face_like, confidence
    
    @staticmethod
    def detect_bubble_overlap(gray, saturation, y, y_end, x_start_wm, x_end_wm, img_height, clearance=24, col_white=None):
        """
        Detect speech bubble overlap in localized sub-cells of the watermark
        footprint (plus a small clearance band above and below). Whole-region
        statistics miss bubbles that only clip a corner or edge of the
        watermark area; a per-cell check catches them.

        Full-width white bands (gutters, white page background) are exempted
        so the watermark can still sit tight against a panel edge.

        Returns (overlap, overlap_cells) where overlap_cells is a list of
        (row, col) grid coordinates of the offending cells.
        """
        grid_rows, grid_cols = 3, 3
        y0 = max(0, y - clearance)
        y1 = min(img_height, y_end + clearance)
        
        while y0 < y and ContentAwarePanelDetector.is_gutter_row(gray[y0])[0]:
            y0 += 1
        while y1 > y_end and ContentAwarePanelDetector.is_gutter_row(gray[y1 - 1])[0]:
            y1 -= 1
            
        # Full-height column whiteness over the watermark's x-range. This only
        # depends on (x_start_wm, x_end_wm), which is fixed for every candidate
        # position of one placement search — callers precompute it once and
        # pass it in, so it is not re-scanned over the whole image height for
        # every tested y position.
        if col_white is None:
            col_white = np.mean(gray[:, x_start_wm:x_end_wm] > ContentAwarePanelDetector.BUBBLE_WHITE_THRESHOLD, axis=0)
        x_start = x_start_wm
        while x_start < x_end_wm - 3 and col_white[x_start - x_start_wm] > 0.9:
            x_start += 1
            
        x_end = x_end_wm
        while x_end > x_start + 3 and col_white[x_end - 1 - x_start_wm] > 0.9:
            x_end -= 1

        region = gray[y0:y1, x_start:x_end]
        sat_region = saturation[y0:y1, x_start:x_end] if saturation is not None else None
        h, w = region.shape[:2]
        
        if h < grid_rows or w < grid_cols:
            return False, []
            
        row_edges = np.linspace(0, h, grid_rows + 1).astype(int)
        col_edges = np.linspace(0, w, grid_cols + 1).astype(int)
        overlap_cells = []
        
        for r in range(grid_rows):
            band = gray[y0 + row_edges[r]:y0 + row_edges[r + 1], :]
            band_white = np.count_nonzero(band > ContentAwarePanelDetector.BUBBLE_WHITE_THRESHOLD) / band.size if band.size else 0
            if band_white >= ContentAwarePanelDetector.MIN_GUTTER_COVERAGE:
                # Exempt the band only if it is genuinely empty (gutter/page
                # background). A large speech bubble can also make a full-width
                # band mostly white, but it carries text edges — keep checking it.
                if band.shape[0] > 2 and band.shape[1] > 2:
                    band_gy = np.abs(np.diff(band.astype(np.int16), axis=0))
                    band_edges = np.count_nonzero(band_gy > 40) / band_gy.size
                else:
                    band_edges = 0
                if band_edges < 0.01:
                    continue
                
            for c in range(grid_cols):
                cell = region[row_edges[r]:row_edges[r + 1], col_edges[c]:col_edges[c + 1]]
                if cell.size < 25:
                    continue
                    
                bright_mask = cell > ContentAwarePanelDetector.BUBBLE_WHITE_THRESHOLD
                very_white = np.count_nonzero(bright_mask) / bright_mask.size
                if very_white < 0.05:
                    continue
                    
                if sat_region is not None:
                    sat_cell = sat_region[row_edges[r]:row_edges[r + 1], col_edges[c]:col_edges[c + 1]]
                    if sat_cell.size > 0 and np.mean(sat_cell[bright_mask]) > 0.15 * 255:
                        continue
                        
                has_text, _ = ContentAwarePanelDetector.detect_text_pattern(cell)
                if cell.shape[0] > 2 and cell.shape[1] > 2:
                    c16 = cell.astype(np.int16)
                    gy = np.abs(np.diff(c16, axis=0))
                    gx = np.abs(np.diff(c16, axis=1))
                    edge_density = (np.count_nonzero(gy > 40) / gy.size + np.count_nonzero(gx > 40) / gx.size) / 2
                else:
                    edge_density = 0
                    
                if has_text or edge_density > 0.015 or very_white > 0.75:
                    overlap_cells.append((r, c))
                    
        return len(overlap_cells) > 0, overlap_cells

    @staticmethod
    def analyze_region_detailed(gray, saturation, y, wm_height, wm_width, img_height, edge='left', x_margin=15,
                                bubble_mask=None, mask_scale=None, panel_edges=None, col_white=None):
        """
        Detailed analysis of a watermark candidate region.
        """
        y_end = min(y + wm_height, img_height)
        img_width = gray.shape[1]
        
        if edge == 'left':
            x_start = x_margin
            x_end = min(x_margin + wm_width, img_width)
        else:
            x_start = max(0, img_width - x_margin - wm_width)
            x_end = img_width - x_margin
        
        if y_end <= y or x_end <= x_start:
            return -999, {'valid': False, 'reason': 'invalid_bounds'}
        
        region_gray = gray[y:y_end, x_start:x_end]
        region_sat = saturation[y:y_end, x_start:x_end] if saturation is not None else None
        
        if region_gray.size == 0:
            return -999, {'valid': False, 'reason': 'empty_region'}
        
        # === Basic Statistics ===
        mean_brightness = np.mean(region_gray)
        variance = np.var(region_gray)

        # === White/Black Analysis ===
        n_region = region_gray.size
        very_white_ratio = np.count_nonzero(region_gray > 235) / n_region
        white_ratio = np.count_nonzero(region_gray > 220) / n_region
        black_ratio = np.count_nonzero(region_gray < 30) / n_region
        
        # === Speech Bubble Detection ===
        has_text, text_confidence = ContentAwarePanelDetector.detect_text_pattern(region_gray)
        is_speech_bubble = (very_white_ratio > 0.25) or (very_white_ratio > 0.15 and has_text)
        
        bubble_overlap, overlap_cells = ContentAwarePanelDetector.detect_bubble_overlap(
            gray, saturation, y, y_end, x_start, x_end, img_height, col_white=col_white
        )
        overlap_rows = {r for r, _ in overlap_cells}
        overlap_at_top = 0 in overlap_rows and 2 not in overlap_rows
        overlap_at_bottom = 2 in overlap_rows and 0 not in overlap_rows

        # === Connected Bubble-Mask Overlap (catches bubble tails) ===
        mask_overlap = 0.0
        mask_top = mask_bottom = 0.0
        if bubble_mask is not None and bubble_mask.size > 0:
            ms = mask_scale or ContentAwarePanelDetector.BUBBLE_MASK_SCALE
            clr = ContentAwarePanelDetector.MASK_CLEARANCE
            my0 = max(0, y - clr) // ms
            my1 = min(bubble_mask.shape[0], (min(img_height, y_end + clr) + ms - 1) // ms)
            mx0 = min(bubble_mask.shape[1] - 1, x_start // ms)
            mx1 = min(bubble_mask.shape[1], max(mx0 + 1, (x_end + ms - 1) // ms))
            sub = bubble_mask[my0:my1, mx0:mx1]
            if sub.size > 0:
                mask_overlap = float(np.mean(sub))
                mid = sub.shape[0] // 2
                if mid > 0:
                    mask_top = float(np.mean(sub[:mid]))
                    mask_bottom = float(np.mean(sub[mid:]))
                else:
                    mask_top = mask_bottom = mask_overlap
        mask_hit = mask_overlap > 0.02
        mask_at_top = mask_hit and mask_top > 2 * mask_bottom
        mask_at_bottom = mask_hit and mask_bottom > 2 * mask_top
        
        # === Face/Character Detection ===
        is_face, face_confidence = ContentAwarePanelDetector.detect_face_region(region_gray, region_sat)
        
        # === Top/Bottom Half Analysis ===
        mid_y = wm_height // 2
        if mid_y > 0 and y_end - y > mid_y:
            top_half = region_gray[:mid_y, :]
            bottom_half = region_gray[mid_y:, :]

            top_very_white = np.count_nonzero(top_half > 235) / top_half.size
            bottom_very_white = np.count_nonzero(bottom_half > 235) / bottom_half.size
            
            top_has_text, _ = ContentAwarePanelDetector.detect_text_pattern(top_half)
            bottom_has_text, _ = ContentAwarePanelDetector.detect_text_pattern(bottom_half)
            
            top_bubble = top_very_white > 0.2 or (top_very_white > 0.1 and top_has_text)
            bottom_bubble = bottom_very_white > 0.2 or (bottom_very_white > 0.1 and bottom_has_text)
        else:
            top_very_white = bottom_very_white = very_white_ratio
            top_bubble = bottom_bubble = is_speech_bubble
        
        # === Color/Saturation Analysis ===
        # (saturation is uint8 0-255; normalize the scalar mean back to 0-1)
        mean_saturation = np.mean(region_sat) / 255.0 if region_sat is not None else 0
        
        # === Calculate Score ===
        score = 50  # Base score
        
        # Speech bubble penalty (HEAVY)
        if is_speech_bubble:
            if has_text:
                score -= 200
            elif very_white_ratio > 0.4:
                score -= 180
            elif very_white_ratio > 0.25:
                score -= 120
            else:
                score -= 80
        
        # Partial bubble penalty
        if top_bubble and not bottom_bubble:
            score -= 60
        elif bottom_bubble and not top_bubble:
            score -= 60
            
        if bubble_overlap and not is_speech_bubble:
            score -= 90 * min(len(overlap_cells), 3)

        # Connected bubble-mask penalty (catches tails the cell grid misses).
        # Strong enough that no color/texture bonus can outweigh a real hit.
        if mask_hit:
            score -= 150 + 400 * min(mask_overlap, 0.5)
        
        # Black/gutter penalty
        if black_ratio > 0.5:
            score -= 150
        elif black_ratio > 0.3:
            score -= 80
        
        # Face/character penalty
        if is_face:
            score -= 100 * face_confidence
        
        # Color bonus
        if mean_saturation > 0.25:
            score += 80
        elif mean_saturation > 0.15:
            score += 50
        elif mean_saturation > 0.08:
            score += 25
        
        # Medium brightness bonus
        if 70 < mean_brightness < 190:
            score += 25
        
        # Texture/detail bonus
        if 300 < variance < 2500:
            score += 30
        elif variance < 100:
            score -= 30
        elif variance > 4000:
            score -= 20

        # === Panel-Edge Affinity ===
        # A watermark should hug a panel boundary (top/bottom of a panel, next
        # to a gutter), not float vertically in the middle of a panel.
        if panel_edges:
            edge_dist = min(min(abs(y - e), abs(y_end - e)) for e in panel_edges)
            if edge_dist <= 12:
                score += 40
            elif edge_dist <= 35:
                score += 25
            elif edge_dist <= 80:
                score += 10
            elif edge_dist >= 160 and len(panel_edges) > 2:
                # Real gutters exist in this image, yet this spot is far from
                # every panel boundary — penalize mid-panel floating.
                score -= 45

        # === PROXIMITY CHECK (Border Sensor) ===
        check_margin = 4
        proximity_threshold = 240
        
        # Check Top Edge
        if y > check_margin:
            top_strip = gray[y-check_margin:y, x_start:x_end]
            if np.count_nonzero(top_strip > proximity_threshold) / top_strip.size > 0.7:
                score -= 200

        # Check Bottom Edge
        if y_end < img_height - check_margin:
            bottom_strip = gray[y_end:y_end+check_margin, x_start:x_end]
            if np.count_nonzero(bottom_strip > proximity_threshold) / bottom_strip.size > 0.7:
                score -= 200
        
        # === Build Info Dictionary ===
        info = {
            'valid': True,
            'mean_brightness': mean_brightness,
            'variance': variance,
            'very_white_ratio': very_white_ratio,
            'white_ratio': white_ratio,
            'black_ratio': black_ratio,
            'saturation': mean_saturation,
            'has_text': has_text,
            'text_confidence': text_confidence,
            'is_speech_bubble': is_speech_bubble,
            'is_face': is_face,
            'face_confidence': face_confidence,
            'top_very_white': top_very_white,
            'bottom_very_white': bottom_very_white,
            'top_bubble': top_bubble,
            'bottom_bubble': bottom_bubble,
            'bubble_overlap': bubble_overlap or mask_hit,
            'overlap_cells': overlap_cells,
            'mask_overlap': mask_overlap,
            'bubble_at_top': (top_bubble and not bottom_bubble) or overlap_at_top or mask_at_top,
            'bubble_at_bottom': (bottom_bubble and not top_bubble) or overlap_at_bottom or mask_at_bottom,
        }
        
        return score, info
    
    @staticmethod
    def is_gutter_row(gray_row, sat_row=None):
        """Check if a row is part of a gutter (panel divider)."""
        n = gray_row.size
        white_ratio = np.count_nonzero(gray_row > ContentAwarePanelDetector.WHITE_THRESHOLD) / n
        black_ratio = np.count_nonzero(gray_row < ContentAwarePanelDetector.BLACK_THRESHOLD) / n
        
        if white_ratio >= ContentAwarePanelDetector.MIN_GUTTER_COVERAGE:
            if sat_row is not None and np.mean(sat_row) > 0.15 * 255:
                return False, 'colored'
            return True, 'white'
        
        if black_ratio >= ContentAwarePanelDetector.MIN_GUTTER_COVERAGE:
            return True, 'black'
        
        return False, 'content'
    
    @staticmethod
    def find_gutters(gray, saturation):
        """Find all gutter regions in the image.

        Fully vectorized: per-row white/black coverage and saturation means
        are computed in single numpy passes instead of one Python call per
        row, then gutter runs are extracted from the row-type array. Produces
        the same gutter list as the previous per-row loop.
        """
        height = gray.shape[0]

        white_r = np.mean(gray > ContentAwarePanelDetector.WHITE_THRESHOLD, axis=1)
        black_r = np.mean(gray < ContentAwarePanelDetector.BLACK_THRESHOLD, axis=1)
        cov = ContentAwarePanelDetector.MIN_GUTTER_COVERAGE

        # 0 = content, 1 = white gutter, 2 = black gutter (mirrors is_gutter_row:
        # a white-covered row is checked for color first and never counts as black)
        types = np.zeros(height, dtype=np.uint8)
        white_cov = white_r >= cov
        if saturation is not None:
            sat_m = np.mean(saturation, axis=1)  # uint8 scale (0-255)
            types[white_cov & (sat_m <= 0.15 * 255)] = 1
        else:
            types[white_cov] = 1
        types[~white_cov & (black_r >= cov)] = 2

        # Split into runs of identical type
        change = np.flatnonzero(np.diff(types)) + 1
        starts = np.concatenate(([0], change))
        ends = np.concatenate((change, [height]))

        gutters = []
        for s, e in zip(starts, ends):
            t = types[s]
            if t != 0 and e - s >= ContentAwarePanelDetector.MIN_GUTTER_HEIGHT:
                gutters.append({
                    'start': int(s),
                    'end': int(e),
                    'type': 'white' if t == 1 else 'black',
                    'height': int(e - s)
                })

        return gutters
    
    @staticmethod
    def find_adjusted_position(gray, saturation, initial_y, direction, wm_height, wm_width,
                                img_height, range_start, range_end, margin, initial_score, initial_info, edge='left', x_margin=15,
                                bubble_mask=None, mask_scale=None, panel_edges=None, col_white=None):
        """
        Find an adjusted position away from problematic content.
        """
        best_y = initial_y
        best_score = initial_score
        best_info = initial_info

        step = ContentAwarePanelDetector.ADJUSTMENT_STEP
        max_adj = ContentAwarePanelDetector.MAX_ADJUSTMENT

        for offset in range(step, max_adj + step, step):
            test_y = initial_y + (offset * direction)

            if test_y < range_start + margin or test_y + wm_height > range_end - margin:
                break

            test_score, test_info = ContentAwarePanelDetector.analyze_region_detailed(
                gray, saturation, test_y, wm_height, wm_width, img_height, edge, x_margin,
                bubble_mask=bubble_mask, mask_scale=mask_scale, panel_edges=panel_edges, col_white=col_white
            )
            
            if test_score > best_score:
                best_y = test_y
                best_score = test_score
                best_info = test_info
            
            if (test_score > ContentAwarePanelDetector.MIN_SAFE_SCORE and 
                not test_info.get('is_speech_bubble', False) and
                not test_info.get('bubble_overlap', False) and
                not test_info.get('is_face', False)):
                break
        
        adjustment = best_y - initial_y
        return best_y, best_score, adjustment, best_info
    
    @staticmethod
    def _fallback_scan(gray, saturation, range_start, range_end, wm_width, wm_height, margin, edge='left', x_margin=15,
                       bubble_mask=None, mask_scale=None, panel_edges=None, col_white=None):
        """
        Fallback: Scan the segment for best placement.
        """
        best_y = range_start + (range_end - range_start) // 3
        best_score = -999999
        best_info = {}

        scan_start = range_start + margin
        scan_end = range_end - wm_height - margin

        if scan_end <= scan_start:
            return max(0, min(range_start + (range_end - range_start - wm_height) // 2, gray.shape[0] - wm_height)), 0, "fallback(center)"

        # Dense coarse sweep (mirrors the reference engine's ~50px stride) so we do
        # not skip over the one clean, non-bubble spot in a tall segment.
        coarse_step = min(50, max(10, wm_height // 3))
        for y in range(scan_start, scan_end, coarse_step):
            score, info = ContentAwarePanelDetector.analyze_region_detailed(
                gray, saturation, y, wm_height, wm_width, gray.shape[0], edge, x_margin,
                bubble_mask=bubble_mask, mask_scale=mask_scale, panel_edges=panel_edges, col_white=col_white
            )
            if score > best_score:
                best_score = score
                best_y = y
                best_info = info

        fine_start = max(scan_start, best_y - coarse_step)
        fine_end = min(scan_end, best_y + coarse_step)
        for y in range(fine_start, fine_end, 5):
            score, info = ContentAwarePanelDetector.analyze_region_detailed(
                gray, saturation, y, wm_height, wm_width, gray.shape[0], edge, x_margin,
                bubble_mask=bubble_mask, mask_scale=mask_scale, panel_edges=panel_edges, col_white=col_white
            )
            if score > best_score:
                best_score = score
                best_y = y
                best_info = info

        return best_y, best_score, "fallback(scan)"
    
    @staticmethod
    def find_best_watermark_position(composite, img_width, img_height, wm_w, wm_h, range_start, range_end, edge='left', x_margin=15, gray=None, saturation=None,
                                     bubble_mask=None, mask_scale=None, gutters=None):
        """
        Find the best watermark position with content-aware adjustment inside a specific segment.
        """
        if gray is None or saturation is None:
            if isinstance(composite, Image.Image):
                rgb = np.array(composite.convert('RGB'))
            else:
                rgb = composite[:, :, :3] if len(composite.shape) > 2 and composite.shape[2] >= 3 else composite

            if gray is None:
                gray = ContentAwarePanelDetector.to_grayscale(rgb)
            if saturation is None:
                saturation = ContentAwarePanelDetector.get_saturation(rgb)

        if bubble_mask is None:
            bubble_mask = ContentAwarePanelDetector.build_bubble_mask(gray, saturation)
            mask_scale = ContentAwarePanelDetector.BUBBLE_MASK_SCALE

        seg_h = range_end - range_start
        margin = min(ContentAwarePanelDetector.EDGE_MARGIN, int(seg_h * 0.1))
        if margin < 10:
            margin = 10

        # Full-height column whiteness for the (fixed) watermark x-range,
        # computed once here instead of inside every candidate evaluation.
        if edge == 'left':
            cw_x0 = x_margin
            cw_x1 = min(x_margin + wm_w, img_width)
        else:
            cw_x0 = max(0, img_width - x_margin - wm_w)
            cw_x1 = img_width - x_margin
        if cw_x1 > cw_x0:
            col_white = np.mean(gray[:, cw_x0:cw_x1] > ContentAwarePanelDetector.BUBBLE_WHITE_THRESHOLD, axis=0)
        else:
            col_white = None

        # Find gutters (whole-image; callers placing several watermarks pass
        # a precomputed list so this is not repeated per segment)
        if gutters is None:
            gutters = ContentAwarePanelDetector.find_gutters(gray, saturation)

        # Panel boundaries for edge-affinity scoring: every gutter start/end
        # plus the physical image top/bottom. Used to pull watermarks toward
        # panel edges instead of letting them float mid-panel.
        panel_edges = [0, img_height]
        for g in gutters:
            panel_edges.append(g['start'])
            panel_edges.append(g['end'])
        
        # Get panel edges from gutters
        edges = []
        for g in gutters:
            if g['start'] > range_start + margin and g['start'] < range_end - margin:
                edges.append({
                    'y': g['start'],
                    'type': 'panel_end',
                    'gutter_type': g['type'],
                    'confidence': min(1.0, g['height'] / 30.0)
                })
            
            if g['end'] > range_start + margin and g['end'] < range_end - margin:
                edges.append({
                    'y': g['end'],
                    'type': 'panel_start',
                    'gutter_type': g['type'],
                    'confidence': min(1.0, g['height'] / 30.0)
                })
        
        candidates = []
        
        for edge_item in edges:
            edge_y = edge_item['y']
            edge_type = edge_item['type']
            
            if edge_type == 'panel_start':
                initial_y = edge_y
            else:
                initial_y = edge_y - wm_h
            
            if initial_y < range_start + margin or initial_y + wm_h > range_end - margin:
                continue
            
            score, info = ContentAwarePanelDetector.analyze_region_detailed(
                gray, saturation, initial_y, wm_h, wm_w, img_height, edge, x_margin,
                bubble_mask=bubble_mask, mask_scale=mask_scale, panel_edges=panel_edges, col_white=col_white
            )
            
            final_y = initial_y
            adjustment = 0
            was_adjusted = False
            
            needs_adjustment = (
                info.get('is_speech_bubble', False) or
                info.get('bubble_overlap', False) or
                info.get('is_face', False) or
                score < ContentAwarePanelDetector.MIN_SAFE_SCORE
            )
            
            if needs_adjustment:
                if info.get('bubble_at_top', False):
                    direction = 1
                elif info.get('bubble_at_bottom', False):
                    direction = -1
                elif edge_type == 'panel_start':
                    direction = 1
                else:
                    direction = -1
                
                adj_y, adj_score, adj_amount, adj_info = ContentAwarePanelDetector.find_adjusted_position(
                    gray, saturation, initial_y, direction, wm_h, wm_w,
                    img_height, range_start, range_end, margin, score, info, edge, x_margin,
                    bubble_mask=bubble_mask, mask_scale=mask_scale, panel_edges=panel_edges, col_white=col_white
                )
                
                if adj_score > score:
                    final_y = adj_y
                    score = adj_score
                    info = adj_info
                    adjustment = adj_amount
                    was_adjusted = True
            
            adj_str = ""
            if was_adjusted:
                adj_dir = "↓" if adjustment > 0 else "↑"
                adj_str = f"[{adj_dir}{abs(adjustment)}px]"
            
            candidates.append({
                'y': final_y,
                'score': score,
                'edge_type': edge_type,
                'gutter_type': edge_item['gutter_type'],
                'adjusted': was_adjusted,
                'adjustment': adjustment,
                'adj_str': adj_str,
                'info': info,
                'confidence': edge_item['confidence']
            })
        
        if edge == 'left':
            x_pos = x_margin
        else:
            x_pos = img_width - x_margin - wm_w
            if x_pos < 0:
                x_pos = 0
                
        candidates.sort(key=lambda x: x['score'], reverse=True)
        best = candidates[0] if candidates else None

        # If the best gutter-based candidate is unsafe (speech bubble, face, or just
        # a low score) — or there were no gutter candidates at all — sweep the whole
        # segment densely and keep whichever spot scores higher. This mirrors the
        # reference engine, whose whole-image gutter set almost always offers a clean
        # spot; per-segment detection can otherwise be forced onto a bubble that
        # merely happens to border a detected gutter.
        best_unsafe = (
            best is None or
            best['score'] < ContentAwarePanelDetector.MIN_SAFE_SCORE or
            best['info'].get('is_speech_bubble', False) or
            best['info'].get('bubble_overlap', False) or
            best['info'].get('is_face', False)
        )

        if best_unsafe:
            scan_y, scan_score, scan_info = ContentAwarePanelDetector._fallback_scan(
                gray, saturation, range_start, range_end, wm_w, wm_h, margin, edge, x_margin,
                bubble_mask=bubble_mask, mask_scale=mask_scale, panel_edges=panel_edges, col_white=col_white
            )
            if best is None or scan_score > best['score']:
                return x_pos, scan_y, scan_score, scan_info

        edge_info = f"{best['edge_type']}({best['gutter_type']}){best['adj_str']}"
        return x_pos, best['y'], best['score'], edge_info
def compute_watermark_placements(img, watermark_path, count, edge, watermark_width_percent=12, margin=15):
    """
    Computes the best positions for `count` watermarks on `img` using the
    ContentAwarePanelDetector logic, WITHOUT modifying the image.

    Returns a tuple `(wm, placements)` where `wm` is the resized watermark
    (PIL image) and `placements` is a list of `(x, y)` positions.
    Returns `(None, [])` if the watermark cannot be loaded.
    """
    if not watermark_path or not os.path.exists(watermark_path):
        return None, []

    try:
        W, H = img.size

        # Load + scale the watermark to fit this canvas
        wm = _prepare_watermark_for_canvas(watermark_path, W, H, count)
        if wm is None:
            return None, []
        wm_w, wm_h = wm.size

        # Precalculate gray and saturation once for the entire image using native PIL conversions.
        # Saturation stays uint8 (PIL's native S channel) — no float32 copy of the
        # whole image, which for a tall page saves tens of MB and a full-image division.
        gray = np.array(img.convert('L'))
        # Convert to RGB first to ensure HSV conversion is fully supported across all
        # PIL versions (skipping the copy when the image is already RGB)
        rgb_src = img if img.mode == 'RGB' else img.convert('RGB')
        saturation = np.array(rgb_src.convert('HSV').getchannel('S'))

        # Whole-image connected bubble mask (built once, shared by all segments):
        # covers each bubble's full outline including its tail.
        bubble_mask = ContentAwarePanelDetector.build_bubble_mask(gray, saturation)
        mask_scale = ContentAwarePanelDetector.BUBBLE_MASK_SCALE

        # Whole-image gutter list (built once, shared by all segments — it was
        # previously recomputed from scratch inside every segment's search).
        gutters = ContentAwarePanelDetector.find_gutters(gray, saturation)

        # Segment page height into `count` segments
        segment_height = H / float(count)

        placements = []
        for i in range(count):
            seg_start = int(i * segment_height)
            seg_end = int((i + 1) * segment_height)

            if seg_end - seg_start < wm_h:
                continue

            # Find watermark position using the content-aware panel detector
            x_pos, y_pos, score, edge_info = ContentAwarePanelDetector.find_best_watermark_position(
                img, W, H, wm_w, wm_h, seg_start, seg_end, edge=edge, x_margin=margin,
                gray=gray, saturation=saturation, bubble_mask=bubble_mask, mask_scale=mask_scale,
                gutters=gutters
            )

            # Ensure y_pos is within bounds
            y_pos = max(seg_start, min(y_pos, seg_end - wm_h))
            placements.append((x_pos, y_pos))

        return wm, placements

    except Exception as e:
        print(f"Error computing watermark placements: {e}")
        return None, []


def apply_watermark(img, watermark_path, count, edge, watermark_width_percent=12, margin=15):
    """
    Applies `count` watermarks to `img` at the best locations on the left or right edge.
    Uses the advanced ContentAwarePanelDetector logic.
    """
    try:
        # Ensure img is writeable and in RGB/RGBA
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')

        wm, placements = compute_watermark_placements(
            img, watermark_path, count, edge, watermark_width_percent, margin
        )
        if not wm:
            return img

        for x_pos, y_pos in placements:
            img.paste(wm, (x_pos, y_pos), wm)

    except Exception as e:
        print(f"Error applying watermark: {e}")

    return img


def _save_multilayer_psd(path: str, base_image: Image.Image, placements: list) -> bool:
    """Write a Photoshop-compatible PSD with the slice art as the background layer and
    each watermark as its own movable/editable layer on top.

    Hand-rolled writer (not pytoshop) because pytoshop's output passes the basic format
    checks (Pillow/sips read it) but Photoshop refuses it as "not compatible" — it's
    missing tagged blocks that newer Photoshop versions require. This writer follows
    the Adobe PSD spec section-by-section and matches Photoshop's own output.

    Args:
        path: target .psd file
        base_image: PIL RGB image — the slice art (becomes the "Art" layer)
        placements: list of {"image": PIL RGBA, "x": int, "y": int, "name": str}

    Returns True on success.
    """
    import struct
    import zlib

    def be_u16(v): return struct.pack(">H", v & 0xFFFF)
    def be_u32(v): return struct.pack(">I", v & 0xFFFFFFFF)
    def be_s16(v): return struct.pack(">h", v)
    def be_s32(v): return struct.pack(">i", v)

    def pascal_name(name: str) -> bytes:
        """Pascal-style layer name, padded so the whole field is a multiple of 4 bytes."""
        nb = name.encode("utf-8", errors="replace")[:255]
        raw = bytes([len(nb)]) + nb
        pad = (4 - (len(raw) % 4)) % 4
        return raw + (b"\x00" * pad)

    def unicode_name_block(name: str) -> bytes:
        """`luni` tagged block — Unicode layer name. Photoshop strongly prefers this."""
        utf16 = name.encode("utf-16-be")
        char_count = len(name)
        body = be_u32(char_count) + utf16
        # Pad body to 4-byte boundary
        pad = (4 - (len(body) % 4)) % 4
        body += b"\x00" * pad
        return b"8BIM" + b"luni" + be_u32(len(body)) + body

    def lsct_divider_block() -> bytes:
        """`lsct` — section divider; flat layer (type 0). Helps Photoshop layer panel."""
        body = be_u32(0)  # type: 0 = any other type of layer
        return b"8BIM" + b"lsct" + be_u32(len(body)) + body

    def build_channel_data_zip(arr_2d: np.ndarray) -> bytes:
        """Per-channel PSD data: compression code (2 = zip-no-prediction) + zlib bytes.

        Zip is in the PSD spec and Photoshop opens it. It's also 10-50× faster than
        Python-level RLE/PackBits for big channels.
        """
        return be_u16(2) + zlib.compress(arr_2d.tobytes(), 6)

    try:
        # ── Canvas / Art layer ──
        base_rgb = base_image.convert("RGB") if base_image.mode != "RGB" else base_image
        h, w = base_rgb.height, base_rgb.width
        base_arr = np.asarray(base_rgb, dtype=np.uint8)
        base_r = np.ascontiguousarray(base_arr[:, :, 0])
        base_g = np.ascontiguousarray(base_arr[:, :, 1])
        base_b = np.ascontiguousarray(base_arr[:, :, 2])

        # ── Watermark layers ──
        wm_records = []  # list of (name, top, left, bottom, right, alpha_arr, r, g, b)
        for idx, p in enumerate(placements):
            wm = p["image"]
            if wm.mode != "RGBA":
                wm = wm.convert("RGBA")
            wm_arr = np.asarray(wm, dtype=np.uint8)
            ww, wh = wm.width, wm.height
            x = int(p["x"]); y = int(p["y"])
            x = max(0, min(w, x))
            y = max(0, min(h, y))
            right = max(0, min(w, x + ww))
            bottom = max(0, min(h, y + wh))
            if right <= x or bottom <= y:
                continue
            ch = bottom - y
            cw = right - x
            if cw != ww or ch != wh:
                wm_arr = wm_arr[:ch, :cw]
            name = (p.get("name") or f"Watermark {idx + 1}").replace("\x00", "").strip()
            wm_records.append((
                name, y, x, bottom, right,
                np.ascontiguousarray(wm_arr[:, :, 3]),
                np.ascontiguousarray(wm_arr[:, :, 0]),
                np.ascontiguousarray(wm_arr[:, :, 1]),
                np.ascontiguousarray(wm_arr[:, :, 2]),
            ))
        # Layer order in PSD bottom-up: index 0 = bottom layer. So Art first, then WMs.
        all_layers = [("Art", 0, 0, h, w, None, base_r, base_g, base_b)] + wm_records

        # ── Build Layer Records + Channel Data ──
        layer_records = []
        channel_data_blobs = []  # corresponds 1:1 with layer order

        for name, top, left, bottom, right, alpha, r_ch, g_ch, b_ch in all_layers:
            chans_data = []  # (channel_id, compressed_bytes) tuples
            if alpha is not None:
                chans_data.append((-1, build_channel_data_zip(alpha)))
            chans_data.append((0, build_channel_data_zip(r_ch)))
            chans_data.append((1, build_channel_data_zip(g_ch)))
            chans_data.append((2, build_channel_data_zip(b_ch)))

            # Layer Record header
            rec = b""
            rec += be_s32(top) + be_s32(left) + be_s32(bottom) + be_s32(right)
            rec += be_u16(len(chans_data))
            for cid, cdata in chans_data:
                rec += be_s16(cid) + be_u32(len(cdata))
            rec += b"8BIM" + b"norm"           # blend mode signature + key
            rec += bytes([255, 0, 0, 0])        # opacity, clipping, flags, filler

            # Extra data field
            extra = b""
            extra += be_u32(0)  # Layer mask data: length 0
            # Layer blending ranges: composite + 4 channels = 5 ranges × 8 bytes
            blending_data = b""
            for _ in range(5):
                blending_data += b"\x00\x00\xff\xff" + b"\x00\x00\xff\xff"
            extra += be_u32(len(blending_data)) + blending_data
            extra += pascal_name(name)
            # Additional layer info: Unicode name (luni). Photoshop expects this.
            extra += unicode_name_block(name)

            rec += be_u32(len(extra)) + extra

            layer_records.append(rec)
            channel_data_blobs.append(b"".join(cdata for _, cdata in chans_data))

        # ── Layer Info ──
        layer_count = len(all_layers)
        layer_info = b""
        layer_info += be_s16(layer_count)  # positive = first alpha is NOT transparency
        for r in layer_records:
            layer_info += r
        for cd in channel_data_blobs:
            layer_info += cd

        # Pad layer_info to 2-byte boundary
        if len(layer_info) % 2 == 1:
            layer_info += b"\x00"

        # ── Layer and Mask Information section ──
        # = u32(length of layer_info) + layer_info + global_layer_mask_info + additional
        layer_info_with_len = be_u32(len(layer_info)) + layer_info
        global_layer_mask = be_u32(0)  # 0 = no global mask
        layer_mask_section_body = layer_info_with_len + global_layer_mask
        layer_mask_section = be_u32(len(layer_mask_section_body)) + layer_mask_section_body

        # ── Merged Image Data (compressed flat preview) ──
        # Compose the watermarks onto a copy of base to produce the preview.
        preview = base_rgb.copy().convert("RGBA")
        for name, top, left, bottom, right, alpha, r_ch, g_ch, b_ch in wm_records:
            ww_p = right - left
            wh_p = bottom - top
            rgba = np.zeros((wh_p, ww_p, 4), dtype=np.uint8)
            rgba[:, :, 0] = r_ch
            rgba[:, :, 1] = g_ch
            rgba[:, :, 2] = b_ch
            rgba[:, :, 3] = alpha if alpha is not None else 255
            wm_pil = Image.fromarray(rgba, "RGBA")
            preview.alpha_composite(wm_pil, (left, top))
        preview_rgb = np.asarray(preview.convert("RGB"), dtype=np.uint8)
        prev_r = np.ascontiguousarray(preview_rgb[:, :, 0])
        prev_g = np.ascontiguousarray(preview_rgb[:, :, 1])
        prev_b = np.ascontiguousarray(preview_rgb[:, :, 2])
        # Merged image data section. PSD spec: one compression code (2 bytes) at the
        # start, then per-channel data concatenated. Compression 0 = raw uncompressed,
        # which is the simplest format Photoshop reads natively. Writing this raw is
        # ~100× faster than per-row PackBits and avoids any subtle encoder bugs.
        merged_section = (
            be_u16(0)
            + prev_r.tobytes()
            + prev_g.tobytes()
            + prev_b.tobytes()
        )

        # ── Header ──
        header = b""
        header += b"8BPS"
        header += be_u16(1)                # version 1 (PSD)
        header += b"\x00" * 6              # reserved
        header += be_u16(3)                # 3 channels (RGB)
        header += be_u32(h)
        header += be_u32(w)
        header += be_u16(8)                # 8-bit depth
        header += be_u16(3)                # RGB mode

        # ── Color Mode Data: empty for RGB ──
        color_mode_data = be_u32(0)

        # ── Image Resources: minimal — just resolution info (~28 bytes) ──
        # Resolution block (1005): 16 bytes resolution info inside.
        # Build the resolution info: hRes(4), hResUnit(2), widthUnit(2), vRes(4), vResUnit(2), heightUnit(2) = 16 bytes
        res_info = b""
        res_info += be_u32(72 << 16) + be_u16(1) + be_u16(1)
        res_info += be_u32(72 << 16) + be_u16(1) + be_u16(1)
        # Image resource block: '8BIM' + id(2) + name(pascal, padded to 2) + size(4) + data
        ir_block = b"8BIM" + be_u16(1005) + b"\x00\x00" + be_u32(len(res_info)) + res_info
        if len(ir_block) % 2:
            ir_block += b"\x00"
        image_resources = be_u32(len(ir_block)) + ir_block

        # ── Write the file ──
        with open(path, "wb") as f:
            f.write(header)
            f.write(color_mode_data)
            f.write(image_resources)
            f.write(layer_mask_section)
            f.write(merged_section)
        return True
    except Exception as e:
        import traceback
        print(f"hand-rolled PSD writer failed: {e}")
        traceback.print_exc()
        return False


def save_psd_layered(img, filepath, watermark_enabled=False, watermark_path="", watermark_count=1, watermark_edge="right", watermark_width_percent=12):
    """
    Saves `img` as a PSD file.

    When the watermark is enabled, the watermark is NOT baked into the pixels;
    instead the base image and each watermark are written as separate layers so
    the user can freely reposition (or hide) the watermark in Photoshop.

    The watermark layer is guaranteed to be present in every PSD produced
    while watermarking is on: if the content-aware placement search fails
    (detector error, segment too small, ...) the watermark is still added at
    deterministic fallback positions instead of being silently dropped.
    Only when the watermark file itself cannot be loaded (or watermarking is
    off) does this fall back to a flat, layer-less PSD.
    """
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')

    placements_dict = []

    if watermark_enabled:
        wm = None
        placements = []
        try:
            wm, placements = compute_watermark_placements(
                img, watermark_path, watermark_count, watermark_edge, watermark_width_percent
            )
        except Exception as e:
            print(f"Error computing watermark placements for PSD: {e}")

        # The content-aware search can fail or come back empty (e.g. every
        # segment shorter than the watermark). The watermark layer must still
        # exist in the PSD, so fall back to fixed edge-hugging positions.
        if wm is None and watermark_path and os.path.exists(watermark_path):
            wm = _prepare_watermark_for_canvas(watermark_path, img.width, img.height, watermark_count)
        if wm is not None and not placements:
            placements = _default_watermark_placements(
                img.size, wm.size, watermark_count, watermark_edge
            )

        if wm and placements:
            for i, (x_pos, y_pos) in enumerate(placements):
                layer_name = 'Watermark' if len(placements) == 1 else f'Watermark {i + 1}'
                placements_dict.append({
                    "image": wm,
                    "x": x_pos,
                    "y": y_pos,
                    "name": layer_name
                })
        else:
            if watermark_path:
                print(
                    f"Warning: watermark could not be loaded from '{watermark_path}'; "
                    f"saving flat PSD without a watermark layer: {filepath}"
                )

    # Use the hand-rolled PSD writer instead of psd-tools to avoid compatibility issues.
    success = _save_multilayer_psd(filepath, img, placements_dict)
    if not success:
        print(f"Warning: Hand-rolled layered PSD saving failed, falling back to basic flat image save.")
        # Fallback to basic flat image save using Pillow
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(filepath)


def mergerImages(mode, newWidth, isChecked, imagePaths, saveFormat, SaveQuality, saveDirectory, heightLimit, current_date, is_zip, isPdf, isNoStitch=False, isCbz=False, progress_callback=None, webp_fallback_callback=None, output_base="./Results", max_workers=4, filename_pattern="[number]", filename_digits=3, watermark_enabled=False, watermark_path="", watermark_count=1, watermark_edge="right", watermark_width_percent=12):
    """
    Main orchestration function for image processing.
    Determines whether to stitch images or process them individually (no-stitch mode).
    """
    images = getAllImagesDirectory(imagePaths)
    if len(images) == 0:
        return False

    # If no-stitch mode is selected with WebP output and any single image exceeds WebP's
    # maximum height limit, fall back to stitched mode (where cut points are capped under the limit)
    # and notify via callback.
    if isNoStitch and saveFormat.lower() == 'webp':
        if any_image_exceeds_webp_limit(images, isChecked, newWidth):
            isNoStitch = False
            if webp_fallback_callback:
                webp_fallback_callback()

    # --- 1. Determine Output Directory ---
    base_folder = output_base
    if mode == 'single':
        folderName = saveDirectory or "folderName"
        save_path = os.path.join(base_folder, folderName)
    elif mode == 'multi':
        folderName = saveDirectory or current_date
        save_path = os.path.join(base_folder, current_date, folderName)
    else:
        raise ValueError("Invalid mode.")

    # Avoid duplicate output folder names
    counter = 0
    original_save_path = save_path
    while os.path.exists(save_path) or os.path.exists(f"{save_path}.zip") or os.path.exists(f"{save_path}.pdf") or os.path.exists(f"{save_path}.cbz"):
        counter += 1
        save_path = f"{original_save_path} ({counter})"

    # PSD format cannot be embedded in PDF; fallback to JPG if PDF is requested
    if isPdf and saveFormat.upper() == 'PSD':
        saveFormat = 'JPG'

    # --- 2. Execution Branching ---
    if isNoStitch:
        # Process images individually
        return process_batch_no_stitch(
            images, save_path, newWidth, isChecked, saveFormat,
            SaveQuality, is_zip, isPdf, isCbz, current_date, mode, progress_callback,
            output_base=output_base, max_workers=max_workers,
            filename_pattern=filename_pattern, filename_digits=filename_digits,
            watermark_enabled=watermark_enabled, watermark_path=watermark_path,
            watermark_count=watermark_count, watermark_edge=watermark_edge,
            watermark_width_percent=watermark_width_percent
        )
    else:
        # Stitched processing
        result = get_concat_v_optimized(images, newWidth, isChecked, max_workers=max_workers)
        if result is None:
            return False

        SlicerCount = int(result.height) / heightLimit if heightLimit > 0 else 1
        slicer(result, saveFormat, SlicerCount, SaveQuality, mode, current_date, saveDirectory, is_zip, isPdf, isCbz, progress_callback, output_base=output_base, max_workers=max_workers, filename_pattern=filename_pattern, filename_digits=filename_digits, watermark_enabled=watermark_enabled, watermark_path=watermark_path, watermark_count=watermark_count, watermark_edge=watermark_edge, watermark_width_percent=watermark_width_percent)
        
        result.close()
        return True
