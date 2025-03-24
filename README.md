# Screen Reader

## Overview
This is a lightweight Windows application that provides an adjustable overlay frame for selecting a screenshot area. The selected area is then processed using OCR (Optical Character Recognition) with Tesseract-OCR, and the extracted text is copied to the clipboard.

## Features
- Frameless overlay window for selecting a screenshot area
- Adjustable and resizable frame
- Extracts text from screenshots using Tesseract-OCR
- Copies extracted text to the clipboard automatically
- Simple GUI with settings to configure Tesseract-OCR path

## Prerequisites
Ensure you have the following installed on your system:
- **Python 3.8+**
- **Tesseract-OCR** (Download from [here](https://github.com/tesseract-ocr/tesseract))
- Required Python packages (see Installation section)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/repository-name.git
   cd repository-name
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Tesseract-OCR is installed and the correct path is set. The default path for Windows is:
   ```
   C:\Program Files\Tesseract-OCR\tesseract.exe
   ```
   If necessary, update the path in the application settings.

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. Adjust the overlay frame to select the desired screen area.
3. Click the **Capture Screenshot** button.
4. The extracted text will be copied to the clipboard.
5. Configure Tesseract-OCR path in settings if OCR fails.

## Dependencies
This project relies on the following libraries:
- `PySide6`
- `pyautogui`
- `pytesseract`
- `pyperclip`

Run the following command to install the necessary Python packages:
```bash
pip install -r requirements.txt
```

## Troubleshooting
- **OCR not working?** Ensure Tesseract-OCR is installed and the path is correctly set in the application.
- **App not capturing correctly?** Try adjusting the overlay frame and ensure the region is properly selected.
- **Permission issues?** Run the script as an administrator.

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to submit a pull request.

