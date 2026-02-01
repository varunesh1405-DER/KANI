#!/usr/bin/env python3
"""
DocuVoice Local APK Builder for Windows
Builds APK using buildozer without Docker
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required tools are installed."""
    print("\n" + "="*60)
    print("DocuVoice Local APK Builder - Checking Requirements")
    print("="*60 + "\n")
    
    required = {
        'java': 'Java Development Kit (JDK 11+)',
        'python': 'Python 3.7+',
        'buildozer': 'buildozer',
    }
    
    missing = []
    
    # Check Java
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True, timeout=5)
        if 'version' in result.stderr.lower():
            print("✓ Java found")
        else:
            missing.append('Java')
    except:
        missing.append('Java')
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
        print(f"✓ Python found: {result.stdout.strip()}")
    except:
        missing.append('Python')
    
    # Check buildozer
    try:
        result = subprocess.run(['buildozer', '--version'], capture_output=True, text=True, timeout=5)
        print(f"✓ buildozer found")
    except:
        missing.append('buildozer')
    
    if missing:
        print(f"\n✗ Missing requirements: {', '.join(missing)}")
        print("\nInstall missing packages:")
        print("  pip install buildozer cython kivy requests pyjnius")
        if 'buildozer' in missing:
            print("\nNote: After installing buildozer, run:")
            print("  buildozer android debug")
            print("  (This initializes Android toolchain)")
        return False
    
    print("\n✓ All requirements met!\n")
    return True


def setup_environment():
    """Set up environment variables for Android build."""
    print("Setting up Android environment...\n")
    
    # Check available buildozer targets
    try:
        result = subprocess.run(['buildozer', '--help'], capture_output=True, text=True, timeout=10)
        if 'android' not in result.stdout.lower():
            print("⚠ WARNING: buildozer doesn't recognize 'android' target")
            print("\nInstalling buildozer-android toolchain...\n")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'buildozer'], check=True)
            print("\n")
    except Exception as e:
        print(f"⚠ Could not check buildozer targets: {e}\n")
    
    # Try to find Android SDK
    android_home = os.environ.get('ANDROID_HOME')
    if not android_home:
        # Common locations
        possible_homes = [
            os.path.expanduser('~/.buildozer/android/platform/android-sdk'),
            os.path.expanduser('~/AppData/Local/.buildozer/android/platform/android-sdk'),
            'C:\\Android\\sdk',
        ]
        
        for home in possible_homes:
            if os.path.exists(home):
                android_home = home
                os.environ['ANDROID_HOME'] = android_home
                print(f"✓ Found Android SDK: {android_home}\n")
                break
    
    if not android_home:
        print("⚠ ANDROID_HOME not set. buildozer will download Android SDK (this may take a while).\n")


def build_apk():
    """Build APK using buildozer."""
    print("="*60)
    print("Starting APK Build")
    print("="*60 + "\n")
    
    try:
        # Change to app directory
        app_dir = Path(__file__).parent
        os.chdir(app_dir)
        
        print(f"Building in: {app_dir}\n")
        
        # Check if buildozer.spec exists
        spec_file = app_dir / 'buildozer.spec'
        if not spec_file.exists():
            print(f"✗ buildozer.spec not found in {app_dir}")
            print("\nMake sure you're running this script from the android_app directory")
            return False
        
        print(f"✓ Found buildozer.spec\n")
        
        # Initialize buildozer android (downloads Android SDK if needed)
        print("Initializing buildozer android (this may take a few minutes)...\n")
        init_cmd = ['buildozer', 'android', 'debug']
        init_result = subprocess.run(init_cmd, capture_output=True, text=True, timeout=300)
        
        if init_result.returncode != 0:
            print("✓ Android toolchain initialized or already available\n")
        
        # Run buildozer with verbose output
        cmd = ['buildozer', '-v', 'android', 'release']
        print(f"Running: {' '.join(cmd)}\n")
        print("This will take 15-30 minutes on first build...\n")
        print("-" * 60 + "\n")
        
        result = subprocess.run(cmd, timeout=3600)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("✓ Build Successful!")
            print("="*60)
            
            # Look for APK
            bin_dir = app_dir / 'bin'
            if bin_dir.exists():
                apks = list(bin_dir.glob('*.apk'))
                if apks:
                    print(f"\n✓ APK generated: {apks[0].name}")
                    print(f"  Location: {apks[0]}")
                    print(f"\nNext steps:")
                    print(f"  1. Transfer APK to Android device")
                    print(f"  2. Install: adb install {apks[0].name}")
                    return True
        else:
            print("\n✗ Build failed with return code:", result.returncode)
            print("\nTroubleshooting:")
            print("1. Check disk space (need ~10GB)")
            print("2. Ensure Java is properly installed")
            print("3. Check buildozer.spec configuration")
            print("4. Try: pip install --upgrade buildozer")
            return False
            
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("\nMake sure buildozer is installed:")
        print("  pip install buildozer")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def main():
    """Main entry point."""
    try:
        if not check_requirements():
            print("\nPlease install missing requirements and try again.")
            return 1
        
        setup_environment()
        
        if not build_apk():
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
