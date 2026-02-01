# DocuVoice Android App - Complete Setup Guide

## 📱 Project Overview

DocuVoice has been converted into a **native Android application** with all features intact:

✅ **Text to Speech** - Convert text input to audio
✅ **Word to Speech** - Convert .docx files to audio
✅ **Voice Recording** - Record and save audio
✅ **Cloud Backend** - Connects to your Flask server
✅ **Material Design UI** - Modern Android interface

## 📂 What's Included

```
android_app/
├── main.py                 # Kivy application source (MAIN FILE)
├── buildozer.spec         # Android build configuration
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker build environment
├── build.bat             # Windows build script
├── build.sh              # Linux/Mac build script
├── generate_apk.py       # APK generator utility
├── INSTALL.md            # Installation guide
├── README_BUILD.md       # Build documentation
└── build_config.json     # Auto-generated config (after first run)
```

## 🚀 Quick Start (Choose One Method)

### Method 1: Docker on Windows (RECOMMENDED)

**Fastest & Easiest - No complex setup!**

```cmd
cd android_app
build.bat
```

Wait 20-30 minutes, APK will be in `output/` folder.

### Method 2: WSL2 on Windows

```bash
wsl
cd /mnt/c/Users/Varunesh/Desktop/New\ folder/KANI/android_app
buildozer android release
```

### Method 3: Linux/Mac

```bash
cd android_app
chmod +x build.sh
./build.sh
```

### Method 4: Online (No Setup)

Visit: https://kivy2apk.appspot.com/
- Upload `main.py`
- Download APK in 5-10 minutes

## ⚙️ Pre-Build Configuration

**IMPORTANT:** Update the backend URL in `main.py` BEFORE building:

```python
# Line 40 (HomeScreen)
self.api_url = "http://192.168.0.12:5000"

# Line ~150 (TextToSpeechScreen)  
self.api_url = "http://192.168.0.12:5000"

# Line ~270 (WordToSpeechScreen)
self.api_url = "http://192.168.0.12:5000"
```

Replace `http://192.168.0.12:5000` with:
- Your actual IP address or domain
- Keep port 5000 if Flask runs on that port

Example:
```python
self.api_url = "http://docuvoice.example.com"
self.api_url = "http://192.168.1.100:5000"
self.api_url = "http://server.local:5000"
```

## 📋 Requirements for Building

### Using Docker (Windows - Easiest):
- Docker Desktop
- Internet connection
- ~20GB free space

### Using Local Build (Linux/Mac):
- Java 11+
- Python 3.7+
- Android SDK
- Android NDK 25b
- ~10GB free space
- 15-30 minutes

### Using Online:
- Internet browser
- No local setup needed!

## 🏗️ Building the APK

### Windows (Docker Method):

1. Open Command Prompt in `android_app` folder:
   ```cmd
   cd C:\Users\Varunesh\Desktop\New folder\KANI\android_app
   ```

2. Run:
   ```cmd
   build.bat
   ```

3. Wait for completion (~25 minutes)

4. Find APK in `output/` folder:
   ```
   output/docuvoice-1.0.0-release.apk
   ```

### Linux/Mac:

1. Navigate to folder:
   ```bash
   cd ~/Desktop/KANI/android_app
   ```

2. Make script executable:
   ```bash
   chmod +x build.sh
   ```

3. Run:
   ```bash
   ./build.sh
   ```

4. Find APK in `bin/` folder:
   ```
   bin/docuvoice-1.0.0-release.apk
   ```

## 📲 Installing on Android

### Option A: Via ADB (USB Cable)

```bash
adb devices  # List connected phones
adb install bin/docuvoice-1.0.0-release.apk
```

### Option B: Via File Transfer

1. Copy APK to phone (USB, cloud, etc.)
2. Open file manager
3. Tap APK file
4. Grant installation permissions
5. App installs automatically

### Option C: QR Code

1. Generate QR from APK download URL
2. Scan with phone camera
3. Tap notification to install

## ✅ First Run Checklist

After installation:

- [ ] Launch DocuVoice app
- [ ] Grant microphone permission when prompted
- [ ] Grant storage permission
- [ ] Test Text to Speech feature
- [ ] Test Word to Speech (upload .docx)
- [ ] Test Voice Recording feature
- [ ] Verify app connects to backend

## 🔧 Troubleshooting

### "Docker not found" (Windows)
→ Install Docker Desktop: https://www.docker.com/products/docker-desktop

### "buildozer command not found" (Linux/Mac)
```bash
pip3 install buildozer --upgrade
```

### "Java not found"
```bash
# Ubuntu/Debian
sudo apt-get install openjdk-11-jdk-headless

# macOS
brew install openjdk@11
```

### App crashes on startup
1. Check backend URL is correct in `main.py`
2. Ensure Flask server is running
3. Verify phone is on same network
4. Check firewall allows connections

### Microphone not working
1. Grant microphone permission in app settings
2. Check Android Settings > Apps > DocuVoice > Permissions
3. Test microphone with system voice recording app

### File upload fails
1. Check storage permission is granted
2. Ensure .docx file exists on device
3. Verify file is not corrupted

## 📊 Build Times

| Method | First Time | Subsequent | Notes |
|--------|-----------|-----------|-------|
| Docker | 20-30 min | 15-20 min | Easiest, no setup |
| WSL2 | 15-25 min | 10-15 min | Windows Linux layer |
| Local Linux | 10-20 min | 5-10 min | Fastest but complex |
| Online | 5-10 min | 5-10 min | No setup needed |

## 🎯 Architecture

```
┌─────────────────────────────────────┐
│     Android Phone (Kivy App)        │
│  ┌─────────────────────────────┐   │
│  │ Text-to-Speech Screen       │   │
│  │ Word-to-Speech Screen       │   │
│  │ Voice Recording Screen      │   │
│  │ Home/Navigation             │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │ HTTP API
               ▼
┌─────────────────────────────────────┐
│    Flask Backend Server             │
│  ┌─────────────────────────────┐   │
│  │ /text-to-audio  (gTTS)      │   │
│  │ /word-to-audio  (pydub)     │   │
│  │ /save-voice     (recording) │   │
│  │ /job-status     (tracking)  │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## 📝 App Features

### Text to Speech
- Input: Text via keyboard
- Output: MP3 audio file
- Backend: gTTS (Google Text-to-Speech)
- Storage: Uploaded to backend

### Word to Speech
- Input: .docx files from device
- Processing: Per-paragraph conversion
- Output: Combined MP3 audio
- Backend: python-docx + gTTS + pydub

### Voice Recording
- Input: Microphone audio
- Duration: Configurable (default 5 sec)
- Format: WAV
- Upload: To backend server

## 🔒 Security Notes

⚠️ **For Production:**
- Use HTTPS instead of HTTP
- Implement authentication
- Add rate limiting
- Validate all inputs
- Use signed APK with keystore
- Test thoroughly before release

## 📦 APK Details

- **Name:** docuvoice-1.0.0-release.apk
- **Size:** ~25-40 MB
- **Target SDK:** 31 (Android 12)
- **Min SDK:** 21 (Android 5.0)
- **Architecture:** ARM 32-bit & 64-bit
- **Permissions:** Internet, Microphone, Storage

## 🌐 Network Setup

**On Local Network:**
```
Phone ──HTTP──→ Computer (Running Flask)
```

**Requirements:**
- Phone on same WiFi as computer
- Firewall allows port 5000
- Computer Flask app running

**Find Your IP:**
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

Look for address like: `192.168.x.x`

## 🚚 Deployment

### Development
```
1. Start Flask server on your computer
2. Update backend URL in main.py
3. Build APK
4. Test on phone connected to same WiFi
```

### Production
```
1. Deploy Flask server on cloud (AWS, Heroku, etc.)
2. Use HTTPS with SSL certificate
3. Sign APK with production keystore
4. Update backend URL to production server
5. Publish on Google Play Store
```

## 📚 Additional Resources

- **Kivy Documentation:** https://kivy.org/doc/stable/
- **Buildozer Docs:** https://buildozer.readthedocs.io/
- **Android Dev Guide:** https://developer.android.com/guide
- **Flask Guide:** https://flask.palletsprojects.com/
- **Google Play Publish:** https://play.google.com/console

## 🎬 Next Steps

1. **Verify Flask backend is running:**
   ```bash
   cd word_to_audio
   python app.py
   ```

2. **Update backend URL in `android_app/main.py`**

3. **Choose build method and build APK:**
   - Windows: `build.bat`
   - Linux/Mac: `bash build.sh`
   - Online: Visit kivy2apk.appspot.com

4. **Install on Android device**

5. **Test all features**

6. **Deploy to production**

## 📞 Support

For help with:
- **Kivy issues:** Kivy community forums
- **Android issues:** Android Stack Overflow
- **Flask issues:** Flask documentation
- **Build issues:** Buildozer documentation

## ✨ What's New in Android Version

✅ Native Android interface
✅ Material Design UI
✅ Better performance
✅ Offline support for recordings
✅ Improved error handling
✅ Cleaner button/screen layout
✅ Real-time status updates
✅ Easier permission management

## 📄 License & Credits

Built with:
- **Kivy** - Open source Python framework
- **Buildozer** - Build tool for APK generation
- **Flask** - Backend server framework
- **gTTS** - Google Text-to-Speech
- **python-docx** - Word document processing
- **pydub** - Audio processing

---

## ⏱️ Estimated Timeline

| Task | Time |
|------|------|
| Setup environment | 5-15 min |
| Configure settings | 2-5 min |
| Build APK | 15-30 min |
| Install on phone | 2-5 min |
| Test features | 5-10 min |
| **TOTAL** | **30-60 min** |

---

**Good luck with your Android app! 🚀**

For questions or issues, refer to the documentation files:
- `INSTALL.md` - Detailed installation guide
- `README_BUILD.md` - Build documentation
- `generate_apk.py` - Run for interactive setup guide

Generated: February 2026
