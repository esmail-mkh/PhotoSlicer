[🇮🇷 **Read in Persian (فارسی)**](README-fa.md)

# 📸 PhotoSlicer v5.1
### The Ultimate Manhwa & Webtoon Processing Tool

[![Version](https://img.shields.io/github/v/release/esmail-mkh/PhotoSlicer?label=Version&color=blue)](https://github.com/esmail-mkh/PhotoSlicer/releases/latest)
[![Download](https://img.shields.io/github/downloads/esmail-mkh/PhotoSlicer/total?label=Downloads&color=success)](https://github.com/esmail-mkh/PhotoSlicer/releases/latest)
[![Stars](https://img.shields.io/github/stars/esmail-mkh/PhotoSlicer?style=flat&label=Stars&color=tomato)](https://github.com/esmail-mkh/PhotoSlicer)
[![Platform](https://img.shields.io/badge/platform-Windows-informational?logo=windows&color=blue)](<#-installation>)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

<p align="left">
  <img src="assets/app-v5.1-fa-image.jpg" alt="PhotoSlicer v5.1 Interface" width="400">
</p>

**PhotoSlicer** is a blazing-fast, aesthetically stunning, and feature-rich application designed specifically for **Webtoon, Manhwa, and Manga translators/editors**. It automates the tedious process of stitching images together, resizing them, improving quality via AI, intelligently slicing them back into web-friendly chunks without cutting through dialogue bubbles, and adding **smart watermarks** with content-aware bubble avoidance.

---

## 📑 Table of Contents

* [✨ Key Features](#-key-features)
* [🚀 Core Capabilities](#-core-capabilities)
* [🖼️ Smart Watermarking System](#-smart-watermarking-system)
* [🎨 Stunning UI & UX](#-stunning-ui--ux)
* [🛠️ Power User Tools](#-power-user-tools)
* [⚡ Quick Start](#-quick-start)
* [📥 Installation](#-installation)
* [🎮 How to Use](#-how-to-use)
* [📸 Watermarking Guide](#-watermarking-guide)
* [🎨 Presets](#-presets)
* [🖼️ Themes](#-themes)
* [🧩 Tech Stack](#-tech-stack)
* [☕ Support Me](#-support-me)
* [🤝 Contributing](#-contributing)

---

## ✨ Key Features

### 🚀 Core Capabilities

* **Smart Stitching:** Seamlessly merges multiple image files into long strips.
* **Content-Aware Slicing:** Uses an intelligent algorithm (`Comparison Detector`) to find safe cutting points (whitespaces/gaps), ensuring text bubbles and artwork are never split in half.
* **AI Enhancement:** Integrated support for **Real-ESRGAN** to upscale and denoise low-quality images before processing.
* **Format Mastery:** Supports input from **JPG, PNG, WEBP, AVIF,** and even **PSD** files.
* **Multi-language:** Fully supports **English** and **Farsi (Persian)** interfaces.
* **Multi-Mode Processing:**
  * **Single Mode:** Process one chapter/folder instantly.
  * **Batch Mode:** Point to a root directory and process dozens of chapters automatically.

### 🖼️ Smart Watermarking System

* **Layout-Aware Placement:** Automatically detects panel borders and gutters to place watermarks intelligently.
* **Bubble Avoidance:** Uses advanced algorithms to detect speech bubbles and ensure watermarks never overlap with dialogue.
* **Custom Watermark Support:** Add your own PNG watermark with configurable opacity, size, and positioning.
* **Progress Tracking:** Dedicated progress step for watermark operations with real-time feedback.
* **Native PNG Dimensions:** Uses original PNG resolution for crisp, high-quality watermark rendering.
* **Speed Optimized:** Multi-threaded watermark processing for lightning-fast performance.

### 🎨 Stunning UI & UX

* **Neon Aurora Design:** A modern, glassmorphism-based interface with animated backgrounds.
* **6 Color Themes:** Switch between Cyber Blue, Electric Purple, Ruby Red, Sunset Orange, Luxury Gold, and Neo Emerald instantly.
* **Custom Theme Editor:** Create your own theme with the built-in color picker featuring a color wheel, live preview, saturation slider, and 10×10 color grid.
* **Adaptive Contrast:** Foreground colors automatically adjust based on theme brightness for optimal readability.
* **Settings Tab:** Configurable save location, presets management, and advanced options in a dedicated settings panel.
* **Drag & Drop Support:** Drag and drop folders directly onto the app with an animated drop zone.
* **Advanced Filename Patterning:** Custom filename templates with a visual guide for organized output.
* **Interactive Elements:** Animated logos, glassmorphism tabs with sliding pill indicator, smooth transitions, and sound alerts upon completion.
* **Notification Toggle:** Easily enable or disable sound and visual notifications during processing.
* **Collapsible Progress Bar:** The workspace progress bar auto-collapses to save space when not needed.
* **Control Center:** Pause and Resume large batch operations at any time.

### 🛠️ Power User Tools

* **Custom Resizing:** High-quality Bicubic resizing to your target width (e.g., 800px standard).
* **Export Options:**
  * Save as **JPG, PNG, WEBP, PSD or CBZ**.
  * Custom layered **PSD** export with editable watermark layers.
  * Auto-archive into **ZIP** files.
  * Generate long-strip **PDFs** for easy reading.
* **Presets:** Save and load entire configurations (format, quality, width, etc.) for quick reuse.
* **Performance:** Multi-threaded architecture for lightning-fast resizing, slicing, and watermarking.

---

## ⚡ Quick Start

**Try it now in 3 commands:**

```bash
git clone https://github.com/esmail-mkh/PhotoSlicer.git
cd PhotoSlicer
pip install -r requirements.txt && python main.py
```

> 💡 **Prefer a standalone EXE?** Download the latest compiled release from the [Releases page](https://github.com/esmail-mkh/PhotoSlicer/releases/latest) — no Python setup required!

---

## 📥 Installation

### Option 1: Run from Source (Recommended for development)

| Requirement | Version |
|:---|---:|
| Python | 3.8+ |
| pip | Latest |
| OS | Windows 10 / 11 |

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/esmail-mkh/PhotoSlicer.git
   cd PhotoSlicer
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Key libraries: `pywebview`, `Pillow`, `pillow-heif`, `psd-tools`, `numpy`*

3. **Run the App:**
   ```bash
   python main.py
   ```

### Option 2: Standalone EXE (Recommended for end users)

Download the latest `PhotoSlicer-v5.1.zip` from the [Releases page](https://github.com/esmail-mkh/PhotoSlicer/releases/latest), extract it, and run `PhotoSlicer.exe` directly.

---

## 🎮 How to Use

### 1️⃣ Select Source
Click the folder icon to choose your directory.

* **If the folder contains images:** **Single Mode** is activated.
* **If the folder contains sub-folders:** **Batch Mode** is activated (processes all sub-folders one by one).

### 2️⃣ Configure Settings

| Setting | Description | Default |
|:---|:---|---:|
| **Width** | Target width for output images (in pixels) | `800` |
| **Height Limit** | Maximum height of a single slice (in pixels) | `15000` |
| **Quality** | JPG/WebP compression quality (1–100) | `95` |
| **Format** | Output image format | `WEBP` |

### 3️⃣ Advanced Options

* **AI Enhance** — Toggle **Real-ESRGAN** upscaling for low-quality source images.
* **ZIP** — Auto-archive all outputs into a ZIP file.
* **PDF** — Generate a long-strip PDF for easy reading.
* **Presets** — Load a saved configuration with one click (see [Presets](#-presets) below).
* **Watermark** — Enable smart watermarking (see [Watermarking Guide](#-watermarking-guide) below).

### 4️⃣ Initiate!
Click the **🚀 ROCKET** button to start processing.

* **Pause/Resume** — Use the control center to pause or resume the operation at any time.
* **Notifications** — A sound alert plays when the job is complete.

---

## 📸 Watermarking Guide

PhotoSlicer v5.1 introduces a powerful **Smart Watermarking System**. To use it:

1. **Prepare your watermark:** Use a **PNG file with transparency** (e.g., a logo or signature).
2. **Enable watermarking:** In the settings panel, toggle the **Watermark** option.
3. **Select your watermark file:** Click the watermark path input to browse and select your PNG file.
4. **Configure placement:**
   * **Opacity:** Adjust transparency level.
   * **Size:** Scale the watermark relative to the panel.
   * **Position:** Choose placement (center, corners, or auto).
5. **Let AI handle the rest:** The engine automatically:
   * Detects panel borders and gutters.
   * Avoids speech bubbles and dialogue areas.
   * Places watermarks intelligently without ruining the artwork.
6. **For PSD output:** Watermarks are saved as **editable layers** in Photoshop, allowing further adjustments.

---

## 🎨 Presets

Save time by creating **presets** — reusable configurations that store all your settings:

| Preset Feature | Description |
|:---|---:|
| **Save** | Store Width, Height Limit, Quality, Format, and advanced options in a named preset |
| **Load** | Restore any saved preset with a single click |
| **Hover Preview** | Hover over a preset name to see a tooltip of its configuration |
| **Auto-Manage** | Presets persist between app restarts |

To save a preset: Configure your settings → Click **Save Preset** → Give it a name.

---

## 🖼️ Themes

Customize your experience with built-in themes — or create your own!

### Default Themes

| Theme | Description |
|:---:|:---|
| 🔵 **Blue** | Default Cyberpunk look |
| 🟣 **Purple** | Vaporwave aesthetic |
| 🔴 **Ruby** | Aggressive & Bold |
| 🟠 **Sunset** | Warm & Cozy |
| 🟡 **Gold** | Premium feel |
| 🟢 **Emerald** | Matrix vibes |

### Custom Theme Editor

Go to the **Settings** tab → **Theme** section to access the built-in theme editor:

* **Color Wheel** — Pick any hue visually.
* **Saturation Slider** — Fine-tune color intensity.
* **10×10 Color Grid** — Quick pick from a curated palette.
* **Live Preview** — Changes reflect instantly on the interface.
* **Adaptive Contrast** — Text colors automatically adjust for readability, no matter how bright or dark your custom theme is.

---

## 🧩 Tech Stack

| Layer | Technology |
|:---|---:|
| **Backend** | Python (Pillow, NumPy, psd-tools, ThreadPoolExecutor) |
| **GUI** | PyWebView (Edge Chromium engine) |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JavaScript |
| **AI Engine** | Real-ESRGAN (NCNN Vulkan) |

---

## ☕ Support Me

If you find this tool useful, consider supporting its development!

<a href="https://daramet.com/esmailmkh"><img src="https://panel.daramet.com/static/media/daramet-pizza-donate.8ecef99d74658fec0caf.png" width="300" height="100" /></a>
<a href="https://coffeebede.com/esmailmkh"><img src="https://coffeebede.ir/DashboardTemplateV2/app-assets/images/banner/default-yellow.svg" width="300" height="100" /></a>

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

* 🐛 **Report bugs** by opening an [Issue](https://github.com/esmail-mkh/PhotoSlicer/issues)
* 💡 **Suggest features** via Issues or Discussions
* 🔧 **Submit a Pull Request** with improvements

Created with ❤️ by **E.MKH**.
