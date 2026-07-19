const translations = {
    en: {
        appTitle: "PhotoSlicer",
        tabWorkspace: "Workspace",
        tabInfo: "Info",
        sourceDirectory: "Source Directory",
        pastePath: "Paste path",
        selectFolder: "Browse folder",
        clearPath: "Clear",
        width: "Width",
        height: "Height",
        quality: "Quality",
        format: "Format",
        formatJpgDesc: "Smallest file size",
        formatPngDesc: "Lossless quality",
        formatWebpDesc: "Modern & compact",
        formatPsdDesc: "Photoshop layers",
        aiEnhance: "AI Enhance",
        noStitch: "No Stitch",
        zip: "ZIP Archive",
        pdf: "PDF File",
        cbz: "CBZ Archive",
        readyStatus: "Ready to Slice",
        // Presets
        noPreset: "No Preset",
        presetsTitle: "Presets",
        presetSave: "Save changes to preset",
        presetSaveAs: "Save as new preset",
        presetRename: "Rename preset",
        presetDelete: "Delete preset",
        presetImport: "Import presets",
        presetExport: "Export presets",
        exportCurrent: "Export current",
        exportAll: "Export all",
        setDefault: "Set as default",
        saveAsTitle: "Save as new preset",
        renameTitle: "Rename preset",
        deleteTitle: "Delete preset",
        namePlaceholder: "Preset name",
        cancel: "Cancel",
        confirm: "OK",
        back: "Back",
        noPresetsYet: "No presets yet",
        deleteConfirmMsg: "will be permanently removed.",
        toastSaved: "Preset saved",
        toastUpdated: "Preset updated",
        toastDeleted: "Preset deleted",
        toastRenamed: "Preset renamed",
        toastDefaultSet: "Default preset set",
        toastDefaultCleared: "Default preset cleared",
        toastApplied: "Preset applied",
        toastExported: "Presets exported",
        toastImported: "Presets imported",
        errNameRequired: "Please enter a name",
        errNameExists: "A preset with this name already exists",
        errSelectFirst: "Select a preset first",
        errNothingExport: "There are no presets to export",
        errImportInvalid: "Invalid or unreadable preset file",
        btnInitiate: "INITIATE",
        btnProcessing: "PROCESSING",
        btnPause: "PAUSE",
        btnResume: "RESUME",
        btnStop: "STOP",
        openFolder: "Open Folder",
        proTool: "Professional Manhwa Tool",
        desc: "Optimized for high-speed image stitching and editing workflow. Designed for efficiency.",
        dev: "Dev:",
        joinChannel: "Join Channel",
        versionLabel: "Version",
        pythonLabel: "Python",
        clipboardPasted: "Path pasted successfully.",
        clipboardInvalid: "Clipboard text is not a valid directory path.",
        clipboardError: "Failed to get clipboard text.",
        dropSuccess: "Folder dropped successfully.",
        dropHint: "Drop folder here",
        featFast: "Fast Stitching",
        featFastDesc: "High-speed image stitching with optimized algorithms.",
        featAI: "AI Enhance",
        featAIDesc: "Smart quality enhancement for sharper results.",
        featFormat: "Multi-Format",
        featFormatDesc: "JPG, PNG, WEBP, PSD, ZIP, PDF & CBZ support.",
        featBatch: "Batch Process",
        featBatchDesc: "Process entire folders with one click.",
        filesLabel: "Files",
        currentLabel: "Current",
        statusLabel: "Status",
        elapsedLabel: "Elapsed",
        etaLabel: "ETA",
        statusEnhancing: "Enhancing images...",
        statusStitching: "Stitching images...",
        statusSlicing: "Slicing images...",
        statusWatermarking: "Watermarking...",
        statusPreparing: "Preparing...",
        statusComplete: "Processing complete",
        stepReady: "Ready",
        stepScan: "Scan",
        stepProcess: "Process",
        stepWatermark: "Watermark",
        stepSave: "Save",
        stepDone: "Done",
        stepTipReady: "Preparing to start processing",
        stepTipScan: "Scanning folders for images",
        stepTipProcess: "Processing and stitching images",
        stepTipWatermark: "Applying watermark to images",
        stepTipSave: "Saving output files to disk",
        stepTipDone: "All done! Processing complete",
        selectDirFirst: "Please select a directory first.",
        errorTitle: "Error",
        successTitle: "Success",
        webpLimitTitle: "WebP Size Limit",
        webpLimitMsg: "WebP supports a maximum height of {0}px. The crop height limit will be adjusted to {0}px and processing will start.",
        tabSettings: "Settings",
        saveLocation: "Save Location",
        saveLocationDesc: "Choose where sliced output is saved. Leave empty to use the default \"Results\" folder next to the app.",
        resetDefault: "Reset to default",
        toastSaveLocationSet: "Save location updated",
        toastSaveLocationReset: "Save location reset to default",
        saveNextToSource: "Save Next to Source Folder",
        saveNextToSourceHint: "Output will be saved in a \"<name> [Stitched]\" folder next to the source",
        toastSaveNextSourceAuto: "Output will be saved next to source folder",
        // Behavior settings
        behaviorSettings: "Behavior",
        behaviorSettingsDesc: "General application behavior and performance settings.",
        playSound: "Play Sound",
        showNotifications: "Show Notifications",
        threadCount: "Threads",
        threadCountUnit: "cores",
        outputSuffix: "Output Folder Suffix",
        // Filename format
        filenameFormatTitle: "Output Filename Format",
        filenameFormatDesc: "Customize how output image files are named. Dynamic placeholders are supported (see guide below).",
        filenamePattern: "Pattern",
        filenameDigits: "Digits",
        filenameDigitsUnit: "pad",
        filenamePreview: "Preview:",
        filenameGuideTitle: "Placeholders Guide:",
        guideNumber: "Sequential number (e.g. 001) - Required",
        guideFolder: "Source folder name",
        guideDate: "Current date (YYYY-MM-DD)",
        guideTotal: "Total slice count",
        // Tooltips
        tipLogo: "Click to spin!",
        tipLang: "Switch Language",
        tipBlue: "Cyber Blue",
        tipPurple: "Electric Purple",
        tipRuby: "Ruby Red",
        tipSunset: "Sunset Orange",
        tipGold: "Luxury Gold",
        tipEmerald: "Neo Emerald",
        // Appearance settings
        appearanceSettings: "Appearance",
        appearanceSettingsDesc: "Pick a custom theme color or choose from the preset color dots in the header.",
        customThemeColor: "Custom Color",
        resetCustomTheme: "Reset",
        // Color picker
        noColor: "No color",
        chooseColor: "Choose Color",
        viewAllColors: "View All Colors",
        brightness: "Brightness",
        saturation: "Saturation",
        hex: "HEX",
        rgb: "RGB",
        hsl: "HSL",
        // Watermark settings
        watermarkSettings: "Watermark Settings",
        watermarkSettingsDesc: "Enable and configure transparent PNG watermark overlay.",
        watermarkEnabled: "Enable Watermark",
        watermarkPath: "Watermark Image (PNG)",
        watermarkCount: "Count Per Page",
        watermarkCountUnit: "times",
        watermarkEdge: "Placement Edge",
        watermarkLeft: "Left Edge",
        watermarkRight: "Right Edge",
        watermarkPathPlaceholder: "Choose a transparent PNG file..."
    },
    fa: {
        appTitle: "فوتو اسلایسر",
        tabWorkspace: "میز کار",
        tabInfo: "درباره ما",
        sourceDirectory: "پوشه منبع تصاویر",
        pastePath: "جای‌گذاری مسیر",
        selectFolder: "انتخاب پوشه",
        clearPath: "پاک کردن",
        width: "عرض دلخواه",
        height: "حد ارتفاع برش",
        quality: "کیفیت ذخیره",
        format: "فرمت خروجی",
        formatJpgDesc: "کمترین حجم فایل",
        formatPngDesc: "کیفیت بدون افت",
        formatWebpDesc: "مدرن و کم‌حجم",
        formatPsdDesc: "لایه‌های فتوشاپ",
        aiEnhance: "افزایش کیفیت هوشمند",
        noStitch: "بدون چسباندن (تغییر فرمت)",
        zip: "فشرده‌سازی ZIP",
        pdf: "تبدیل به PDF",
        cbz: "خروجی CBZ",
        readyStatus: "آماده برای شروع",
        // Presets
        noPreset: "بدون پریست",
        presetsTitle: "پریست‌ها",
        presetSave: "ذخیره تغییرات در پریست",
        presetSaveAs: "ذخیره به عنوان پریست جدید",
        presetRename: "تغییر نام پریست",
        presetDelete: "حذف پریست",
        presetImport: "وارد کردن پریست‌ها",
        presetExport: "خروجی گرفتن پریست‌ها",
        exportCurrent: "خروجی پریست فعلی",
        exportAll: "خروجی همه پریست‌ها",
        setDefault: "تنظیم به عنوان پیش‌فرض",
        saveAsTitle: "ذخیره پریست جدید",
        renameTitle: "تغییر نام پریست",
        deleteTitle: "حذف پریست",
        namePlaceholder: "نام پریست",
        cancel: "انصراف",
        confirm: "تأیید",
        back: "بازگشت",
        noPresetsYet: "هنوز پریستی ساخته نشده",
        deleteConfirmMsg: "برای همیشه حذف خواهد شد.",
        toastSaved: "پریست ذخیره شد",
        toastUpdated: "پریست به‌روزرسانی شد",
        toastDeleted: "پریست حذف شد",
        toastRenamed: "نام پریست تغییر کرد",
        toastDefaultSet: "پریست پیش‌فرض تنظیم شد",
        toastDefaultCleared: "پریست پیش‌فرض حذف شد",
        toastApplied: "پریست اعمال شد",
        toastExported: "پریست‌ها خروجی گرفته شد",
        toastImported: "پریست‌ها وارد شد",
        errNameRequired: "لطفاً یک نام وارد کنید",
        errNameExists: "پریستی با این نام از قبل وجود دارد",
        errSelectFirst: "ابتدا یک پریست انتخاب کنید",
        errNothingExport: "هیچ پریستی برای خروجی وجود ندارد",
        errImportInvalid: "فایل پریست نامعتبر یا غیرقابل خواندن است",
        btnInitiate: "شـروع عملیـات",
        btnProcessing: "در حال پردازش...",
        btnPause: "مکث",
        btnResume: "ادامـه",
        btnStop: "توقف",
        openFolder: "باز کردن پوشه",
        proTool: "ابزار حرفه‌ای مانهوا و کمیک",
        desc: "بهینه‌سازی شده برای سرعت بالا در چسباندن و ویرایش تصاویر. طراحی شده برای کارایی.",
        dev: "توسعه‌دهنده:",
        joinChannel: "عضویت در کانال",
        versionLabel: "نسخه",
        pythonLabel: "پایتون",
        clipboardPasted: "مسیر با موفقیت جای‌گذاری شد.",
        clipboardInvalid: "متن کپی شده یک مسیر معتبر نیست.",
        clipboardError: "خطا در دریافت متن کلیپ‌بورد.",
        dropSuccess: "پوشه با موفقیت رها شد.",
        dropHint: "پوشه را اینجا رها کنید",
        featFast: "چسباندن سریع",
        featFastDesc: "چسباندن تصاویر با سرعت بالا و الگوریتم‌های بهینه.",
        featAI: "افزایش کیفیت هوشمند",
        featAIDesc: "بهبود هوشمند کیفیت برای نتایج واضح‌تر.",
        featFormat: "چندفرمتی",
        featFormatDesc: "پشتیبانی از JPG, PNG, WEBP, PSD, ZIP, PDF و CBZ.",
        featBatch: "پردازش گروهی",
        featBatchDesc: "پردازش کل پوشه‌ها با یک کلیک.",
        filesLabel: "فایل‌ها",
        currentLabel: "فایل فعلی",
        statusLabel: "وضعیت",
        elapsedLabel: "گذشته",
        etaLabel: "زمان باقیمانده",
        statusEnhancing: "افزایش کیفیت...",
        statusStitching: "چسباندن...",
        statusSlicing: "برش...",
        statusWatermarking: "درج واترمارک...",
        statusPreparing: "آماده‌سازی...",
        statusComplete: "پایان",
        stepReady: "آماده",
        stepScan: "اسکن",
        stepProcess: "پردازش",
        stepWatermark: "واترمارک",
        stepSave: "ذخیره",
        stepDone: "انجام شد",
        stepTipReady: "آماده‌سازی برای شروع پردازش",
        stepTipScan: "اسکن پوشه‌ها برای یافتن تصاویر",
        stepTipProcess: "پردازش و چسباندن تصاویر",
        stepTipWatermark: "درج واترمارک روی تصاویر",
        stepTipSave: "ذخیره فایل‌های خروجی",
        stepTipDone: "تمام شد! پردازش کامل شد",
        selectDirFirst: "لطفا ابتدا یک پوشه انتخاب کنید.",
        errorTitle: "خطا",
        successTitle: "موفق",
        webpLimitTitle: "محدودیت ابعاد WebP",
        webpLimitMsg: "فرمت WebP حداکثر تا ارتفاع {0} پیکسل را پشتیبانی می‌کند. حد ارتفاع برش روی {0} تنظیم شده و پردازش آغاز می‌شود.",
        tabSettings: "تنظیمات",
        saveLocation: "محل ذخیره",
        saveLocationDesc: "محل ذخیره خروجی برش‌ها را انتخاب کنید. برای استفاده از پوشه پیش‌فرض «Results» کنار برنامه، خالی بگذارید.",
        resetDefault: "بازگردانی به پیش‌فرض",
        toastSaveLocationSet: "محل ذخیره به‌روزرسانی شد",
        toastSaveLocationReset: "محل ذخیره به پیش‌فرض بازگشت",
        saveNextToSource: "ذخیره کنار پوشه منبع",
        saveNextToSourceHint: "خروجی در پوشه «<name> [Stitched]» کنار پوشه منبع ذخیره می‌شود",
        toastSaveNextSourceAuto: "خروجی کنار پوشه منبع ذخیره خواهد شد",
        // Behavior settings
        behaviorSettings: "رفتار",
        behaviorSettingsDesc: "تنظیمات رفتار عمومی برنامه و عملکرد.",
        playSound: "پخش صدا",
        showNotifications: "نمایش اعلان‌ها",
        threadCount: "تعداد هسته",
        threadCountUnit: "هسته",
        outputSuffix: "پسوند پوشه خروجی",
        // Filename format
        filenameFormatTitle: "فرمت نام فایل خروجی",
        filenameFormatDesc: "نحوه نام‌گذاری فایل‌های خروجی را سفارشی کنید. الگوهای پویا پشتیبانی می‌شوند (راهنمای زیر را ببینید).",
        filenamePattern: "الگو",
        filenameDigits: "تعداد ارقام",
        filenameDigitsUnit: "رقم",
        filenamePreview: "پیش‌نمایش:",
        filenameGuideTitle: "راهنمای متغیرها:",
        guideNumber: "شمارنده ترتیبی (مثال: 001) - الزامی",
        guideFolder: "نام پوشه منبع",
        guideDate: "تاریخ فعلی (YYYY-MM-DD)",
        guideTotal: "تعداد کل تکه‌ها",
        // Tooltips
        tipLogo: "برای چرخش کلیک کنید!",
        tipLang: "تغییر زبان",
        tipBlue: "آبی سایبری",
        tipPurple: "بنفش الکتریک",
        tipRuby: "قرمز یاقوتی",
        tipSunset: "نارنجی غروب",
        tipGold: "طلایی لوکس",
        tipEmerald: "سبز زمردی",
        // Appearance settings
        appearanceSettings: "ظاهر",
        appearanceSettingsDesc: "یک رنگ دلخواه برای تم انتخاب کنید یا از دایره‌های رنگی در هدر استفاده کنید.",
        customThemeColor: "رنگ دلخواه",
        resetCustomTheme: "بازنشانی",
        // Color picker
        noColor: "بدون رنگ",
        chooseColor: "انتخاب رنگ",
        viewAllColors: "مشاهده همه رنگ‌ها",
        brightness: "روشنایی",
        saturation: "اشباع",
        hex: "HEX",
        rgb: "RGB",
        hsl: "HSL",
        // Watermark settings
        watermarkSettings: "تنظیمات واترمارک",
        watermarkSettingsDesc: "فعال‌سازی و پیکربندی واترمارک تصویر PNG شفاف روی صفحات.",
        watermarkEnabled: "فعال‌سازی سیستم واترمارک",
        watermarkPath: "تصویر واترمارک (PNG)",
        watermarkCount: "تعداد در هر صفحه",
        watermarkCountUnit: "بار",
        watermarkEdge: "لبه قرارگیری",
        watermarkLeft: "لبه چپ",
        watermarkRight: "لبه راست",
        watermarkPathPlaceholder: "یک فایل PNG شفاف انتخاب کنید..."
    }
};

let currentLang = 'fa';
let isInitializing = true;

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

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (texts[key]) {
            el.placeholder = texts[key];
        }
    });

    // Translate title-attribute tooltips (e.g. preset action buttons)
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (texts[key]) el.title = texts[key];
    });

    // Rebuild custom format dropdown so option descriptions follow the language
    if (typeof buildFormatMenu === 'function') {
        buildFormatMenu();
    }

    // Re-position tab indicator after text changes shift tab widths
    positionTabIndicator();

    // Refresh the presets dropdown/labels for the new language
    if (typeof renderPresetMenu === 'function') {
        renderPresetMenu();
        updatePresetTrigger();
    }
	
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
    // Drives CSS that shows the header presets bar only on the Workspace tab
    document.body.dataset.tab = tabName;

    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');

    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    const tabElement = document.querySelector(`#tab-${tabName}`);
    if (tabElement) {
        tabElement.classList.add('active');
    }

    positionTabIndicator();
    updateSettings();
}

function positionTabIndicator() {
    const tabsContainer = document.querySelector('.tabs');
    const activeTab = document.querySelector('.tab.active');
    if (!tabsContainer || !activeTab) return;
    tabsContainer.style.setProperty('--tab-indicator-left', activeTab.offsetLeft + 'px');
    tabsContainer.style.setProperty('--tab-indicator-width', activeTab.offsetWidth + 'px');
}

function selectFolder() {
    pywebview.api.select_folder().then(function(folderPath) {
        if (folderPath) {
            document.getElementById('directory-input').value = folderPath;
            refreshDirectoryState();
            updateSettings();
        }
    });
}

// Reflect whether the directory field has a value: toggles the filled state
// (shows the clear button) and exposes the full path as a hover tooltip.
function refreshDirectoryState() {
    const input = document.getElementById('directory-input');
    const wrapper = input && input.closest('.folder-wrapper');
    if (!input || !wrapper) return;
    const hasValue = input.value.trim().length > 0;
    wrapper.classList.toggle('has-value', hasValue);
    input.title = hasValue ? input.value : '';
}

function clearDirectory() {
    const input = document.getElementById('directory-input');
    if (!input) return;
    input.value = '';
    refreshDirectoryState();
    updateSettings();
    input.focus();
}

/* ---- Settings: output save location ---- */
function selectSaveLocation() {
    pywebview.api.select_folder().then(function(res) {
        if (!res) return;
        const path = Array.isArray(res) ? res[0] : res;
        if (!path) return;
        const input = document.getElementById('save-location-input');
        input.value = path;
        refreshSaveLocationState();
        updateSettings();
        showSuccess(translations[currentLang].toastSaveLocationSet);
    });
}

function resetSaveLocation() {
    const input = document.getElementById('save-location-input');
    if (!input) return;
    input.value = '';
    refreshSaveLocationState();
    updateSettings();
    showSuccess(translations[currentLang].toastSaveLocationReset);
}

// Expose the full save path as a hover tooltip (mirrors the directory field).
function refreshSaveLocationState() {
    const input = document.getElementById('save-location-input');
    const nextToSource = document.getElementById('save-next-to-source');
    if (!input) return;
    input.title = input.value || '';
    if (nextToSource) {
        const locationControl = input.closest('.location-control');
        if (locationControl) {
            locationControl.classList.toggle('disabled-by-checkbox', nextToSource.checked);
        }
        input.readOnly = nextToSource.checked;
        // Also toggle suffix input visibility
        const suffixWrapper = document.getElementById('output-suffix-wrapper');
        if (suffixWrapper) {
            suffixWrapper.classList.toggle('visible', nextToSource.checked);
        }
    }
}

// Handle save-next-to-source checkbox toggle
(function initSaveNextToSource() {
    const cb = document.getElementById('save-next-to-source');
    if (!cb) return;
    function syncSuffixVisibility() {
        const wrapper = document.getElementById('output-suffix-wrapper');
        if (wrapper) {
            wrapper.classList.toggle('visible', cb.checked);
        }
    }
    cb.addEventListener('change', function() {
        refreshSaveLocationState();
        syncSuffixVisibility();
        updateSettings();
        if (this.checked) {
            const texts = translations[currentLang] || {};
            showSuccess(texts.toastSaveNextSourceAuto || 'Output will be saved next to source folder');
        }
    });
    // Initial sync on page load
    syncSuffixVisibility();
})();

// ============================================================
// COLOR PICKER — modal with preset grid + custom color wheel
// ============================================================

// The color the user last picked from the wheel (HSL).
// Brightness slider stores percentage 0–100.
let wheelHue = 210;
let wheelSat = 80;
let wheelBrightness = 100;

// Store original color/theme so Cancel/Back can revert the live preview
let wheelOriginalHex = '';
let wheelOriginalTheme = 'blue';

// Preset solid colors for contrast calculation
const PRESET_SOLIDS = {
    blue: '#0ea5e9',
    purple: '#d946ef',
    sunset: '#fbbf24',
    emerald: '#34d399',
    ruby: '#ef4444',
    gold: '#d4a017'
};

// Compute and set the best foreground color (white or dark) for the current theme
function setThemeContrast(hex) {
    if (!hex || hex.length < 7) {
        document.documentElement.style.removeProperty('--on-theme-text');
        document.documentElement.style.removeProperty('--theme-is-light');
        return;
    }
    var r = parseInt(hex.slice(1, 3), 16);
    var g = parseInt(hex.slice(3, 5), 16);
    var b = parseInt(hex.slice(5, 7), 16);
    // YIQ luminance — values ≥ 150 are considered "light"
    var yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
    var isLight = yiq >= 165;
    var contrast = isLight ? '#0a0e1a' : '#ffffff';
    document.documentElement.style.setProperty('--on-theme-text', contrast);
    document.documentElement.style.setProperty('--theme-is-light', isLight ? '1' : '0');
}

// Update all UI that reflects the current custom color
// Update preview dot and hex label only (no state changes — used for live wheel preview)
function updatePreviewUI(hex) {
    var dot = document.getElementById('theme-preview-dot');
    if (dot) dot.style.background = hex;
    var hl = document.getElementById('custom-theme-hex');
    if (hl) hl.textContent = hex;
}

// Update the color preview panel inside the wheel modal
function updateWheelPreviewPanel(hex) {
    var swatch = document.getElementById('color-preview-swatch');
    if (swatch) swatch.style.background = hex;
    var hexInput = document.getElementById('wheel-hex-input');
    if (hexInput && document.activeElement !== hexInput) hexInput.value = hex;
    var rgbVal = document.getElementById('wheel-rgb-value');
    if (rgbVal) {
        var rgb = hexToRgb(hex);
        rgbVal.textContent = rgb ? rgb.r + ', ' + rgb.g + ', ' + rgb.b : '';
    }
    var hslVal = document.getElementById('wheel-hsl-value');
    if (hslVal) {
        hslVal.textContent = wheelHue + ', ' + wheelSat + '%, ' + wheelBrightness + '%';
    }
}

// Update brightness slider gradient to reflect current hue/sat
function updateWheelSliderGradient() {
    var slider = document.getElementById('brightness-slider');
    if (!slider) return;
    var fullColor = hslToHex(wheelHue, wheelSat, 100);
    slider.style.background = 'linear-gradient(90deg, #000000, ' + fullColor + ')';
}

// Update saturation slider gradient to reflect current hue/brightness
function updateSaturationSliderGradient() {
    var slider = document.getElementById('saturation-slider');
    if (!slider) return;
    var gray = hslToHex(wheelHue, 0, wheelBrightness);
    var fullColor = hslToHex(wheelHue, 100, wheelBrightness);
    slider.style.background = 'linear-gradient(90deg, ' + gray + ', ' + fullColor + ')';
}

// Update the live color strip gradient and handle position
function updateColorStrip() {
    var strip = document.getElementById('color-strip');
    var handle = document.getElementById('color-strip-handle');
    if (!strip) return;
    var gray = hslToHex(wheelHue, 0, wheelBrightness);
    var fullColor = hslToHex(wheelHue, 100, wheelBrightness);
    strip.style.background = 'linear-gradient(90deg, ' + gray + ', ' + fullColor + ')';
    if (handle) {
        handle.style.left = wheelSat + '%';
        handle.style.background = hslToHex(wheelHue, wheelSat, wheelBrightness);
    }
}

// Pick saturation from the color strip based on click position
function pickColorStrip(e) {
    var strip = document.getElementById('color-strip');
    if (!strip) return;
    var rect = strip.getBoundingClientRect();
    var x = e.clientX - rect.left;
    var pct = Math.max(0, Math.min(100, (x / rect.width) * 100));
    wheelSat = Math.round(pct);
    var satSlider = document.getElementById('saturation-slider');
    if (satSlider) satSlider.value = wheelSat;
    updateWheelDot();
    var liveHex = hslToHex(wheelHue, wheelSat, wheelBrightness);
    applyLiveWheelPreview(liveHex);
    updateSaturationSliderGradient();
    updateColorStrip();
    updateWheelPreviewPanel(liveHex);
}

// Parse hex to RGB object
function hexToRgb(hex) {
    var r = parseInt(hex.slice(1, 3), 16);
    var g = parseInt(hex.slice(3, 5), 16);
    var b = parseInt(hex.slice(5, 7), 16);
    if (isNaN(r) || isNaN(g) || isNaN(b)) return null;
    return { r: r, g: g, b: b };
}

// Update full color state: preview dot, hidden input, hex label, and swatch selection
function updateColorUI(hex) {
    updatePreviewUI(hex);
    var cp = document.getElementById('custom-theme-color');
    if (cp) cp.value = hex;
    document.querySelectorAll('.color-preset-swatch').forEach(function(s) {
        var swatchColor = s.getAttribute('data-color');
        s.classList.toggle('selected', swatchColor !== 'none' && swatchColor.toUpperCase() === hex.toUpperCase());
    });
}

function generatePresetGrid() {
    var grid = document.getElementById('preset-colors-grid');
    if (!grid) return;
    grid.innerHTML = '';

    // 10 rows x 10 columns
    // Row 0: no-color swatch + black-to-white grayscale
    // Rows 1-9: 9 hues with lightness from dark (col 0) to light (col 9)
    var hues = [0, 30, 60, 90, 120, 180, 210, 270, 300];
    var graySteps = ['#000000','#222222','#444444','#666666','#888888','#aaaaaa','#cccccc','#eeeeee','#ffffff'];

    for (var row = 0; row < 10; row++) {
        for (var col = 0; col < 10; col++) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'color-preset-swatch';
            var hex;

            if (row === 0) {
                if (col === 0) {
                    btn.classList.add('no-color-swatch');
                    btn.setAttribute('data-color', 'none');
                    btn.title = (translations[currentLang] || {}).noColor || 'No color';
                } else {
                    hex = graySteps[col - 1];
                    btn.setAttribute('data-color', hex);
                    btn.style.background = hex;
                    btn.title = hex;
                }
            } else {
                var hue = hues[row - 1];
                var lightness = Math.min(10 + col * 10, 95); // 10, 20, ..., 95 (avoid white)
                hex = hslToHex(hue, 90, lightness);
                btn.setAttribute('data-color', hex);
                btn.style.background = hex;
                btn.title = hex;
            }

            btn.addEventListener('click', function() {
                var color = this.getAttribute('data-color');
                if (color === 'none') {
                    resetCustomTheme();
                    closeColorPickerModal();
                    return;
                }
                var currentHex = document.getElementById('custom-theme-color').value || '#0ea5e9';
                if (color.toUpperCase() === currentHex.toUpperCase()) return;
                updateColorUI(color);
                applyCustomTheme(color);
                updateSettings();
                closeColorPickerModal();
            });

            grid.appendChild(btn);
        }
    }

    // Highlight current color
    var currentHex = document.getElementById('custom-theme-color').value || '#0ea5e9';
    updateColorUI(currentHex);

    // If no custom theme is active, highlight the "no color" swatch
    if (document.body.getAttribute('data-theme') !== 'custom') {
        var noColorSwatch = grid.querySelector('.no-color-swatch');
        if (noColorSwatch) {
            document.querySelectorAll('.color-preset-swatch').forEach(function(s) {
                s.classList.remove('selected');
            });
            noColorSwatch.classList.add('selected');
        }
    }
}

// Modal open/close
function openColorPickerModal() {
    var overlay = document.getElementById('color-picker-modal');
    if (!overlay) return;
    generatePresetGrid();
    overlay.dataset.open = 'true';
}

function closeColorPickerModal() {
    var overlay = document.getElementById('color-picker-modal');
    if (!overlay) return;
    overlay.dataset.open = 'false';
}

// Show the custom color wheel
// Open the dedicated wheel picker modal
function openColorWheelModal() {
    var overlay = document.getElementById('color-wheel-modal');
    if (!overlay) return;

    // Save original color/theme so we can revert on Cancel/Back
    wheelOriginalHex = document.getElementById('custom-theme-color').value || '';
    wheelOriginalTheme = document.body.getAttribute('data-theme') || 'blue';

    // Initialise wheel values from current color
    var currentHex = wheelOriginalHex || '#0ea5e9';
    var r = parseInt(currentHex.slice(1,3), 16);
    var g = parseInt(currentHex.slice(3,5), 16);
    var b = parseInt(currentHex.slice(5,7), 16);
    // RGB → HSL
    r /= 255; g /= 255; b /= 255;
    var max = Math.max(r,g,b), min = Math.min(r,g,b);
    var h, s, l = (max+min)/2;
    if (max === min) { h = s = 0; }
    else {
        var d = max-min;
        s = l > 0.5 ? d/(2-max-min) : d/(max+min);
        switch(max) {
            case r: h = ((g-b)/d + (g<b?6:0))/6; break;
            case g: h = ((b-r)/d + 2)/6; break;
            case b: h = ((r-g)/d + 4)/6; break;
        }
    }
    wheelHue = Math.round(h * 360);
    wheelSat = Math.round(s * 100);
    wheelBrightness = Math.round(l * 100);

    var slider = document.getElementById('brightness-slider');
    if (slider) slider.value = wheelBrightness;
    var satSlider = document.getElementById('saturation-slider');
    if (satSlider) satSlider.value = wheelSat;

    drawColorWheel();
    updateWheelDot();
    updateWheelSliderGradient();
    updateSaturationSliderGradient();
    updateColorStrip();
    updateWheelPreviewPanel(currentHex);

    // Close the presets modal and open the wheel modal
    closeColorPickerModal();
    overlay.dataset.open = 'true';
}

function closeColorWheelModal() {
    var overlay = document.getElementById('color-wheel-modal');
    if (!overlay) return;
    overlay.dataset.open = 'false';
}

// Restore the original color/theme when the user cancels the wheel picker
function restoreWheelOriginalColor() {
    if (wheelOriginalTheme === 'custom') {
        if (wheelOriginalHex) {
            applyCustomTheme(wheelOriginalHex);
        } else {
            resetCustomTheme();
        }
    } else {
        applyCustomTheme('');
        setTheme(wheelOriginalTheme);
    }
}

function confirmColorWheel() {
    // Theme was already applied live during dragging; just finalize the hidden input and save
    var hex = hslToHex(wheelHue, wheelSat, wheelBrightness);
    applyCustomTheme(hex);
    updateSettings();
    closeColorWheelModal();
}

function backToPresetModal() {
    restoreWheelOriginalColor();
    closeColorWheelModal();
    openColorPickerModal();
}

// Convert HSL (with brightness) to hex
function hslToHex(h, s, l) {
    h /= 360; s /= 100; l /= 100;
    var r, g, b;
    if (s === 0) {
        r = g = b = l;
    } else {
        var hue2rgb = function(p, q, t) {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1/6) return p + (q-p)*6*t;
            if (t < 1/2) return q;
            if (t < 2/3) return p + (q-p)*(2/3-t)*6;
            return p;
        };
        var q = l < 0.5 ? l*(1+s) : l+s-l*s;
        var p = 2*l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }
    var toHex = function(c) {
        var hex = Math.round(c*255).toString(16);
        return hex.length === 1 ? '0'+hex : hex;
    };
    return '#' + toHex(r) + toHex(g) + toHex(b);
}

// Draw the circular color wheel (HSV: hue=angle, sat=radius)
function drawColorWheel() {
    var canvas = document.getElementById('color-wheel-canvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var w = canvas.width, h = canvas.height;
    var cx = w/2, cy = h/2;
    var radius = Math.min(cx, cy) - 2;
    ctx.clearRect(0, 0, w, h);

    // Draw hue/sat wheel
    for (var angle = 0; angle < 360; angle += 1) {
        var rad = angle * Math.PI / 180;
        for (var r = 0; r < radius; r += 1) {
            var sat = r / radius;
            var hex = hslToHex(angle, sat * 100, 50);
            ctx.fillStyle = hex;
            ctx.fillRect(cx + Math.cos(rad)*r, cy + Math.sin(rad)*r, 1.5, 1.5);
        }
    }

    // Draw white center (saturation = 0)
    var centerGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius * 0.15);
    centerGrad.addColorStop(0, '#ffffff');
    centerGrad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = centerGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, radius * 0.15, 0, Math.PI * 2);
    ctx.fill();
}

// Update the wheel dot position based on current hue/sat
function updateWheelDot() {
    var canvas = document.getElementById('color-wheel-canvas');
    var dot = document.getElementById('wheel-dot');
    if (!canvas || !dot) return;
    var w = canvas.width, h = canvas.height;
    var cx = w/2, cy = h/2;
    var radius = Math.min(cx, cy) - 2;
    var rad = wheelHue * Math.PI / 180;
    var dist = (wheelSat / 100) * radius;
    var x = cx + Math.cos(rad) * dist;
    var y = cy + Math.sin(rad) * dist;
    dot.style.left = x + 'px';
    dot.style.top = y + 'px';
    // Update dot border color to be visible against the wheel
    var dotHex = hslToHex(wheelHue, wheelSat, 50);
    dot.style.background = dotHex;
}

// Pick a color from the wheel based on mouse position
function pickWheelColor(e) {
    var canvas = document.getElementById('color-wheel-canvas');
    if (!canvas) return;
    var rect = canvas.getBoundingClientRect();
    var w = canvas.width, h = canvas.height;
    var cx = w/2, cy = h/2;
    var radius = Math.min(cx, cy) - 2;

    var x = (e.clientX - rect.left) * (w / rect.width);
    var y = (e.clientY - rect.top) * (h / rect.height);

    var dx = x - cx, dy = y - cy;
    var dist = Math.sqrt(dx*dx + dy*dy);
    if (dist > radius) dist = radius;

    var angle = Math.atan2(dy, dx) * 180 / Math.PI;
    if (angle < 0) angle += 360;

    wheelHue = Math.round(angle);
    wheelSat = Math.round((dist / radius) * 100);
    updateWheelDot();
    // Live preview: update the whole app theme in real-time (lightweight, no swatch loop)
    var liveHex = hslToHex(wheelHue, wheelSat, wheelBrightness);
    applyLiveWheelPreview(liveHex);
    updateWheelSliderGradient();
    updateSaturationSliderGradient();
    updateColorStrip();
    updateWheelPreviewPanel(liveHex);
    // Sync saturation slider
    var satSlider = document.getElementById('saturation-slider');
    if (satSlider) satSlider.value = wheelSat;
}

// Confirm: close the preset picker (colors are already applied live on click)
// Colour wheel canvas mouse events
(function initColorWheel() {
    var canvas = document.getElementById('color-wheel-canvas');
    if (!canvas) return;
    var dragging = false;
    canvas.addEventListener('mousedown', function(e) {
        dragging = true;
        pickWheelColor(e);
    });
    canvas.addEventListener('mousemove', function(e) {
        if (dragging) pickWheelColor(e);
    });
    canvas.addEventListener('mouseup', function() { dragging = false; });
    canvas.addEventListener('mouseleave', function() { dragging = false; });

    // Saturation slider
    var satSlider = document.getElementById('saturation-slider');
    if (satSlider) {
        satSlider.addEventListener('input', function() {
            wheelSat = parseInt(this.value);
            var liveHex = hslToHex(wheelHue, wheelSat, wheelBrightness);
            applyLiveWheelPreview(liveHex);
            updateWheelDot();
            updateSaturationSliderGradient();
            updateColorStrip();
            updateWheelPreviewPanel(liveHex);
        });
    }

    // Brightness slider
    var slider = document.getElementById('brightness-slider');
    if (slider) {
        slider.addEventListener('input', function() {
            wheelBrightness = parseInt(this.value);
            // Live preview: update the whole app theme in real-time (lightweight, no swatch loop)
            var liveHex = hslToHex(wheelHue, wheelSat, wheelBrightness);
            applyLiveWheelPreview(liveHex);
            updateWheelSliderGradient();
            updateSaturationSliderGradient();
            updateColorStrip();
            updateWheelPreviewPanel(liveHex);
        });
    }

    // Color strip click
    var strip = document.getElementById('color-strip');
    if (strip) {
        var stripDragging = false;
        strip.addEventListener('mousedown', function(e) {
            stripDragging = true;
            pickColorStrip(e);
        });
        strip.addEventListener('mousemove', function(e) {
            if (stripDragging) pickColorStrip(e);
        });
        window.addEventListener('mouseup', function() { stripDragging = false; });
    }

    // Hex input inside wheel modal
    var hexInput = document.getElementById('wheel-hex-input');
    if (hexInput) {
        function onWheelHexInput() {
            var val = hexInput.value.trim();
            if (!/^#[0-9A-Fa-f]{6}$/.test(val)) return;
            var r = parseInt(val.slice(1,3), 16) / 255;
            var g = parseInt(val.slice(3,5), 16) / 255;
            var b = parseInt(val.slice(5,7), 16) / 255;
            var max = Math.max(r,g,b), min = Math.min(r,g,b);
            var h, s, l = (max+min)/2;
            if (max === min) { h = s = 0; }
            else {
                var d = max-min;
                s = l > 0.5 ? d/(2-max-min) : d/(max+min);
                switch(max) {
                    case r: h = ((g-b)/d + (g<b?6:0))/6; break;
                    case g: h = ((b-r)/d + 2)/6; break;
                    case b: h = ((r-g)/d + 4)/6; break;
                }
            }
            wheelHue = Math.round(h * 360);
            wheelSat = Math.round(s * 100);
            wheelBrightness = Math.round(l * 100);
            var bSlider = document.getElementById('brightness-slider');
            if (bSlider) bSlider.value = wheelBrightness;
            var sSlider = document.getElementById('saturation-slider');
            if (sSlider) sSlider.value = wheelSat;
            updateWheelDot();
            updateWheelSliderGradient();
            updateSaturationSliderGradient();
            updateColorStrip();
            applyLiveWheelPreview(val);
            updateWheelPreviewPanel(val);
        }
        hexInput.addEventListener('change', onWheelHexInput);
        hexInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                onWheelHexInput();
                this.blur();
            }
        });
    }
})();

// Modal backdrop click to close
(function initColorPickerModal() {
    var overlay = document.getElementById('color-picker-modal');
    if (overlay) {
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) closeColorPickerModal();
        });
    }
    var wheelOverlay = document.getElementById('color-wheel-modal');
    if (wheelOverlay) {
        wheelOverlay.addEventListener('click', function(e) {
            if (e.target === wheelOverlay) {
                restoreWheelOriginalColor();
                closeColorWheelModal();
            }
        });
    }
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (overlay && overlay.dataset.open === 'true') closeColorPickerModal();
            if (wheelOverlay && wheelOverlay.dataset.open === 'true') {
                restoreWheelOriginalColor();
                closeColorWheelModal();
            }
        }
    });
})();

// Live preview for filename pattern
(function initFilenamePreview() {
    const patternInput = document.getElementById('filename-pattern');
    const digitsInput = document.getElementById('filename-digits');
    const preview = document.getElementById('filename-preview-text');
    if (!patternInput || !digitsInput || !preview) return;
    const formatSelect = document.getElementById('format-select');
    function refreshPreview() {
        const pattern = (patternInput.value || '').trim() || '[number]';
        const digits = Math.max(1, Math.min(6, parseInt(digitsInput.value) || 3));
        const ext = (formatSelect?.value || 'jpg').toLowerCase();
        const padded = '1'.padStart(digits, '0');
        
        let name = pattern;
        if (name.includes('[number]')) {
            name = name.replace('[number]', padded);
        } else {
            name = name + ' ' + padded;
        }
        
        if (name.includes('[folder]')) {
            name = name.replace('[folder]', 'MyFolder');
        }
        if (name.includes('[date]')) {
            const today = new Date().toISOString().slice(0, 10);
            name = name.replace('[date]', today);
        }
        if (name.includes('[total]')) {
            name = name.replace('[total]', '012');
        }
        
        // Remove characters invalid in Windows filenames for the preview
        name = name.replace(/[\\/:*?"<>|]/g, '_');
        
        preview.textContent = name + '.' + ext;
    }
    // Auto-append [number] if user removed it (on blur, to avoid disturbing typing)
    patternInput.addEventListener('blur', function() {
        const val = (this.value || '').trim();
        if (val && !val.includes('[number]')) {
            this.value = val + ' [number]';
            refreshPreview();
            updateSettings();
        }
    });
    patternInput.addEventListener('input', refreshPreview);
    digitsInput.addEventListener('input', refreshPreview);
    if (formatSelect) formatSelect.addEventListener('change', refreshPreview);
    refreshPreview();
})();

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

// WebP can't encode an image taller than this. Must match WEBP_MAX_DIMENSION
// in engine.py.
const WEBP_MAX_DIMENSION = 16383;

function start() {
    document.getElementById('timer').style.display = 'block';
    document.getElementById('mini-open-btn').style.display = 'none';

    if (!document.getElementById('directory-input').value) {
        showError(translations[currentLang].selectDirFirst);
        return;
    }

    // WebP has a hard 16383px height limit. With a larger crop-height limit the
    // slices silently fail to save, so warn the user, then clamp the limit to
    // the WebP maximum and proceed. Only relevant in stitch mode (the height
    // limit isn't applied when "No Stitch" is on).
    const format = (document.getElementById('format-select').value || '').toUpperCase();
    const heightLimit = parseInt(document.getElementById('height-input').value) || 0;
    const noStitch = document.getElementById('no-stitch').checked;
    if (format === 'WEBP' && !noStitch && heightLimit > WEBP_MAX_DIMENSION) {
        const texts = translations[currentLang] || {};
        openPresetModal({
            mode: 'confirm',
            title: texts.webpLimitTitle,
            message: (texts.webpLimitMsg || '').split('{0}').join(WEBP_MAX_DIMENSION),
            onConfirm: () => {
                const heightInput = document.getElementById('height-input');
                heightInput.value = WEBP_MAX_DIMENSION;
                // Persist the adjusted value before Python reads it from the DOM.
                heightInput.dispatchEvent(new Event('change', { bubbles: true }));
                pywebview.api.start();
                return true;
            }
        });
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
    if (isInitializing) return;
    const currentTheme = document.body.getAttribute('data-theme') || 'blue';
    const settings = {
        custom_width_checked: document.getElementById('custom-width').checked,
        width: parseInt(document.getElementById('width-input').value) || 800,
        height_limit: parseInt(document.getElementById('height-input').value) || 15000,
        save_quality: parseInt(document.getElementById('quality-input').value) || 100,
        save_format: document.getElementById('format-select').value || 'jpg',
        zip_checked: document.getElementById('is-zip').checked,
        pdf_checked: document.getElementById('is-pdf').checked,
        cbz_checked: document.getElementById('is-cbz').checked,
        enhance_checked: document.getElementById('enhance-quality').checked,
        no_stitch_checked: document.getElementById('no-stitch').checked,
        selected_tab: document.querySelector('.tab-content.active')?.id || 'process',
        theme: currentTheme,
        language: currentLang,
        save_location: document.getElementById('save-location-input')?.value || '',
        save_next_to_source: document.getElementById('save-next-to-source')?.checked || false,
        play_sound: document.getElementById('play-sound')?.checked ?? true,
        show_notification: document.getElementById('show-notifications')?.checked ?? true,
        thread_count: parseInt(document.getElementById('thread-count')?.value) || 4,
        output_suffix: document.getElementById('output-suffix')?.value || ' [Stitched]',
        filename_pattern: document.getElementById('filename-pattern')?.value || '[number]',
        filename_digits: parseInt(document.getElementById('filename-digits')?.value) || 3,
        custom_theme_color: document.getElementById('custom-theme-color')?.value || '',
        watermark_enabled: document.getElementById('watermark-enabled')?.checked || false,
        watermark_path: document.getElementById('watermark-path')?.value || '',
        watermark_count: parseInt(document.getElementById('watermark-count')?.value) || 1,
        watermark_edge: document.getElementById('watermark-edge')?.value || 'right',
        presets: appPresets,
        default_preset: defaultPresetName
    };
    if(window.pywebview) {
        pywebview.api.save_settings(settings);
    }
}

document.querySelectorAll('input, select').forEach(element => {
    element.addEventListener('change', updateSettings);
});

// Keep the directory field's filled state + tooltip in sync while typing/editing
(function initDirectoryField() {
    const input = document.getElementById('directory-input');
    if (!input) return;
    input.addEventListener('input', refreshDirectoryState);
    refreshDirectoryState();
})();

/* ============================================
   Custom output-format dropdown
   Drives the hidden <select id="format-select">,
   which stays the single source of truth.
   ============================================ */
const FORMAT_DESC_KEYS = {
    JPG: 'formatJpgDesc',
    PNG: 'formatPngDesc',
    WEBP: 'formatWebpDesc',
    PSD: 'formatPsdDesc'
};

function getFormatWrap() {
    return document.querySelector('.format-dropdown');
}

function buildFormatMenu() {
    const wrap = getFormatWrap();
    if (!wrap) return;
    const select = wrap.querySelector('#format-select');
    const menu = wrap.querySelector('.select-menu');
    const texts = translations[currentLang] || {};
    menu.innerHTML = '';

    Array.from(select.options).forEach(opt => {
        const descKey = FORMAT_DESC_KEYS[opt.value];
        const desc = (descKey && texts[descKey]) ? texts[descKey] : '';
        const li = document.createElement('li');
        li.className = 'select-option';
        li.setAttribute('role', 'option');
        li.dataset.value = opt.value;
        li.setAttribute('aria-selected', String(opt.value === select.value));
        li.innerHTML =
            `<span class="opt-name">${opt.value}</span>` +
            `<span class="opt-desc">${desc}</span>` +
            `<svg class="opt-check" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor">` +
            `<path d="M13.485 1.929a1 1 0 0 1 .087 1.32l-.087.094L6.4 10.486 2.515 6.6a1 1 0 0 1 1.32-1.5l.094.086L6.4 7.657l5.671-5.671a1 1 0 0 1 1.414-.057z"/></svg>`;
        li.addEventListener('click', () => selectFormat(opt.value));
        menu.appendChild(li);
    });
}

function syncFormatDropdown() {
    const wrap = getFormatWrap();
    if (!wrap) return;
    const select = wrap.querySelector('#format-select');
    if (select.selectedIndex < 0 && select.options.length) {
        select.selectedIndex = 0;
    }
    const valueEl = wrap.querySelector('.select-value');
    if (valueEl) valueEl.textContent = select.value;
    wrap.querySelectorAll('.select-option').forEach(li => {
        li.setAttribute('aria-selected', String(li.dataset.value === select.value));
    });
}

function selectFormat(value) {
    const wrap = getFormatWrap();
    if (!wrap) return;
    const select = wrap.querySelector('#format-select');
    if (select.value !== value) {
        select.value = value;
        select.dispatchEvent(new Event('change', { bubbles: true }));
    }
    syncFormatDropdown();
    closeFormatDropdown();
}

function openFormatDropdown() {
    const wrap = getFormatWrap();
    if (!wrap) return;
    wrap.dataset.open = 'true';
    wrap.querySelector('.select-trigger').setAttribute('aria-expanded', 'true');
}

function closeFormatDropdown() {
    const wrap = getFormatWrap();
    if (!wrap) return;
    wrap.dataset.open = 'false';
    wrap.querySelector('.select-trigger').setAttribute('aria-expanded', 'false');
}

function initFormatDropdown() {
    const wrap = getFormatWrap();
    if (!wrap) return;
    buildFormatMenu();
    syncFormatDropdown();

    wrap.querySelector('.select-trigger').addEventListener('click', (e) => {
        e.stopPropagation();
        (wrap.dataset.open === 'true') ? closeFormatDropdown() : openFormatDropdown();
    });

    document.addEventListener('click', (e) => {
        if (!wrap.contains(e.target)) closeFormatDropdown();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeFormatDropdown();
    });
}

initFormatDropdown();

/* ============================================
   PRESETS
   A preset captures the full configuration (incl. theme & language).
   Persisted inside settings.json as { presets: [...], default_preset }.
   ============================================ */
let appPresets = [];
let defaultPresetName = null;
let activePresetName = null;

const PRESET_FIELD_DEFS = [
    { key: 'custom_width_checked', id: 'custom-width', type: 'check' },
    { key: 'width', id: 'width-input', type: 'int', def: 800 },
    { key: 'height_limit', id: 'height-input', type: 'int', def: 15000 },
    { key: 'save_quality', id: 'quality-input', type: 'int', def: 100 },
    { key: 'save_format', id: 'format-select', type: 'value', def: 'jpg' },
    { key: 'zip_checked', id: 'is-zip', type: 'check' },
    { key: 'pdf_checked', id: 'is-pdf', type: 'check' },
    { key: 'cbz_checked', id: 'is-cbz', type: 'check' },
    { key: 'enhance_checked', id: 'enhance-quality', type: 'check' },
    { key: 'no_stitch_checked', id: 'no-stitch', type: 'check' },
    { key: 'watermark_enabled', id: 'watermark-enabled', type: 'check' },
    { key: 'watermark_path', id: 'watermark-path', type: 'value', def: '' },
    { key: 'watermark_count', id: 'watermark-count', type: 'int', def: 1 },
    { key: 'watermark_edge', id: 'watermark-edge', type: 'value', def: 'right' }
];

function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => (
        { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
}

function sanitizeFilename(s) {
    return (String(s).replace(/[\\/:*?"<>|]+/g, '_').trim().slice(0, 60)) || 'preset';
}

function findPreset(name) {
    return appPresets.find(p => p && p.name === name);
}

function readCurrentValues() {
    const v = {};
    PRESET_FIELD_DEFS.forEach(f => {
        const el = document.getElementById(f.id);
        if (!el) return;
        if (f.type === 'check') v[f.key] = el.checked;
        else if (f.type === 'int') v[f.key] = parseInt(el.value) || f.def;
        else v[f.key] = el.value || f.def;
    });
    v.theme = document.body.getAttribute('data-theme') || 'blue';
    v.language = currentLang;
    return v;
}

function applyPresetValues(values) {
    if (!values) return;
    PRESET_FIELD_DEFS.forEach(f => {
        if (!(f.key in values)) return;
        const el = document.getElementById(f.id);
        if (!el) return;
        if (f.type === 'check') el.checked = !!values[f.key];
        else el.value = values[f.key];
    });
    if (typeof syncFormatDropdown === 'function') syncFormatDropdown();
    if (values.theme) setTheme(values.theme);
    if (values.language && values.language !== currentLang) setLanguage(values.language);
    if (typeof toggleWatermarkOptions === 'function') toggleWatermarkOptions();
}

function renderPresetMenu() {
    const menu = document.querySelector('.preset-menu');
    if (!menu) return;
    const texts = translations[currentLang] || {};
    menu.innerHTML = '';

    if (!appPresets.length) {
        const li = document.createElement('li');
        li.className = 'preset-empty';
        li.textContent = texts.noPresetsYet || 'No presets yet';
        menu.appendChild(li);
        return;
    }

    const starPath = '<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>';
    const saveIcon = '<path d="M11 2H9v3h2z"/><path d="M1.5 0h11.586a1.5 1.5 0 0 1 1.06.44l1.415 1.414A1.5 1.5 0 0 1 16 2.914V14.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 14.5v-13A1.5 1.5 0 0 1 1.5 0M1 1.5v13a.5.5 0 0 0 .5.5H2v-4.5A1.5 1.5 0 0 1 3.5 9h9a1.5 1.5 0 0 1 1.5 1.5V15h.5a.5.5 0 0 0 .5-.5V2.914a.5.5 0 0 0-.146-.353l-1.415-1.415A.5.5 0 0 0 13.086 1H13v4.5A1.5 1.5 0 0 1 11.5 7h-7A1.5 1.5 0 0 1 3 5.5V1H1.5a.5.5 0 0 0-.5.5m3 4a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 .5-.5V1H4zM3 15h10v-4.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5z"/>';
    const renameIcon = '<path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325"/>';
    const deleteIcon = '<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/><path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>';

    appPresets.forEach(p => {
        const li = document.createElement('li');
        li.className = 'select-option preset-option';
        li.setAttribute('role', 'option');
        li.dataset.name = p.name;
        li.setAttribute('aria-selected', String(p.name === activePresetName));
        const isDefault = p.name === defaultPresetName;
        li.innerHTML =
            `<button type="button" class="preset-star ${isDefault ? 'is-default' : ''}" title="${escapeHtml(texts.setDefault || 'Set as default')}" aria-label="default">` +
            `<svg viewBox="0 0 16 16" fill="currentColor">${starPath}</svg></button>` +
            `<span class="preset-opt-name"><span class="preset-opt-name-inner">${escapeHtml(p.name)}</span></span>` +
            `<span class="preset-row-actions">` +
                `<button type="button" class="preset-row-btn" data-act="save" title="${escapeHtml(texts.presetSave || 'Save settings to preset')}" aria-label="save"><svg viewBox="0 0 16 16" fill="currentColor">${saveIcon}</svg></button>` +
                `<button type="button" class="preset-row-btn" data-act="rename" title="${escapeHtml(texts.presetRename || 'Rename preset')}" aria-label="rename"><svg viewBox="0 0 16 16" fill="currentColor">${renameIcon}</svg></button>` +
                `<button type="button" class="preset-row-btn preset-row-btn-danger" data-act="delete" title="${escapeHtml(texts.presetDelete || 'Delete preset')}" aria-label="delete"><svg viewBox="0 0 16 16" fill="currentColor">${deleteIcon}</svg></button>` +
            `</span>`;
        li.querySelector('.preset-star').addEventListener('click', (e) => {
            e.stopPropagation();
            setDefaultPreset(p.name);
        });
        li.querySelector('[data-act="save"]').addEventListener('click', (e) => {
            e.stopPropagation();
            presetSave(p.name);
        });
        li.querySelector('[data-act="rename"]').addEventListener('click', (e) => {
            e.stopPropagation();
            presetRename(p.name);
        });
        li.querySelector('[data-act="delete"]').addEventListener('click', (e) => {
            e.stopPropagation();
            presetDelete(p.name);
        });
        li.addEventListener('click', () => applyPreset(p.name));
        menu.appendChild(li);
    });
    calculatePresetNameOverflows();
}

function calculatePresetNameOverflows() {
    const menu = document.querySelector('.preset-menu');
    if (!menu) return;
    menu.querySelectorAll('.preset-option').forEach(option => {
        const nameEl = option.querySelector('.preset-opt-name');
        const nameInner = option.querySelector('.preset-opt-name-inner');
        if (nameEl && nameInner) {
            const containerWidth = nameEl.clientWidth;
            const contentWidth = nameInner.scrollWidth;
            if (contentWidth > containerWidth) {
                nameEl.classList.add('has-overflow');
                const scrollDist = contentWidth - containerWidth;
                const isRTL = document.body.getAttribute('dir') === 'rtl';
                const sign = isRTL ? '' : '-';
                nameEl.style.setProperty('--scroll-dist', `${sign}${scrollDist}px`);
                
                // Keep scroll speed consistent (approx 35px per second)
                const duration = Math.max(1.5, scrollDist / 35);
                nameEl.style.setProperty('--scroll-duration', `${duration}s`);
            } else {
                nameEl.classList.remove('has-overflow');
                nameEl.style.removeProperty('--scroll-dist');
                nameEl.style.removeProperty('--scroll-duration');
            }
        }
    });
}

function updatePresetTrigger() {
    const wrap = document.getElementById('preset-open');
    if (!wrap) return;
    const nameText = wrap.querySelector('.preset-name-text');
    const star = wrap.querySelector('.preset-star-ind');
    const texts = translations[currentLang] || {};
    if (activePresetName && findPreset(activePresetName)) {
        nameText.textContent = activePresetName;
        nameText.removeAttribute('data-i18n');
        // Icon-only button: surface the active preset name via the tooltip
        wrap.title = activePresetName;
        wrap.classList.add('has-active');
        if (star) star.style.display = (activePresetName === defaultPresetName) ? '' : 'none';
    } else {
        nameText.textContent = texts.noPreset || 'No Preset';
        nameText.setAttribute('data-i18n', 'noPreset');
        wrap.title = texts.presetsTitle || 'Presets';
        wrap.classList.remove('has-active');
        if (star) star.style.display = 'none';
    }
}

function persistPresets() {
    updateSettings();
}

function initPresets(presets, defaultName) {
    appPresets = Array.isArray(presets) ? presets.filter(p => p && typeof p.name === 'string' && p.values) : [];
    defaultPresetName = (typeof defaultName === 'string' && findPreset(defaultName)) ? defaultName : null;
    // On startup the default preset's values were already applied by Python.
    activePresetName = defaultPresetName;
    renderPresetMenu();
    updatePresetTrigger();
    isInitializing = false;
}

/* ---- CRUD actions ---- */
function applyPreset(name) {
    const p = findPreset(name);
    if (!p) return;
    applyPresetValues(p.values);
    activePresetName = name;
    closePresetsModal();
    renderPresetMenu();
    updatePresetTrigger();
    persistPresets();
    showSuccess((translations[currentLang] || {}).toastApplied || 'Preset applied');
}

function presetSave(name) {
    const texts = translations[currentLang] || {};
    const target = name || activePresetName;
    if (!target || !findPreset(target)) {
        presetSaveAs();
        return;
    }
    findPreset(target).values = readCurrentValues();
    renderPresetMenu();
    updatePresetTrigger();
    persistPresets();
    showSuccess(texts.toastUpdated);
}

function presetSaveAs() {
    const texts = translations[currentLang] || {};
    openPresetModal({
        mode: 'input',
        title: texts.saveAsTitle,
        value: '',
        onConfirm: (name) => doSavePresetAs(name)
    });
}

function doSavePresetAs(rawName) {
    const texts = translations[currentLang] || {};
    const name = (rawName || '').trim();
    if (!name) { showError(texts.errNameRequired); return false; }
    if (findPreset(name)) { showError(texts.errNameExists); return false; }
    appPresets.push({ name, values: readCurrentValues() });
    activePresetName = name;
    renderPresetMenu();
    updatePresetTrigger();
    persistPresets();
    showSuccess(texts.toastSaved);
    return true;
}

function presetRename(name) {
    const texts = translations[currentLang] || {};
    const old = name || activePresetName;
    if (!old || !findPreset(old)) { showError(texts.errSelectFirst); return; }
    openPresetModal({
        mode: 'input',
        title: texts.renameTitle,
        value: old,
        onConfirm: (newName) => doRename(old, newName)
    });
}

function doRename(oldName, rawNew) {
    const texts = translations[currentLang] || {};
    const newName = (rawNew || '').trim();
    if (!newName) { showError(texts.errNameRequired); return false; }
    if (newName !== oldName && findPreset(newName)) { showError(texts.errNameExists); return false; }
    const p = findPreset(oldName);
    if (!p) return true;
    p.name = newName;
    if (defaultPresetName === oldName) defaultPresetName = newName;
    if (activePresetName === oldName) activePresetName = newName;
    renderPresetMenu();
    updatePresetTrigger();
    persistPresets();
    showSuccess(texts.toastRenamed);
    return true;
}

function presetDelete(name) {
    const texts = translations[currentLang] || {};
    const target = name || activePresetName;
    if (!target || !findPreset(target)) { showError(texts.errSelectFirst); return; }
    openPresetModal({
        mode: 'confirm',
        title: texts.deleteTitle,
        message: `"${target}" ${texts.deleteConfirmMsg || ''}`,
        onConfirm: () => { doDelete(target); return true; }
    });
}

function doDelete(name) {
    appPresets = appPresets.filter(p => p.name !== name);
    if (defaultPresetName === name) defaultPresetName = null;
    if (activePresetName === name) activePresetName = null;
    renderPresetMenu();
    updatePresetTrigger();
    persistPresets();
    showSuccess((translations[currentLang] || {}).toastDeleted);
}

function setDefaultPreset(name) {
    const texts = translations[currentLang] || {};
    if (defaultPresetName === name) {
        defaultPresetName = null;
        showSuccess(texts.toastDefaultCleared);
    } else {
        defaultPresetName = name;
        showSuccess(texts.toastDefaultSet);
    }
    renderPresetMenu();
    updatePresetTrigger();
    persistPresets();
}

/* ---- Import / Export ---- */
function presetExportMenuToggle(e) {
    if (e) e.stopPropagation();
    const menu = document.getElementById('preset-export-menu');
    if (menu) menu.classList.toggle('open');
}

function presetExport(scope, e) {
    if (e) e.stopPropagation();
    const menu = document.getElementById('preset-export-menu');
    if (menu) menu.classList.remove('open');
    const texts = translations[currentLang] || {};
    let payload, filename;
    if (scope === 'current') {
        if (!activePresetName || !findPreset(activePresetName)) { showError(texts.errSelectFirst); return; }
        const p = findPreset(activePresetName);
        payload = { type: 'photoslicer-preset', version: 1, preset: p };
        filename = `${sanitizeFilename(p.name)}.json`;
    } else {
        if (!appPresets.length) { showError(texts.errNothingExport); return; }
        payload = { type: 'photoslicer-presets', version: 1, presets: appPresets };
        filename = 'photoslicer-presets.json';
    }
    if (!window.pywebview) return;
    pywebview.api.export_presets(JSON.stringify(payload, null, 2), filename).then(path => {
        if (path) showSuccess(texts.toastExported);
    });
}

function presetImport() {
    const texts = translations[currentLang] || {};
    if (!window.pywebview) return;
    pywebview.api.import_presets().then(text => {
        if (!text) return;
        let data;
        try { data = JSON.parse(text); } catch (err) { showError(texts.errImportInvalid); return; }

        let incoming = [];
        if (data && data.type === 'photoslicer-preset' && data.preset) incoming = [data.preset];
        else if (data && Array.isArray(data.presets)) incoming = data.presets;
        else if (Array.isArray(data)) incoming = data;
        else { showError(texts.errImportInvalid); return; }

        let added = 0;
        incoming.forEach(p => {
            if (!p || typeof p.name !== 'string' || typeof p.values !== 'object' || !p.values) return;
            let name = p.name.trim();
            if (!name) return;
            if (findPreset(name)) {
                let n = 2;
                while (findPreset(`${name} (${n})`)) n++;
                name = `${name} (${n})`;
            }
            appPresets.push({ name, values: p.values });
            added++;
        });

        if (!added) { showError(texts.errImportInvalid); return; }
        renderPresetMenu();
        updatePresetTrigger();
        persistPresets();
        showSuccess(texts.toastImported);
    });
}

/* ---- Presets modal open/close ---- */
function openPresetsModal() {
    const overlay = document.getElementById('presets-modal');
    if (!overlay) return;
    renderPresetMenu();
    overlay.dataset.open = 'true';
    setTimeout(calculatePresetNameOverflows, 100);
}

function closePresetsModal() {
    const overlay = document.getElementById('presets-modal');
    if (!overlay) return;
    overlay.dataset.open = 'false';
    const em = document.getElementById('preset-export-menu');
    if (em) em.classList.remove('open');
}

/* ---- Modal (name input / confirm) ---- */
function openPresetModal(opts) {
    const overlay = document.getElementById('preset-modal');
    if (!overlay) return;
    const titleEl = document.getElementById('preset-modal-title');
    const msgEl = document.getElementById('preset-modal-message');
    const input = document.getElementById('preset-modal-input');
    const confirmBtn = document.getElementById('preset-modal-confirm');
    const cancelBtn = document.getElementById('preset-modal-cancel');
    const texts = translations[currentLang] || {};

    const isInput = opts.mode !== 'confirm';
    titleEl.textContent = opts.title || '';
    input.style.display = isInput ? '' : 'none';
    msgEl.style.display = opts.message ? '' : 'none';
    msgEl.textContent = opts.message || '';
    input.value = opts.value || '';
    input.placeholder = texts.namePlaceholder || 'Preset name';
    confirmBtn.textContent = texts.confirm || 'OK';
    cancelBtn.textContent = texts.cancel || 'Cancel';

    function close() {
        overlay.dataset.open = 'false';
        confirmBtn.onclick = null;
        cancelBtn.onclick = null;
        overlay.onclick = null;
        var closeBtn = document.getElementById('preset-modal-close');
        if (closeBtn) closeBtn.onclick = null;
        document.removeEventListener('keydown', onKey);
    }
    function doConfirm() {
        const result = opts.onConfirm ? opts.onConfirm(isInput ? input.value : null) : true;
        if (result !== false) close();
    }
    function onKey(e) {
        if (e.key === 'Escape') { e.preventDefault(); close(); }
        else if (e.key === 'Enter' && isInput) { e.preventDefault(); doConfirm(); }
    }

    confirmBtn.onclick = doConfirm;
    cancelBtn.onclick = close;
    var closeBtn = document.getElementById('preset-modal-close');
    if (closeBtn) closeBtn.onclick = close;
    overlay.onclick = (e) => { if (e.target === overlay) close(); };
    document.addEventListener('keydown', onKey);

    overlay.dataset.open = 'true';
    if (isInput) setTimeout(() => { input.focus(); input.select(); }, 30);
}

function initPresetsModal() {
    const overlay = document.getElementById('presets-modal');
    if (!overlay) return;
    // Click on the dimmed backdrop closes the modal
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closePresetsModal();
    });
    // Click outside the export submenu collapses it
    document.addEventListener('click', (e) => {
        const em = document.getElementById('preset-export-menu');
        const exportWrap = document.querySelector('.preset-export-wrap');
        if (em && exportWrap && !exportWrap.contains(e.target)) em.classList.remove('open');
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay.dataset.open === 'true') closePresetsModal();
    });
}

initPresetsModal();

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.id.replace('tab-', '');
        showTab(tabName);
    });
});

function handleCheckboxClick(checkbox) {
    const zipCheckbox = document.getElementById('is-zip');
    const pdfCheckbox = document.getElementById('is-pdf');
    const cbzCheckbox = document.getElementById('is-cbz');

    if (checkbox.checked) {
        if (checkbox.id === 'is-zip') {
            pdfCheckbox.checked = false;
            cbzCheckbox.checked = false;
        } else if (checkbox.id === 'is-pdf') {
            zipCheckbox.checked = false;
            cbzCheckbox.checked = false;
        } else if (checkbox.id === 'is-cbz') {
            zipCheckbox.checked = false;
            pdfCheckbox.checked = false;
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

function stopProcessing() {
    const state = startButton.dataset.state || 'idle';
    if (state === 'idle') return;
    if (window.pywebview) pywebview.api.stop_processing();
    // Optimistic feedback: disable Stop until the worker unwinds and resets to idle
    const stopBtn = document.getElementById('stop-button');
    if (stopBtn) stopBtn.disabled = true;
}

function setButtonState(state) {
    startButton.dataset.state = state;
    // Drive idle-pausing of the progress-bar animations (see styles.css)
    document.body.classList.toggle('is-processing', state === 'processing' || state === 'busy');
    // Show the Stop button for any active job (processing / paused / busy)
    document.body.classList.toggle('job-active', state !== 'idle');
    // Collapse/expand workspace controls and progress details
    document.body.classList.toggle('workspace-processing', state === 'processing' || state === 'busy' || state === 'paused');
    const stopBtn = document.getElementById('stop-button');
    if (stopBtn) stopBtn.disabled = (state === 'idle');
    const texts = translations[currentLang];

    if (state === 'idle') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-rocket-takeoff" viewBox="0 0 16 16"><path d="M9.752 6.193c.599.6 1.73.437 2.528-.362s.96-1.932.362-2.531c-.599-.6-1.73-.438-2.528.361-.798.8-.96 1.933-.362 2.532"/><path d="M15.811 3.312c-.363 1.534-1.334 3.626-3.64 6.218l-.24 2.408a2.56 2.56 0 0 1-.732 1.526L8.817 15.85a.51.51 0 0 1-.867-.434l.27-1.899c.04-.28-.013-.593-.131-.956a9 9 0 0 0-.249-.657l-.082-.202c-.815-.197-1.578-.662-2.191-1.277-.614-.615-1.079-1.379-1.275-2.195l-.203-.083a10 10 0 0 0-.655-.248c-.363-.119-.675-.172-.955-.132l-1.896.27A.51.51 0 0 1 .15 7.17l2.382-2.386c.41-.41.947-.67 1.524-.734h.006l2.4-.238C9.005 1.55 11.087.582 12.623.208c.89-.217 1.59-.232 2.08-.188.244.023.435.06.57.093q.1.026.16.045c.184.06.279.13.351.295l.029.073a3.5 3.5 0 0 1 .157.721c.055.485.051 1.178-.159 2.065m-4.828 7.475.04-.04-.107 1.081a1.54 1.54 0 0 1-.44.913l-1.298 1.3.054-.38c.072-.506-.034-.993-.172-1.418a9 9 0 0 0-.164-.45c.738-.065 1.462-.38 2.087-1.006M5.205 5c-.625.626-.94 1.351-1.004 2.09a9 9 0 0 0-.45-.164c-.424-.138-.91-.244-1.416-.172l-.38.054 1.3-1.3c.245-.246.566-.401.91-.44l1.08-.107zm9.406-3.961c-.38-.034-.967-.027-1.746.163-1.558.38-3.917 1.496-6.937 4.521-.62.62-.799 1.34-.687 2.051.107.676.483 1.362 1.048 1.928.564.565 1.25.941 1.924 1.049.71.112 1.429-.067 2.048-.688 3.079-3.083 4.192-5.444 4.556-6.987.183-.771.18-1.345.138-1.713a3 3 0 0 0-.045-.283 3 3 0 0 0-.3-.041Z"/><path d="M7.009 12.139a7.6 7.6 0 0 1-1.804-1.352A7.6 7.6 0 0 1 3.794 8.86c-1.102.992-1.965 5.054-1.839 5.18.125.126 3.936-.896 5.054-1.902Z"/></svg><span>${texts.btnInitiate}</span></div>`;
        resetProgressUI();
    } else if (state === 'processing') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-pause-fill" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5m5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5"/></svg><span>${texts.btnPause}</span></div>`;
        showProgressUI();
    } else if (state === 'paused') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-play-fill" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393"/></svg><span>${texts.btnResume}</span></div>`;
    } else if (state === 'busy') {
        startButton.innerHTML = `<div class="btn-content"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 15a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1 0-1h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11zm2-13v1c0 .537.12 1.045.337 1.5h6.326c.216-.455.337-.963.337-1.5V2h-7zm3 6.35c0 .701-.478 1.236-1.011 1.492A3.5 3.5 0 0 0 4.5 13s.866-1.299 3-1.48V8.35zm1 0v1.48c2.134.181 3 1.48 3 1.48a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 10.052 8.5 9.35z"/></svg><span>${texts.btnProcessing}</span></div>`;
        showProgressUI();
    }
}

/* ============================================
   PROGRESS UI HELPERS
   ============================================ */
function showProgressUI() {
    var meta = document.getElementById('progress-meta');
    if (meta) meta.classList.add('visible');
    var info = document.getElementById('progress-info');
    if (info) info.classList.add('visible');
    var steps = document.getElementById('step-indicator');
    if (steps) steps.classList.add('visible');
}

function resetProgressUI() {
    var meta = document.getElementById('progress-meta');
    if (meta) meta.classList.remove('visible');
    var info = document.getElementById('progress-info');
    if (info) info.classList.remove('visible');
    var steps = document.getElementById('step-indicator');
    if (steps) steps.classList.remove('visible');
    resetProgressInfo();
    resetStepIndicator();
    var percent = document.getElementById('progress-percent');
    if (percent) percent.textContent = '0%';
    var detail = document.getElementById('progress-detail');
    if (detail) {
        var texts = translations[currentLang] || {};
        detail.textContent = texts.readyStatus || 'Ready to Slice';
    }
}

var PROGRESS_STATUS_MAP = {
    'Enhancing...': 'statusEnhancing',
    'Stitching...': 'statusStitching',
    'Slicing...': 'statusSlicing',
    'Watermarking...': 'statusWatermarking',
    'Preparing...': 'statusPreparing',
    'Complete': 'statusComplete'
};

// Show/hide the optional Watermark step in the step indicator.
// Called from Python at the start of each run based on the watermark setting.
function setWatermarkStepVisible(visible) {
    var step = document.getElementById('step-watermark');
    var line = document.getElementById('step-watermark-line');
    if (step) step.style.display = visible ? '' : 'none';
    if (line) line.style.display = visible ? '' : 'none';
}

// Swap the progress label between "Current" (multi-folder mode, pi-current shows a
// folder name) and "Status" (single-folder mode, pi-current already shows a status
// string like "Slicing…").  A status string is any value in PROGRESS_STATUS_MAP.
// Switching the data-i18n key keeps language toggles in sync automatically.
function applyProgressModeLabel(currentFile) {
    var labelEl = document.getElementById('pi-current')?.parentElement?.querySelector('.progress-info-label');
    if (!labelEl) return;
    var texts = translations[currentLang] || {};
    var isStatus = !!(currentFile && PROGRESS_STATUS_MAP[currentFile]);
    var newKey = isStatus ? 'statusLabel' : 'currentLabel';
    if (labelEl.getAttribute('data-i18n') !== newKey) {
        labelEl.setAttribute('data-i18n', newKey);
        labelEl.textContent = texts[newKey] || (isStatus ? 'Status' : 'Current');
    }
}

function updateProgressInfo(current, total, currentFile, elapsed, eta) {
    applyProgressModeLabel(currentFile);

    var filesEl = document.getElementById('pi-files');
    if (filesEl) filesEl.textContent = (current || 0) + '/' + (total || 0);

    var texts = translations[currentLang] || {};
    var displayFile = currentFile;
    if (currentFile && PROGRESS_STATUS_MAP[currentFile]) {
        displayFile = texts[PROGRESS_STATUS_MAP[currentFile]] || currentFile;
    }

    var currentEl = document.getElementById('pi-current');
    if (currentEl) {
        currentEl.textContent = (displayFile && displayFile.length > 16) ? displayFile.slice(0, 13) + '...' : (displayFile || '-');
    }
    var elapsedEl = document.getElementById('pi-elapsed');
    if (elapsedEl) elapsedEl.textContent = elapsed || '00:00:00';
    var etaEl = document.getElementById('pi-eta');
    if (etaEl) etaEl.textContent = eta || '-';

}

function resetProgressInfo() {
    var filesEl = document.getElementById('pi-files');
    if (filesEl) filesEl.textContent = '0/0';
    var currentEl = document.getElementById('pi-current');
    if (currentEl) currentEl.textContent = '-';
    var elapsedEl = document.getElementById('pi-elapsed');
    if (elapsedEl) elapsedEl.textContent = '00:00:00';
    var etaEl = document.getElementById('pi-eta');
    if (etaEl) etaEl.textContent = '-';
    applyProgressModeLabel('');
}

function updateStepIndicator(step) {
    var steps = document.querySelectorAll('.step-indicator .step');
    var lines = document.querySelectorAll('.step-indicator .step-line');
    var passed = true;
    steps.forEach(function(s, i) {
        var sStep = s.getAttribute('data-step');
        if (sStep === step) {
            s.classList.add('active');
            s.classList.remove('completed');
            passed = false;
        } else if (passed) {
            s.classList.remove('active');
            s.classList.add('completed');
        } else {
            s.classList.remove('active');
            s.classList.remove('completed');
        }
        if (lines[i]) {
            if (passed && sStep !== step) {
                lines[i].classList.add('completed');
            } else {
                lines[i].classList.remove('completed');
            }
        }
    });
}

function resetStepIndicator() {
    var steps = document.querySelectorAll('.step-indicator .step');
    var lines = document.querySelectorAll('.step-indicator .step-line');
    steps.forEach(function(s) {
        s.classList.remove('active');
        s.classList.remove('completed');
    });
    if (steps[0]) steps[0].classList.add('active');
    lines.forEach(function(l) {
        l.classList.remove('completed');
    });
}

function setTheme(themeName) {
    // Clear any custom theme overrides when switching to a predefined theme
    if (themeName !== 'custom') {
        // Only clear CSS var overrides, don't touch data-theme or dots
        ['--theme-gradient','--theme-gradient-hover','--theme-gradient-soft',
         '--theme-solid','--theme-solid-2','--theme-glow','--theme-glow-strong',
         '--theme-glow-soft','--input-focus-border'].forEach(function(v) {
            document.documentElement.style.removeProperty(v);
        });
        // Clear the color picker to empty so updateSettings saves ''
        var cp = document.getElementById('custom-theme-color');
        if (cp) cp.value = '';
        var hexLabel = document.getElementById('custom-theme-hex');
        if (hexLabel) hexLabel.textContent = '';
        // Reset preview dot to default blue
        var dot = document.getElementById('theme-preview-dot');
        if (dot) dot.style.background = '#0ea5e9';
    }
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

    // Update adaptive contrast color based on the preset's solid color
    setThemeContrast(PRESET_SOLIDS[themeName] || '#0ea5e9');
}

function changeTheme(themeName) {
    setTheme(themeName);
    // Clear saved custom color when picking a preset theme dot
    var cp = document.getElementById('custom-theme-color');
    if (cp) cp.value = '';
    var hexLabel = document.getElementById('custom-theme-hex');
    if (hexLabel) hexLabel.textContent = '';
    updateSettings();
}

// Lightweight live preview for the wheel: updates CSS vars and preview dot only,
// skipping the expensive preset-swatch loop (the preset modal is closed during wheel use).
function applyLiveWheelPreview(hex) {
    if (!hex || hex === '') return;
    // Update preview dot and hex label only (no hidden input, no swatch loop)
    updatePreviewUI(hex);

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

    document.body.setAttribute('data-theme', 'custom');
    document.querySelectorAll('.theme-dot').forEach(function(d) { d.classList.remove('active'); });

    // Update adaptive contrast so text/icons stay readable on light backgrounds
    setThemeContrast(hex);
}

function applyCustomTheme(hex) {
    if (!hex || hex === '') {
        // Revert: clear all custom CSS variable overrides
        ['--theme-gradient','--theme-gradient-hover','--theme-gradient-soft',
         '--theme-solid','--theme-solid-2','--theme-glow','--theme-glow-strong',
         '--theme-glow-soft','--input-focus-border'].forEach(function(v) {
            document.documentElement.style.removeProperty(v);
        });
        // Reset preview dot to default blue
        var dot = document.getElementById('theme-preview-dot');
        if (dot) dot.style.background = '#0ea5e9';
        // Remove adaptive contrast — it will be set by setTheme
        document.documentElement.style.removeProperty('--on-theme-text');
        document.documentElement.style.removeProperty('--theme-is-light');
        return;
    }

    // Update the hex label, preview dot, hidden input, and swatch selection
    updateColorUI(hex);

    var r = parseInt(hex.slice(1,3), 16);
    var g = parseInt(hex.slice(3,5), 16);
    var b = parseInt(hex.slice(5,7), 16);

    // Generate color variations for a rich gradient
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

    document.body.setAttribute('data-theme', 'custom');
    document.querySelectorAll('.theme-dot').forEach(function(d) { d.classList.remove('active'); });

    // Update adaptive contrast so text/icons stay readable on light backgrounds
    setThemeContrast(hex);
}

function resetCustomTheme() {
    var cp = document.getElementById('custom-theme-color');
    if (cp) cp.value = '#0ea5e9';
    var hexLabel = document.getElementById('custom-theme-hex');
    if (hexLabel) hexLabel.textContent = '#0ea5e9';
    var dot = document.getElementById('theme-preview-dot');
    if (dot) dot.style.background = '#0ea5e9';
    applyCustomTheme('');
    setTheme('blue');
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

window.addEventListener('DOMContentLoaded', function() {
    handleResize();
    positionTabIndicator();
});
window.addEventListener('resize', function() {
    handleResize();
    positionTabIndicator();
});

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

// ===== DRAG & DROP =====
// The actual absolute-path delivery happens on the Python side (main.py:
// on_folder_dropped), which calls window.handleDroppedPaths. This JS only
// manages preventDefault + the drag-over highlight.
let _dragDepth = 0;
function _isFileDrag(e) {
    if (!e.dataTransfer) return false;
    const types = e.dataTransfer.types;
    if (!types) return false;
    for (let i = 0; i < types.length; i++) if (types[i] === 'Files') return true;
    return false;
}
function setupDragAndDrop() {
    const wrapper = document.querySelector('.folder-wrapper');
    window.addEventListener('dragenter', (e) => {
        if (!_isFileDrag(e)) return;
        e.preventDefault();
        _dragDepth++;
        if (wrapper) wrapper.classList.add('drag-over');
    });
    window.addEventListener('dragover', (e) => {
        if (!_isFileDrag(e)) return;
        e.preventDefault();
        if (e.dataTransfer) e.dataTransfer.dropEffect = 'copy';
    });
    window.addEventListener('dragleave', (e) => {
        if (!_isFileDrag(e)) return;
        _dragDepth = Math.max(0, _dragDepth - 1);
        if (_dragDepth === 0 && wrapper) wrapper.classList.remove('drag-over');
    });
    window.addEventListener('drop', (e) => {
        if (!_isFileDrag(e)) return;
        e.preventDefault();
        _dragDepth = 0;
        if (wrapper) wrapper.classList.remove('drag-over');
    });
}

// Called from Python with the resolved absolute path(s) of the dropped items.
// PhotoSlicer works on a single source folder (or .cbz), so we take the first.
window.handleDroppedPaths = function(paths) {
    _dragDepth = 0;
    const wrapper = document.querySelector('.folder-wrapper');
    if (wrapper) wrapper.classList.remove('drag-over');
    if (!paths || paths.length === 0) return;

    const path = paths[0];
    const input = document.getElementById('directory-input');
    if (!input) return;
    input.value = path;
    refreshDirectoryState();
    updateSettings();

    // Brief success-pop animation on the field
    if (wrapper) {
        wrapper.classList.remove('drop-success');
        void wrapper.offsetWidth; // restart the animation
        wrapper.classList.add('drop-success');
        setTimeout(() => wrapper.classList.remove('drop-success'), 600);
    }

    const texts = translations[currentLang] || {};
    showSuccess(texts.dropSuccess || 'Folder dropped successfully.');
};
// Back-compat in case Python ever calls the singular name
window.handleDroppedPath = function(path) { window.handleDroppedPaths([path]); };
document.addEventListener('DOMContentLoaded', setupDragAndDrop);

async function pasteFromClipboard() {
    try {
        const text = await window.pywebview.api.get_clipboard_text();
        const trimmedText = text.trim();
        const texts = translations[currentLang] || {};

        const isLikelyPath = 
            /^([a-zA-Z]:\\|\/|\\\\)/.test(trimmedText) ||
            trimmedText.includes('\\') || 
            trimmedText.includes('/');

        if (isLikelyPath) {
            const input = document.getElementById('directory-input');
            input.value = trimmedText;

            input.focus();
            input.blur();

            refreshDirectoryState();
            updateSettings();
            showSuccess(texts.clipboardPasted || 'Path pasted successfully.');
        } else {
            showError(texts.clipboardInvalid || 'Clipboard text is not a valid directory path.');
        }
    } catch (err) {
        console.error('Failed to get clipboard text from Python: ', err);
        const texts = translations[currentLang] || {};
        showError(texts.clipboardError || 'Failed to get clipboard text.');
    }
}

/* ============================================
   Watermark UI Helpers
   ============================================ */
function selectWatermarkFile() {
    if (!window.pywebview) return;
    pywebview.api.select_watermark_file().then(function(res) {
        if (!res) return;
        const path = Array.isArray(res) ? res[0] : res;
        if (!path) return;
        const input = document.getElementById('watermark-path');
        if (input) {
            input.value = path;
            updateSettings();
        }
    });
}

function toggleWatermarkOptions() {
    const el = document.getElementById('watermark-enabled');
    const enabled = el ? el.checked : false;
    document.querySelectorAll('.watermark-option').forEach(row => {
        row.classList.toggle('disabled-by-checkbox', !enabled);
    });
}

function validateWatermarkSettings() {
    const countInput = document.getElementById('watermark-count');
    if (countInput) {
        let countVal = parseInt(countInput.value) || 1;
        if (countVal < 1) countVal = 1;
        if (countVal > 10) countVal = 10;
        countInput.value = countVal;
    }

    updateSettings();
}
