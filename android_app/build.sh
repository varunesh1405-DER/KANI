#!/bin/bash

# DocuVoice Android APK Builder

echo "======================================"
echo "DocuVoice Android APK Builder"
echo "======================================"
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "[ERROR] buildozer is not installed!"
    echo "Install with: pip install buildozer"
    exit 1
fi

echo "[OK] buildozer found"

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "[ERROR] Java is not installed!"
    echo "Install with: sudo apt-get install openjdk-11-jdk"
    exit 1
fi

echo "[OK] Java found"

# Create output directory
mkdir -p bin
echo "[OK] Build directory ready"

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
buildozer android clean

# Build APK
echo ""
echo "Building APK..."
echo "This may take 10-30 minutes..."
echo ""

buildozer android release

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Build completed successfully!"
    echo "======================================"
    echo ""
    
    if ls bin/*.apk 1> /dev/null 2>&1; then
        echo "[OK] APK files generated:"
        ls -lh bin/*.apk
    fi
else
    echo ""
    echo "[ERROR] Build failed!"
    echo "Check the output above for errors"
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. Transfer APK to your Android device"
echo "2. Enable 'Unknown Sources' in Android Settings"
echo "3. Install the APK"
echo "4. Grant necessary permissions"
echo ""
