from math import ceil
from PIL import Image, ImageFile
import os, glob

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


def image_width_changer(image_paths, new_width: int):
    new_images = []

    for image_path in image_paths:
        with Image.open(image_path) as image:
            width, height = image.size
            new_height = int(new_width * height / width)
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


def slicer(image, saveFormat, slicesCount, saveQuality, mode, current_date, saveDirectory=None):
    try:
        width, height = image.size
        slices = height / ceil(slicesCount)
        last = 0
        # Create the save directory if it does not exist

        if mode == 'single':
            save_path = os.path.join("./Results", saveDirectory or "")
        elif mode == 'multi':
            save_path = os.path.join("./Results", current_date, saveDirectory or "")
        else:
            raise ValueError("Invalid mode. Mode should be either 'single' or 'multi'.")
        os.makedirs(save_path, exist_ok=True)

        for i in range(1, ceil(slicesCount) + 1):
            res = image.crop((0, last, width, i * slices))
            last = slices * i
            filename = f"{str(i).zfill(3)}.{saveFormat}"
            filepath = os.path.join(save_path, filename)

            if saveFormat == "jpg":
                res.save(filepath, quality=saveQuality)
            elif saveFormat == "png":
                res.save(filepath)
            elif saveFormat == "webp":
                res.save(filepath, quality=saveQuality, method=6)

            res.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        image.close()


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    return subfolders

def getAllImagesDirectory(imagesPath):
    imagesLocations = []
    for i in ["jpg", "jpeg", "png", "webp"]:
        imagesLocations.extend(glob.glob(fr"{imagesPath}/*.{i}"))
    return sorted(imagesLocations)


def mergerImages(mode, newWidth, isChecked, imagePaths, saveFormat, SaveQuality, saveDirectory, heightLimit, current_date):
    images = getAllImagesDirectory(imagePaths)
    if len(images) > 0:
        if isChecked:
            images_list = image_width_changer(images, newWidth)
            result = get_concat_v_image(images_list, saveFormat)

        else:
            result = get_concat_v(images, saveFormat)
        SlicerCount = (int(result.height) / heightLimit)
        slicer(result, saveFormat, SlicerCount,SaveQuality, mode, current_date, saveDirectory)
        return True
    else:
        return False
