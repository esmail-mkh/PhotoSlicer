// This file is generated dynamically by PhotoSlicer on startup to prevent theme/language flash.
(function() {
    var theme = "purple";
    var customThemeColor = "";
    var lang = "fa";
    var dir = (lang === 'fa') ? 'rtl' : 'ltr';

    // Apply layout direction immediately to documentElement
    document.documentElement.setAttribute('dir', dir);
    document.documentElement.setAttribute('lang', lang);

    // Apply theme immediately to documentElement
    if (customThemeColor) {
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
    } else {
        if (theme !== 'blue') {
            document.documentElement.setAttribute('data-theme', theme);
        }
        var solids = {
            blue: '#0ea5e9',
            purple: '#d946ef',
            sunset: '#fbbf24',
            emerald: '#34d399',
            ruby: '#ef4444',
            gold: '#d4a017'
        };
        var hex = solids[theme] || '#0ea5e9';
        var r = parseInt(hex.slice(1, 3), 16);
        var g = parseInt(hex.slice(3, 5), 16);
        var b = parseInt(hex.slice(5, 7), 16);
        var yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        var isLight = yiq >= 165;
        var contrast = isLight ? '#0a0e1a' : '#ffffff';
        document.documentElement.style.setProperty('--on-theme-text', contrast);
        document.documentElement.style.setProperty('--theme-is-light', isLight ? '1' : '0');
    }

    // When the body is ready, copy attributes so existing scripts work seamlessly
    document.addEventListener('DOMContentLoaded', function() {
        var t = document.documentElement.getAttribute('data-theme');
        if (t) {
            document.body.setAttribute('data-theme', t);
        } else {
            document.body.removeAttribute('data-theme');
        }
        document.body.setAttribute('dir', dir);
    });
})();
