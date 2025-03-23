import sys
import pyautogui
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
import ctypes  # Import ctypes to fix DPI issues
import os
from PIL import Image
import pytesseract
import pyperclip
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# !!!!!! IMPORTANT !!!!!!
# Set the Tesseract executable path in the environment variables
# Get the path to the Tesseract executable from the environment variables
tesseract_path = os.getenv("TESSERACT_PATH")



# Disable the DPI awareness (this suppresses the warning)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Disables DPI awareness
except Exception as e:
    print(f"DPI awareness setting failed: {e}")

def transfer(file):
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


    # Perform OCR to extract text
    text = pytesseract.image_to_string(file)

    # Copy the extracted text to the clipboard
    pyperclip.copy(text)

    # Print the extracted text
    print(text)


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(300, 255, 400, 300)  # Initial position and size
        self.dragging = False
        self.resizing = False
        self.offset = None

        # Capture button
        self.capture_button = QPushButton("Capture Screenshot", self)
        self.capture_button.setGeometry(10, 10, 150, 30)
        self.capture_button.clicked.connect(self.capture_screenshot)
        

        # Exit button
        exit_button = QPushButton("Exit", self)
        exit_button.setGeometry(170, 10, 50, 30)
        exit_button.clicked.connect(self.close)
    
    def close(self):
        os._exit(0)
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 6))  # Red border
        button_bottom = self.capture_button.geometry().bottom()  # Get bottom position of the button

        # Draw only the side and bottom borders normally
        painter.drawRect(0, button_bottom + 5, self.width() - 1, self.height() - button_bottom - 5)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.position().x() >= self.width() - 10 or event.position().y() >= self.height() - 10:
                self.resizing = True
            else:
                self.dragging = True
                self.offset = event.globalPosition().toPoint() - self.pos()  # Fixed!

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)  # Fixed!
        elif self.resizing:
            new_width = event.position().x()
            new_height = event.position().y()
            self.setGeometry(self.x(), self.y(), max(new_width, 50), max(new_height, 50))

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resizing = False

    def capture_screenshot(self):
        # Get the current overlay window position and size
        x, y, width, height = self.geometry().x(), self.geometry().y(), self.width(), self.height()
        # Capture the screen at the selected region
        screenshot = pyautogui.screenshot(region=(x+3, y+47, width-7, height-50))

        # Perform OCR on the screenshot
        transfer(screenshot)

        # Save the screenshot
        # print(f"Captured region: x={x}, y={y}, width={width}, height={height}")
        # screenshot.save("temp.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()
    sys.exit(app.exec())
