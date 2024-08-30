function showTab(tabName) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');

    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
}

function focusInput(input) {
    input.nextElementSibling.classList.add('focus');
    input.placeholder = '';
}

function blurInput(input) {
    if (input.value === '') {
        input.nextElementSibling.classList.remove('focus');
        input.placeholder = ' ';
    }
}

function selectDirectory(inputId) {
    // Placeholder function for folder selection
    document.getElementById(inputId).value = 'C:\\Users\\User\\SelectedFolder';
}

function selectFolder(mode) {
    pywebview.api.select_folder().then(function(folderPath) {
        if (mode === 'one'){
            document.getElementById('directory-input-one').value = folderPath;
        } else if (mode === 'multi') {
            document.getElementById('directory-input').value = folderPath;
        }
    });
}

function showError(message){
    const popup = Notification({
    position: 'top',
    duration: 2000,
    isHidePrev: false,
    isHideTitle: false,
    maxOpened: 2,
    })

    popup.error({
        title: 'Error!',
        message: message,
    })
}

function showSuccess(message){
    const popup = Notification({
    position: 'top',
    duration: 2000,
    isHidePrev: false,
    isHideTitle: false,
    maxOpened: 2,
    })

    popup.success({
        title: 'Started!',
        message: message,
    })
}
function start(mode) {
    if (mode === 'single'){
        var folderAddress = document.getElementById('directory-input-one').value;
        if (folderAddress === '') {
            showError("The Directory Address is required, please enter a directory address.")
        } else {
            pywebview.api.isDirectory(folderAddress).then(function(result) {
            if (result) {
                pywebview.api.start('single')
            } else {
                showError('The Address is not valid! Please enter a valid directory address.')
            }
        });
        }

    } else if (mode === 'multi') {
        const folderAddress = document.getElementById('directory-input').value;
        if (folderAddress === '') {
            showError("The Directory Address is required, please enter a directory address.")
        } else {
            pywebview.api.isDirectory(folderAddress).then(function (result) {
                if (result) {
                    pywebview.api.start('multi')
                } else {
                    showError('The Address is not valid! Please enter a valid directory address.')
                }
            });
        }
    }
}

function isChecked(id) {
    return document.getElementById(id).checked
}

function disableStartButton(mode) {
    if (mode === 'single') {
        document.getElementById('start-button-one').disabled = true;
        document.getElementById('tab-multi').disabled = true;
    } else if (mode === 'multi') {
        document.getElementById('start-button').disabled = true;
        document.getElementById('tab-one').disabled = true;
    }
}

function enableStartButton(mode) {
    if (mode === 'single') {
        document.getElementById('start-button-one').disabled = false;
        document.getElementById('tab-multi').disabled = false;
    } else if (mode === 'multi') {
        document.getElementById('start-button').disabled = false;
        document.getElementById('tab-one').disabled = false;
    }
}


function playAudio(soundDirectory) {
    let audio = new Audio(soundDirectory);
    audio.play();
}
