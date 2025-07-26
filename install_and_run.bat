@echo off
echo.
echo ========================================
echo    🔥 ChakraBeats Installation 🔥
echo ========================================
echo.
echo Welcome to ChakraBeats - Anime Music Player!
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available!
    echo.
    echo Please ensure pip is installed with Python.
    echo.
    pause
    exit /b 1
)

echo ✅ pip found!
echo.

REM Install dependencies
echo 📦 Installing ChakraBeats dependencies...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Failed to install dependencies!
    echo.
    echo Please try running the following commands manually:
    echo pip install PyQt6==6.6.1
    echo pip install pygame==2.5.2
    echo pip install mutagen==1.47.0
    echo pip install Pillow==10.1.0
    echo pip install numpy==1.24.3
    echo pip install matplotlib==3.7.2
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.

REM Ask user if they want to run ChakraBeats
echo ========================================
echo    🎵 Ready to Launch ChakraBeats! 🎵
echo ========================================
echo.
set /p choice="Do you want to launch ChakraBeats now? (y/n): "

if /i "%choice%"=="y" (
    echo.
    echo 🚀 Launching ChakraBeats...
    echo.
    python launcher.py
) else (
    echo.
    echo To run ChakraBeats later, use one of these commands:
    echo   python launcher.py    (with splash screen)
    echo   python main.py        (direct launch)
    echo.
    echo Thank you for installing ChakraBeats!
    echo Channel your inner anime protagonist! 🔥⚡🌊🐉
    echo.
    pause
) 