# Internet Speed Meter

A lightweight desktop widget to monitor your internet download and upload speeds in real-time, built with Python and PyQt5.

## Features
- Displays download and upload speeds in KB/s.
- Customizable appearance (background color, theme, opacity, icon size).
- Option to hide speed labels.
- Auto-start on Windows startup.
- Resizable widget (drag the bottom-right corner).

## Installation

### Prerequisites
- Python 3.6 or higher
- Required Python libraries:
  ```bash
  pip install pyqt5 psutil winshell
  ```

### Running the Script
1. Clone or download this repository.
2. Ensure `download_icon.png` and `upload_icon.png` are in the same directory as the script.
3. Run the script:
   ```bash
   python internet-speed-widget.py
   ```

### Creating an Executable
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Convert your PNG logo to ICO format (e.g., using Pillow):
   ```bash
   pip install Pillow
   python -c "from PIL import Image; Image.open('logo.png').save('logo.ico', format='ICO')"
   ```
3. Build the executable:
   ```bash
   pyinstaller --onefile --noconsole --icon=logo.ico --add-data "download_icon.png;." --add-data "upload_icon.png;." internet-speed-widget.py
   ```
4. Find the executable in the `dist` folder.

## Usage
- **Launch**: Double-click `internet-speed-widget.exe` (or run the script with Python).
- **Move**: Click and drag the widget to reposition it.
- **Resize**: Drag the bottom-right corner to resize (currently under debugging).
- **Customize**: Right-click the widget or tray icon to access options like changing the background color, toggling themes, adjusting opacity, and more.
- **Run on Startup**: Enable "Run on Startup" in the context menu to start the widget automatically on Windows boot.

## Troubleshooting
- **Icons Not Showing**: If the upload/download icons appear as colored squares, ensure `download_icon.png` and `upload_icon.png` are in the same directory as the script when building the executable.
- **Resizing Not Working**: This feature is under debugging. Check the console output for debug messages when attempting to resize.
- **Startup Issues**: Ensure `winshell` is installed (`pip install winshell`) for the "Run on Startup" feature to work.

## License
This project is licensed under the MIT License.