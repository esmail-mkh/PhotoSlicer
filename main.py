import webview
from engine import mergerImages, fast_scandir
import time
import os
import tempfile
import ctypes
from ctypes import wintypes


VERSION = "3.5.1"

temp_dir = tempfile.TemporaryDirectory()
os.environ["WEBVIEW2_USER_DATA_FOLDER"] = temp_dir.name

#Make an Empty Folder Named Results
os.makedirs("Results", exist_ok=True)

#Enable Dark Mode
DWMWA_USE_IMMERSIVE_DARK_MODE = 20

user32 = ctypes.WinDLL("user32", use_last_error=True)
dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)

def on_before_show(window):
    value = ctypes.c_int(1)  # Enable dark mode (0 to disable)
    dwmapi.DwmSetWindowAttribute(
        wintypes.HWND(window.native.Handle.ToInt32()),
        DWMWA_USE_IMMERSIVE_DARK_MODE,
        ctypes.byref(value),
        ctypes.sizeof(value)
    )


def changeProgress(percent):
    progress = window.dom.get_element('#pr')
    progress.text = f"{percent}%"
    progress.style['width'] = f"{percent}%"

def is_checkbox_checked(mode):
    if mode == 'single':
        idOfElement = 'custom-width-one'
    else:
        idOfElement = 'custom-width'
    script = f'''
        isChecked("{idOfElement}")
    '''
    result = window.evaluate_js(script)
    return result

def is_zip_checked(mode):
    if mode == 'single':
        idOfElement = 'is-zip-one'
    else:
        idOfElement = 'is-zip'
    script = f'''
        isChecked("{idOfElement}")
    '''
    result = window.evaluate_js(script)
    return result


def getWidth(mode):
    if mode == 'single':
        width = window.dom.get_element('#width-input-one').value
    else:
        width = window.dom.get_element('#width-input').value
    return width

def getDirectory(mode):
    if mode == 'single':
        directory = window.dom.get_element('#directory-input-one').value
    else:
        directory = window.dom.get_element('#directory-input').value
    return directory

def getHeight(mode):
    if mode == 'single':
        height = window.dom.get_element('#height-input-one').value
    else:
        height = window.dom.get_element('#height-input').value
    return height

def changeStatusText(mode, text):
    if mode == 'single':
        window.dom.get_element('#status-one').text = f"Status: {text}"
    else:
        window.dom.get_element('#status').text = f"Status: {text}"


def getQuality(mode):
    if mode == 'single':
        quality = window.dom.get_element('#quality-input-one').value
    else:
        quality = window.dom.get_element('#quality-input-multi').value
    return quality

def getFormat(mode):
    if mode == 'single':
        formatImage = window.dom.get_element('#format-select-one').value
    else:
        formatImage = window.dom.get_element('#format-select').value
    return formatImage

def disableStartButton(mode):
    window.evaluate_js(f"disableStartButton('{mode}')")

def enableStartButton(mode):
    window.evaluate_js(f"enableStartButton('{mode}')")

def clearInput(mode):
    if mode == 'single':
        window.dom.get_element('#directory-input-one').value = ""
    else:
        window.dom.get_element('#directory-input').value = ""

def showError(text):
    window.evaluate_js(f"showError('{text}')")

def showSuccess(text):
    window.evaluate_js(f"showSuccess('{text}')")


def alert(file_path="success.wav"):
    window.evaluate_js(f"playAudio('{file_path}')")

def start_timer():
    window.evaluate_js(f"startTimer()")

def stop_timer():
    window.evaluate_js(f"stopTimer()")

def reset_timer():
    window.evaluate_js(f"resetTimer()")

def on_close():
    window.destroy()


class Api:
    def select_folder(self):
        result = window.create_file_dialog(webview.FOLDER_DIALOG)
        return result

    def isDirectory(self, path):
        return os.path.isdir(path)

    def folderName(self, path):
        return os.path.basename(path)

    def start(self, mode):
        #Needed Variables
        isChecked = is_checkbox_checked(mode)
        isZip = is_zip_checked(mode)
        directoryAddress = getDirectory(mode)
        newWidth = int(getWidth(mode))
        heightLimit = int(getHeight(mode))
        saveQuality = int(getQuality(mode))
        saveFormat = getFormat(mode)
        folderName = os.path.basename(directoryAddress)

        if mode == 'single':
            disableStartButton(mode)
            showSuccess(f"Preparing: {folderName}...✨")
            changeStatusText(mode, f"Preparing... 🔥")
            merged = mergerImages(mode, newWidth, isChecked, directoryAddress, saveFormat, saveQuality, folderName, heightLimit, "No", isZip)
            if merged:
                alert()
                clearInput(mode)
                changeStatusText(mode, "Done! Idle.✅")
            else:
                clearInput(mode)
                showError("There is no Images inside Entered Folder, Please select a correct Folder.")
                changeStatusText(mode, "Select Correct Folder!")
            enableStartButton(mode)


        elif mode == 'multi':
            count = 0
            allFolders = fast_scandir(directoryAddress)
            if len(allFolders) > 0:
                disableStartButton(mode)
                reset_timer()
                current_date = time.strftime("%Y-%m-%d %H-%M-%S")
                showSuccess(f"Preparing: {folderName}...✨")
                changeProgress(0)
                start_timer()
                for folder in allFolders:
                    count += 1
                    folderName = os.path.basename(folder)
                    merged = mergerImages(mode, newWidth, isChecked, folder, saveFormat, saveQuality, folderName, heightLimit, current_date, isZip)
                    changeStatusText(mode, f"{folderName} - {count}/{len(allFolders)}... 🔥")
                    changeProgress(round(count / len(allFolders) * 100, 2))

                alert()
                clearInput(mode)
                stop_timer()
                changeStatusText(mode, "Done! Idle.✅")
                enableStartButton(mode)

            else:
                clearInput(mode)
                showError("There is no Folders inside the selected Directory, Please select a correct Directory.")
                changeStatusText(mode, "Select Correct Directory!")


window = webview.create_window(title=f"PhotoSlicer v{VERSION}", url="assets/index.html", width=int(450), height=int(780), resizable=False, js_api=Api(), shadow=True)

window.events.closed += on_close
window.events.before_show += on_before_show
webview.start()
