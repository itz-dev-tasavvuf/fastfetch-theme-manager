<div align="center">

# 🌈 Fastfetch Theme Manager

### *Professional CLI Theme Management for Fastfetch*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-brightgreen.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager)
[![AUR version](https://img.shields.io/aur/version/fastfetch-theme-manager?logo=arch-linux)](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager)

**Created by** [Tasavvuf Gori](https://github.com/itz-dev-tasavvuf) *(itz-dev-tasavvuf)*

---

A professional, **zero-dependency** CLI tool to build, manage, and preview Fastfetch themes with an interactive wizard, crash protection, and smart distro detection.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Contributing](CONTRIBUTING.md) • [License](#-license)

</div>

---

## 🚀 Features

<table>
<tr>
<td width="50%">

### ✨ Interactive Theme Builder
Create custom themes step-by-step with a visual wizard. Choose logos, borders, and colors without writing any code.

### 🛡️ Smart Safety System
Automatic config backups before changes. Auto-reverts if a theme crashes Fastfetch.

### ⚡ Zero Dependencies
Pure Python 3 using only the standard library. No `pip install` required.

</td>
<td width="50%">

### 📂 Universal Presets
Intelligently detects system presets, official examples, and user themes across all major distributions.

### 🔍 TUI Picker
Fuzzy-find themes with live previews using `fzf` integration.

### 📦 One-Line Installer
Auto-detects package managers (apt, pacman, dnf, apk, brew) and suggests missing dependencies.

</td>
</tr>
</table>

---

## 📸 Demo

### 🛠️ Interactive Theme Builder
```bash
ftm build
```
*Build themes through an intuitive wizard interface*
<img width="1915" height="791" alt="Screenshot From 2025-12-07 16-32-35" src="https://github.com/user-attachments/assets/998c59ca-d271-48bc-a46f-5d7db3105052" />
<img width="1915" height="832" alt="Screenshot From 2025-12-07 16-33-02" src="https://github.com/user-attachments/assets/0fff8ca6-8392-495e-b872-49930f0e671a" />
<img width="1915" height="557" alt="Screenshot From 2025-12-07 16-33-17" src="https://github.com/user-attachments/assets/5ac35dfc-969a-4fff-b834-0821a08b401d" />




### 🎯 FZF Picker
```bash
ftm pick
```
*Live preview and selection with arrow key navigation*
<img width="1920" height="1080" alt="Screenshot From 2025-12-07 16-33-49" src="https://github.com/user-attachments/assets/8bd204bb-92c0-48a2-b379-5705473f5cb7" />


### 📂 Theme List
```bash
ftm list
```
*Smart detection of system and user themes*


---

## 💾 Installation

### Option 1: One-Line Install *(Recommended)*

This script automatically detects your shell, installs FTM, and checks for dependencies:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/itz-dev-tasavvuf/fastfetch-theme-manager/main/install.sh)
```

### Option 2: Manual Install

```bash
# Clone the repository
git clone https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager.git
cd fastfetch-theme-manager

# Run the installer
chmod +x install.sh
./install.sh
```

> **Note:** Ensure `~/.local/bin` is in your `$PATH`

---

## 📖 Usage

### 1️⃣ Build a New Theme

Create a theme from scratch using the interactive wizard:

```bash
ftm build
```

### 2️⃣ Pick a Theme Visually

Browse and preview themes instantly with arrow keys:

```bash
ftm pick
```

### 3️⃣ Manage Themes

```bash
# List all detected themes
ftm list

# Set a specific theme (by name or path)
ftm set neofetch
ftm set my-custom-theme

# Reset to default configuration
ftm reset
```

### 4️⃣ Download Community Packs

Pull curated themes directly from GitHub (no git/pip needed):

```bash
ftm pull
```

---

## 🔧 Requirements

| Requirement | Status | Notes |
|------------|--------|-------|
| **Python 3.6+** | ✅ Required | Pre-installed on most Linux systems |
| **Fastfetch** | ✅ Required | The core program being themed |
| **fzf** | ⭐ Optional | Highly recommended for `ftm pick` |

> The installer automatically detects missing tools and suggests the correct installation command for your OS (Pacman, Apt, Dnf, Brew, etc.)

---

## 🌐 Supported Platforms

<div align="center">

| **Operating System** | **Support Status** |
|---------------------|-------------------|
| 🐧 Arch Linux | ✅ Full Support |
| 🐧 Debian/Ubuntu | ✅ Full Support |
| 🐧 Fedora/RHEL | ✅ Full Support |
| 🐧 Alpine Linux | ✅ Full Support |
| 🐧 Void Linux | ✅ Full Support |
| 🍎 macOS | ✅ Full Support |

</div>

---

## 🤝 Contributing

We welcome contributions! Whether you're reporting bugs, suggesting features, or submitting code, please check out our [Contributing Guidelines](CONTRIBUTING.md).

**Quick Links:**
- 🐛 [Report a Bug](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues)
- 💡 [Request a Feature](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues)
- 🎨 [Submit a Theme](CONTRIBUTING.md#3-submitting-themes)
- 💻 [Code Contribution Guide](CONTRIBUTING.md#4-code-contributions)

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for full details.

---

<div align="center">

### ⭐ If you find FTM useful, consider giving it a star!

**Made with ❤️ by [Tasavvuf Gori](https://github.com/itz-dev-tasavvuf)**

[Report Issue](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues) • [Request Feature](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues) • [View Discussions](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/discussions)

</div>
