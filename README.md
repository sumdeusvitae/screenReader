# Installation Guide

If you're using **Windows OS**, you will need the `tesseract.exe` binary for proper installation of the Tesseract OCR library. You can download it from the official [installation page](https://github.com/UB-Mannheim/tesseract/wiki).

### Steps:

1. **Create a `.env` file** in your project directory.
2. Add the following line to the `.env` file, updating the path to the location where `tesseract.exe` is installed on your system:

   ```text
   TESSERACT_PATH = C:\Program Files\Tesseract-OCR\tesseract.exe
   ```
Make sure to change the path to match your installation location.

# Install Dependencies:

Run the following command to install the necessary Python packages:
```bash
pip install -r requirements.txt
```

# Run App:

```bash
python main.py
```