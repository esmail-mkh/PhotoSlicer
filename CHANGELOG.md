[🇮🇷 **فارسی**](#-فوتو-اسلایسر-نسخه-۵۱۳-بهبود-عملکرد-بهینه-سازی-و-ارتقای-هوش-مصنوعی) | [🇬🇧 **English**](#-photoslicer-v513-performance-heuristics--core-polish)

---

<div dir="rtl">

# 🚀 فوتو اسلایسر نسخه ۵.۱.۳: بهبود عملکرد، بهینه‌سازی و ارتقای هوش مصنوعی

**نسخه ۵.۱.۳ منتشر شد!** این نسخه شامل ارتقای چشمگیر الگوریتم‌های واترمارک هوشمند، بهینه‌سازی سرعت راه‌اندازی و مصرف حافظه، و استانداردسازی جامع کدهای هسته می‌باشد.

### 🌟 تغییرات جدید (نسخه ۵.۱.۳)

* **⚡ بهینه‌سازی سرعت بارگذاری و حافظه WebView2:** افزودن فلگ‌های بهینه‌سازی موتور کرومیوم جهت کاهش فرآیندهای اضافه پس‌زمینه و کاهش زمان راه‌اندازی اولیه.
* **🖼️ فشرده‌سازی گرافیک لودینگ (Splash Screen):** فشرده‌سازی و کاهش ۸۸.۶٪ حجم تصویر اسپلش برای سرعت بیشتر در باز شدن برنامه.
* **🧠 ارتقای الگوریتم واترمارک و تشخیص حباب گفتگو:**
  * محدودسازی دقیق نفوذ ماسک حباب‌های دیالوگ (Bubble Mask) به نواحی پس‌زمینه.
  * پیش‌محاسبه ستونی میزان سفیدی تصویر (Precomputed Column Whiteness) جهت افزایش سرعت تحلیل.
  * امتیازدهی هوشمند بر پایه روشنایی و کنتراست تصویر برای اولویت‌دادن به کادرهای هنری غنی به جای نواحی سفید خالی یا تاریک.
  * پاداش‌دهی به لبه‌های تمیز و هم‌تراز پنل‌ها و اعمال جریمه در صورت جابجایی ناخواسته از لبه‌های اصلی.
* **🤖 ارتقای ماژول هوش مصنوعی (AI Upscaler):** رد کردن خودکار تصاویر با ارتفاع کم (Short Images) جهت جلوگیری از پردازش غیرضروری و خطاهای احتمالی مدل.
* **📂 بهبود استخراج آرشیوها و مرتب‌سازی فایل‌ها:** مرتب‌سازی طبیعی دقیق‌تر (Natural Sorting) برای فایل‌های استخراج شده از ZIP، CBZ و PDF.
* **💻 استانداردسازی کدها و داکیومنت کامل:** بازنویسی کامل مطابق با استانداردهای PEP 8، رفع خطاهای فرمت‌بندی و مستندسازی انگلیسی ۱۰۰٪ توابع در `main.py` و `engine.py`.

---

# 🚀 فوتو اسلایسر نسخه ۵.۱: حرفه‌ای‌تر از همیشه

**نسخه ۵.۱ منتشر شد!** این آپدیت بزرگ شامل سیستم واترمارک‌گذاری هوشمند با تشخیص حباب‌های گفتگو، خروجی PSD با لایه‌های قابل ویرایش، و بهبودهای گسترده در رابط کاربری می‌باشد.

### 🌟 تغییرات جدید (نسخه ۵.۱)

* **🔍 نادیده‌گرفتن نویزها و ابزارهای حاشیه تصویر:** نادیده‌گرفتن هوشمند اسکرول‌بارها، لبه‌های اسکرین‌شات و نشانگرهای برنامه‌های ریدر هنگام اسکن خطوط برش، جهت تشخیص دقیق فضاهای خالی بین پنل‌ها.
* **🛡️ لایه ایمنی سقف ارتفاع و جلوگیری از خطای `broken data stream`:** محدودسازی خودکار ارتفاع تمام قطعات برش به سقف مجاز فرمت (۶۵,۵۰۰ پیکسل برای JPG) و افزودن حالت Fallback برای تصاویر بدون خط برش جهت جلوگیری از هرگونه خطای ذخیره‌سازی.
* **🖼️ سیستم واترمارک هوشمند:** افزودن سیستم واترمارک‌گذاری آگاه از طرح‌بندی که به طور خودکار مرزهای پنل‌ها را تشخیص می‌دهد.
* **💬 جلوگیری از تداخل با حباب‌های گفتگو:** واترمارک‌ها با استفاده از الگوریتم‌های پیشرفته هرگز روی حباب‌های دیالوگ قرار نمی‌گیرند.
* **📐 اندازه‌گیری با وضوح اصلی PNG:** استفاده از رزولوشن اصلی PNG برای واترمارک‌های شفاف و باکیفیت.
* **📝 الگوی نام‌گذاری پیشرفته:** امکان تعریف تمپلیت‌های دلخواه برای نام فایل‌های خروجی با راهنمای بصری.
* **📂 خروجی PSD لایه‌بندی شده:** خروجی PSD با لایه‌های واترمارک قابل ویرایش در فتوشاپ.
* **⚡ بهبود سرعت واترمارک:** افزایش چشمگیر سرعت عملیات واترمارک‌گذاری.
* **🎨 رفع فلش تم در هنگام راه‌اندازی:** جلوگیری از چشمک زدن تم هنگام اجرای برنامه.
* **🎞️ انیمیشن نام پریست‌ها:** نام پریست‌ها هنگام overflow با انیمیشن نمایش داده می‌شوند.
* **🔧 رفع باگ‌های متعدد:** رفع مشکل پس‌زمینه سیاه در خروجی PSD، رفع باگ تب About Us، رفع مشکل پریست‌ها و موارد دیگر.

---

# 🚀 فوتو اسلایسر نسخه ۵.۰: تحول در طراحی

**نسخه ۵.۰ منتشر شد!** یک تحول بزرگ در رابط کاربری با تمرکز روی شیشه‌ای‌سازی واقعی، درگ‌اند‌دراپ، و بهبودهای اساسی.

### 🌟 تغییرات جدید (نسخه ۵.۰)

* **📂 پشتیبانی از درگ‌اند‌دراپ:** پوشه‌ها را مستقیماً روی برنامه بکشید و رها کنید با انیمیشن drop zone.
* **💎 شیشه‌ای‌سازی واقعی تب‌ها:** تب‌ها با افکت شیشه‌ای واقعی و نشان‌گر لغزنده (sliding glass pill).
* **📊 نوار پیشرفت جمع‌شونده:** نوار پیشرفت فضای کاری با قابلیت جمع شدن خودکار.
* **🔔 دکمه قطع و وصل اعلان:** امکان قطع و وصل صدا و نوتیفیکیشن.
* **🛡️ رفع فریز UI:** رفع مشکل قفل شدن رابط کاربری هنگام بروز خطا.
* **🔄 رفع مشکل Pause در حالت Single:** رفع باگ توقف و ادامه در حالت تکی.
* **📝 بهبود برچسب نوار پیشرفت:** نمایش "Status" در حالت تکی به جای "Current".
* **🔧 رفع همپوشانی منوی Format:** رفع مشکل تداخل منوی کشویی فرمت.
* **✨ بهبود آیکون‌ها:** ممیزی و بهبود تمام آیکون‌های برنامه.

---

# 🚀 فوتو اسلایسر نسخه ۴.۵: قدرت شخصی‌سازی

**نسخه ۴.۵ منتشر شد!** در این نسخه تمرکز ما روی شخصی‌سازی بی‌نظیر برنامه با تم‌های سفارشی، تنظیمات پیشرفته و بهبود تجربه کاربری بوده است.

### 🌟 تغییرات جدید (نسخه ۴.۵)

* **🎨 ویرایشگر تم اختصاصی:** تم دلخواه خود را با چرخه رنگ زنده، شبکه ۱۰×۱۰، و لغزنده اشباع بسازید.
* **🌈 کنتراست تطبیقی:** رنگ‌های متون به طور خودکار با روشنایی تم تنظیم می‌شوند.
* **⚙️ تب تنظیمات:** پنل تنظیمات اختصاصی با قابلیت تعیین محل ذخیره‌سازی.
* **🖼️ بهبود ویرایشگر رنگ:** پیش‌نمایش زنده چرخه رنگ، grid ۱۰×۱۰، و تجربه دو-مداله.
* **✨ شیشه‌ای‌سازی مودال‌ها:** طراحی شیشه‌ای با glow و دکمه‌های حرفه‌ای برای مودال‌ها.
* **📊 نوار پیشرفت جمع‌شونده:** فضای کاری بهینه با قابلیت جمع شدن نوار پیشرفت.
* **🔄 رفع همپوشانی منوها:** رفع مشکل تداخل منوی کشویی Format.
* **🔧 تب About Us بهبودیافته:** کارت‌های شیشه‌ای با هایلایت ویژگی‌ها.
* **🌐 ترجمه‌های فارسی کامل:** اضافه شدن ترجمه‌های از قلم افتاده برای Version و Python.
* **📏 مدیریت محدودیت WEBP:** پشتیبانی از سایز ۱۶۳۸۳ پیکسل در فرمت WebP.
* **🔢 بهینه‌سازی تب‌ها:** تب‌های شیشه‌ای واقعی با نشان‌گر لغزنده.

---

# 🚀 فوتو اسلایسر نسخه ۴.۴: خروجی‌های جدید

**نسخه ۴.۴ منتشر شد!** در این نسخه پشتیبانی از فرمت CBZ، سیستم پریست‌ها و بازطراحی بخش آدرس دایرکتوری اضافه شده است.

### 🌟 تغییرات جدید (نسخه ۴.۴)

* **📚 پشتیبانی از CBZ:** افزودن فرمت خروجی CBZ (Comic Book Zip) برای کتابخانه‌های کمیک.
* **🔄 بازطراحی UI خروجی:** بازطراحی کامل بخش انتخاب فرمت خروجی.
* **💾 سیستم پریست‌ها:** ذخیره و بارگذاری تنظیمات کامل برای استفاده مجدد سریع.
* **⏹️ توقف کامل فرآیند:** افزودن گزینه توقف کامل (Full Stop) برای پردازش.
* **📁 بازطراحی بخش آدرس:** بخش انتخاب دایرکتوری بهبود یافته با طراحی جدید.
* **🔧 رفع باگ WebP:** رفع محدودیت سایز در فرمت WebP.

---

### 📥 دانلود و نصب

فایل **ZIP** آخرین نسخه را از صفحه [Release](https://github.com/esmail-mkh/PhotoSlicer/releases/latest) دانلود کنید، اکسترکت کنید و `PhotoSlicer.exe` را اجرا کنید. لذت ببرید!

</div>

---

# 🚀 PhotoSlicer v5.1.3: Performance, Heuristics & Core Polish

**Version 5.1.3 is here!** This release brings advanced smart watermarking heuristics, WebView2 startup and memory optimizations, AI upscaler enhancements, and complete PEP 8 standardization.

### 🌟 What's New (v5.1.3)

* **⚡ WebView2 Startup & Memory Optimizations:** Configured Chromium optimization arguments to eliminate unnecessary background tasks and reduce initial launch overhead.
* **🖼️ Splash Screen Compression:** Compressed and optimized the splash screen image by 88.6% for snappy application startup.
* **🧠 Advanced Smart Watermark Heuristics:**
  * Constrained speech bubble mask propagation to prevent background leakage.
  * Precomputed column whiteness profiles for fast layout and gutter analysis.
  * Contrast-aware brightness scoring prioritizing rich artwork boundaries over empty white backgrounds or murky shadows.
  * Panel edge alignment rewards and displacement penalties ensuring clean placement along panel corners.
* **🤖 AI Upscaler Improvements:** Automatically bypasses short images (below minimum height threshold) during AI enhancement to prevent errors and wasted GPU/CPU cycles.
* **📂 Natural Sorting & Archive Handling:** Enhanced natural sorting order for extracted images from ZIP, CBZ, and PDF containers.
* **💻 PEP 8 & Full Codebase Documentation:** 100% comprehensive English docstrings, clean formatting, and PEP 8 compliance across `main.py` and `engine.py`.

---

# 🚀 PhotoSlicer v5.1: More Professional Than Ever

**Version 5.1 is here!** This major update brings a smart watermarking system with speech bubble detection, layered PSD export with editable watermark layers, and extensive UI/UX improvements.

### 🌟 What's New (v5.1)

* **🔍 Margin Edge Artifact Ignoring:** Smartly ignores side margin artifacts such as scrollbars, screenshot UI indicators, or edge borders during cut-point scanning to ensure clean panel gap detection.
* **🛡️ Robust Slice Capping & Stream Error Fix:** Automatically enforces slice height capping for all export formats (including JPEG's 65,500px dimension limit) with an even-cut fallback mode, completely eliminating `broken data stream` exceptions on ultra-tall images.
* **🖼️ Smart Watermarking System:** Added a layout-aware watermarking system that automatically detects panel borders and gutters.
* **💬 Speech Bubble Avoidance:** Watermarks are intelligently placed to never overlap with dialogue bubbles using advanced detection algorithms.
* **📐 Native PNG Resolution:** Uses original PNG resolution for crisp, high-quality watermark rendering.
* **📝 Advanced Filename Patterning:** Custom filename templates with a visual guide for organized output.
* **📂 Layered PSD Export:** PSD output with editable watermark layers for professional editing in Photoshop.
* **⚡ Watermark Speed Boost:** Significant performance improvements in watermark processing.
* **🎨 Theme Startup Flash Fix:** Prevent theme flash when launching the application.
* **🎞️ Animated Preset Names:** Preset names animate on hover when they overflow, improving readability.
* **🔧 Multiple Bug Fixes:** Fixed PSD black background issue, About Us tab loading bug, preset preservation issue, and more.

---

# 🚀 PhotoSlicer v5.0: A Design Revolution

**Version 5.0 is here!** A major UI overhaul focusing on true glassmorphism, drag-and-drop support, and fundamental improvements.

### 🌟 What's New (v5.0)

* **📂 Drag & Drop Support:** Drag and drop folders directly onto the app with an animated drop zone.
* **💎 Real Glassmorphism Tabs:** Tabs with real glass effect and a sliding glass pill indicator.
* **📊 Collapsible Progress Bar:** Workspace progress bar with auto-collapse animation.
* **🔔 Notification Toggle:** Toggle sound and notifications on/off.
* **🛡️ UI Freeze Fix:** Fixed interface freezing when errors occur during processing.
* **🔄 Single-Mode Pause Fix:** Fixed pause/resume functionality in single-folder mode.
* **📝 Progress Bar Label Fix:** Shows "Status" instead of "Current" in single-folder mode.
* **🔧 Format Dropdown Overlap Fix:** Fixed dropdown menu overlap issues.
* **✨ Icon Audit:** Comprehensive review and improvement of all application icons.

---

# 🚀 PhotoSlicer v4.5: Ultimate Customization

**Version 4.5 is here!** This release focuses on unparalleled customization with custom themes, advanced settings, and UX improvements.

### 🌟 What's New (v4.5)

* **🎨 Custom Theme Editor:** Create your own theme with a live color wheel, 10x10 grid, and saturation slider.
* **🌈 Adaptive Contrast:** Foreground colors automatically adjust based on theme brightness for readability.
* **⚙️ Settings Tab:** Dedicated settings panel with configurable save location.
* **🖼️ Improved Color Picker:** Live wheel preview, 10x10 grid, and dual-modal experience.
* **✨ Glassmorphism Modal UI:** Professional glass design with glows and refined buttons.
* **📊 Collapsible Progress Bar:** Optimized workspace with collapsible progress bar.
* **🔄 Dropdown Overlap Fix:** Fixed format dropdown menu overlap issues.
* **🔧 Enhanced About Us Tab:** Glassmorphism cards with feature highlights.
* **🌐 Complete Persian Translations:** Added missing translations for Version and Python labels.
* **📏 WebP Dimension Handling:** Support for WebP's 16383px dimension limit.
* **🔢 Sliding Glass Tabs:** Real glassmorphism tabs with sliding pill indicator.

---

# 🚀 PhotoSlicer v4.4: New Export Formats

**Version 4.4 is here!** This update adds CBZ format support, a preset system, and a revamped directory address section.

### 🌟 What's New (v4.4)

* **📚 CBZ Support:** Added CBZ (Comic Book Zip) output format for comic libraries.
* **🔄 Export UI Revamp:** Complete redesign of the export format selection UI.
* **💾 Preset System:** Save and load entire configurations for quick reuse.
* **⏹️ Full Stop Process:** Added option to fully stop the processing mid-operation.
* **📁 Directory Address Redesign:** Improved folder selection with new design layout.
* **🔧 WebP Bug Fix:** Fixed dimension limit handling for WebP format.

---

### 📥 Installation

Download the latest **ZIP** file from the [Release page](https://github.com/esmail-mkh/PhotoSlicer/releases/latest), extract it, and run `PhotoSlicer.exe`. Enjoy!
