import webview
from engine import mergerImages, fast_scandir, getAllImagesDirectory
import time
import os
import tempfile
import ctypes
from ctypes import wintypes
import json
from pathlib import Path
import subprocess
import shutil
from PIL import Image
from io import BytesIO
import threading

VERSION = "4.0"

# مسیر فایل تنظیمات
SETTINGS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "EMKH_Apps", "PhotoSlicer")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")

# تنظیمات پیش‌فرض
DEFAULT_SETTINGS = {
    "custom_width_checked": True,
    "width": 800,
    "height_limit": 16000,
    "save_quality": 100,
    "save_format": "jpg",
    "zip_checked": False,
    "pdf_checked": False,
    "enhance_checked": False,
    "selected_tab": "process",
    "theme": "blue"
}

# ایجاد پوشه تنظیمات و فایل تنظیمات اگر وجود نداشته باشند
def initialize_settings():
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
    return load_settings()

# خواندن تنظیمات از فایل
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            for key, default_value in DEFAULT_SETTINGS.items():
                if key not in settings or not isinstance(settings.get(key), type(default_value)):
                    settings[key] = default_value
            return settings
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return DEFAULT_SETTINGS

# ذخیره تنظیمات در فایل
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# اعمال تنظیمات در رابط کاربری
def apply_settings(window, settings):
    def bool_to_js(value):
        return 'true' if value else 'false'
    
    current_theme = settings.get('theme', 'blue')

    js_code = f"""
        document.getElementById('custom-width').checked = {bool_to_js(settings.get('custom_width_checked', True))};
        document.getElementById('width-input').value = {settings.get('width', 800)};
        document.getElementById('height-input').value = {settings.get('height_limit', 15000)};
        document.getElementById('quality-input').value = {settings.get('save_quality', 100)};
        document.getElementById('format-select').value = '{settings.get('save_format', 'jpg')}';
        document.getElementById('is-zip').checked = {bool_to_js(settings.get('zip_checked', False))};
        document.getElementById('is-pdf').checked = {bool_to_js(settings.get('pdf_checked', False))};
        document.getElementById('enhance-quality').checked = {bool_to_js(settings.get('enhance_checked', False))};
        showTab('{settings.get('selected_tab', 'process')}');
        setTheme('{current_theme}');
    """
    window.evaluate_js(js_code)

temp_dir = tempfile.TemporaryDirectory()
os.environ["WEBVIEW2_USER_DATA_FOLDER"] = temp_dir.name

os.makedirs("Results", exist_ok=True)

DWMWA_USE_IMMERSIVE_DARK_MODE = 20
user32 = ctypes.WinDLL("user32", use_last_error=True)
dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)

def on_before_show(window):
    value = ctypes.c_int(1)
    dwmapi.DwmSetWindowAttribute(
        wintypes.HWND(window.native.Handle.ToInt32()),
        DWMWA_USE_IMMERSIVE_DARK_MODE,
        ctypes.byref(value),
        ctypes.sizeof(value)
    )
    
    try:
        import pyi_splash
    # وقتی که پنجره اصلی آماده شد، اسپلش رو می‌بندیم
        pyi_splash.close()
    except ImportError:
    # اگه به صورت عادی اجرا بشه، این ماژول وجود نداره و مشکلی نیست
        pass

def on_shown(window):
    settings = load_settings()
    apply_settings(window, settings)

def changeProgress(percent):
    window.evaluate_js(f"document.getElementById('pr').style.width = '{percent}%'")
    window.evaluate_js(f"document.getElementById('pr-text').textContent = '{percent}%'")

def is_checkbox_checked(element_id):
    return window.evaluate_js(f'document.getElementById("{element_id}").checked')

def getWidth():
    return window.dom.get_element('#width-input').value

def getDirectory():
    return window.dom.get_element('#directory-input').value

def getHeight():
    return window.dom.get_element('#height-input').value

def changeStatusText(text):
    escaped_text = json.dumps(text)
    window.evaluate_js(f"document.getElementById('status').textContent = `Status: {text}`")

def getQuality():
    return window.dom.get_element('#quality-input').value

def getFormat():
    return window.dom.get_element('#format-select').value

def disableStartButton():
    window.evaluate_js("disableStartButton()")

def enableStartButton():
    window.evaluate_js("enableStartButton(); setButtonState('idle');")

def clearInput():
    window.dom.get_element('#directory-input').value = ""

def showError(text):
    escaped_text = json.dumps(text)
    window.evaluate_js(f"showError({escaped_text})")

def showSuccess(text):
    escaped_text = json.dumps(text)
    window.evaluate_js(f"showSuccess({escaped_text})")

def alert(file_path="success.wav"):
    window.evaluate_js(f"playAudio('{file_path}')")

def start_timer():
    window.evaluate_js("startTimer()")

def stop_timer():
    window.evaluate_js("stopTimer()")

def reset_timer():
    window.evaluate_js("resetTimer()")

def on_close():
    window.destroy()

def detect_folder_mode(directory):
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.psd'}
    has_images = False
    has_subfolders = False

    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path) and os.path.splitext(item)[1].lower() in image_extensions:
                has_images = True
            elif os.path.isdir(item_path):
                has_subfolders = True
    except (OSError, PermissionError):
        return None

    if has_images and not has_subfolders:
        return 'single'
    elif has_subfolders:
        return 'multi'
    else:
        return None

def run_enhancement(input_folder):
    changeStatusText("Preparing for enhancement... ✨")
    realesrgan_path = os.path.join('up-model', 'realesrgan-ncnn-vulkan.exe')
    if not os.path.exists(realesrgan_path):
        showError("Enhancer not found! Ensure 'realesrgan-ncnn-vulkan.exe' is in the 'up-model' folder.")
        return None

    temp_input_dir = tempfile.mkdtemp(prefix="photoslicer_pre_enhance_")
    output_dir = tempfile.mkdtemp(prefix="photoslicer_enhanced_")
    
    files_to_process = getAllImagesDirectory(input_folder)
    total_files = len(files_to_process)
    if total_files == 0:
        shutil.rmtree(temp_input_dir)
        shutil.rmtree(output_dir)
        return input_folder

    changeStatusText(f"loading {total_files} images to AI...")
    changeProgress(0)

    try:
        from engine import open_image_robust
        for index, image_path in enumerate(files_to_process):
            base_name_full = os.path.basename(image_path)
            base_name, _ = os.path.splitext(base_name_full)
            
            img = open_image_robust(image_path)
            if img is None: continue

            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            temp_save_path = os.path.join(temp_input_dir, f"{base_name}.jpg")
            img.save(temp_save_path, format='JPEG', quality=100)
            img.close()
            
            changeProgress(round(((index + 1) / total_files) * 50))

    except Exception as e:
        showError(f"Error during image pre-processing: {e}")
        shutil.rmtree(temp_input_dir)
        shutil.rmtree(output_dir)
        return None

    try:
        changeStatusText(f"Enhancing {total_files} images... 🔥")
        command = [
            realesrgan_path, '-i', temp_input_dir, '-o', output_dir,
            '-m', os.path.join('up-model', 'models'),
            '-n', 'realesr-animevideov3-x2', '-s', '2', '-f', 'jpg'
        ]
        
        process = subprocess.run(command, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        changeProgress(100)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        error_message = getattr(e, 'stderr', str(e))
        showError(f"Error during batch enhancement: {error_message}")
        shutil.rmtree(output_dir)
        return None
    finally:
        shutil.rmtree(temp_input_dir)

    changeStatusText("Enhancement complete. ✅")
    return output_dir

class Api:
    def __init__(self):
        # این دو خط رو برای کنترل وضعیت توقف اضافه کن
        self.pause_event = threading.Event()
        self.processing_thread = None
        
    def select_folder(self):
        result = window.create_file_dialog(webview.FileDialog.FOLDER)
        return result

    def isDirectory(self, path):
        return os.path.isdir(path)

    def folderName(self, path):
        return os.path.basename(path)

    def save_settings(self, settings):
        save_settings(settings)
        
    def pause_processing(self):
        """جاوا اسکریپت این متد رو برای متوقف کردن پردازش صدا می‌زنه"""
        if self.processing_thread and self.processing_thread.is_alive():
            self.pause_event.clear()  # چراغ رو قرمز می‌کنه
            window.evaluate_js("stopTimer()")
            changeStatusText("Paused... ⏸️")

    def resume_processing(self):
        """جاوا اسکریپت این متد رو برای ادامه پردازش صدا می‌زنه"""
        if self.processing_thread and self.processing_thread.is_alive():
            window.evaluate_js("startTimer()")
            changeStatusText("Resuming... ▶️")
            self.pause_event.set() # چراغ رو سبز می‌کنه
    
    def start_processing(self):
        reset_timer()
        start_timer()
        
        isCustomWidth = is_checkbox_checked('custom-width')
        isZip = is_checkbox_checked('is-zip')
        isPdf = is_checkbox_checked('is-pdf')
        isEnhance = is_checkbox_checked('enhance-quality')
        directoryAddress = getDirectory()
        newWidth = int(getWidth())
        heightLimit = int(getHeight())
        saveQuality = int(getQuality())
        saveFormat = getFormat()

        settings = load_settings()
        settings.update({
            "custom_width_checked": isCustomWidth, "width": newWidth,
            "height_limit": heightLimit, "save_quality": saveQuality,
            "save_format": saveFormat, "zip_checked": isZip,
            "pdf_checked": isPdf,
            "enhance_checked": isEnhance
        })
        save_settings(settings)

        original_folder_name = os.path.basename(directoryAddress)
        mode = detect_folder_mode(directoryAddress)

        if mode is None:
            showError("No images or subfolders found. Please select a valid directory.")
            changeStatusText("Select Valid Directory! 🚫")
            stop_timer(); enableStartButton(); return
        
        showSuccess(f"Preparing: {original_folder_name}...✨")
        changeProgress(0)

        # Define a simple callback helper
        def progress_updater(percent):
            changeProgress(round(percent))
            

        if mode == 'single':
            window.evaluate_js("setButtonState('busy')")
            window.evaluate_js("document.getElementById('start-button').disabled = true;")
            processing_dir = directoryAddress
            temp_enhancement_dir = None
            if isEnhance:
                # Note: run_enhancement already handles its own progress roughly
                temp_enhancement_dir = run_enhancement(directoryAddress)
                if temp_enhancement_dir is None:
                    stop_timer(); enableStartButton(); return
                processing_dir = temp_enhancement_dir

            changeStatusText(f"Processing single folder... 🔥")
            
            merged = mergerImages('single', newWidth, isCustomWidth, processing_dir, saveFormat, saveQuality, original_folder_name, heightLimit, "No", isZip, isPdf, progress_callback=progress_updater)
            
            if temp_enhancement_dir: shutil.rmtree(temp_enhancement_dir)

            if merged:
                # Ensure bar hits 100% at the very end
                changeProgress(100) 
                alert(); changeStatusText("Done! Idle.✅")
            else:
                showError("No images found to process."); changeStatusText("No images found! 🚫")

        elif mode == 'multi':
            window.evaluate_js("setButtonState('processing')")
            
            allFolders = fast_scandir(directoryAddress)
            if not allFolders:
                showError("No subfolders with images found."); changeStatusText("No subfolders! 🚫")
                stop_timer(); enableStartButton(); return

            current_date = time.strftime("%Y-%m-%d %H-%M-%S")
            
            for i, folder in enumerate(allFolders):
                
                self.pause_event.wait()
                
                folderName = os.path.basename(folder)
                changeStatusText(f"Processing {folderName} - {i+1}/{len(allFolders)}... 🔥")
                
                processing_sub_dir = folder
                temp_enhancement_sub_dir = None
                if isEnhance:
                    temp_enhancement_sub_dir = run_enhancement(folder)
                    if temp_enhancement_sub_dir is None:
                        changeStatusText(f"Skipping {folderName} (enhancement failed).")
                        continue
                    processing_sub_dir = temp_enhancement_sub_dir
                
                mergerImages('multi', newWidth, isCustomWidth, processing_sub_dir, saveFormat, saveQuality, folderName, heightLimit, current_date, isZip, isPdf)
                if temp_enhancement_sub_dir: shutil.rmtree(temp_enhancement_sub_dir)

                changeProgress(round((i + 1) / len(allFolders) * 100, 2))
            
            alert(); changeStatusText("Done! Idle.✅")

        clearInput()
        stop_timer()
        window.evaluate_js("setButtonState('idle')")
        window.evaluate_js("document.getElementById('start-button').disabled = false;")
        enableStartButton()

    def start(self):
        self.pause_event.set() 
        self.processing_thread = threading.Thread(target=self.start_processing)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def minimize_window(self):
        window.minimize()

    def close_window(self):
        window.destroy()

w = 520
h = 810

# 2. Get screen size (using the ctypes you already imported)
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# 3. Calculate the center (Screen - Window) / 2
x_pos = int((screen_width - w) / 2)
y_pos = int((screen_height - h) / 2)

window = webview.create_window(
    title=f"PhotoSlicer v{VERSION}",
    url="assets/index.html",
    width=int(520),
    height=int(810),
    x=x_pos,
    y=y_pos,
    resizable=True,
    js_api=Api(),
    shadow=True,
)

window.events.closed += on_close
window.events.before_show += on_before_show
window.events.shown += on_shown
initialize_settings()
webview.start()
