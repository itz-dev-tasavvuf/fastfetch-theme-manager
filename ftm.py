#!/usr/bin/env python3
# =============================================================
# 🌈 Fastfetch Theme Manager (FTM) — Full Smart Detection Edition
# Author: tasavvuf gori
# =============================================================

"""
FTM — Fastfetch Theme Manager
Beautiful Unicode + Emoji Edition
Smart-Detection for Fastfetch 2.x and 3.x compatible layouts.
"""

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

USER_THEMES_DIR = Path.home() / ".local/share/fastfetch/themes"

@dataclass
class ThemeEntry:
    key: str
    origin: str
    path: Optional[Path]

# ---------------------- Utility ----------------------
def run(cmd: List[str], check=False) -> Tuple[int, str, str]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, out, err)
    return proc.returncode, out, err

def find_fastfetch():
    exe = shutil.which("fastfetch")
    if not exe:
        print("❌ fastfetch not found. Install it first.")
        sys.exit(1)
    return exe

# ---------------------- Smart Detection ----------------------
def smart_detect_paths() -> List[Path]:
    code, out, _ = run(["fastfetch", "--list-data-paths"])

    if code == 0 and out.strip():
        return [Path(p.strip()) for p in out.splitlines() if p.strip()]

    fallback = [
        Path("/usr/share/fastfetch"),
        Path.home() / "fastfetch",
        Path.home() / ".local/share/fastfetch",
    ]
    valid = [p for p in fallback if p.exists()]
    if valid:
        return valid

    print("❌ Could not detect fastfetch preset paths.")
    sys.exit(1)

# ---------------------- Preset Scanner ----------------------
def discover_presets() -> List[ThemeEntry]:
    paths = smart_detect_paths()
    entries = []

    builtin = ["neofetch", "paleofetch", "screenfetch", "archey", "ci", "all"]

    for base in paths:
        p1 = base / "fastfetch" / "presets"
        p2 = base / "presets"

        for pres in (p1, p2):
            if not pres.is_dir():
                continue

            # built-ins
            for name in builtin:
                f = pres / f"{name}.jsonc"
                if f.exists():
                    entries.append(ThemeEntry(name, "builtins", f))

            # examples
            ex = pres / "examples"
            if ex.is_dir():
                for f in sorted(ex.glob("*.jsonc")):
                    entries.append(ThemeEntry(f"examples/{f.stem}", "examples", f))

    if USER_THEMES_DIR.is_dir():
        for f in sorted(USER_THEMES_DIR.glob("*.jsonc")):
            entries.append(ThemeEntry(f"user/{f.stem}", "user", f))

    seen = set()
    uniq = []
    for e in entries:
        if e.key not in seen:
            seen.add(e.key)
            uniq.append(e)

    return uniq

# ---------------------- Printing ----------------------
def print_table(entries: List[ThemeEntry]):
    print("\n🌈 Fastfetch Themes (by tasavvuf gori)\n")
    print(f"{'#':<3}  {'KEY':<32}  {'ORIGIN':<10}  PATH")
    print("-" * 90)
    for i, e in enumerate(entries):
        print(f"{i:<3}  {e.key:<32}  {e.origin:<10}  {e.path}")
    print()

# ---------------------- Resolver ----------------------
def resolve_theme(arg: str, entries: List[ThemeEntry]) -> Optional[ThemeEntry]:
    if arg.isdigit():
        idx = int(arg)
        if 0 <= idx < len(entries):
            return entries[idx]

    for e in entries:
        if e.key == arg:
            return e

    for e in entries:
        if e.key.endswith("/" + arg):
            return e

    return None

# ---------------------- Actions ----------------------
def preview(key: str):
    subprocess.call(["fastfetch", "--config", key])

def set_default(key: str):
    # Try to resolve to a concrete theme path first
    entries = discover_presets()
    entry = resolve_theme(key, entries)

    # Destination config path
    dest = Path.home() / ".config/fastfetch/config.jsonc"
    dest.parent.mkdir(parents=True, exist_ok=True)

    if entry and entry.path and entry.path.exists():
        try:
            shutil.copy2(entry.path, dest)
            print(f"✅ Default theme applied → {key} → {dest}")
            return
        except Exception as ex:
            print("⚠️  Copy failed, falling back to fastfetch generator:", ex)

    # Fallback to fastfetch generating config
    code, _, err = run(["fastfetch", "--config", key, "--gen-config"])
    if code == 0 and dest.exists():
        print(f"✅ Default theme generated → {dest} (from {key})")
    elif code == 0:
        print("⚠️  fastfetch reported success but config not found at", dest)
    else:
        print("❌ Error setting default:", err)

# ---------------------- User Theme ----------------------
def ensure_user_dir():
    USER_THEMES_DIR.mkdir(parents=True, exist_ok=True)

def add_theme(src: Path, name: Optional[str]):
    ensure_user_dir()

    if not src.exists():
        print("❌ Theme file not found:", src)
        sys.exit(1)

    out = USER_THEMES_DIR / f"{name or src.stem}.jsonc"
    shutil.copy2(src, out)
    print(f"✨ Added → {out}")

# ---------------------- Pull (GitHub) ----------------------
def pull_themes(repo: str, subpath: str):
    try:
        import requests
    except:
        print("❌ Install python-requests first.")
        sys.exit(1)

    ensure_user_dir()

    url = f"https://api.github.com/repos/{repo}/contents/{subpath}"
    print(f"🌐 Pulling from {repo}/{subpath}…")

    r = requests.get(url, headers={"Accept": "application/vnd.github+json"})
    if r.status_code != 200:
        print("❌ GitHub error:", r.text)
        sys.exit(1)

    for it in r.json():
        if it.get("type") == "file" and it["name"].endswith(".jsonc"):
            print(f"⬇️  {it['name']}")
            data = requests.get(it["download_url"]).content
            with open(USER_THEMES_DIR / it["name"], "wb") as f:
                f.write(data)

    print("✨ Done! Themes saved.")

# ---------------------- fzf Picker ----------------------
def have_fzf():
    return shutil.which("fzf") is not None

def pick(args):
    if not have_fzf():
        print("❌ fzf missing. Install: sudo pacman -S fzf")
        sys.exit(1)

    entries = discover_presets()
    if not entries:
        print("❌ No themes found.")
        return

    lines = []
    for e in entries:
        lines.append(f"{e.key}\t{e.origin}\t{e.path}")

    proc = subprocess.Popen([
        "fzf",
        "--delimiter=\t",
        "--with-nth=1,2",
        "--preview", "bash -lc 'fastfetch --config {1} || true'",
        "--preview-window=right,70%",
        "--header", "🎨 Pick a theme (ENTER = apply)"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    out, _ = proc.communicate("\n".join(lines))
    if not out:
        return

    key = out.split("\t", 1)[0]
    print(f"🎯 Selected: {key}")

    if args.apply:
        set_default(key)
    else:
        preview(key)

# ---------------------- Toggle ----------------------
def toggle(_):
    entries = discover_presets()
    if not entries:
        print("❌ No themes found.")
        return

    i = 0
    while True:
        e = entries[i]
        os.system("clear")
        print("🔥 Toggle Themes — (n) next | (p) prev | (s) set | (q) quit")
        print(f"🎨 Showing → {e.key} [{e.origin}]")
        print("--------------------------------------------------")
        preview(e.key)

        choice = input("→ ").strip().lower()
        if choice == "n":
            i = (i + 1) % len(entries)
        elif choice == "p":
            i = (i - 1) % len(entries)
        elif choice == "s":
            set_default(e.key)
        elif choice == "q":
            break

# ---------------------- CLI ----------------------
def build_parser():
    p = argparse.ArgumentParser(description="🌈 Fastfetch Theme Manager (by tasavvuf gori)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List themes").set_defaults(func=lambda a: print_table(discover_presets()))

    pv = sub.add_parser("preview", help="Preview theme")
    pv.add_argument("theme")
    pv.set_defaults(func=lambda a: preview(theme.key) if (theme := resolve_theme(a.theme, discover_presets())) else print("❌ Not found"))

    st = sub.add_parser("set", help="Set default")
    st.add_argument("theme")
    st.set_defaults(func=lambda a: set_default(theme.key) if (theme := resolve_theme(a.theme, discover_presets())) else print("❌ Not found"))
    # toggle
    tg = sub.add_parser("toggle", help="Toggle themes interactively")
    tg.set_defaults(func=toggle)

    # fzf picker
    pk = sub.add_parser("pick", help="fzf theme picker")
    pk.add_argument("--apply", action="store_true", help="Apply theme after selecting")
    pk.set_defaults(func=pick)

    # add
    ad = sub.add_parser("add", help="Add a user theme")
     ad.add_argument("file", help="Path to .jsonc file")
    ad.add_argument("--name", help="Optional name (default = file name)")
    ad.set_defaults(func=lambda a: add_theme(Path(a.file).expanduser(), a.name))

    # pull
    pl = sub.add_parser("pull", help="Pull themes from GitHub")
    pl.add_argument("--repo", default="fastfetch-cli/fastfetch")
    pl.add_argument("--path", default="presets/examples")
    pl.set_defaults(func=lambda a: pull_themes(a.repo, a.path))

    return p


# ---------------------- Main ----------------------
def main():
    find_fastfetch()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
