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
import platform

VERSION = "4.2"

# مسیر فایل تنظیمات
SETTINGS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "EMKH_Apps", "PhotoSlicer")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")

current_os = platform.system()

# --- TRANSLATION DICTIONARY ---
TRANSLATIONS = {
    "en": {
        "ready": "Ready to Slice",
        "app_window_title": f"PhotoSlicer v{VERSION}",
        "paused": "Paused... ⏸️",
        "resuming": "Resuming... ▶️",
        "idle_done": "Done! Idle. ✅",
        "error_folder": "Please select a directory first.",
        "error_no_images": "No images or subfolders found.",
        "error_valid_dir": "Select Valid Directory! 🚫",
        "preparing": "Preparing: {0}... ✨",
        "processing_single": "Processing single folder... 🔥",
        "processing_multi": "Processing {0} - {1}/{2}... 🔥",
        "enhancer_missing": "Enhancer not found! Ensure 'realesrgan-ncnn-vulkan.exe' is in the 'up-model' folder.",
        "enhancing_load": "Loading {0} images to AI...",
        "enhancing_run": "Enhancing {0} images... 🔥",
        "enhancing_done": "Enhancement complete. ✅",
        "enhancing_fail": "Enhancement failed or skipped.",
        "error_pre_process": "Error during image pre-processing: {0}",
        "error_batch": "Error during batch enhancement: {0}",
        "skip_folder": "Skipping {0} (enhancement failed).",
        "no_images_process": "No images found to process.",
        "no_subfolders": "No subfolders with images found!",
        "open_folder_err": "Could not open folder: {0}",
        "path_not_exist": "Folder path does not exist."
    },
    "fa": {
        "ready": "آماده برای شروع",
        "app_window_title": f"فوتو اسلایسر - نسخه {VERSION}",
        "paused": "توقف... ⏸️",
        "resuming": "در حال ادامه... ▶️",
        "idle_done": "تمام شد! آماده. ✅",
        "error_folder": "لطفا ابتدا یک پوشه انتخاب کنید.",
        "error_no_images": "هیچ تصویر یا زیرپوشه‌ای یافت نشد.",
        "error_valid_dir": "پوشه معتبر انتخاب کنید! 🚫",
        "preparing": "آماده‌سازی: {0}... ✨",
        "processing_single": "پردازش پوشه تکی... 🔥",
        "processing_multi": "پردازش {0} - {1}/{2}... 🔥",
        "enhancer_missing": "فایل هوش مصنوعی یافت نشد! مطمئن شوید 'realesrgan-ncnn-vulkan.exe' در پوشه 'up-model' است.",
        "enhancing_load": "بارگذاری {0} تصویر در هوش مصنوعی...",
        "enhancing_run": "افزایش کیفیت {0} تصویر... 🔥",
        "enhancing_done": "افزایش کیفیت تکمیل شد. ✅",
        "enhancing_fail": "افزایش کیفیت شکست خورد.",
        "error_pre_process": "خطا در پیش‌پردازش تصاویر: {0}",
        "error_batch": "خطا در افزایش کیفیت گروهی: {0}",
        "skip_folder": "رد کردن {0} (خطا در AI).",
        "no_images_process": "تصویری برای پردازش یافت نشد.",
        "no_subfolders": "هیچ زیرپوشه‌ای یافت نشد! 🚫",
        "open_folder_err": "خطا در باز کردن پوشه: {0}",
        "path_not_exist": "مسیر پوشه وجود ندارد."
    }
}

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
    "no_stitch_checked": False,
    "selected_tab": "process",
    "theme": "blue",
    "language": "fa"
}

def get_msg(key, lang_code, *args):
    """Helper function to get translated message"""
    lang_dict = TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])
    msg = lang_dict.get(key, key)
    if args:
        try:
            return msg.format(*args)
        except:
            return msg
    return msg

def initialize_settings():
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
    return load_settings()

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

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def apply_settings(window, settings):
    def bool_to_js(value):
        return 'true' if value else 'false'
    
    current_theme = settings.get('theme', 'blue')
    current_lang = settings.get('language', 'fa')

    js_code = f"""
        // بررسی وجود تابع برای جلوگیری از ارور
        if (typeof showTab === 'function') {{
            document.getElementById('custom-width').checked = {bool_to_js(settings.get('custom_width_checked', True))};
            document.getElementById('width-input').value = {settings.get('width', 800)};
            document.getElementById('height-input').value = {settings.get('height_limit', 15000)};
            document.getElementById('quality-input').value = {settings.get('save_quality', 100)};
            document.getElementById('format-select').value = '{settings.get('save_format', 'jpg')}';
            document.getElementById('is-zip').checked = {bool_to_js(settings.get('zip_checked', False))};
            document.getElementById('is-pdf').checked = {bool_to_js(settings.get('pdf_checked', False))};
            document.getElementById('enhance-quality').checked = {bool_to_js(settings.get('enhance_checked', False))};
            document.getElementById('no-stitch').checked = {bool_to_js(settings.get('no_stitch_checked', False))}; 
            
            setTheme('{current_theme}');
            setLanguage('{current_lang}');
            showTab('{settings.get('selected_tab', 'process')}');
        }} else {{
            console.error('Functions not loaded yet!');
        }}
    """
    window.evaluate_js(js_code)

temp_dir = tempfile.TemporaryDirectory()
os.environ["WEBVIEW2_USER_DATA_FOLDER"] = temp_dir.name

os.makedirs("Results", exist_ok=True)

if current_os == "Windows":
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)

def on_before_show(window):
    # این کد فقط روی ویندوز اجرا شود
    if current_os == "Windows":
        value = ctypes.c_int(1)
        dwmapi.DwmSetWindowAttribute(
            wintypes.HWND(window.native.Handle.ToInt32()),
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
    # اسپلش اسکرین مشترک است
    try:
        import pyi_splash
        pyi_splash.close()
    except ImportError:
        pass

def on_shown(window):
    pass

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
    window.evaluate_js(f"document.getElementById('status').textContent = {escaped_text}")

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

def run_enhancement(input_folder, lang='fa'):
    changeStatusText(get_msg("preparing", lang, ""))
    realesrgan_path = os.path.join('up-model', 'realesrgan-ncnn-vulkan.exe')
    if not os.path.exists(realesrgan_path):
        showError(get_msg("enhancer_missing", lang))
        return None

    temp_input_dir = tempfile.mkdtemp(prefix="photoslicer_pre_enhance_")
    output_dir = tempfile.mkdtemp(prefix="photoslicer_enhanced_")
    
    files_to_process = getAllImagesDirectory(input_folder)
    total_files = len(files_to_process)
    if total_files == 0:
        shutil.rmtree(temp_input_dir)
        shutil.rmtree(output_dir)
        return input_folder

    changeStatusText(get_msg("enhancing_load", lang, total_files))
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
        showError(get_msg("error_pre_process", lang, str(e)))
        shutil.rmtree(temp_input_dir)
        shutil.rmtree(output_dir)
        return None

    try:
        changeStatusText(get_msg("enhancing_run", lang, total_files))
        command = [
            realesrgan_path, '-i', temp_input_dir, '-o', output_dir,
            '-m', os.path.join('up-model', 'models'),
            '-n', 'realesr-animevideov3-x2', '-s', '2', '-f', 'jpg'
        ]
        
        process = subprocess.run(command, check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        changeProgress(100)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        error_message = getattr(e, 'stderr', str(e))
        showError(get_msg("error_batch", lang, error_message))
        shutil.rmtree(output_dir)
        return None
    finally:
        shutil.rmtree(temp_input_dir)

    changeStatusText(get_msg("enhancing_done", lang))
    return output_dir

class Api:
    def __init__(self):
        self.pause_event = threading.Event()
        self.processing_thread = None
        self.current_lang = 'fa' # Default

    def app_ready(self):
        """وقتی جاوا اسکریپت کامل لود شد، این تابع را صدا می‌زند"""
        settings = load_settings()
        self.current_lang = settings.get('language', 'fa')
        apply_settings(window, settings)
        
        window.set_title(get_msg("app_window_title", self.current_lang))
        changeStatusText(get_msg("ready", self.current_lang))
        
    def select_folder(self):
        result = window.create_file_dialog(webview.FileDialog.FOLDER)
        return result

    def isDirectory(self, path):
        return os.path.isdir(path)

    def folderName(self, path):
        return os.path.basename(path)

    def save_settings(self, settings):
        if 'language' in settings:
            self.current_lang = settings['language']
            
            new_title = get_msg("app_window_title", self.current_lang)
            window.set_title(new_title)

            update_js = f"""
                var btnState = document.getElementById('start-button').dataset.state;
                var statusElem = document.getElementById('status');
                if(btnState === 'idle') {{
                    statusElem.textContent = {json.dumps(get_msg('ready', self.current_lang))};
                }} else if (btnState === 'paused') {{
                    statusElem.textContent = {json.dumps(get_msg('paused', self.current_lang))};
                }}
                document.documentElement.lang = '{self.current_lang}';
            """
            window.evaluate_js(update_js)
            
        save_settings(settings)
        
    def pause_processing(self):
        if self.processing_thread and self.processing_thread.is_alive():
            self.pause_event.clear()
            window.evaluate_js("stopTimer()")
            changeStatusText(get_msg("paused", self.current_lang))

    def resume_processing(self):
        if self.processing_thread and self.processing_thread.is_alive():
            window.evaluate_js("startTimer()")
            changeStatusText(get_msg("resuming", self.current_lang))
            self.pause_event.set()
    
    def open_file_explorer(self, path):
        if path and os.path.exists(path):
            try:
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin": # macOS
                    subprocess.call(["open", path])
                else: # Linux
                    subprocess.call(["xdg-open", path])
            except Exception as e:
                showError(get_msg("open_folder_err", self.current_lang, str(e)))
        else:
            showError(get_msg("path_not_exist", self.current_lang))
    
    def start_processing(self):
        # خواندن دوباره زبان برای اطمینان
        settings = load_settings()
        lang = settings.get('language', 'fa')
        self.current_lang = lang

        reset_timer()
        start_timer()
        
        isCustomWidth = is_checkbox_checked('custom-width')
        isZip = is_checkbox_checked('is-zip')
        isPdf = is_checkbox_checked('is-pdf')
        isEnhance = is_checkbox_checked('enhance-quality')
        isNoStitch = is_checkbox_checked('no-stitch')
        
        directoryAddress = getDirectory()
        newWidth = int(getWidth())
        heightLimit = int(getHeight())
        saveQuality = int(getQuality())
        saveFormat = getFormat()

        settings.update({
            "custom_width_checked": isCustomWidth, "width": newWidth,
            "height_limit": heightLimit, "save_quality": saveQuality,
            "save_format": saveFormat, "zip_checked": isZip,
            "pdf_checked": isPdf,
            "enhance_checked": isEnhance,
            "no_stitch_checked": isNoStitch
        })
        save_settings(settings)

        original_folder_name = os.path.basename(directoryAddress)
        mode = detect_folder_mode(directoryAddress)

        if mode is None:
            showError(get_msg("error_no_images", lang))
            changeStatusText(get_msg("error_valid_dir", lang))
            stop_timer(); enableStartButton(); return
        
        showSuccess(get_msg("preparing", lang, original_folder_name))
        changeProgress(0)

        def progress_updater(percent):
            changeProgress(round(percent))
            
        final_output_path = ""

        if mode == 'single':
            window.evaluate_js("setButtonState('busy')")
            window.evaluate_js("document.getElementById('start-button').disabled = true;")
            processing_dir = directoryAddress
            temp_enhancement_dir = None
            if isEnhance:
                temp_enhancement_dir = run_enhancement(directoryAddress, lang)
                if temp_enhancement_dir is None:
                    stop_timer(); enableStartButton(); return
                processing_dir = temp_enhancement_dir

            changeStatusText(get_msg("processing_single", lang))
            
            merged = mergerImages('single', newWidth, isCustomWidth, processing_dir, saveFormat, saveQuality, original_folder_name, heightLimit, "No", isZip, isPdf, isNoStitch, progress_callback=progress_updater)
            
            if temp_enhancement_dir: shutil.rmtree(temp_enhancement_dir)

            if merged:
                changeProgress(100) 
                alert(); changeStatusText(get_msg("idle_done", lang))
                final_output_path = os.path.join("Results")
            else:
                showError(get_msg("no_images_process", lang))
                changeStatusText(get_msg("no_images_process", lang))

        elif mode == 'multi':
            window.evaluate_js("setButtonState('processing')")
            
            allFolders = fast_scandir(directoryAddress)
            if not allFolders:
                showError(get_msg("no_subfolders", lang))
                changeStatusText(get_msg("no_subfolders", lang))
                stop_timer(); enableStartButton(); return

            current_date = time.strftime("%Y-%m-%d %H-%M-%S")
            
            for i, folder in enumerate(allFolders):
                self.pause_event.wait()
                folderName = os.path.basename(folder)
                changeStatusText(get_msg("processing_multi", lang, folderName, i+1, len(allFolders)))
                
                processing_sub_dir = folder
                temp_enhancement_sub_dir = None
                if isEnhance:
                    temp_enhancement_sub_dir = run_enhancement(folder, lang)
                    if temp_enhancement_sub_dir is None:
                        changeStatusText(get_msg("skip_folder", lang, folderName))
                        continue
                    processing_sub_dir = temp_enhancement_sub_dir
                
                mergerImages('multi', newWidth, isCustomWidth, processing_sub_dir, saveFormat, saveQuality, folderName, heightLimit, current_date, isZip, isPdf, isNoStitch)
                if temp_enhancement_sub_dir: shutil.rmtree(temp_enhancement_sub_dir)

                changeProgress(round((i + 1) / len(allFolders) * 100, 2))
            
            final_output_path = os.path.abspath(os.path.join("Results", current_date))
            alert(); changeStatusText(get_msg("idle_done", lang))
            
        if final_output_path:
            escaped_path = json.dumps(final_output_path)
            window.evaluate_js(f"showOpenFolderButton({escaped_path})")

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

base_w = 510
base_h = 830
screens = webview.screens
screen = screens[0]
screen_width = screen.width
screen_height = screen.height

if screen_height < 900:
    safe_height = screen_height - 100
    if base_h > safe_height:
        ratio = safe_height / base_h
        final_h = int(safe_height)
        final_w = int(base_w * ratio)
    else:
        final_h = base_h
        final_w = base_w
elif screen_height > 1200:
    scale_factor = 1.3
    final_w = int(base_w * scale_factor)
    final_h = int(base_h * scale_factor)
else:
    final_w = base_w
    final_h = base_h

if final_w > screen_width:
    ratio = (screen_width - 50) / final_w
    final_w = int(screen_width - 50)
    final_h = int(final_h * ratio)

x_pos = int((screen_width - final_w) / 2)
y_pos = int((screen_height - final_h) / 2)

window = webview.create_window(
    title=f"PhotoSlicer v{VERSION}",
    url="assets/index.html",
    width=final_w,
    height=final_h,
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
