#!/usr/bin/env python3
# =============================================================
# 🌈 Fastfetch Theme Manager (FTM) — Professional Edition
# A robust, dependency-free manager and builder for Fastfetch.
#
# Author: Tasavvuf Gori
# License: MIT
# =============================================================

import argparse
import os
import shutil
import subprocess
import sys
import json
import urllib.request
import urllib.error
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any

# --- Configuration Constants ---
APP_NAME = "Fastfetch Theme Manager"
VERSION = "2.0.0"
CONFIG_DIR = Path.home() / ".config/fastfetch"
CONFIG_FILE = CONFIG_DIR / "config.jsonc"
USER_THEMES_DIR = Path.home() / ".local/share/fastfetch/themes"
BACKUP_DIR = Path.home() / ".local/share/fastfetch/backups"

# --- ANSI Colors & Styles ---
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    HEADER = "\033[44;37m"  # Blue background, white text

    @staticmethod
    def print_header(text: str):
        print(f"\n{Style.HEADER}  {text.center(60)}  {Style.RESET}\n")

    @staticmethod
    def success(text: str):
        print(f"{Style.GREEN}✔ {text}{Style.RESET}")

    @staticmethod
    def error(text: str):
        print(f"{Style.RED}✖ {text}{Style.RESET}")

    @staticmethod
    def info(text: str):
        print(f"{Style.BLUE}ℹ {text}{Style.RESET}")

    @staticmethod
    def warning(text: str):
        print(f"{Style.YELLOW}⚠ {text}{Style.RESET}")

@dataclass
class ThemeEntry:
    key: str
    origin: str
    path: Optional[Path]

# =============================================================
# 🛠️ UTILITIES & SAFETY
# =============================================================

def ensure_dirs():
    """Creates necessary directories safely."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        USER_THEMES_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        Style.error(f"Permission denied creating directories: {e}")
        sys.exit(1)

def backup_config():
    """Creates a timestamped backup of the current config."""
    if CONFIG_FILE.exists():
        timestamp = int(time.time())
        backup_path = BACKUP_DIR / f"config_{timestamp}.jsonc"
        try:
            shutil.copy2(CONFIG_FILE, backup_path)
            # Keep only last 10 backups
            backups = sorted(BACKUP_DIR.glob("config_*.jsonc"), key=os.path.getmtime)
            while len(backups) > 10:
                backups.pop(0).unlink()
        except Exception:
            pass # Silent fail on backup cleanup is acceptable

def restore_backup():
    """Restores the most recent backup."""
    backups = sorted(BACKUP_DIR.glob("config_*.jsonc"), key=os.path.getmtime, reverse=True)
    if not backups:
        Style.error("No backups found to restore.")
        return
    
    latest = backups[0]
    try:
        shutil.copy2(latest, CONFIG_FILE)
        Style.success(f"Restored configuration from {latest.name}")
    except Exception as e:
        Style.error(f"Failed to restore backup: {e}")

def run_command(cmd: List[str], verbose=False) -> bool:
    """Runs a shell command safely."""
    try:
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE if not verbose else None, 
            stderr=subprocess.PIPE if not verbose else None, 
            text=True
        )
        if result.returncode != 0 and verbose:
            print(result.stderr)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_dependencies():
    """Checks for core dependencies and suggests fixes."""
    deps = {
        "fastfetch": "Required to display system info.",
        "fzf": "Required for the interactive picker."
    }
    missing = []
    for dep, reason in deps.items():
        if not shutil.which(dep):
            missing.append(dep)
    
    if missing:
        Style.warning("Missing Dependencies:")
        for m in missing:
            print(f"  - {Style.BOLD}{m}{Style.RESET}: {deps[m]}")
        
        # Smart Install Suggestion
        mgr = "apt" if shutil.which("apt") else \
              "pacman" if shutil.which("pacman") else \
              "dnf" if shutil.which("dnf") else \
              "brew" if shutil.which("brew") else None

        if mgr:
            cmd = ""
            if mgr == "apt": cmd = "sudo apt install fastfetch fzf"
            elif mgr == "pacman": cmd = "sudo pacman -S fastfetch fzf"
            elif mgr == "dnf": cmd = "sudo dnf install fastfetch fzf"
            elif mgr == "brew": cmd = "brew install fastfetch fzf"
            
            print(f"\n👉 Recommended command:\n   {Style.CYAN}{cmd}{Style.RESET}\n")
        else:
            print("\nPlease install them using your package manager.")

# =============================================================
# 🔍 THEME DISCOVERY
# =============================================================

def get_fastfetch_presets() -> List[Path]:
    """Smartly finds where fastfetch stores its presets."""
    # 1. Ask fastfetch
    try:
        proc = subprocess.run(["fastfetch", "--list-data-paths"], capture_output=True, text=True)
        if proc.returncode == 0:
            paths = [Path(p.strip()) for p in proc.stdout.splitlines() if p.strip()]
            valid = []
            for p in paths:
                # Common preset locations
                if (p / "presets").exists(): valid.append(p / "presets")
                if (p / "fastfetch/presets").exists(): valid.append(p / "fastfetch/presets")
            if valid: return valid
    except:
        pass

    # 2. Fallbacks
    candidates = [
        Path("/usr/share/fastfetch/presets"),
        Path("/usr/share/fastfetch/fastfetch/presets"),
        Path.home() / ".local/share/fastfetch/presets"
    ]
    return [p for p in candidates if p.exists()]

def list_themes() -> List[ThemeEntry]:
    """Scans system and user directories for themes."""
    entries = []
    
    # System Presets
    preset_dirs = get_fastfetch_presets()
    for d in preset_dirs:
        # Root presets
        for f in d.glob("*.jsonc"):
            entries.append(ThemeEntry(f.stem, "System", f))
        # Example presets
        for f in (d / "examples").glob("*.jsonc"):
            entries.append(ThemeEntry(f"examples/{f.stem}", "Example", f))

    # User Themes
    if USER_THEMES_DIR.exists():
        for f in USER_THEMES_DIR.glob("*.jsonc"):
            entries.append(ThemeEntry(f"user/{f.stem}", "User", f))
            
    # Deduplicate (prefer User > Example > System)
    unique_map = {}
    for e in entries:
        if e.key not in unique_map:
            unique_map[e.key] = e
    
    return sorted(unique_map.values(), key=lambda x: x.key)

def resolve_theme(name: str) -> Optional[ThemeEntry]:
    """Finds a theme by fuzzy name or exact match."""
    themes = list_themes()
    
    # Exact match
    for t in themes:
        if t.key == name: return t
    
    # Partial match (suffix)
    for t in themes:
        if t.key.endswith(f"/{name}"): return t
        
    # Loose match
    for t in themes:
        if name.lower() in t.key.lower(): return t
        
    return None

# =============================================================
# 🎨 INTERACTIVE BUILDER
# =============================================================

def ask_choice(prompt: str, options: List[str]) -> str:
    print(f"\n{Style.BOLD}? {prompt}{Style.RESET}")
    for i, opt in enumerate(options):
        print(f"  {Style.CYAN}{i+1}){Style.RESET} {opt}")
    
    while True:
        try:
            choice = input(f"{Style.DIM}Select [1-{len(options)}]: {Style.RESET}")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx]
        except KeyboardInterrupt:
            print()
            sys.exit(0)

def build_theme():
    """Interactive wizard to generate a config file."""
    Style.print_header("✨ Interactive Theme Builder ✨")
    
    # --- Step 1: Logo ---
    logo_type = ask_choice("Select Logo Style", ["Current OS (Auto)", "Small/Minimal", "None (Text Only)", "Custom Image Path"])
    
    logo_config = {}
    if logo_type == "Current OS (Auto)":
        logo_config = {"type": "auto"}
    elif logo_type == "Small/Minimal":
        logo_config = {"type": "small"}
    elif logo_type == "None (Text Only)":
        logo_config = {"type": "none"}
    elif logo_type == "Custom Image Path":
        path = input(f"{Style.BOLD}Enter image path: {Style.RESET}").strip()
        logo_config = {"type": "file", "source": path}

    # --- Step 2: Borders & Colors ---
    border = ask_choice("Select Border Style", ["None", "Double", "Rounded", "Solid"])
    color = ask_choice("Select Primary Color", ["Default", "Blue", "Red", "Green", "Magenta", "Yellow", "Cyan"])

    # --- Step 3: Modules ---
    print(f"\n{Style.BOLD}? Select Info Modules to Display{Style.RESET}")
    print(f"{Style.DIM}(Modules will be added in standard order){Style.RESET}")
    
    available_modules = [
        "Title (User@Host)", "Separator", "OS", "Host", "Kernel", "Uptime", 
        "Packages", "Shell", "Display", "DE/WM", "Terminal", "CPU", "GPU", 
        "Memory", "Disk", "Battery", "Local IP", "Break (Space)", "Colors (Palette)"
    ]
    
    selected_modules = []
    
    # Simple selection logic
    preset_choice = ask_choice("Choose Module Layout", ["Standard (Recommended)", "Minimal (Essential)", "All Info", "Custom..."])
    
    if preset_choice == "Standard (Recommended)":
        selected_modules = ["Title", "Separator", "OS", "Host", "Kernel", "Uptime", "Packages", "Shell", "DE/WM", "Terminal", "CPU", "Memory", "Break", "Colors"]
    elif preset_choice == "Minimal (Essential)":
        selected_modules = ["OS", "Kernel", "Packages", "Memory"]
    elif preset_choice == "All Info":
        selected_modules = [m.split(" (")[0] for m in available_modules]
    else:
        # Custom loop
        print("Type 'y' to include, 'n' to skip:")
        for mod in available_modules:
            key = mod.split(" (")[0]
            if input(f"  Include {key}? [Y/n] ").lower() != 'n':
                selected_modules.append(key)

    # --- Generate JSON Structure ---
    config = {
        "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
        "logo": logo_config,
        "display": {
            "separator": " ➜  " if border == "None" else " │ ",
            "color": color.lower() if color != "Default" else "blue"
        },
        "modules": []
    }

    # Map friendly names to fastfetch module keys
    mod_map = {
        "Title": "title", "Separator": "separator", "OS": "os", "Host": "host",
        "Kernel": "kernel", "Uptime": "uptime", "Packages": "packages", "Shell": "shell",
        "Display": "display", "DE/WM": "de", "Terminal": "terminal", "CPU": "cpu",
        "GPU": "gpu", "Memory": "memory", "Disk": "disk", "Battery": "battery",
        "Local IP": "localip", "Break": "break", "Colors": "colors"
    }

    for sm in selected_modules:
        key = mod_map.get(sm.split(" (")[0], sm.lower())
        config["modules"].append(key)

    # --- Save ---
    name = input(f"\n{Style.BOLD}Name your theme (e.g., 'my_cool_theme'): {Style.RESET}").strip()
    if not name: name = "custom_theme"
    if not name.endswith(".jsonc"): name += ".jsonc"
    
    ensure_dirs()
    out_path = USER_THEMES_DIR / name
    
    try:
        with open(out_path, "w") as f:
            json.dump(config, f, indent=4)
        Style.success(f"Theme saved to {out_path}")
        
        if input("\nSet as default now? [y/N] ").lower() == 'y':
            apply_theme(str(out_path))
            
    except Exception as e:
        Style.error(f"Failed to save theme: {e}")

# =============================================================
# ⚙️ CORE LOGIC
# =============================================================

def apply_theme(path_str: str):
    """Safely applies a theme."""
    target = Path(path_str)
    if not target.exists():
        # Try resolving
        entry = resolve_theme(path_str)
        if entry:
            target = entry.path
        else:
            Style.error(f"Theme not found: {path_str}")
            return

    ensure_dirs()
    backup_config()
    
    try:
        shutil.copy2(target, CONFIG_FILE)
        Style.success(f"Applied theme: {target.name}")
        
        # Validation Check
        print(f"{Style.DIM}Validating...{Style.RESET}")
        if not run_command(["fastfetch", "--config", str(CONFIG_FILE)], verbose=False):
            Style.warning("Theme applied, but Fastfetch reported errors/warnings.")
            if input("Revert to previous? [y/N] ").lower() == 'y':
                restore_backup()
        else:
            run_command(["fastfetch"])
            
    except Exception as e:
        Style.error(f"Critical error applying theme: {e}")
        restore_backup()

def run_fzf_picker():
    """Enhanced FZF picker with live preview."""
    if not shutil.which("fzf"):
        Style.error("fzf is not installed.")
        check_dependencies()
        return

    themes = list_themes()
    if not themes:
        Style.error("No themes found.")
        return

    # Prepare input for fzf
    input_str = "\n".join([f"{t.key}\t{t.origin}\t{t.path}" for t in themes])
    
    # FZF Command with Preview
    preview_cmd = "fastfetch --config {3} --structure title:os:kernel:uptime:memory:break:colors"
    
    cmd = [
        "fzf",
        "--delimiter=\t",
        "--with-nth=1,2",
        "--preview", preview_cmd,
        "--preview-window=right,65%,border-left",
        "--header", "ENTER: Apply | ESC: Quit",
        "--color=bg+:#3B4252,bg:#2E3440,spinner:#81A1C1,hl:#616E88,fg:#D8DEE9,header:#616E88,info:#81A1C1,pointer:#81A1C1,marker:#81A1C1,fg+:#D8DEE9,prompt:#81A1C1,hl+:#81A1C1"
    ]

    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stdout, _ = proc.communicate(input=input_str)
        
        if stdout.strip():
            selected = stdout.split("\t")[0]
            apply_theme(selected)
            
    except Exception as e:
        Style.error(f"Picker error: {e}")

def reset_to_defaults():
    """Resets everything to a clean state."""
    if input(f"{Style.RED}WARNING: This will reset your Fastfetch config. Continue? [y/N] {Style.RESET}").lower() != 'y':
        return
    
    backup_config()
    
    # Generate fresh config using fastfetch itself
    if run_command(["fastfetch", "--gen-config-force"]):
        Style.success("Reset complete. Default config generated.")
        run_command(["fastfetch"])
    else:
        Style.error("Failed to generate default config.")

def pull_themes(repo="itz-dev-tasavvuf/fastfetch-theme-manager", path="themes"):
    """Downloads themes without 'requests' library."""
    ensure_dirs()
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    
    Style.info(f"Connecting to GitHub ({repo})...")
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ftm-cli"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            
        count = 0
        for item in data:
            if item["name"].endswith(".jsonc"):
                raw_url = item["download_url"]
                dest = USER_THEMES_DIR / item["name"]
                print(f"  ⬇️  Downloading {item['name']}...")
                with urllib.request.urlopen(raw_url) as r, open(dest, "wb") as f:
                    f.write(r.read())
                count += 1
                
        Style.success(f"Downloaded {count} themes to {USER_THEMES_DIR}")
        
    except Exception as e:
        Style.error(f"Download failed: {e}")
        print("Check your internet connection or GitHub API rate limits.")

# =============================================================
# 🚀 ENTRY POINT
# =============================================================

def main():
    parser = argparse.ArgumentParser(description="Fastfetch Theme Manager (FTM)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all available themes")
    subparsers.add_parser("pick", help="Interactive theme picker (fzf)")
    subparsers.add_parser("build", help="Create a new theme interactively")
    subparsers.add_parser("reset", help="Reset configuration to defaults")
    
    set_parser = subparsers.add_parser("set", help="Apply a specific theme")
    set_parser.add_argument("theme", help="Theme name or path")

    pull_parser = subparsers.add_parser("pull", help="Download community themes")
    pull_parser.add_argument("--repo", default="itz-dev-tasavvuf/fastfetch-theme-manager")

    # If no args, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Pre-flight check
    ensure_dirs()
    if args.command != "list": 
        check_dependencies()

    try:
        if args.command == "list":
            themes = list_themes()
            print(f"\n{Style.BOLD}{'KEY':<35} {'SOURCE':<10} {'PATH'}{Style.RESET}")
            print("─" * 80)
            for t in themes:
                c = Style.GREEN if t.origin == "User" else Style.BLUE
                print(f"{t.key:<35} {c}{t.origin:<10}{Style.RESET} {t.path}")
            print()

        elif args.command == "set":
            apply_theme(args.theme)

        elif args.command == "pick":
            run_fzf_picker()

        elif args.command == "build":
            build_theme()

        elif args.command == "reset":
            reset_to_defaults()

        elif args.command == "pull":
            pull_themes(repo=args.repo)

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    main()