# AudioFix

AudioFix is a utility designed to monitor and manage the memory usage of the `audiodg.exe` process, which is responsible for audio processing on Windows. This tool was created to address a specific issue with Wave Link 3.0 (currently in beta), where a memory leak causes audio crackling when the process consumes too much RAM. AudioFix forcefully restarts the process to resolve this issue.

## Features

- **Memory Monitoring**: Continuously monitors the memory usage of `audiodg.exe`.
- **Threshold-Based Restart**: Automatically restarts the process if its memory usage exceeds 400 MB (default threshold).
- **System Tray Integration**: Displays a tray icon (if `pystray` and `Pillow` are installed) to indicate the process status:
  - **Gray**: `audiodg.exe` is not running.
  - **Green**: `audiodg.exe` is running and within the memory threshold.
  - **Red**: `audiodg.exe` exceeded the memory threshold and was restarted.
- **Console Fallback**: Runs in the console if tray libraries are unavailable.

## Requirements

- Python 3.8 or higher
- Administrator privileges (required to manage the `audiodg.exe` process)
- Dependencies listed in `requirements.txt`:
  - `psutil`
  - `pystray`
  - `Pillow`

## Installation

1. Clone this repository or download the source code.
2. Create a virtual environment in the project directory:
   ```powershell
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

1. Run the application using the provided batch script:
   ```powershell
   .\run_audiofix.bat
   ```
   - This script ensures the application runs in the background, using `pythonw.exe` if available.
2. Ensure the application is run as an administrator. Otherwise it can't kill the `audiodg.exe` process.

## Notes

- The default memory threshold is set to 400 MB. You can adjust this value by modifying the `THRESHOLD_MB` variable in `audiofix.py`.
- The application is designed to handle the memory leak issue in Wave Link 3.0 beta, but it can be used for other scenarios where `audiodg.exe` memory management is required.

## Troubleshooting

- If the tray icon does not appear, ensure `pystray` and `Pillow` are installed.
- If you encounter issues with the batch script, verify that the virtual environment is correctly set up in the `.venv` directory.
- For debugging, you can run the script directly in the console:
  ```powershell
  python audiofix.py
  ```

## License

This project is provided as-is, without any warranty. Use at your own risk.