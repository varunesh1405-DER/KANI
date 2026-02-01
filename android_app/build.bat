@echo off
REM DocuVoice Android APK Builder for Windows (using Docker)

echo.
echo ======================================
echo DocuVoice Android APK Builder
echo ======================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed!
    echo Please install Docker from: https://www.docker.com/products/docker-desktop
    echo.
    exit /b 1
)

echo [OK] Docker found

REM Check if Docker daemon is running
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker daemon is not running!
    echo Please start Docker Desktop and try again.
    echo.
    exit /b 1
)

echo [OK] Docker daemon is running

REM Create output directory
if not exist "output" (
    mkdir output
    echo [OK] Created output directory
)

REM Build Docker image
echo.
echo Building Docker image...
docker build -t docuvoice-builder .

if errorlevel 1 (
    echo [ERROR] Failed to build Docker image
    exit /b 1
)

echo [OK] Docker image built successfully

REM Run build in container
echo.
echo Starting APK build in Docker container...
echo This may take 15-30 minutes...
echo.

docker run --rm -v "%cd%\output":/output docuvoice-builder

if errorlevel 1 (
    echo [ERROR] Build failed
    exit /b 1
)

echo.
echo ======================================
echo Build completed!
echo ======================================
echo.

if exist "output\*.apk" (
    echo [OK] APK file generated in output\ directory
    for %%F in (output\*.apk) do (
        echo File: %%F
        echo Size: For size run: dir /s output
    )
) else (
    echo [WARNING] APK file not found in output directory
)

echo.
echo Next steps:
echo 1. Transfer APK to your Android device
echo 2. Install the APK
echo 3. Grant necessary permissions
echo 4. Configure backend URL in app settings
echo.

pause
