import webview
from engine import *
import time
import os
import tempfile


temp_dir = tempfile.TemporaryDirectory()
os.environ["WEBVIEW2_USER_DATA_FOLDER"] = temp_dir.name

if not os.path.isdir(f"Results"):
    os.mkdir(f"Results")


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


def alert(file_path="sounds/success.wav"):
    window.evaluate_js(f"playAudio('{file_path}')")


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
        directoryAddress = getDirectory(mode)
        newWidth = int(getWidth(mode))
        heightLimit = int(getHeight(mode))
        saveQuality = int(getQuality(mode))
        saveFormat = getFormat(mode)
        folderName = os.path.basename(directoryAddress)

        if mode == 'single':
            disableStartButton(mode)
            alert()
            showSuccess(f"Preparing: {folderName}...✨")
            changeStatusText(mode, f"Preparing... 🔥")
            merged = mergerImages(mode, newWidth, isChecked, directoryAddress, saveFormat, saveQuality, folderName, heightLimit, "No")
            if merged:
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
                current_date = time.strftime("%Y-%m-%d %H-%M-%S")
                alert()
                showSuccess(f"Preparing: {folderName}...✨")
                changeProgress(0)
                for folder in allFolders:
                    count += 1
                    folderName = os.path.basename(folder)
                    merged = mergerImages(mode, newWidth, isChecked, folder, saveFormat, saveQuality, folderName, heightLimit, current_date)
                    changeStatusText(mode, f"{folderName} - {count}/{len(allFolders)}... 🔥")
                    changeProgress(round(count / len(allFolders) * 100, 2))

                clearInput(mode)
                changeStatusText(mode, "Done! Idle.✅")
                enableStartButton(mode)

            else:
                clearInput(mode)
                showError("There is no Folders inside the selected Directory, Please select a correct Directory.")
                changeStatusText(mode, "Select Correct Directory!")


window = webview.create_window(title="PhotoSlicer v3", url="assets/index.html", width=450, height=730, resizable=False, js_api=Api(), confirm_close=True, shadow=True)

window.events.closed += on_close
webview.start()

