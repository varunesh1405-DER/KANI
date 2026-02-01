@echo off
REM DocuVoice Local APK Builder for Windows (no Docker)
REM This script builds the APK using buildozer installed locally

setlocal enabledelayedexpansion

echo.
echo ======================================
echo DocuVoice Local APK Builder
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python from: https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found

REM Check if buildozer is installed
python -c "import buildozer" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] buildozer not found
    echo Installing buildozer and dependencies...
    echo.
    pip install -q buildozer cython kivy requests pyjnius
    if errorlevel 1 (
        echo [ERROR] Failed to install buildozer
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] buildozer found
)

REM Check if Java is installed
java -version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Java Development Kit not found
    echo Please install JDK 11+ from: https://www.oracle.com/java/technologies/downloads/
    echo After installing Java, run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Java found

echo.
echo ======================================
echo Starting Local APK Build
echo ======================================
echo.
echo This will take 15-30 minutes...
echo (First run downloads Android SDK - may take longer)
echo.

REM Run buildozer
buildozer android release

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed
    echo.
    echo Troubleshooting:
    echo - Check buildozer.spec configuration
    echo - Ensure Java path is set correctly
    echo - Check available disk space (need ~10GB)
    echo.
    pause
    exit /b 1
)

echo.
echo ======================================
echo Build Completed Successfully!
echo ======================================
echo.

REM Check for generated APK
if exist "bin\*.apk" (
    echo [OK] APK generated in bin\ directory
    for /f %%F in ('dir /b bin\*.apk 2^>nul') do (
        echo File: %%F
        echo.
        echo Next steps:
        echo 1. Transfer APK to your Android device
        echo 2. Install: adb install bin\%%F
        echo 3. Or copy file and tap to install on device
        echo.
    )
) else (
    echo [WARNING] APK not found in bin directory
)

echo.
pause
