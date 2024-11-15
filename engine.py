from math import ceil
from PIL import Image
import os, glob
from PIL import ImageFile
import zipfile
import shutil
from pillow_heif import register_avif_opener
import re

register_avif_opener()

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


def image_width_changer(image_paths, new_width: int):
    new_images = []

    for image_path in image_paths:
        with Image.open(image_path) as image:
            width, height = image.size
            if width > 0 and height > 0 and new_width > 0:
                new_height = int(new_width * height / width)
                if new_height > 0:
                    resized_image = image.resize((new_width, new_height))
                    new_images.append(resized_image)

    return new_images


def get_concat_v(image_paths, save_format):
    if not image_paths:
        raise ValueError("The image path list is empty.")

    # Open the first image to get width and mode
    first_image = Image.open(image_paths[0])
    width = first_image.width
    mode = 'RGB' if save_format == "jpg" else 'RGBA'

    # Calculate total height
    total_height = sum(Image.open(img).height for img in image_paths)

    # Create new image canvas
    dst = Image.new(mode, (width, total_height))

    current_height = 0
    for path in image_paths:
        img = Image.open(path)
        dst.paste(img, (0, current_height))
        current_height += img.height

    return dst


def get_concat_v_image(images, save_format):
    if not images:
        raise ValueError("The image list is empty.")

    width = images[0].width
    total_height = sum(img.height for img in images)

    mode = 'RGB' if save_format == "jpg" else 'RGBA'
    dst = Image.new(mode, (width, total_height))

    current_height = 0
    for img in images:
        dst.paste(img, (0, current_height))
        current_height += img.height

    return dst


def slicer(image, saveFormat, slicesCount, saveQuality, mode, current_date, saveDirectory=None, isZip=False):
    try:
        width, height = image.size
        slices = height / ceil(slicesCount)
        last = 0
        # Create the save directory if it does not exist

        # Determine the base save path and folder name
        base_folder = "./Results"
        if mode == 'single':
            folderName = saveDirectory or "folderName"
            save_path = os.path.join(base_folder, folderName)
        elif mode == 'multi':
            folderName = saveDirectory or current_date
            save_path = os.path.join(base_folder, current_date, folderName)
        else:
            raise ValueError("Invalid mode. Mode should be either 'single' or 'multi'.")

        # Check for existing folders and zip files and add numbering if necessary
        counter = 0
        original_save_path = save_path
        while os.path.exists(save_path) or os.path.exists(f"{save_path}.zip"):
            counter += 1
            save_path = f"{original_save_path} ({counter})"

        # Create the final save directory
        os.makedirs(save_path, exist_ok=True)

        for i in range(1, ceil(slicesCount) + 1):
            res = image.crop((0, last, width, i * slices))
            last = slices * i
            filename = f"{str(i).zfill(3)}.{saveFormat}"
            filepath = os.path.join(save_path, filename)

            if saveFormat == "jpg":
                res.save(filepath, quality=saveQuality, optimize=True, progressive=True)
            elif saveFormat == "png":
                res.save(filepath)
            elif saveFormat == "webp":
                res.save(filepath, quality=saveQuality, method=6, optimize=True, progressive=True)

            res.close()

        if isZip:
            folderName = os.path.basename(save_path)
            if mode == 'single':
                zipFilePath = os.path.join(os.path.dirname(save_path), f"{folderName}.zip")
            elif mode == 'multi':
                zipFilePath = os.path.join("./Results", current_date, f"{folderName}.zip")

            with zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
                for file in os.listdir(save_path):
                    file_path = os.path.join(save_path, file)
                    if os.path.isfile(file_path):
                        zip_file.write(file_path, arcname=file)  # Only add the file without directory structure

            shutil.rmtree(save_path)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        image.close()


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    return subfolders


def getAllImagesDirectory(imagesPath):
    imagesLocations = []
    for i in ["jpg", "jpeg", "png", "webp", "avif"]:
        imagesLocations.extend(glob.glob(fr"{imagesPath}/*.{i}"))
    return sorted(
        imagesLocations,
        key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()) if re.search(r'\d+', os.path.basename(x)) else 0
    )


def mergerImages(mode, newWidth, isChecked, imagePaths, saveFormat, SaveQuality, saveDirectory, heightLimit, current_date, is_zip):
    images = getAllImagesDirectory(imagePaths)
    if len(images) > 0:
        if isChecked:
            images_list = image_width_changer(images, newWidth)
            result = get_concat_v_image(images_list, saveFormat)

        else:
            result = get_concat_v(images, saveFormat)
        SlicerCount = (int(result.height) / heightLimit)
        slicer(result, saveFormat, SlicerCount,SaveQuality, mode, current_date, saveDirectory, is_zip)
        return True
    else:
        return False
