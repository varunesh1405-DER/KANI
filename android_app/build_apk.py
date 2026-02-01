#!/usr/bin/env python3
"""
DocuVoice APK Builder
Builds the Android APK from the Kivy app

Requirements:
- Java Development Kit (JDK) 11 or higher
- Android SDK
- Android NDK 25b
- Buildozer
"""

import os
import sys
import subprocess
import platform

def check_requirements():
    """Check if all required tools are installed"""
    print("Checking requirements...")
    
    # Check if buildozer is installed
    try:
        import buildozer
        print("✓ Buildozer found")
    except ImportError:
        print("✗ Buildozer not found. Install with: pip install buildozer")
        return False
    
    # Check if Cython is installed
    try:
        import Cython
        print("✓ Cython found")
    except ImportError:
        print("✗ Cython not found. Install with: pip install Cython")
        return False
    
    # Check if Java is installed
    try:
        result = subprocess.run(['java', '-version'], capture_output=True)
        if result.returncode == 0:
            print("✓ Java found")
        else:
            print("✗ Java not found")
            return False
    except FileNotFoundError:
        print("✗ Java not found. Please install JDK 11 or higher")
        return False
    
    return True

def install_buildozer_requirements():
    """Install additional buildozer requirements"""
    print("\nInstalling buildozer requirements...")
    packages = [
        'buildozer',
        'Cython',
        'pyjnius',
        'android'
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to install {package}")

def build_apk():
    """Build the APK"""
    print("\nBuilding APK...")
    print("This may take 10-30 minutes on first build...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    try:
        # Run buildozer
        result = subprocess.run(
            ['buildozer', 'android', 'release'],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✓ APK built successfully!")
            apk_path = os.path.join(current_dir, 'bin', 'docuvoice-1.0.0-release.apk')
            if os.path.exists(apk_path):
                print(f"✓ APK located at: {apk_path}")
                return True
        else:
            print("\n✗ Build failed")
            return False
    except Exception as e:
        print(f"\n✗ Error during build: {e}")
        return False

def main():
    print("=" * 60)
    print("DocuVoice APK Builder")
    print("=" * 60)
    
    # For Windows, we'll provide an alternative method
    if platform.system() == 'Windows':
        print("\n⚠️  Note: Building APK on Windows requires WSL or Docker.")
        print("\nAlternative methods:")
        print("1. Use WSL2 (Windows Subsystem for Linux 2)")
        print("2. Use Docker with an Android build image")
        print("3. Use the APK generation service online")
        print("\nFor WSL2, run:")
        print("  wsl buildozer android release")
        return
    
    if not check_requirements():
        print("\nInstalling requirements...")
        install_buildozer_requirements()
    
    if build_apk():
        print("\nBuild process completed successfully!")
    else:
        print("\nBuild process failed. Check logs above for details.")

if __name__ == '__main__':
    main()
