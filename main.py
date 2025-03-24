import sys
import pyautogui
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox
import ctypes  # Import ctypes to fix DPI issues
import os
import pytesseract
import pyperclip
import platform
import subprocess

variable_name = "TESSERACT_PATH"

def setTesseractPath(variable_name):
    # Check if the environment variable exists
    if not os.environ.get(variable_name):
        print(f"Environment variable '{variable_name}' does not exist.")
        
        # Set default value for Tesseract path
        default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        # Check the operating system
        system = platform.system()

        if system == "Windows":
            # Set the Tesseract path for Windows using setx
            os.environ[variable_name] = default_path
            # Construct the setx command
            try:
                os.system(f'setx {variable_name} "{default_path}"')
                print(f"Setting environment variable '{variable_name}' for Windows.")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")  
        
        elif system == "Linux" or system == "Darwin":  # Darwin is for macOS
            # Set the Tesseract path for Linux/macOS
            # Modify the ~/.bashrc or ~/.zshrc to include the variable
            home_dir = os.path.expanduser("~")
            shell_config_file = os.path.join(home_dir, '.bashrc' if system == 'Linux' else '.zshrc')
            
            with open(shell_config_file, 'a') as file:
                file.write(f'\nexport {variable_name}="{default_path}"\n')
            
            # You may also want to notify the user to reload the shell config
            print(f"Added Tesseract path to {shell_config_file}. Please reload your shell.")
        
        else:
            print(f"Unsupported system: {system}")
    else:
        print(f"Environment variable '{variable_name}' already exists with value: {os.environ[variable_name]}")

    # Disable the DPI awareness (this suppresses the warning)
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Disables DPI awareness
    except Exception as e:
        print(f"DPI awareness setting failed: {e}")


def transfer(file, tesseract_path):
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    # Perform OCR to extract text
    text = pytesseract.image_to_string(file)

    # Copy the extracted text to the clipboard
    pyperclip.copy(text)

    # Print the extracted text
    # print(text)


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(300, 255, 400, 300)  # Initial position and size
        self.dragging = False
        self.resizing = False
        self.offset = None
        self.tesLoc = os.environ[variable_name]

        # Capture button
        self.capture_button = QPushButton("Capture Screenshot", self)
        self.capture_button.setGeometry(10, 10, 150, 30)
        self.capture_button.clicked.connect(self.capture_screenshot)
        
        # Settings button
        settings_button = QPushButton("Settings", self)
        settings_button.setGeometry(250, 10, 50, 30)   
        settings_button.clicked.connect(self.setting)

        # Exit button
        exit_button = QPushButton("Exit", self)
        exit_button.setGeometry(325, 10, 50, 30)
        exit_button.clicked.connect(self.close)
    
    def close(self):
        os._exit(0)
        
    def setting(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.tesLoc = file_path
            global variable_name            
            try:
                os.system(f'setx {variable_name} "{file_path}"')
            except subprocess.CalledProcessError as e:
                self.show_error("An error occurred during setting the environment variable.")
                


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
        try:
            transfer(screenshot, self.tesLoc)
        except Exception as e:
            self.show_error("An error occurred during OCR, please add path to tesseract.exe in settings")



    def show_error(self, message):
        alert = QMessageBox(self)
        alert.setIcon(QMessageBox.Icon.Critical)
        alert.setWindowTitle("Error")
        alert.setText(message)
        alert.exec()

if __name__ == "__main__":
    setTesseractPath(variable_name)
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()
    sys.exit(app.exec())
