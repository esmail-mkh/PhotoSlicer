import webview
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
import pyperclip
import sys
import traceback

VERSION = "5.1"

# مسیر فایل تنظیمات
SETTINGS_DIR = os.path.join(os.path.expanduser("~"), "Documents", "EMKH_Apps", "PhotoSlicer")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")
LOG_FILE = os.path.join(SETTINGS_DIR, "photoslicer_error.log")

def log_and_show_exception(exc_type, exc_value, exc_tb, thread_name=None):
    """
    Global handler for unhandled exceptions (main thread & worker threads).
    Logs full traceback to SETTINGS_DIR/photoslicer_error.log and surfaces
    the error in the UI so console-less EXE mode reveals bugs.
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return

    tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    header = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Unhandled Exception"
    if thread_name:
        header += f" in thread '{thread_name}'"

    log_entry = f"{header}:\n{tb_str}\n" + ("-" * 60) + "\n"

    try:
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as log_err:
        print(f"Failed to write log file: {log_err}", file=sys.stderr)

    print(log_entry, file=sys.stderr)

    err_summary = str(exc_value) or str(exc_type.__name__)
    user_msg = f"Application Error: {err_summary}"

    if 'window' in globals() and window:
        try:
            showError(user_msg, force=True)
            enableStartButton()
            stop_timer()
        except Exception:
            pass

def install_exception_hooks():
    sys.excepthook = lambda exc_type, exc_value, exc_tb: log_and_show_exception(exc_type, exc_value, exc_tb, thread_name="Main")
    if hasattr(threading, "excepthook"):
        def thread_hook(args):
            t_name = args.thread.name if args.thread else "Worker"
            log_and_show_exception(args.exc_type, args.exc_value, args.exc_traceback, thread_name=t_name)
        threading.excepthook = thread_hook

install_exception_hooks()

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
        "path_not_exist": "Folder path does not exist.",
        "stopping": "Stopping... ⏹️",
        "stopped": "Stopped by user. ⏹️",
        "webp_nostitch_fallback": "An image is larger than WebP's limit — stitching normally instead.",
        "error_invalid_input": "Please enter valid numbers for width, height, and quality.",
        "error_watermark_path": "Please select a valid PNG watermark image.",
        "error_unexpected": "An unexpected error occurred: {0}"
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
        "path_not_exist": "مسیر پوشه وجود ندارد.",
        "stopping": "در حال توقف... ⏹️",
        "stopped": "توسط کاربر متوقف شد. ⏹️",
        "webp_nostitch_fallback": "یک تصویر بزرگ‌تر از حد مجاز WebP است؛ به‌جای حالت بدون چسباندن، به‌صورت عادی چسبانده می‌شود.",
        "error_invalid_input": "لطفاً برای عرض، ارتفاع و کیفیت عددهای معتبر وارد کنید.",
        "error_watermark_path": "لطفاً یک تصویر واترمارک PNG معتبر انتخاب کنید.",
        "error_unexpected": "خطای غیرمنتظره‌ای رخ داد: {0}"
    }
}

class ProcessStopped(Exception):
    """Raised from a progress/cancel callback to abort processing when the user clicks Stop."""
    pass

# تنظیمات پیش‌فرض
DEFAULT_SETTINGS = {
    "custom_width_checked": True,
    "width": 800,
    "height_limit": 16000,
    "save_quality": 100,
    "save_format": "jpg",
    "zip_checked": False,
    "pdf_checked": False,
    "cbz_checked": False,
    "enhance_checked": False,
    "no_stitch_checked": False,
    "selected_tab": "process",
    "theme": "blue",
    "language": "fa",
    "save_location": "",
    "save_next_to_source": False,
    "play_sound": True,
    "show_notification": True,
    "thread_count": 4,
    "output_suffix": " [Stitched]",
    "filename_pattern": "[number]",
    "filename_digits": 3,
    "custom_theme_color": "",
    "watermark_enabled": False,
    "watermark_path": "",
    "watermark_count": 1,
    "watermark_edge": "right"
}

def get_output_base(settings):
    """محل ذخیره خروجی: مسیر سفارشی کاربر یا پوشه پیش‌فرض Results کنار برنامه."""
    loc = (settings.get('save_location') or '').strip()
    return loc if loc else "./Results"

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
            # Presets are handled leniently (kept out of the strict DEFAULT_SETTINGS loop
            # because default_preset is None|str and would be reset every load otherwise)
            if not isinstance(settings.get('presets'), list):
                settings['presets'] = []
            if not isinstance(settings.get('default_preset'), (str, type(None))):
                settings['default_preset'] = None
            return settings
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        res = dict(DEFAULT_SETTINGS)
        res['presets'] = []
        res['default_preset'] = None
        return res

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)
    generate_theme_preload(settings)

def generate_theme_preload(settings):
    presets = settings.get('presets', []) or []
    default_preset = settings.get('default_preset')

    # The effective values: base settings, overlaid by the default preset (if any)
    eff = dict(settings)
    if default_preset:
        match = next((p for p in presets if isinstance(p, dict) and p.get('name') == default_preset), None)
        if match and isinstance(match.get('values'), dict):
            eff.update(match['values'])

    current_theme = eff.get('theme', 'blue')
    custom_theme_color = eff.get('custom_theme_color', '') or ''
    current_lang = eff.get('language', 'fa')
    
    js_content = f"""// This file is generated dynamically by PhotoSlicer on startup to prevent theme/language flash.
(function() {{
    var theme = {json.dumps(current_theme)};
    var customThemeColor = {json.dumps(custom_theme_color)};
    var lang = {json.dumps(current_lang)};
    var dir = (lang === 'fa') ? 'rtl' : 'ltr';

    // Apply layout direction immediately to documentElement
    document.documentElement.setAttribute('dir', dir);
    document.documentElement.setAttribute('lang', lang);

    // Apply theme immediately to documentElement
    if (customThemeColor) {{
        document.documentElement.setAttribute('data-theme', 'custom');
        var hex = customThemeColor;
        var r = parseInt(hex.slice(1,3), 16);
        var g = parseInt(hex.slice(3,5), 16);
        var b = parseInt(hex.slice(5,7), 16);
        var mid = 'rgb(' + r + ',' + g + ',' + b + ')';
        var light = 'rgb(' + Math.min(255,r+60) + ',' + Math.min(255,g+60) + ',' + Math.min(255,b+60) + ')';
        var lighter = 'rgb(' + Math.min(255,r+100) + ',' + Math.min(255,g+100) + ',' + Math.min(255,b+100) + ')';
        var variant = 'rgb(' + Math.min(255,r+30) + ',' + Math.min(255,g+15) + ',' + Math.max(0,b-15) + ')';
        
        var root = document.documentElement.style;
        root.setProperty('--theme-gradient', 'linear-gradient(135deg, ' + mid + ' 0%, ' + variant + ' 50%, ' + light + ' 100%)');
        root.setProperty('--theme-gradient-hover', 'linear-gradient(135deg, ' + light + ' 0%, ' + lighter + ' 50%, ' + light + ' 100%)');
        root.setProperty('--theme-gradient-soft', 'linear-gradient(135deg, rgba(' + r + ',' + g + ',' + b + ',0.18), rgba(' + r + ',' + g + ',' + b + ',0.18))');
        root.setProperty('--theme-solid', light);
        root.setProperty('--theme-solid-2', lighter);
        root.setProperty('--theme-glow', 'rgba(' + r + ',' + g + ',' + b + ',0.45)');
        root.setProperty('--theme-glow-strong', 'rgba(' + r + ',' + g + ',' + b + ',0.65)');
        root.setProperty('--theme-glow-soft', 'rgba(' + r + ',' + g + ',' + b + ',0.18)');
        root.setProperty('--input-focus-border', 'rgba(' + r + ',' + g + ',' + b + ',0.5)');
        
        var yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        var isLight = yiq >= 165;
        var contrast = isLight ? '#0a0e1a' : '#ffffff';
        root.setProperty('--on-theme-text', contrast);
        root.setProperty('--theme-is-light', isLight ? '1' : '0');
    }} else {{
        if (theme !== 'blue') {{
            document.documentElement.setAttribute('data-theme', theme);
        }}
        var solids = {{
            blue: '#0ea5e9',
            purple: '#d946ef',
            sunset: '#fbbf24',
            emerald: '#34d399',
            ruby: '#ef4444',
            gold: '#d4a017'
        }};
        var hex = solids[theme] || '#0ea5e9';
        var r = parseInt(hex.slice(1, 3), 16);
        var g = parseInt(hex.slice(3, 5), 16);
        var b = parseInt(hex.slice(5, 7), 16);
        var yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        var isLight = yiq >= 165;
        var contrast = isLight ? '#0a0e1a' : '#ffffff';
        document.documentElement.style.setProperty('--on-theme-text', contrast);
        document.documentElement.style.setProperty('--theme-is-light', isLight ? '1' : '0');
    }}

    // When the body is ready, copy attributes so existing scripts work seamlessly
    document.addEventListener('DOMContentLoaded', function() {{
        var t = document.documentElement.getAttribute('data-theme');
        if (t) {{
            document.body.setAttribute('data-theme', t);
        }} else {{
            document.body.removeAttribute('data-theme');
        }}
        document.body.setAttribute('dir', dir);
    }});
}})();
"""
    preload_path = os.path.join("assets", "theme-preload.js")
    try:
        with open(preload_path, "w", encoding="utf-8") as f:
            f.write(js_content)
    except Exception as e:
        print(f"Error writing theme-preload.js: {{e}}")

def apply_settings(window, settings):
    def bool_to_js(value):
        return 'true' if value else 'false'

    presets = settings.get('presets', []) or []
    default_preset = settings.get('default_preset')

    # The effective values: base settings, overlaid by the default preset (if any)
    # so the default preset fully loads on startup — including theme & language.
    eff = dict(settings)
    if default_preset:
        match = next((p for p in presets if isinstance(p, dict) and p.get('name') == default_preset), None)
        if match and isinstance(match.get('values'), dict):
            eff.update(match['values'])

    current_theme = eff.get('theme', 'blue')
    current_lang = eff.get('language', 'fa')

    js_code = f"""
        // بررسی وجود تابع برای جلوگیری از ارور
        if (typeof showTab === 'function') {{
            document.getElementById('custom-width').checked = {bool_to_js(eff.get('custom_width_checked', True))};
            document.getElementById('width-input').value = {eff.get('width', 800)};
            document.getElementById('height-input').value = {eff.get('height_limit', 15000)};
            document.getElementById('quality-input').value = {eff.get('save_quality', 100)};
            document.getElementById('format-select').value = '{eff.get('save_format', 'jpg')}';
            document.getElementById('is-zip').checked = {bool_to_js(eff.get('zip_checked', False))};
            document.getElementById('is-pdf').checked = {bool_to_js(eff.get('pdf_checked', False))};
            document.getElementById('is-cbz').checked = {bool_to_js(eff.get('cbz_checked', False))};
            document.getElementById('enhance-quality').checked = {bool_to_js(eff.get('enhance_checked', False))};
            document.getElementById('no-stitch').checked = {bool_to_js(eff.get('no_stitch_checked', False))};
            document.getElementById('save-location-input').value = {json.dumps(eff.get('save_location', '') or '')};
            document.getElementById('save-next-to-source').checked = {bool_to_js(eff.get('save_next_to_source', False))};
            document.getElementById('play-sound').checked = {bool_to_js(eff.get('play_sound', True))};
            document.getElementById('show-notifications').checked = {bool_to_js(eff.get('show_notification', True))};
            document.getElementById('thread-count').value = {eff.get('thread_count', 4)};
            document.getElementById('output-suffix').value = {json.dumps(eff.get('output_suffix', ' [Stitched]') or ' [Stitched]')};
            document.getElementById('filename-pattern').value = {json.dumps(eff.get('filename_pattern', '[number]') or '[number]')};
            document.getElementById('filename-digits').value = {eff.get('filename_digits', 3)};
            document.getElementById('custom-theme-color').value = {json.dumps(eff.get('custom_theme_color', '') or '')};
            document.getElementById('watermark-enabled').checked = {bool_to_js(eff.get('watermark_enabled', False))};
            document.getElementById('watermark-path').value = {json.dumps(eff.get('watermark_path', '') or '')};
            document.getElementById('watermark-count').value = {eff.get('watermark_count', 1)};
            document.getElementById('watermark-edge').value = '{eff.get('watermark_edge', 'right')}';
            if (typeof refreshSaveLocationState === 'function') {{ refreshSaveLocationState(); }}
            if (typeof toggleWatermarkOptions === 'function') {{ toggleWatermarkOptions(); }}

            setTheme('{current_theme}');
            var ctColor = {json.dumps(eff.get('custom_theme_color', '') or '')};
            if (ctColor && typeof applyCustomTheme === 'function') {{ applyCustomTheme(ctColor); }}
            setLanguage('{current_lang}');
            showTab('{settings.get('selected_tab', 'process')}');
            if (typeof syncFormatDropdown === 'function') {{ syncFormatDropdown(); }}
            if (typeof initPresets === 'function') {{ initPresets({json.dumps(presets)}, {json.dumps(default_preset)}); }}
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

def on_folder_dropped(event):
    """Handle a folder (or .cbz) dropped onto the window.

    pywebview populates pywebviewFullPath on each file ONLY when a Python-side
    drop handler is registered (see webview/util.py + edgechromium.py). The
    browser drop event alone gives no real path — that's the bug everyone hits
    first. The dragover/preventDefault is handled on the JS side.
    """
    try:
        files = ((event or {}).get('dataTransfer') or {}).get('files') or []
        paths = []
        for f in files:
            full = (f or {}).get('pywebviewFullPath')
            if full:
                paths.append(full)
        if not paths:
            return
        payload = json.dumps(paths)
        window.evaluate_js(f"window.handleDroppedPaths({payload})")
    except Exception:
        import traceback
        traceback.print_exc()

def register_drop_handler():
    """Register the drop handler via the Python DOM API so the native backend
    resolves real dropped paths (a JS-only handler only ever sees blank paths)."""
    from webview.dom import DOMEventHandler
    try:
        window.dom.body.events.drop += DOMEventHandler(on_folder_dropped, prevent_default=True)
        from webview.dom import _dnd_state
        print(f'[drop] handler registered, num_listeners={_dnd_state["num_listeners"]}', flush=True)
    except Exception:
        import traceback
        traceback.print_exc()

def changeProgress(percent):
    window.evaluate_js(f"document.getElementById('pr').style.width = '{percent}%'")
    window.evaluate_js(f"document.getElementById('pr-text').textContent = '{percent}%'")
    window.evaluate_js(f"document.getElementById('progress-percent').textContent = '{percent}%'")

def changeProgressDetail(current, total, current_file, elapsed_str, eta_str):
    """Update the detailed progress info panel in the UI."""
    safe_file = json.dumps(current_file or '')
    window.evaluate_js(f"updateProgressInfo({current}, {total}, {safe_file}, {json.dumps(elapsed_str)}, {json.dumps(eta_str)})")

def updateStep(step_name):
    """Update the step indicator (ready, scan, process, save, done)."""
    window.evaluate_js(f"updateStepIndicator({json.dumps(step_name)})")

def resetProgressUI():
    """Reset all progress UI elements to idle state."""
    window.evaluate_js("resetProgressUI()")

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
    window.evaluate_js(f"document.getElementById('progress-detail').textContent = {escaped_text}")

def changeStatusOnly(text):
    """Update only the main status line, leaving progress-detail untouched."""
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

def showError(text, force=False):
    escaped_text = json.dumps(text)
    if force:
        window.evaluate_js(f"showError({escaped_text})")
    else:
        window.evaluate_js(f"if(document.getElementById('show-notifications')?.checked !== false) showError({escaped_text})")

def showSuccess(text):
    escaped_text = json.dumps(text)
    window.evaluate_js(f"if(document.getElementById('show-notifications')?.checked !== false) showSuccess({escaped_text})")

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
    # فرمت‌هایی که به عنوان پوشه مجازی در نظر گرفته می‌شوند
    virtual_folder_extensions = {'.zip', '.pdf', '.cbz'}
    
    has_images = False
    has_subfolders = False

    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            item_ext = os.path.splitext(item)[1].lower()
            
            if os.path.isfile(item_path):
                if item_ext in image_extensions:
                    has_images = True
                elif item_ext in virtual_folder_extensions:
                    # ZIP و PDF را مثل پوشه حساب کن
                    has_subfolders = True
                    
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


def run_enhancement(input_folder, lang='fa', start_time=None):
    from engine import getAllImagesDirectory, open_image_robust
    
    if start_time is None:
        start_time = time.time()
    
    system = platform.system()
    if system == "Windows":
        realesrgan_path = os.path.join('up-model', 'realesrgan-ncnn-vulkan.exe')
    elif system == "Darwin":
        realesrgan_path = os.path.join('up-model', 'realesrgan-ncnn-vulkan-macos')
    else:
        realesrgan_path = os.path.join('up-model', 'realesrgan-ncnn-vulkan-ubuntu')

    if not os.path.exists(realesrgan_path):
        alt_path = os.path.join('up-model', 'realesrgan-ncnn-vulkan')
        if os.path.exists(alt_path):
            realesrgan_path = alt_path
        else:
            showError(get_msg("enhancer_missing", lang))
            return None

    if system != "Windows" and os.path.exists(realesrgan_path):
        try:
            os.chmod(realesrgan_path, 0o755)
        except Exception:
            pass

    temp_input_dir = tempfile.mkdtemp(prefix="photoslicer_pre_enhance_")
    output_dir = tempfile.mkdtemp(prefix="photoslicer_enhanced_")
    
    files_to_process = getAllImagesDirectory(input_folder)
    total_files = len(files_to_process)
    if total_files == 0:
        shutil.rmtree(temp_input_dir)
        shutil.rmtree(output_dir)
        return input_folder

    changeStatusOnly(get_msg("enhancing_load", lang, total_files))
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
            
            percent = round(((index + 1) / total_files) * 50)
            changeProgress(percent)
            elapsed = time.time() - start_time
            elapsed_str = formatDuration(elapsed)
            eta_str = calculateEta(start_time, percent)
            changeProgressDetail(index + 1, total_files, 'Preparing...', elapsed_str, eta_str)

    except Exception as e:
        showError(get_msg("error_pre_process", lang, str(e)))
        shutil.rmtree(temp_input_dir)
        shutil.rmtree(output_dir)
        return None

    try:
        changeStatusOnly(get_msg("enhancing_run", lang, total_files))
        # Show "Enhancing..." in detail during the external AI process
        elapsed = time.time() - start_time
        elapsed_str = formatDuration(elapsed)
        changeProgressDetail(total_files, total_files, 'Enhancing...', elapsed_str, '-')
        
        command = [
            realesrgan_path, '-i', temp_input_dir, '-o', output_dir,
            '-m', os.path.join('up-model', 'models'),
            '-n', 'realesr-animevideov3-x2', '-s', '2', '-f', 'jpg'
        ]
        
        creationflags = getattr(subprocess, 'CREATE_NO_WINDOW', 0) if system == 'Windows' else 0
        process = subprocess.run(command, check=True, capture_output=True, text=True, creationflags=creationflags)
        changeProgress(100)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        error_message = getattr(e, 'stderr', str(e))
        showError(get_msg("error_batch", lang, error_message))
        shutil.rmtree(output_dir)
        return None
    finally:
        shutil.rmtree(temp_input_dir)

    changeStatusOnly(get_msg("enhancing_done", lang))
    return output_dir

def formatDuration(seconds):
    if not seconds or seconds < 0:
        return '00:00:00'
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def calculateEta(startTime, percent):
    if not startTime or percent <= 0:
        return '-'
    elapsed = time.time() - startTime
    totalEstimated = elapsed / (percent / 100)
    remaining = totalEstimated - elapsed
    if remaining < 0:
        return '0s'
    if remaining < 60:
        return f"{int(round(remaining))}s"
    if remaining < 3600:
        return f"{int(round(remaining / 60))}m"
    h = int(remaining // 3600)
    m = int(round((remaining % 3600) / 60))
    return f"{h}h {m}m"

class Api:
    def __init__(self):
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()
        self.processing_thread = None
        self.current_lang = 'fa' # Default
        self.start_time = None

    def app_ready(self):
        """وقتی جاوا اسکریپت کامل لود شد، این تابع را صدا می‌زند"""
        # Load settings asynchronously after UI is shown
        initialize_settings()
        settings = load_settings()
        self.current_lang = settings.get('language', 'fa')
        apply_settings(window, settings)

        window.set_title(get_msg("app_window_title", self.current_lang))
        changeStatusText(get_msg("ready", self.current_lang))
        
    def select_folder(self):
        result = window.create_file_dialog(webview.FileDialog.FOLDER)
        return result

    def select_watermark_file(self):
        result = window.create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=("PNG Image (*.png)", "All files (*.*)")
        )
        return result

    def export_presets(self, json_text, suggested_filename="photoslicer-presets.json"):
        """Write preset JSON (single or all) to a user-chosen file. Returns path or None."""
        try:
            result = window.create_file_dialog(
                webview.FileDialog.SAVE,
                save_filename=suggested_filename or "photoslicer-presets.json",
                file_types=("JSON File (*.json)",)
            )
            if not result:
                return None
            path = result if isinstance(result, str) else result[0]
            if not path.lower().endswith(".json"):
                path += ".json"
            with open(path, "w", encoding="utf-8") as f:
                f.write(json_text)
            return path
        except Exception:
            return None

    def import_presets(self):
        """Let the user pick a preset JSON file and return its raw text (or None)."""
        try:
            result = window.create_file_dialog(
                webview.FileDialog.OPEN,
                file_types=("JSON File (*.json)", "All files (*.*)")
            )
            if not result:
                return None
            path = result[0] if isinstance(result, (list, tuple)) else result
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def isDirectory(self, path):
        return os.path.isdir(path)

    def folderName(self, path):
        return os.path.basename(path)
    
    def get_clipboard_text(self):
        try:
            text = pyperclip.paste()
            return text
        except Exception as e:
            return ""

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

    def stop_processing(self):
        """Fully cancel the current job (single or multi). Releases any pause so the
        worker reaches a cancellation checkpoint and unwinds cleanly."""
        if self.processing_thread and self.processing_thread.is_alive():
            self.stop_event.set()
            self.pause_event.set()  # release a paused worker so it can observe the stop
            window.evaluate_js("stopTimer()")
            changeStatusText(get_msg("stopping", self.current_lang))
    
    def open_file_explorer(self, path):
        if path and os.path.exists(path):
            try:
                if current_os == "Windows":
                    os.startfile(path)
                elif current_os == "Darwin": # macOS
                    subprocess.call(["open", path])
                else: # Linux
                    subprocess.call(["xdg-open", path])
            except Exception as e:
                showError(get_msg("open_folder_err", self.current_lang, str(e)))
        else:
            showError(get_msg("path_not_exist", self.current_lang))
    
    def start_processing(self):
        from engine import mergerImages, fast_scandir, extract_images_from_zip, getAllImagesDirectory
        
        # خواندن دوباره زبان برای اطمینان
        settings = load_settings()
        lang = settings.get('language', 'fa')
        self.current_lang = lang

        # محل ذخیره خروجی (پیش‌فرض: پوشه Results کنار برنامه)
        output_base = get_output_base(settings)
        try:
            os.makedirs(output_base, exist_ok=True)
        except OSError:
            # مسیر سفارشی نامعتبر بود؛ به پوشه پیش‌فرض برگرد
            output_base = "./Results"
            os.makedirs(output_base, exist_ok=True)

        reset_timer()
        start_timer()
        resetProgressUI()
        self.start_time = time.time()
        
        isCustomWidth = is_checkbox_checked('custom-width')
        isZip = is_checkbox_checked('is-zip')
        isPdf = is_checkbox_checked('is-pdf')
        isCbz = is_checkbox_checked('is-cbz')
        isEnhance = is_checkbox_checked('enhance-quality')
        isNoStitch = is_checkbox_checked('no-stitch')
        
        watermark_enabled = is_checkbox_checked('watermark-enabled')
        watermark_path = window.dom.get_element('#watermark-path').value
        try:
            watermark_count = int(window.dom.get_element('#watermark-count').value or 1)
        except (ValueError, TypeError):
            watermark_count = 1
        watermark_edge = window.dom.get_element('#watermark-edge').value

        # Show the Watermark step in the progress step indicator only when
        # watermarking is enabled for this run.
        window.evaluate_js(f"setWatermarkStepVisible({'true' if watermark_enabled else 'false'})")

        directoryAddress = getDirectory()

        # Handle direct CBZ file input (extract to temp dir, process as single folder)
        cbz_temp_dir = None
        cbz_extraction_root = None
        if not os.path.isdir(directoryAddress) and directoryAddress.lower().endswith('.cbz') and os.path.isfile(directoryAddress):
            cbz_extraction_root = tempfile.mkdtemp(prefix="photoslicer_cbz_")
            cbz_temp_dir = extract_images_from_zip(directoryAddress, cbz_extraction_root)
            if cbz_temp_dir:
                directoryAddress = cbz_temp_dir
            else:
                shutil.rmtree(cbz_extraction_root, ignore_errors=True)
                showError(get_msg("error_no_images", lang))
                changeStatusText(get_msg("error_valid_dir", lang))
                stop_timer(); enableStartButton(); return

        # Check watermark path validity if enabled
        if watermark_enabled:
            if not watermark_path or not os.path.exists(watermark_path):
                if cbz_extraction_root:
                    shutil.rmtree(cbz_extraction_root, ignore_errors=True)
                showError(get_msg("error_watermark_path", lang))
                changeStatusText(get_msg("error_valid_dir", lang))
                stop_timer(); enableStartButton()
                window.evaluate_js("setButtonState('idle')")
                return

        try:
            newWidth = int(getWidth())
            heightLimit = int(getHeight())
            saveQuality = int(getQuality())
        except (ValueError, TypeError):
            if cbz_extraction_root:
                shutil.rmtree(cbz_extraction_root, ignore_errors=True)
            showError(get_msg("error_invalid_input", lang))
            changeStatusText(get_msg("error_valid_dir", lang))
            stop_timer(); enableStartButton()
            window.evaluate_js("setButtonState('idle')")
            return
        saveFormat = getFormat()

        settings.update({
            "custom_width_checked": isCustomWidth, "width": newWidth,
            "height_limit": heightLimit, "save_quality": saveQuality,
            "save_format": saveFormat, "zip_checked": isZip,
            "pdf_checked": isPdf,
            "cbz_checked": isCbz,
            "enhance_checked": isEnhance,
            "no_stitch_checked": isNoStitch,
            "play_sound": settings.get('play_sound', True),
            "show_notification": settings.get('show_notification', True),
            "thread_count": settings.get('thread_count', 4),
            "output_suffix": settings.get('output_suffix', ' [Stitched]'),
            "watermark_enabled": watermark_enabled,
            "watermark_path": watermark_path,
            "watermark_count": watermark_count,
            "watermark_edge": watermark_edge
        })
        save_settings(settings)

        thread_count = int(settings.get('thread_count', 4) or 4)
        if thread_count < 1:
            thread_count = 1
        if thread_count > 16:
            thread_count = 16

        play_sound = settings.get('play_sound', True)

        filename_pattern = (settings.get('filename_pattern') or '').strip() or '[number]'
        filename_digits = int(settings.get('filename_digits', 3) or 3)
        if filename_digits < 1:
            filename_digits = 1
        if filename_digits > 6:
            filename_digits = 6

        try:
            original_folder_name = os.path.basename(directoryAddress)
            mode = detect_folder_mode(directoryAddress)

            if mode is None:
                showError(get_msg("error_no_images", lang))
                changeStatusText(get_msg("error_valid_dir", lang))
                stop_timer(); enableStartButton(); return

            # Handle "Save Next to Source Folder" option
            save_next_src = settings.get('save_next_to_source', False)
            output_suffix = (settings.get('output_suffix') or '').strip()
            output_suffix = (' ' + output_suffix) if output_suffix else ' [Stitched]'
            stitched_save_name = original_folder_name
            if save_next_src:
                abs_src = os.path.abspath(directoryAddress)
                source_parent = os.path.dirname(abs_src)
                source_name = os.path.basename(abs_src)
                stitched_name = f"{source_name}{output_suffix}"
                if mode == 'single':
                    output_base = source_parent
                    stitched_save_name = stitched_name
                else:
                    output_base = os.path.join(source_parent, stitched_name)
                try:
                    os.makedirs(output_base, exist_ok=True)
                except OSError:
                    pass
            
            showSuccess(get_msg("preparing", lang, original_folder_name))
            changeProgress(0)
            updateStep('scan')

            # Tracks whether the step indicator has been flipped to the Watermark
            # step for the current slicing pass (reset per folder in multi mode).
            wm_step_state = {'shown': False}

            def mark_watermark_step():
                if watermark_enabled and not wm_step_state['shown']:
                    wm_step_state['shown'] = True
                    updateStep('watermark')

            def progress_updater(percent):
                # Block here while paused (stop releases the event so we can observe it).
                self.pause_event.wait()
                if self.stop_event.is_set():
                    raise ProcessStopped()
                # Slices are watermarked right before being saved, so once slice
                # progress starts ticking the watermark phase is running.
                mark_watermark_step()
                changeProgress(round(percent))
                elapsed = time.time() - self.start_time
                elapsed_str = formatDuration(elapsed)
                eta_str = calculateEta(self.start_time, percent)
                stage_label = 'Watermarking...' if watermark_enabled else 'Slicing...'
                changeProgressDetail(total_single_images, total_single_images, stage_label, elapsed_str, eta_str)

            # Lightweight checkpoint for multi mode: only aborts, never touches the
            # per-chapter progress bar (which is updated by the outer loop).
            def cancel_check(percent=None):
                if self.stop_event.is_set():
                    raise ProcessStopped()
                mark_watermark_step()

            # Notify (once) when No-Stitch + WebP falls back to normal stitching
            # because an image is taller than WebP's hard limit.
            webp_fallback_state = {"notified": False}
            def webp_fallback_notify():
                if not webp_fallback_state["notified"]:
                    webp_fallback_state["notified"] = True
                    showSuccess(get_msg("webp_nostitch_fallback", lang))

            final_output_path = ""

            if mode == 'single':
                window.evaluate_js("setButtonState('busy')")
                window.evaluate_js("document.getElementById('start-button').disabled = true;")
                processing_dir = directoryAddress
                temp_enhancement_dir = None

                # Count images for meaningful progress info
                single_images = getAllImagesDirectory(directoryAddress)
                total_single_images = len(single_images)

                if isEnhance:
                    updateStep('scan')
                    temp_enhancement_dir = run_enhancement(directoryAddress, lang, self.start_time)
                    if temp_enhancement_dir is None:
                        stop_timer(); enableStartButton(); return
                    processing_dir = temp_enhancement_dir

                updateStep('process')
                changeStatusText(get_msg("processing_single", lang))

                # Update progress info to show the image count
                elapsed = time.time() - self.start_time
                elapsed_str = formatDuration(elapsed)
                changeProgressDetail(total_single_images, total_single_images, 'Slicing...', elapsed_str, '-')

                try:
                    merged = mergerImages('single', newWidth, isCustomWidth, processing_dir, saveFormat, saveQuality, stitched_save_name, heightLimit, "No", isZip, isPdf, isNoStitch, isCbz=isCbz, progress_callback=progress_updater, webp_fallback_callback=webp_fallback_notify, output_base=output_base, max_workers=thread_count, filename_pattern=filename_pattern, filename_digits=filename_digits, watermark_enabled=watermark_enabled, watermark_path=watermark_path, watermark_count=watermark_count, watermark_edge=watermark_edge)
                finally:
                    if temp_enhancement_dir: shutil.rmtree(temp_enhancement_dir, ignore_errors=True)

                if merged:
                    updateStep('save')
                    changeProgress(100)
                    elapsed = time.time() - self.start_time
                    elapsed_str = formatDuration(elapsed)
                    changeProgressDetail(total_single_images, total_single_images, 'Complete', elapsed_str, '-')
                    if play_sound: alert()
                    changeStatusText(get_msg("idle_done", lang))
                    updateStep('done')
                    final_output_path = os.path.abspath(os.path.join(output_base, stitched_save_name)) if save_next_src else os.path.abspath(output_base)
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
                total_folders = len(allFolders)
                
                for i, folder in enumerate(allFolders):
                    self.pause_event.wait()
                    if self.stop_event.is_set():
                        raise ProcessStopped()
                    folderName = os.path.basename(folder)
                    changeStatusText(get_msg("processing_multi", lang, folderName, i+1, total_folders))
                    elapsed = time.time() - self.start_time
                    elapsed_str = formatDuration(elapsed)
                    percent = ((i + 1) / total_folders) * 100
                    eta_str = calculateEta(self.start_time, percent)
                    changeProgressDetail(i + 1, total_folders, folderName, elapsed_str, eta_str)
                    updateStep('process')
                    # Each folder goes through Process -> Watermark again.
                    wm_step_state['shown'] = False

                    processing_sub_dir = folder
                    temp_enhancement_sub_dir = None
                    if isEnhance:
                        temp_enhancement_sub_dir = run_enhancement(folder, lang, self.start_time)
                        if temp_enhancement_sub_dir is None:
                            changeStatusText(get_msg("skip_folder", lang, folderName))
                            continue
                        processing_sub_dir = temp_enhancement_sub_dir

                    try:
                        mergerImages('multi', newWidth, isCustomWidth, processing_sub_dir, saveFormat, saveQuality, folderName, heightLimit, current_date, isZip, isPdf, isNoStitch, isCbz=isCbz, progress_callback=cancel_check, webp_fallback_callback=webp_fallback_notify, output_base=output_base, max_workers=thread_count, filename_pattern=filename_pattern, filename_digits=filename_digits, watermark_enabled=watermark_enabled, watermark_path=watermark_path, watermark_count=watermark_count, watermark_edge=watermark_edge)
                    finally:
                        if temp_enhancement_sub_dir: shutil.rmtree(temp_enhancement_sub_dir, ignore_errors=True)

                    changeProgress(round((i + 1) / total_folders * 100, 2))
                    
                from engine import cleanup_extraction_temps
                cleanup_extraction_temps()
                
                updateStep('save')
                final_output_path = os.path.abspath(os.path.join(output_base, current_date))
                if play_sound: alert()
                changeStatusText(get_msg("idle_done", lang))
                updateStep('done')
                
            if final_output_path:
                escaped_path = json.dumps(final_output_path)
                window.evaluate_js(f"showOpenFolderButton({escaped_path})")

            clearInput()
            stop_timer()
            window.evaluate_js("setButtonState('idle')")
            window.evaluate_js("document.getElementById('start-button').disabled = false;")
            enableStartButton()
        except ProcessStopped:
            # User requested a full stop: unwind cleanly and reset the UI to idle.
            try:
                from engine import cleanup_extraction_temps
                cleanup_extraction_temps()
            except Exception:
                pass
            changeProgress(0)
            stop_timer()
            changeStatusText(get_msg("stopped", lang))
            window.evaluate_js("setButtonState('idle')")
            window.evaluate_js("document.getElementById('start-button').disabled = false;")
            enableStartButton()
        except Exception as e:
            # Any unexpected failure must reset the UI; otherwise the button stays
            # stuck in busy/processing and the timer keeps running ("hung" app).
            try:
                from engine import cleanup_extraction_temps
                cleanup_extraction_temps()
            except Exception:
                pass
            changeProgress(0)
            stop_timer()
            showError(get_msg("error_unexpected", lang, str(e)))
            changeStatusText(get_msg("error_valid_dir", lang))
            window.evaluate_js("setButtonState('idle')")
            window.evaluate_js("document.getElementById('start-button').disabled = false;")
            enableStartButton()
        finally:
            if cbz_extraction_root:
                shutil.rmtree(cbz_extraction_root, ignore_errors=True)

    def start(self):
        self.stop_event.clear()
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

# Load settings and generate theme preload script on startup
initial_settings = initialize_settings()
generate_theme_preload(initial_settings)

api = Api()
window = webview.create_window(
    title=f"PhotoSlicer v{VERSION}",
    url="assets/index.html",
    width=final_w,
    height=final_h,
    x=x_pos,
    y=y_pos,
    resizable=True,
    js_api=api,
    shadow=True,
)

window.events.closed += on_close
window.events.before_show += on_before_show
window.events.shown += on_shown
# Register drag-and-drop once the DOM is ready (needs the Python DOM API so the
# native backend resolves real dropped-folder paths).
window.events.loaded += register_drop_handler
# Settings will be loaded asynchronously in app_ready()
webview.start()
