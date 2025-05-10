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

## License
This project is licensed under the MIT License.