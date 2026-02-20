from math import ceil
from PIL import Image, ImageFile
import os
import zipfile
import shutil
from pillow_heif import register_avif_opener
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
register_avif_opener()
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


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


def get_concat_v_optimized(image_paths, new_width, is_custom_width):
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
    # max_workers=4 is a safe sweet spot for memory/speed
    with ThreadPoolExecutor(max_workers=4) as executor:
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
    
    # ─── پارامترهای جدید برای بررسی عمودی ───
    # فاصله سطرهایی که بالا و پایین بررسی می‌شن
    vertical_check_offsets = [-25, -15, -8, 8, 15, 25]
    # ─────────────────────────────────────────────
    
    slice_locations = [0]
    row = split_height
    move_up = True
    
    while row < last_row:
        if row >= last_row:
            break
            
        # ─── مرحله ۱: بررسی افقی خود سطر (مثل قبل) ───
        can_slice = _is_row_uniform(combined_img, row, width, ignorable_pixels, threshold)
        
        # ─── مرحله ۲: بررسی عمودی - آیا واقعاً فضای خالی است؟ ───
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
    """بررسی یکنواختی افقی یک سطر - استخراج شده برای استفاده مجدد"""
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


def slicer(image, saveFormat, slicesCount, saveQuality, mode, current_date, saveDirectory=None, isZip=False, isPdf=False, progress_callback=None):
    def process_slice(start, end, image_file, index, save_path):
        width, _ = image_file.size
        res = image_file.crop((0, start, width, end))
        filename = f"{str(index).zfill(3)}.{saveFormat.lower()}"
        filepath = os.path.join(save_path, filename)
        if saveFormat.lower() == "webp":
            res.save(filepath, format="webp", quality=saveQuality, method=6)
        else:
            res.save(filepath, quality=saveQuality, optimize=True, progressive=True)
        res.close()

    image_file = image
    base_folder = "./Results"
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
    while os.path.exists(save_path) or os.path.exists(f"{save_path}.zip"):
        counter += 1
        save_path = f"{original_save_path} ({counter})"
    os.makedirs(save_path, exist_ok=True)
    
    cut_points = find_safe_cut_points(image_file, slicesCount)
    cut_points = [0] + cut_points
    
    # --- Slicing Logic with Progress ---
    futures = []
    with ThreadPoolExecutor() as executor:
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
            zipFilePath = os.path.join("./Results", current_date, f"{folderName}.zip")

        with zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
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
            pdfFilePath = os.path.join("./Results", current_date, f"{folderName}.pdf")

        image_files = sorted([os.path.join(save_path, f) for f in os.listdir(save_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
        
        if image_files:
            # Just load the first one for appending, load others as filenames (Pillow handles it)
            # This saves some RAM compared to loading all at once.
            img1 = Image.open(image_files[0]).convert("RGB")
            other_images = [Image.open(f).convert("RGB") for f in image_files[1:]]
            
            img1.save(pdfFilePath, "PDF", resolution=100.0, save_all=True, append_images=other_images)
            
            img1.close()
            for img in other_images:
                img.close()
        
        shutil.rmtree(save_path)
    
    image_file.close()


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    return subfolders


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


def process_batch_no_stitch(images, save_path, newWidth, isChecked, saveFormat, SaveQuality, is_zip, isPdf, current_date, mode, progress_callback=None):
    """
    این تابع مسئولیت پردازش تصاویر بدون چسباندن را بر عهده دارد.
    شامل: ریسایز (اختیاری)، ذخیره سازی، و ساخت ZIP/PDF
    """
    os.makedirs(save_path, exist_ok=True)

    def worker_save_single(args):
        img_path, idx = args
        try:
            img = open_image_robust(img_path)
            if not img: return None

            # ریسایز فقط اگر تیک Width زده شده باشد
            if isChecked:
                w_percent = (newWidth / float(img.size[0]))
                h_size = int((float(img.size[1]) * float(w_percent)))
                img = img.resize((newWidth, h_size), Image.Resampling.BICUBIC)

            filename = f"{str(idx + 1).zfill(3)}.{saveFormat.lower()}"
            filepath = os.path.join(save_path, filename)

            if saveFormat.lower() == "webp":
                img.save(filepath, format="webp", quality=SaveQuality, method=6)
            else:
                img.save(filepath, quality=SaveQuality, optimize=True, progressive=True)
            
            img.close()
            return True
        except Exception as e:
            print(f"Error in no-stitch mode for {img_path}: {e}")
            return False

    # اجرای موازی
    tasks = [(path, i) for i, path in enumerate(images)]
    completed_count = 0
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker_save_single, t) for t in tasks]
        for future in as_completed(futures):
            future.result()
            completed_count += 1
            if progress_callback:
                percent = (completed_count / len(images)) * 100
                progress_callback(percent)

    # مدیریت خروجی فشرده یا PDF
    folderNameBase = os.path.basename(save_path)
    
    if is_zip:
        zipFilePath = ""
        if mode == 'single':
            zipFilePath = os.path.join(os.path.dirname(save_path), f"{folderNameBase}.zip")
        elif mode == 'multi':
            zipFilePath = os.path.join("./Results", current_date, f"{folderNameBase}.zip")

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
            pdfFilePath = os.path.join("./Results", current_date, f"{folderNameBase}.pdf")

        output_images = sorted([os.path.join(save_path, f) for f in os.listdir(save_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
        
        if output_images:
            img1 = Image.open(output_images[0]).convert("RGB")
            other_images = [Image.open(f).convert("RGB") for f in output_images[1:]]
            img1.save(pdfFilePath, "PDF", resolution=100.0, save_all=True, append_images=other_images)
            img1.close()
            for img in other_images: img.close()
        
        shutil.rmtree(save_path)

    return True


def mergerImages(mode, newWidth, isChecked, imagePaths, saveFormat, SaveQuality, saveDirectory, heightLimit, current_date, is_zip, isPdf, isNoStitch=False, progress_callback=None):
    """
    تابع اصلی مدیریت کننده.
    تصمیم می‌گیرد که آیا تصاویر را بچسباند (Stitch) یا جداگانه پردازش کند (No Stitch).
    """
    images = getAllImagesDirectory(imagePaths)
    if len(images) == 0:
        return False

    # --- 1. تعیین مسیر ذخیره سازی (مشترک بین هر دو حالت) ---
    base_folder = "./Results"
    if mode == 'single':
        folderName = saveDirectory or "folderName"
        save_path = os.path.join(base_folder, folderName)
    elif mode == 'multi':
        folderName = saveDirectory or current_date
        save_path = os.path.join(base_folder, current_date, folderName)
    else:
        raise ValueError("Invalid mode.")

    # جلوگیری از تکراری شدن نام پوشه
    counter = 0
    original_save_path = save_path
    while os.path.exists(save_path) or os.path.exists(f"{save_path}.zip") or os.path.exists(f"{save_path}.pdf"):
        counter += 1
        save_path = f"{original_save_path} ({counter})"

    # --- 2. انشعاب منطق ---
    if isNoStitch:
        # فراخوانی تابع جدید جداگانه
        return process_batch_no_stitch(
            images, save_path, newWidth, isChecked, saveFormat, 
            SaveQuality, is_zip, isPdf, current_date, mode, progress_callback
        )
    else:
        # منطق قدیمی (چسباندن)
        result = get_concat_v_optimized(images, newWidth, isChecked)
        if result is None:
            return False

        SlicerCount = int(result.height) / heightLimit if heightLimit > 0 else 1
        slicer(result, saveFormat, SlicerCount, SaveQuality, mode, current_date, saveDirectory, is_zip, isPdf, progress_callback)
        
        result.close()
        return True

