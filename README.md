[🇮🇷 **Read in Persian (فارسی)**](README-fa.md)
# 📸 PhotoSlicer v4.2
### The Ultimate Manhwa & Webtoon Processing Tool

[![Version](https://img.shields.io/github/v/release/esmail-mkh/PhotoSlicer?label=Version&color=blue)](https://github.com/esmail-mkh/PhotoSlicer/releases/latest)
[![Download](https://img.shields.io/github/downloads/esmail-mkh/PhotoSlicer/total?label=Downloads)](https://github.com/esmail-mkh/PhotoSlicer/releases/latest)
[![Stars](https://img.shields.io/github/stars/esmail-mkh/PhotoSlicer?style=flat&label=Stars&color=tomato)](https://github.com/esmail-mkh/PhotoSlicer)
![Platform](https://img.shields.io/badge/platform-Windows-informational?logo=windows)
![License](https://img.shields.io/badge/license-MIT-green)

<p align="left">
  <img src="assets/app-v4-image.jpg" alt="PhotoSlicer Interface" width="400">
</p>

**PhotoSlicer** is a blazing-fast, aesthetically stunning, and feature-rich application designed specifically for **Webtoon, Manhwa, and Manga translators/editors**. It automates the tedious process of stitching images together, resizing them, improving quality via AI, and intelligently slicing them back into web-friendly chunks without cutting through dialogue bubbles.

---

## ✨ Key Features

### 🚀 Core Capabilities
*   **Smart Stitching:** Seamlessly merges multiple image files into long strips.
*   **Content-Aware Slicing:** Uses an intelligent algorithm (`Comparison Detector`) to find safe cutting points (whitespaces/gaps), ensuring text bubbles and artwork are never split in half.
*   **AI Enhancement:** Integrated support for **Real-ESRGAN** to upscale and denoise low-quality images before processing.
*   **Format Mastery:** Supports input from **JPG, PNG, WEBP, AVIF,** and even **PSD** files.
*   **Multi-language English and Farsi
*   **Multi-Mode Processing:**
    *   **Single Mode:** Process one chapter/folder instantly.
    *   **Batch Mode:** Point to a root directory and process dozens of chapters automatically.

### 🎨 Stunning UI & UX
*   **Neon Aurora Design:** A modern, glassmorphism-based interface with animated backgrounds.
*   **6 Color Themes:** Switch between Cyber Blue, Electric Purple, Ruby Red, Sunset Orange, Luxury Gold, and Neo Emerald instantly.
*   **Interactive Elements:** animated logos, smooth transitions, and sound alerts upon completion.
*   **Control Center:** Pause and Resume large batch operations at any time.

### 🛠️ Power User Tools
*   **Custom Resizing:** High-quality Bicubic resizing to your target width (e.g., 800px standard).
*   **Export Options:**
    *   Save as **JPG, PNG, or WEBP**.
    *   Auto-archive into **ZIP** files.
    *   Generate long-strip **PDFs** for easy reading.
*   **Performance:** Multi-threaded architecture for lightning-fast resizing and slicing.

---

## 📥 Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/esmail-mkh/PhotoSlicer.git
    cd PhotoSlicer
    ```

2.  **Install Dependencies:**
    Ensure you have Python 3.8+ installed.
    ```bash
    pip install -r requirements.txt
    ```
    *Required libs based on code: `pywebview`, `Pillow`, `pillow-heif`, `psd-tools`, `numpy`.*

3.  **Run the App:**
    ```bash
    python main.py
    ```

---

## 🎮 How to Use

1.  **Select Source:** Click the folder icon to choose your directory.
    *   *If the folder contains images:* Single Mode is activated.
    *   *If the folder contains sub-folders:* Multi/Batch Mode is activated.
2.  **Configure Settings:**
    *   **Width:** Set your target width (default: 800px).
    *   **Height Limit:** Maximum height for a single slice (default: 15000px).
    *   **Quality:** JPG/WebP compression quality (1-100).
    *   **Format:** Choose your output format.
3.  **Advanced Options:**
    *   Toggle **AI Enhance** for upscaling.
    *   Check **ZIP** or **PDF** if you want packaged outputs.
4.  **Initiate:** Click the **ROCKET** button to start.
    *   You can **Pause/Resume** the process if needed.
    *   A sound will play when the job is done.

---

## 🖼️ Themes

Customize your experience with built-in themes:
| Theme | Description |
| :--- | :--- |
| 🔵 **Blue** | Default Cyberpunk look |
| 🟣 **Purple** | Vaporwave aesthetic |
| 🔴 **Ruby** | Aggressive & Bold |
| 🟠 **Sunset** | Warm & Cozy |
| 🟡 **Gold** | Premium feel |
| 🟢 **Emerald** | Matrix vibes |

---

## 🧩 Tech Stack

*   **Backend:** Python (Pillow, NumPy, ThreadPoolExecutor)
*   **GUI:** PyWebView (Edge Chromium engine)
*   **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
*   **AI Engine:** Real-ESRGAN (NCNN Vulkan)

---

## ☕ Support Me

If you find this tool useful, you can support development by buying me a coffee!

<a href="https://daramet.com/esmailmkh"><img class="img-fluid" src="https://panel.daramet.com/static/media/daramet-pizza-donate.8ecef99d74658fec0caf.png" width="300" height="100/" /></a>
<a href="https://coffeebede.com/esmailmkh"><img class="img-fluid" src="https://coffeebede.ir/DashboardTemplateV2/app-assets/images/banner/default-yellow.svg" width="300" height="100/" /></a>

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.
Created with ❤️ by **E.MKH**.
