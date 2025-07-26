# 🔥 ChakraBeats Installation Guide 🔥

## Prerequisites

### 1. Python Installation

**Option A: Download from Python.org (Recommended)**
1. Visit [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download Python 3.8 or higher for Windows
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Complete the installation

**Option B: Microsoft Store**
1. Open Microsoft Store
2. Search for "Python 3.11" or higher
3. Install the official Python app

### 2. Verify Python Installation

Open Command Prompt or PowerShell and run:
```bash
python --version
```

You should see something like: `Python 3.11.0`

## Installation Methods

### Method 1: Automatic Installation (Windows)

1. **Download ChakraBeats**
   - Extract the ZIP file to a folder of your choice
   - Navigate to the ChakraBeats folder

2. **Run the Installer**
   - Double-click `install_and_run.bat`
   - Follow the on-screen instructions
   - The script will automatically install dependencies and launch ChakraBeats

### Method 2: Manual Installation

1. **Open Command Prompt/PowerShell**
   - Press `Win + R`, type `cmd`, and press Enter
   - Or search for "Command Prompt" in Start menu

2. **Navigate to ChakraBeats folder**
   ```bash
   cd "C:\path\to\ChakraBeats"
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch ChakraBeats**
   ```bash
   python launcher.py
   ```

## Troubleshooting

### Common Issues

**Issue: "Python is not recognized"**
- Solution: Reinstall Python and ensure "Add Python to PATH" is checked
- Alternative: Use the full path to Python (e.g., `C:\Python311\python.exe`)

**Issue: "pip is not recognized"**
- Solution: Python installation may be incomplete. Reinstall Python
- Alternative: Use `python -m pip` instead of `pip`

**Issue: "ModuleNotFoundError"**
- Solution: Install missing dependencies manually:
  ```bash
  pip install PyQt6==6.6.1
  pip install pygame==2.5.2
  pip install mutagen==1.47.0
  pip install Pillow==10.1.0
  pip install numpy==1.24.3
  pip install matplotlib==3.7.2
  ```

**Issue: "Permission denied"**
- Solution: Run Command Prompt as Administrator
- Or use: `pip install --user -r requirements.txt`

**Issue: "Microsoft Visual C++ 14.0 is required"**
- Solution: Install Microsoft Visual C++ Build Tools
- Download from: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Audio Issues

**Issue: No sound output**
- Check system volume
- Ensure audio files are valid
- Try different audio files (.mp3, .wav, .ogg)

**Issue: Audio playback errors**
- Update audio drivers
- Try running as Administrator
- Check if files are corrupted

### Visual Issues

**Issue: Application looks wrong**
- Update graphics drivers
- Ensure Windows is up to date
- Try different themes in the app

## System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum (2GB recommended)
- **Storage**: 50MB for application + your music library
- **Audio**: Any audio output device
- **Graphics**: Any modern graphics card

## First Run

1. **Launch ChakraBeats**
   - Use `python launcher.py` for splash screen experience
   - Or `python main.py` for direct launch

2. **Add Music**
   - Click "➕ Add Songs" button
   - Select your audio files (.mp3, .wav, .ogg)
   - Supported formats: MP3, WAV, OGG

3. **Choose Your Chakra Mode**
   - ⚡ **Kaminari Mode**: High-energy anime openings
   - 🌊 **Susanoo Mode**: Emotional ballads and character themes
   - 🐉 **Dragon God Mode**: Epic battle music and AMVs

4. **Explore Features**
   - Try different visualization modes
   - View song metadata
   - Use shuffle and repeat modes
   - Adjust volume with chakra effects

## File Structure

```
ChakraBeats/
├── main.py                 # Main application
├── launcher.py             # Splash screen launcher
├── visualizer.py           # Enhanced visualizer
├── metadata_handler.py     # Metadata extraction
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── install_and_run.bat     # Windows installer
├── README.md               # Project documentation
├── INSTALLATION.md         # This file
└── sample_settings.json    # Example settings
```

## Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Verify Python installation**: `python --version`
3. **Check dependencies**: `pip list`
4. **Try running with verbose output**: `python main.py --verbose`

## Uninstallation

To remove ChakraBeats:

1. **Delete the ChakraBeats folder**
2. **Remove settings** (optional):
   - Delete `%APPDATA%\ChakraBeats\` folder
   - Or delete `chakrabeats_settings.json` from the app folder

3. **Remove Python dependencies** (optional):
   ```bash
   pip uninstall PyQt6 pygame mutagen Pillow numpy matplotlib
   ```

---

**ChakraBeats** - Channel your inner anime protagonist! 🔥⚡🌊🐉

*"Believe it!" - Naruto Uzumaki* 