const translations = {
    en: {
        appTitle: "PhotoSlicer",
        tabWorkspace: "Workspace",
        tabInfo: "Info",
        sourceDirectory: "Source Directory",
        width: "Width",
        height: "Height",
        quality: "Quality",
        format: "Format",
        aiEnhance: "AI Enhance",
        noStitch: "No Stitch",
        zip: "ZIP Archive",
        pdf: "PDF File",
        readyStatus: "Ready to Slice",
        btnInitiate: "INITIATE",
        btnProcessing: "PROCESSING",
        btnPause: "PAUSE",
        btnResume: "RESUME",
        openFolder: "Open Folder",
        proTool: "Professional Manhwa Tool",
        desc: "Optimized for high-speed image stitching and editing workflow. Designed for efficiency.",
        dev: "Dev:",
        joinChannel: "Join Channel",
        selectDirFirst: "Please select a directory first.",
        errorTitle: "Error",
        successTitle: "Success",
        // Tooltips
        tipLogo: "Click to spin!",
        tipLang: "Switch Language",
        tipBlue: "Cyber Blue",
        tipPurple: "Electric Purple",
        tipRuby: "Ruby Red",
        tipSunset: "Sunset Orange",
        tipGold: "Luxury Gold",
        tipEmerald: "Neo Emerald"
    },
    fa: {
        appTitle: "فوتو اسلایسر",
        tabWorkspace: "میز کار",
        tabInfo: "درباره ما",
        sourceDirectory: "پوشه منبع تصاویر",
        width: "عرض دلخواه",
        height: "حد ارتفاع برش",
        quality: "کیفیت ذخیره",
        format: "فرمت خروجی",
        aiEnhance: "افزایش کیفیت هوشمند",
        noStitch: "بدون چسباندن (تغییر فرمت)",
        zip: "فشرده‌سازی ZIP",
        pdf: "تبدیل به PDF",
        readyStatus: "آماده برای شروع",
        btnInitiate: "شـروع عملیـات",
        btnProcessing: "در حال پردازش...",
        btnPause: "توقـف",
        btnResume: "ادامـه",
        openFolder: "باز کردن پوشه",
        proTool: "ابزار حرفه‌ای مانهوا و کمیک",
        desc: "بهینه‌سازی شده برای سرعت بالا در چسباندن و ویرایش تصاویر. طراحی شده برای کارایی.",
        dev: "توسعه‌دهنده:",
        joinChannel: "عضویت در کانال",
        selectDirFirst: "لطفا ابتدا یک پوشه انتخاب کنید.",
        errorTitle: "خطا",
        successTitle: "موفق",
        // Tooltips
        tipLogo: "برای چرخش کلیک کنید!",
        tipLang: "تغییر زبان",
        tipBlue: "آبی سایبری",
        tipPurple: "بنفش الکتریک",
        tipRuby: "قرمز یاقوتی",
        tipSunset: "نارنجی غروب",
        tipGold: "طلایی لوکس",
        tipEmerald: "سبز زمردی"
    }
};

let currentLang = 'fa';

function toggleLanguage() {
    const newLang = currentLang === 'en' ? 'fa' : 'en';
    setLanguage(newLang);
    updateSettings();
}

function setLanguage(lang) {
    currentLang = lang;
    const texts = translations[lang];
    
    document.body.setAttribute('dir', lang === 'fa' ? 'rtl' : 'ltr');
    
    const langIcon = document.getElementById('lang-icon');
    if (langIcon) langIcon.textContent = lang === 'fa' ? 'EN' : 'FA';

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (texts[key]) {
            el.textContent = texts[key];
        }
    });
	
	document.querySelector('.logo-icon').title = texts.tipLogo;
    document.querySelector('.lang-switch').title = texts.tipLang;
    document.querySelector('.dot-blue').title = texts.tipBlue;
    document.querySelector('.dot-purple').title = texts.tipPurple;
    document.querySelector('.dot-ruby').title = texts.tipRuby;
    document.querySelector('.dot-sunset').title = texts.tipSunset;
    document.querySelector('.dot-gold').title = texts.tipGold;
    document.querySelector('.dot-emerald').title = texts.tipEmerald;
    
    // Update buttons directly if needed
    const startBtn = document.getElementById('start-button');
    const state = startBtn.dataset.state || 'idle';
    updateStartButtonText(state, lang);
}

function updateStartButtonText(state, lang) {
    const texts = translations[lang];
    const btnSpan = document.querySelector('#start-button .btn-content span');
    if (!btnSpan) return;

    if (state === 'idle') btnSpan.textContent = texts.btnInitiate;
    else if (state === 'processing') btnSpan.textContent = texts.btnPause;
    else if (state === 'paused') btnSpan.textContent = texts.btnResume;
    else if (state === 'busy') btnSpan.textContent = texts.btnProcessing;
}

function minimizeWindow() {
    pywebview.api.minimize_window();
}

function closeWindow() {
    pywebview.api.close_window();
}

function animateLogo() {
    const logo = document.querySelector('.logo-icon');
    logo.classList.remove('logo-spin');
    void logo.offsetWidth;
    logo.classList.add('logo-spin');
}

function showTab(tabName) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');

    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    const tabElement = document.querySelector(`#tab-${tabName}`);
    if (tabElement) {
        tabElement.classList.add('active');
    }

    updateSettings();
}

function selectFolder() {
    pywebview.api.select_folder().then(function(folderPath) {
        if (folderPath) {
            document.getElementById('directory-input').value = folderPath;
            updateSettings();
        }
    });
}

function showError(message) {
    // تعیین موقعیت بر اساس زبان
    const position = currentLang === 'fa' ? 'top-right' : 'top-left';
    
    const popup = Notification({
        position: position,
        duration: 3000,
        isHidePrev: false,
        isHideTitle: false,
        maxOpened: 2,
    });
    popup.error({
        title: translations[currentLang].errorTitle,
        message: message,
    });
}

function showSuccess(message) {
    // تعیین موقعیت بر اساس زبان
    const position = currentLang === 'fa' ? 'top-right' : 'top-left';

    const popup = Notification({
        position: position,
        duration: 3000,
        isHidePrev: false,
        isHideTitle: false,
        maxOpened: 2,
    });
    popup.success({
        title: translations[currentLang].successTitle,
        message: message,
    });
}

function start() {
    document.getElementById('timer').style.display = 'block';
    document.getElementById('mini-open-btn').style.display = 'none';

    if (!document.getElementById('directory-input').value) {
        showError(translations[currentLang].selectDirFirst);
        return;
    }
    
    pywebview.api.start();
}

function isChecked(id) {
    return document.getElementById(id).checked;
}

function disableStartButton() {
    document.getElementById('start-button').disabled = true;
}

function enableStartButton() {
    document.getElementById('start-button').disabled = false;
}

function playAudio(soundDirectory) {
    let audio = new Audio(soundDirectory);
    audio.play().catch(e => console.log("Audio play failed", e));
}

let hours = 0, minutes = 0, seconds = 0;
let timerInterval;

function startTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
}

function resetTimer() {
    stopTimer();
    seconds = 0;
    minutes = 0;
    hours = 0;
    document.getElementById('timer').textContent = '00:00:00';
}

function updateTimer() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours++;
        }
    }

    const formattedHours = String(hours).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');
    const formattedSeconds = String(seconds).padStart(2, '0');

    document.getElementById('timer').textContent = `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
}

function updateSettings() {
    const currentTheme = document.body.getAttribute('data-theme') || 'blue';
    const settings = {
        custom_width_checked: document.getElementById('custom-width').checked,
        width: parseInt(document.getElementById('width-input').value) || 800,
        height_limit: parseInt(document.getElementById('height-input').value) || 15000,
        save_quality: parseInt(document.getElementById('quality-input').value) || 100,
        save_format: document.getElementById('format-select').value || 'jpg',
        zip_checked: document.getElementById('is-zip').checked,
        pdf_checked: document.getElementById('is-pdf').checked,
        enhance_checked: document.getElementById('enhance-quality').checked,
        no_stitch_checked: document.getElementById('no-stitch').checked,
        selected_tab: document.querySelector('.tab-content.active')?.id || 'process',
        theme: currentTheme,
        language: currentLang
    };
    if(window.pywebview) {
        pywebview.api.save_settings(settings);
    }
}

document.querySelectorAll('input, select').forEach(element => {
    element.addEventListener('change', updateSettings);
});

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.id.replace('tab-', '');
        showTab(tabName);
    });
});

function handleCheckboxClick(checkbox) {
    const zipCheckbox = document.getElementById('is-zip');
    const pdfCheckbox = document.getElementById('is-pdf');

    if (checkbox.checked) {
        if (checkbox.id === 'is-zip') {
            pdfCheckbox.checked = false;
        } else if (checkbox.id === 'is-pdf') {
            zipCheckbox.checked = false;
        }
    }
    updateSettings();
}

const startButton = document.getElementById('start-button');

function handleProcessClick() {
    const state = startButton.dataset.state || 'idle'; 

    if (state === 'idle') {
        start(); 
    } else if (state === 'processing') {
        pywebview.api.pause_processing();
        setButtonState('paused'); 
    } else if (state === 'paused') {
        pywebview.api.resume_processing();
        setButtonState('processing'); 
    }
}

function setButtonState(state) {
    startButton.dataset.state = state;
    const texts = translations[currentLang];
    
    if (state === 'idle') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-rocket-takeoff" viewBox="0 0 16 16"><path d="M9.752 6.193c.599.6 1.73.437 2.528-.362s.96-1.932.362-2.531c-.599-.6-1.73-.438-2.528.361-.798.8-.96 1.933-.362 2.532"/><path d="M15.811 3.312c-.363 1.534-1.334 3.626-3.64 6.218l-.24 2.408a2.56 2.56 0 0 1-.732 1.526L8.817 15.85a.51.51 0 0 1-.867-.434l.27-1.899c.04-.28-.013-.593-.131-.956a9 9 0 0 0-.249-.657l-.082-.202c-.815-.197-1.578-.662-2.191-1.277-.614-.615-1.079-1.379-1.275-2.195l-.203-.083a10 10 0 0 0-.655-.248c-.363-.119-.675-.172-.955-.132l-1.896.27A.51.51 0 0 1 .15 7.17l2.382-2.386c.41-.41.947-.67 1.524-.734h.006l2.4-.238C9.005 1.55 11.087.582 12.623.208c.89-.217 1.59-.232 2.08-.188.244.023.435.06.57.093q.1.026.16.045c.184.06.279.13.351.295l.029.073a3.5 3.5 0 0 1 .157.721c.055.485.051 1.178-.159 2.065m-4.828 7.475.04-.04-.107 1.081a1.54 1.54 0 0 1-.44.913l-1.298 1.3.054-.38c.072-.506-.034-.993-.172-1.418a9 9 0 0 0-.164-.45c.738-.065 1.462-.38 2.087-1.006M5.205 5c-.625.626-.94 1.351-1.004 2.09a9 9 0 0 0-.45-.164c-.424-.138-.91-.244-1.416-.172l-.38.054 1.3-1.3c.245-.246.566-.401.91-.44l1.08-.107zm9.406-3.961c-.38-.034-.967-.027-1.746.163-1.558.38-3.917 1.496-6.937 4.521-.62.62-.799 1.34-.687 2.051.107.676.483 1.362 1.048 1.928.564.565 1.25.941 1.924 1.049.71.112 1.429-.067 2.048-.688 3.079-3.083 4.192-5.444 4.556-6.987.183-.771.18-1.345.138-1.713a3 3 0 0 0-.045-.283 3 3 0 0 0-.3-.041Z"/><path d="M7.009 12.139a7.6 7.6 0 0 1-1.804-1.352A7.6 7.6 0 0 1 3.794 8.86c-1.102.992-1.965 5.054-1.839 5.18.125.126 3.936-.896 5.054-1.902Z"/></svg><span>${texts.btnInitiate}</span></div>`;
        
    } else if (state === 'processing') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pause-fill" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5m5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5"/></svg><span>${texts.btnPause}</span></div>`;

    } else if (state === 'paused') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393"/></svg><span>${texts.btnResume}</span></div>`;

    } else if (state === 'busy') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 15a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11zm2-13v1c0 .537.12 1.045.337 1.5h6.326c.216-.455.337-.963.337-1.5V2h-7zm3 6.35c0 .701-.478 1.236-1.011 1.492A3.5 3.5 0 0 0 4.5 13s.866-1.299 3-1.48V8.35zm1 0v1.48c2.134.181 3 1.48 3 1.48a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 10.052 8.5 9.35z"/></svg><span>${texts.btnProcessing}</span></div>`;
    }
}

function setTheme(themeName) {
    if (themeName === 'blue') {
        document.body.removeAttribute('data-theme');
    } else {
        document.body.setAttribute('data-theme', themeName);
    }

    document.querySelectorAll('.theme-dot').forEach(btn => {
        btn.classList.remove('active');
        if (btn.classList.contains(`dot-${themeName}`)) {
            btn.classList.add('active');
        }
    });
}

function changeTheme(themeName) {
    setTheme(themeName);
    updateSettings();
}

const DESIGN_WIDTH = 520;
const DESIGN_HEIGHT = 810;

function handleResize() {
    const widthRatio = window.innerWidth / DESIGN_WIDTH;
    const heightRatio = window.innerHeight / DESIGN_HEIGHT;
    let zoomLevel = Math.min(widthRatio, heightRatio);
    const viewport = document.getElementById('main-viewport');
    if (viewport) {
        viewport.style.zoom = zoomLevel;
    }
}

window.addEventListener('DOMContentLoaded', handleResize);
window.addEventListener('resize', handleResize);

let lastOutputPath = "";

function showOpenFolderButton(path) {
    lastOutputPath = path;
    document.getElementById('timer').style.display = 'none';
    const btn = document.getElementById('mini-open-btn');
    if(btn) {
        btn.style.display = 'flex';
    }
}

function openResultFolder() {
    if (lastOutputPath) {
        pywebview.api.open_file_explorer(lastOutputPath);
    }
}

window.addEventListener('pywebviewready', function() {
    pywebview.api.app_ready();
});
