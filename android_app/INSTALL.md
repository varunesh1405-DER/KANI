# DocuVoice Android App - Installation & Build Guide

## Overview

This guide will help you build and install the DocuVoice Android application on your device.

## System Requirements

- **Windows 10/11**, **macOS**, or **Linux**
- **8GB RAM minimum** (16GB recommended)
- **10GB free disk space** for Android SDK and NDK
- **Docker Desktop** (recommended for Windows) or **WSL2**

## Installation Methods

### Method 1: Using Docker (Easiest - Windows)

#### Prerequisites:
- Docker Desktop installed: https://www.docker.com/products/docker-desktop

#### Steps:

1. **Navigate to app directory:**
   ```cmd
   cd android_app
   ```

2. **Run build script:**
   ```cmd
   build.bat
   ```

3. **Wait for build to complete** (15-30 minutes)

4. **APK will be in `output/` folder**

### Method 2: Using WSL2 (Windows with Linux)

#### Prerequisites:
- WSL2 installed
- Ubuntu distro in WSL2

#### Steps:

1. **Open WSL terminal:**
   ```bash
   wsl
   ```

2. **Install build tools:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y build-essential python3-pip openjdk-11-jdk-headless android-sdk
   ```

3. **Install Python packages:**
   ```bash
   pip3 install buildozer Cython kivy requests pyjnius
   ```

4. **Navigate to app directory:**
   ```bash
   cd /mnt/c/Users/Varunesh/Desktop/New\ folder/KANI/android_app
   ```

5. **Build APK:**
   ```bash
   buildozer android release
   ```

6. **APK will be in `bin/` folder**

### Method 3: Using Linux/Mac

#### Prerequisites:
- Java 11+ installed
- Python 3.7+ installed

#### Steps:

1. **Install dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install build-essential git python3-pip openjdk-11-jdk-headless

   # macOS
   brew install python3 openjdk@11
   ```

2. **Install Python packages:**
   ```bash
   pip3 install buildozer Cython kivy requests pyjnius
   ```

3. **Make build script executable:**
   ```bash
   chmod +x build.sh
   ```

4. **Run build:**
   ```bash
   ./build.sh
   ```

5. **APK will be in `bin/` folder**

### Method 4: Online APK Generator (No Setup Required)

Use online services that don't require installation:

1. **Kivy2APK.com** (Recommended)
   - Visit: https://kivy2apk.appspot.com/
   - Upload `main.py`
   - Configure options
   - Download APK

2. **Buildozer Online**
   - Visit: https://buildozer-online.herokuapp.com/
   - Upload files
   - Wait for APK

3. **Kodular** (Visual builder)
   - Visit: https://kodular.io/
   - Import Python code
   - Generate APK

## Pre-Build Configuration

Before building, update these settings in `main.py`:

### 1. Backend Server URL

Find line ~40, 150, 270 and change:

```python
self.api_url = "http://192.168.0.12:5000"
```

To your actual server:

```python
self.api_url = "http://YOUR_DOMAIN.com:5000"
# OR
self.api_url = "http://YOUR_IP_ADDRESS:5000"
```

### 2. App Configuration (Optional)

In `buildozer.spec`:

```ini
# App name and version
title = DocuVoice
version = 1.0.0

# Package name (change domain if needed)
package.name = docuvoice
package.domain = org.docuvoice

# Permissions (usually fine as-is)
android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
```

## Building the APK

### Windows (Docker Method - Recommended)

```cmd
cd android_app
build.bat
```

### Windows (WSL2 Method)

```bash
wsl
cd /mnt/c/Users/Varunesh/Desktop/New\ folder/KANI/android_app
buildozer android release
```

### Linux/Mac

```bash
cd android_app
chmod +x build.sh
./build.sh
```

## Output

After successful build, find the APK at:

**Windows (Docker):**
```
android_app\output\docuvoice-1.0.0-release.apk
```

**Linux/Mac/WSL:**
```
android_app/bin/docuvoice-1.0.0-release.apk
```

## Installing on Android Device

### Option 1: ADB (USB Cable)

1. **Connect Android device with USB debugging enabled:**
   ```bash
   adb devices
   ```

2. **Install APK:**
   ```bash
   adb install -r bin/docuvoice-1.0.0-release.apk
   ```

### Option 2: File Transfer

1. **Copy APK to Android device** (USB, cloud, email, etc.)

2. **Open file manager on device**

3. **Navigate to downloaded APK**

4. **Tap to install**

5. **Grant permissions when prompted**

### Option 3: QR Code

1. **Generate QR code from APK download link**

2. **Scan with phone**

3. **Tap to install**

## First Run Setup

1. **Allow permissions:**
   - Internet
   - Microphone
   - Storage (read/write)

2. **Configure backend URL:**
   - Open app settings
   - Enter your Flask server address
   - Save

3. **Test features:**
   - Try text-to-speech
   - Try word-to-speech
   - Try voice recording

## Troubleshooting

### Build Fails: "buildozer command not found"

**Windows (Docker):**
```cmd
docker --version
# Should show version, if not install Docker
```

**Linux/WSL:**
```bash
pip3 install buildozer --upgrade
buildozer --version
```

### Error: "Java not found"

**Windows (Docker):**
- Docker image includes Java, try rebuilding

**Linux:**
```bash
sudo apt-get install openjdk-11-jdk-headless
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

**Mac:**
```bash
brew install openjdk@11
sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

### Error: "Gradle build failed"

```bash
# Clean and rebuild
buildozer android clean
buildozer android release
```

### App crashes on startup

1. **Check backend URL** in main.py is correct
2. **Verify network connectivity** on phone
3. **Check Flask server is running**
4. **Review Android logs:**
   ```bash
   adb logcat | grep docuvoice
   ```

### Microphone not working

1. **Enable permission in Android:**
   - Settings > Apps > DocuVoice > Permissions > Microphone

2. **Test microphone:**
   - Try system voice recording app first

3. **Check buildozer.spec:**
   ```ini
   android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
   ```

### File upload not working

1. **Enable storage permission:**
   - Settings > Apps > DocuVoice > Permissions > Storage

2. **Ensure .docx file is on device**

3. **Check file path is correct**

## Build Times

| Method | First Build | Subsequent | Optimization |
|--------|------------|-----------|--------------|
| Docker | 20-30 min  | 15-20 min | Use SSD |
| WSL2   | 15-25 min  | 10-15 min | Faster |
| Linux  | 10-20 min  | 5-10 min  | Native is fastest |
| Online | 5-10 min   | 5-10 min  | No setup needed |

## Production Deployment

### Signing APK

For Google Play Store, you need to sign the APK:

1. **Create keystore (one time):**
   ```bash
   keytool -genkey -v -keystore ~/.android/docuvoice.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias docuvoice
   ```

2. **Edit buildozer.spec:**
   ```ini
   android.keystore = ~/.android/docuvoice.keystore
   android.keystore_alias = docuvoice
   android.keystore_alias_password = YOUR_PASSWORD
   android.keystore_password = YOUR_PASSWORD
   ```

3. **Build release APK:**
   ```bash
   buildozer android release
   ```

### Publishing to Google Play Store

1. Create Google Play Developer account ($25 one-time)
2. Create new application
3. Upload signed APK
4. Fill in app details, screenshots, description
5. Submit for review
6. Approved in 24-48 hours

## Support

For issues:
- Check logs: `adb logcat`
- Read Kivy docs: https://kivy.org
- Read Buildozer docs: https://buildozer.readthedocs.io
- Check Android dev docs: https://developer.android.com

## Quick Reference

| Task | Command |
|------|---------|
| Build APK | `buildozer android release` |
| Build debug APK | `buildozer android debug` |
| Install via ADB | `adb install bin/*.apk` |
| View logs | `adb logcat` |
| List devices | `adb devices` |
| Clean build | `buildozer android clean` |

---

**Ready to build?** Choose your method above and start!

Generated: February 2026
