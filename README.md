# 🌈 Fastfetch Theme Manager
#### by Tasavvuf Gori (itz-dev-tasavvuf)

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

A **beautiful, emoji-styled** CLI tool to **preview**, **toggle**, **pick**, **download**, and **manage** Fastfetch themes.

---

## 🚀 Features

- **Built-in Theme Gallery**: Local presets, official examples, and custom user themes.
- **TUI Picker**: Fuzzy-finder with `fzf` for instant theme previews.
- **Toggle Mode**: Quickly navigate themes with `n`/`p`, preview, and set.
- **Theme Downloader**: Pull community packs from GitHub.
- **One-Line Installer**: Easy install via `install.sh`.

---

## 📸 Demo

### Toggle Mode

![](assets/demo-toggle.gif)

### FZF Picker

![](assets/demo-picker.png)

### List Table

![](assets/demo-list.png)

### Theme Preview

![](assets/demo-preview.png)

---

## 💾 Installation

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/itz-dev-tasavvuf/fastfetch-theme-manager/main/install.sh)
```

Ensure `~/.local/bin` is in your `$PATH`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## 📖 Usage

```bash
# List available themes
ftm list

# Preview a theme (by name or index)
ftm preview neofetch
ftm preview 0

# Set a theme as default
ftm set nord

# Toggle mode
ftm toggle

# FZF picker
ftm pick
ftm pick --apply

# Add a local theme
ftm add ~/Downloads/mytheme.jsonc --name mytheme

# Pull community packs
ftm pull --repo itz-dev-tasavvuf/fastfetch-theme-manager --path themes
```

---

## 🎨 Community Theme Packs

5 curated packs included under `/themes`:

- **Nord**
- **Catppuccin**
- **Teal Minimal**
- **Neon Cyber**
- **Black Terminal**

Import them with:
```bash
ftm pull --repo itz-dev-tasavvuf/fastfetch-theme-manager --path themes
```

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on theme submissions, bug reports, and enhancements.

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
