# DocuVoice Android App

Native Android application for converting text/Word documents to audio and recording voice.

## Features

✓ Text to Speech conversion
✓ Word document to Speech conversion  
✓ Voice recording
✓ Cloud-based processing with Flask backend
✓ Material Design UI
✓ Real-time status updates

## Project Structure

```
android_app/
├── main.py              # Main Kivy application
├── buildozer.spec       # Buildozer configuration for APK
├── requirements.txt     # Python dependencies
├── build_apk.py         # APK builder script
└── README.md           # This file
```

## Prerequisites

### For Building on Windows

You need to install these tools:

1. **Java Development Kit (JDK) 11+**
   - Download from: https://www.oracle.com/java/technologies/downloads/
   - Or: Install via `winget install Oracle.JDK.11`

2. **Android SDK**
   - Download Android Studio from: https://developer.android.com/studio
   - Or install tools directly

3. **Android NDK 25b**
   - Download from: https://developer.android.com/ndk/downloads
   - Extract to a known location

4. **WSL2 (Recommended)** or **Docker**
   - Building Android APK is easier with Linux environment

### Python Dependencies

Install Python packages:

```bash
pip install kivy buildozer Cython pyjnius android requests
```

## Quick Build Instructions

### Option 1: Using WSL2 (Recommended for Windows)

1. **Install WSL2:**
   ```bash
   wsl --install
   ```

2. **Install build tools in WSL:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y build-essential git
   sudo apt-get install -y openjdk-11-jdk-headless
   sudo apt-get install -y android-sdk
   ```

3. **Install Python tools:**
   ```bash
   pip install buildozer Cython pyjnius kivy requests
   ```

4. **Build APK:**
   ```bash
   cd /path/to/android_app
   buildozer android release
   ```

### Option 2: Using Docker

1. **Build Docker image:**
   ```bash
   docker build -t kivy-buildozer .
   ```

2. **Build APK in container:**
   ```bash
   docker run -v $(pwd):/home/user/app kivy-buildozer /home/user/app
   ```

### Option 3: Online APK Builders

Use online APK builder services like:
- APKBuilder (https://www.apkbuilder.io/)
- Kodular (https://kodular.io/)
- MIT App Inventor (https://appinventor.mit.edu/)

Simply upload the source files and let the service generate the APK.

## Configuration

### Edit Backend URL

Before building, update the backend API URL in `main.py`:

```python
# Line ~40, ~150, ~270
self.api_url = "http://YOUR_SERVER_IP:5000"
```

Replace `YOUR_SERVER_IP` with your actual Flask server IP/domain.

### Customize App Name/Icon

Edit `buildozer.spec`:

```ini
title = DocuVoice
package.name = docuvoice
package.domain = org.docuvoice

# Add custom icon (create icons in data/ folder)
android.icon = data/icon.png
```

## Building the APK

### Step 1: Update Configuration

```bash
cd android_app

# Edit buildozer.spec to configure:
# - App name, version, package name
# - Backend URL
# - Permissions
# - Icons
```

### Step 2: Build

```bash
# Full release build (recommended)
buildozer android release

# Or debug build (faster)
buildozer android debug
```

### Step 3: Output

The generated APK will be at:
```
android_app/bin/docuvoice-1.0.0-release.apk
```

## Installation on Android Device

### Via USB

```bash
# Connect Android device with USB debugging enabled
adb install bin/docuvoice-1.0.0-release.apk
```

### Via File Transfer

1. Copy APK to Android device
2. Open file manager
3. Tap the APK to install
4. Grant permissions when prompted

## Usage

1. **Launch the app** on your Android device
2. **Grant permissions** for microphone and storage
3. **Choose an option:**
   - Text to Speech: Enter text and convert
   - Word to Speech: Select .docx file and convert
   - Voice Recording: Record and save audio

## Troubleshooting

### Build Fails: "buildozer: command not found"
```bash
pip install buildozer --upgrade
```

### Java not found
```bash
# Windows
# Download JDK from https://www.oracle.com/java/technologies/downloads/

# Or set JAVA_HOME:
export JAVA_HOME=/path/to/jdk
```

### Gradle build fails
```bash
# Clean build directory
buildozer android clean

# Rebuild
buildozer android release
```

### App crashes on startup
1. Check `adb logcat` for error messages
2. Verify backend URL is accessible
3. Check permissions are granted
4. Ensure network connectivity

### Permissions not working
Update `buildozer.spec` and rebuild:
```ini
android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
```

## Deployment

### Release Build (for Play Store)

1. **Sign the APK:**
   ```bash
   buildozer android release
   ```

2. **Generate signed APK for Play Store:**
   - Use Android Studio's "Generate Signed Bundle"
   - Or use jarsigner with a keystore

3. **Upload to Google Play Console**

### Direct Distribution

1. Host APK on your server
2. Create download link
3. Users can install directly from link
4. Enable "Unknown Sources" in Android Settings

## Backend Integration

The app connects to the Flask backend for processing:

- **Text to Speech:** POST `/text-to-audio`
- **Word to Speech:** POST `/word-to-audio`
- **Save Voice:** POST `/save-voice`
- **Job Status:** GET `/job-status/<job_id>`

Ensure Flask server is running and accessible from Android device.

## Performance Tips

- Build on SSD for faster compilation
- First build takes longer (downloads dependencies)
- Subsequent builds are faster
- Debug builds (~2-5 min) faster than release builds (~10-20 min)

## Security

⚠️ **Important for Production:**

1. Use HTTPS for backend connections
2. Implement authentication
3. Validate user input
4. Add API rate limiting
5. Sign APK with production keystore
6. Test on real devices before release

## Support & Troubleshooting

For issues with:

- **Kivy:** https://kivy.org/doc/stable/
- **Buildozer:** https://buildozer.readthedocs.io/
- **Android:** https://developer.android.com/docs
- **Flask:** https://flask.palletsprojects.com/

## License

This app is part of the DocuVoice project.

## Version

- App Version: 1.0.0
- Built with: Kivy 2.2.1
- Target SDK: 31
- Min SDK: 21

---

Generated: February 2026
