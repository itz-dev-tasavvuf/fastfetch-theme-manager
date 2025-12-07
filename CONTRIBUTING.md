<div align="center">

# 🤝 Contributing to Fastfetch Theme Manager

### *Help Make FTM Even Better!*

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Contributors](https://img.shields.io/github/contributors/itz-dev-tasavvuf/fastfetch-theme-manager)](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/graphs/contributors)

First off, **thank you** for considering contributing to FTM! It's people like you that make open source tools great. 🎉

[Report Bugs](#1-reporting-bugs-) • [Suggest Features](#2-suggesting-enhancements-) • [Submit Themes](#3-submitting-themes-) • [Code Guidelines](#4-code-contributions-)

</div>

---

## 🛠️ How Can I Contribute?

### 1. Reporting Bugs 🐛

Found a bug? Help us squash it!

**Before Submitting:**
- 🔍 Search [existing issues](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues) to avoid duplicates
- ✅ Verify you're using the latest version of FTM

**What to Include:**
```markdown
**Environment:**
- OS/Distro: (e.g., Arch Linux, Ubuntu 22.04, macOS 14)
- Python Version: (run `python3 --version`)
- Fastfetch Version: (run `fastfetch --version`)

**Issue Description:**
(Clear description of what went wrong)

**Steps to Reproduce:**
1. Run `ftm <command>`
2. Expected behavior vs. actual behavior

**Error Output:**
```
(Paste any error messages or logs)
```
```

[**Create Bug Report →**](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues/new)

---

### 2. Suggesting Enhancements 💡

Have an idea to make FTM better?

**Guidelines:**
- 🎯 Be specific about the feature and its use case
- 🧐 Explain *why* this would be valuable to users
- 📸 Include mockups or examples if applicable

**Template:**
```markdown
**Feature Name:** (e.g., Theme Export/Import)

**Problem it Solves:**
(What pain point does this address?)

**Proposed Solution:**
(How should this work?)

**Alternatives Considered:**
(Any other approaches?)
```

[**Suggest Feature →**](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues/new?labels=enhancement)

---

### 3. Submitting Themes 🎨

We love seeing creative configurations!

#### **Theme Checklist:**

- [ ] Theme is saved as a `.jsonc` file
- [ ] Tested with the latest Fastfetch version
- [ ] No absolute paths (e.g., `/home/yourname/Pictures/logo.png`)
- [ ] Uses relative paths or standard system icons
- [ ] Includes a brief description/comment at the top

#### **How to Submit:**

**Option A: Pull Request**
```bash
# Fork the repo, then:
git clone https://github.com/YOUR_USERNAME/fastfetch-theme-manager.git
cd fastfetch-theme-manager

# Add your theme
mkdir -p themes/
cp your-theme.jsonc themes/

# Create PR
git checkout -b theme/your-theme-name
git add themes/your-theme.jsonc
git commit -m "feat: Add your-theme-name theme"
git push origin theme/your-theme-name
```

**Option B: Share in Discussions**

Post in [GitHub Discussions](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/discussions) if you prefer a simpler approach.

---

### 4. Code Contributions 💻

Want to improve the core tool? Awesome! Let's keep FTM lightweight and robust.

## ⚠️ The Golden Rule: **Zero Dependencies**

FTM runs on **any** Linux system with Python 3 installed.

<div align="center">

### ❌ DO NOT USE
```python
import requests  # NO
import rich      # NO
import click     # NO
```

### ✅ USE INSTEAD
```python
import urllib.request  # YES
import subprocess      # YES
import json            # YES
```

</div>

> **Why?** To avoid forcing users to run `pip install`, ensuring FTM works out-of-the-box everywhere.

---

## 📋 Coding Standards

### **1. Type Hinting**
Use Python type hints for clarity:

```python
from typing import List, Optional

def get_themes(directory: str) -> List[str]:
    """Returns list of theme files in directory."""
    pass

def find_config(name: Optional[str] = None) -> Optional[str]:
    """Finds config by name, returns path or None."""
    pass
```

### **2. Error Handling**
Never let the program crash with a raw traceback:

```python
# ❌ BAD
file_content = open('/some/path').read()

# ✅ GOOD
try:
    with open('/some/path', 'r') as f:
        file_content = f.read()
except FileNotFoundError:
    print(f"{Style.ERROR}File not found: /some/path")
    return None
except Exception as e:
    print(f"{Style.ERROR}Unexpected error: {e}")
    return None
```

### **3. Cross-Platform Compatibility**
Avoid hardcoded paths:

```python
# ❌ BAD
fastfetch_path = "/usr/bin/fastfetch"

# ✅ GOOD
import shutil
fastfetch_path = shutil.which("fastfetch")
if not fastfetch_path:
    print(f"{Style.ERROR}Fastfetch not found in PATH")
```

---

## 🚀 Development Workflow

### **Step 1: Fork & Clone**
```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/fastfetch-theme-manager.git
cd fastfetch-theme-manager
```

### **Step 2: Create a Branch**
```bash
git checkout -b feature/amazing-new-feature
```

### **Step 3: Make Changes**
Edit `ftm.py` or other files as needed.

### **Step 4: Test Your Changes**
```bash
# Run basic commands
./ftm.py list
./ftm.py build
./ftm.py reset

# Verify error handling
./ftm.py set nonexistent-theme  # Should fail gracefully
```

### **Step 5: Commit & Push**
```bash
# Use clear, descriptive messages
git add .
git commit -m "feat: Add support for NixOS package manager"
git push origin feature/amazing-new-feature
```

### **Step 6: Open a Pull Request**
Go to your fork on GitHub and click **"New Pull Request"**

---

## 🧪 Testing Checklist

Before submitting a PR, verify:

- [ ] `ftm.py` runs without installing any pip packages
- [ ] `install.sh` script still works correctly
- [ ] All potential errors are handled gracefully
- [ ] Code follows the standards above
- [ ] No hardcoded paths or dependencies
- [ ] Tested on at least one Linux distribution

---

## 🎯 Commit Message Guidelines

Follow these conventions for clarity:

| Prefix | Usage |
|--------|-------|
| `feat:` | New feature (e.g., `feat: Add fzf picker integration`) |
| `fix:` | Bug fix (e.g., `fix: Resolve crash on missing config`) |
| `docs:` | Documentation only (e.g., `docs: Update README examples`) |
| `style:` | Code formatting (e.g., `style: Apply PEP 8 formatting`) |
| `refactor:` | Code restructuring (e.g., `refactor: Simplify theme detection`) |
| `test:` | Adding tests (e.g., `test: Add unit tests for parser`) |

---

## 💬 Questions?

- 💡 Not sure where to start? Check [existing issues](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/issues) labeled `good first issue`
- 🗨️ Have questions? Ask in [Discussions](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/discussions)
- 📧 Need help? Open an issue with the `question` label

---

<div align="center">

### 🌟 Thank You for Making FTM Better!

**Every contribution, no matter how small, makes a difference.**

[View Contributors](https://github.com/itz-dev-tasavvuf/fastfetch-theme-manager/graphs/contributors) • [Code of Conduct](CODE_OF_CONDUCT.md)

</div>