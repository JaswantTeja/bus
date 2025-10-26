import os
import shutil
import re

# ---------- CONFIG ----------
SVG_DIR = "output_svgs"           # Source folder where all converted SVGs are
ORG_DIR = "systemui_svgs_ultimate"  # Organized output folder
os.makedirs(ORG_DIR, exist_ok=True)

# ---------- Categories & Keywords ----------
CATEGORIES = {
    "status_bar": ["battery", "wifi", "signal", "airplane", "clock", "alarm", "hotspot", "volume", "dnd", "silent"],
    "quick_settings": ["toggle", "brightness", "rotation", "bluetooth", "airplane", "mobile_data", "hotspot", "dark_mode"],
    "notifications": ["warning", "error", "alert", "dnd", "notification", "chat", "message", "mail", "calendar", "alarm"],
    "actions": ["send", "forward", "back", "play", "pause", "stop", "menu", "reply", "undo", "redo", "attach", "delete"],
    "system": ["settings", "power", "reboot", "screenshot", "systemui", "volume", "keyguard", "lock", "unlock"],
    "media": ["camera", "video", "microphone", "gallery", "image", "photo", "record", "edit"],
    "navigation": ["arrow", "chevron", "up", "down", "left", "right", "more", "home", "back"],
    "misc": []
}

# Color tier for secondary classification
COLOR_KEYWORDS = ["black", "white", "gray", "red", "blue", "green", "yellow"]

# ---------- Helpers ----------
def clean_name(name):
    """Remove Android prefixes and normalize filenames."""
    name = re.sub(r'^(ic_|abc_|btn_|icn_)', '', name, flags=re.IGNORECASE)
    name = name.replace(" ", "_").replace("-", "_").lower()
    return name

def classify_category(name):
    """Determine main category from filename."""
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in name:
                return category
    return "misc"

def classify_color(name):
    """Determine color group from filename."""
    for color in COLOR_KEYWORDS:
        if color in name:
            return color
    return "default"

# ---------- Organize ----------
def organize_svgs():
    count = 0
    for subdir, _, files in os.walk(SVG_DIR):
        for f in files:
            if not f.endswith(".svg"):
                continue
            src = os.path.join(subdir, f)
            clean_filename = clean_name(f)
            category = classify_category(clean_filename)
            color = classify_color(clean_filename)

            dst_dir = os.path.join(ORG_DIR, category, color)
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, clean_filename)

            # Handle duplicates by appending numbers
            base, ext = os.path.splitext(clean_filename)
            counter = 1
            while os.path.exists(dst):
                dst = os.path.join(dst_dir, f"{base}_{counter}{ext}")
                counter += 1

            shutil.move(src, dst)
            count += 1
            print(f"📁 {f} → {category}/{color}/{os.path.basename(dst)}")

    print(f"\n✅ Organized {count} SVGs into '{ORG_DIR}' with deep categorization.")

# ---------- Run ----------
if __name__ == "__main__":
    organize_svgs()
