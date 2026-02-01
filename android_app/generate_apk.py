"""
DocuVoice APK Generator Script
This script generates a pre-built APK or provides download links
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

def generate_build_config():
    """Generate build configuration"""
    config = {
        "app_name": "DocuVoice",
        "version": "1.0.0",
        "package": "org.docuvoice",
        "build_date": datetime.now().isoformat(),
        "target_sdk": 31,
        "min_sdk": 21,
        "features": [
            "Text to Speech",
            "Word Document to Speech",
            "Voice Recording",
            "Cloud Backend Integration"
        ],
        "permissions": [
            "INTERNET",
            "RECORD_AUDIO",
            "READ_EXTERNAL_STORAGE",
            "WRITE_EXTERNAL_STORAGE"
        ]
    }
    
    config_file = Path("build_config.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    return config

def show_build_options():
    """Show build options"""
    print("""
╔════════════════════════════════════════════════════════════╗
║         DocuVoice Android App - Build Options              ║
╚════════════════════════════════════════════════════════════╝

1. BUILD LOCALLY (Advanced)
   ─────────────────────────
   Requirements: Java, Android SDK, NDK, buildozer
   Time: 15-30 minutes (first time)
   OS: Linux, macOS
   
   Command: buildozer android release

2. BUILD WITH WSL2 (Windows)
   ──────────────────────────
   Requirements: WSL2, Linux distro
   Time: 15-25 minutes (first time)
   OS: Windows 10/11
   
   wsl buildozer android release

3. BUILD WITH DOCKER (Windows/Mac/Linux)
   ──────────────────────────────────────
   Requirements: Docker Desktop
   Time: 20-30 minutes (first time)
   OS: Any (Windows, Mac, Linux)
   
   Windows: build.bat
   Linux/Mac: bash build.sh

4. ONLINE BUILD (No Setup)
   ────────────────────────
   Requirements: Internet browser only
   Time: 5-10 minutes
   OS: Any
   
   Visit: https://kivy2apk.appspot.com/

5. USE PRE-BUILT APK (Quick)
   ─────────────────────────
   Requirements: Download link
   Time: 2-3 minutes
   OS: Any
   
   Download & install directly

╔════════════════════════════════════════════════════════════╗
║                  RECOMMENDED APPROACH                       ║
║                                                              ║
║  Windows Users: Use Option 3 (Docker) - build.bat          ║
║  Linux/Mac Users: Use Option 1 or 3                        ║
║  No Setup Users: Use Option 4 (Online)                    ║
╚════════════════════════════════════════════════════════════╝
""")

def show_quick_start():
    """Show quick start guide"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                    QUICK START GUIDE                        ║
╚════════════════════════════════════════════════════════════╝

Step 1: Update Backend URL
──────────────────────────
Edit main.py (lines 40, 150, 270):

    self.api_url = "http://YOUR_SERVER_IP:5000"

Replace YOUR_SERVER_IP with:
- Your computer IP (internal network): 192.168.x.x
- Your domain name: example.com
- Localhost if on same device: 127.0.0.1

Step 2: Choose Build Method
────────────────────────────
Windows:    Double-click build.bat
Linux/Mac:  bash build.sh
Online:     Visit kivy2apk.appspot.com

Step 3: Wait for APK
────────────────────
First build takes 15-30 minutes
Subsequent builds: 5-10 minutes

Step 4: Find APK File
─────────────────────
Location:
- Docker: output/docuvoice-1.0.0-release.apk
- Local: bin/docuvoice-1.0.0-release.apk
- Online: Download after build

Step 5: Install on Android
──────────────────────────
Option A (USB):
    adb install docuvoice-1.0.0-release.apk

Option B (File Transfer):
    1. Copy APK to phone via USB
    2. Tap APK to install
    3. Grant permissions

Step 6: First Run
─────────────────
1. Open DocuVoice app
2. Grant microphone & storage permissions
3. Test features
4. Configure backend if needed

╔════════════════════════════════════════════════════════════╗
║                  BUILD TIME ESTIMATE                        ║
╚════════════════════════════════════════════════════════════╝

Method          First Build    Subsequent    Complexity
─────────────────────────────────────────────────────────
Docker          20-30 min      15-20 min     Easy
WSL2            15-25 min      10-15 min     Medium
Linux/Local     10-20 min      5-10 min      Hard
Online          5-10 min       5-10 min      Very Easy

Tip: Use SSD for faster builds!
""")

def check_prerequisites():
    """Check if prerequisites are available"""
    tools = {
        'Docker': 'docker --version',
        'Java': 'java -version',
        'Python': 'python3 --version',
        'buildozer': 'buildozer --version',
    }
    
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║            CHECKING PREREQUISITES                          ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    available = []
    missing = []
    
    for tool, cmd in tools.items():
        try:
            result = subprocess.run(cmd.split(), capture_output=True, timeout=5)
            if result.returncode == 0:
                available.append(tool)
                print(f"✓ {tool:<20} FOUND")
            else:
                missing.append(tool)
                print(f"✗ {tool:<20} Not found or error")
        except Exception as e:
            missing.append(tool)
            print(f"✗ {tool:<20} Not found ({str(e)[:20]}...)")
    
    print(f"\nAvailable: {len(available)}/{len(tools)}")
    
    if missing:
        print(f"Missing: {', '.join(missing)}")
        print("\nRecommendation: Use Docker (no setup required!)")
        print("  Windows: run build.bat")
        print("  Linux/Mac: bash build.sh")

def main():
    """Main function"""
    import sys
    
    # Generate config
    config = generate_build_config()
    
    print("\n" + "="*60)
    print("  DocuVoice Android App")
    print(f"  Version {config['version']}")
    print("="*60)
    
    # Show options
    show_build_options()
    
    # Show quick start
    show_quick_start()
    
    # Check prerequisites
    check_prerequisites()
    
    print("\n" + "="*60)
    print("For detailed instructions, see:")
    print("  - INSTALL.md")
    print("  - README_BUILD.md")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
