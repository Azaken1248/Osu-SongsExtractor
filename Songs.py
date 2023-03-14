import os
import time
from PyQt5 import QtWidgets, QtGui, QtCore

# Create a PyQt application
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont

import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')

import ctypes
if hasattr(ctypes.windll, "kernel32"):
    try:
        # Hide the console window
        ctypes.windll.kernel32.SetConsoleWindowInfo(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

app = QtWidgets.QApplication([])
app.setStyle('Fusion')

# Define a high contrast dark color palette for the application
dark_palette = QtGui.QPalette()
dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 69, 255))
dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(0, 0, 0))
dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 69, 255))
dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
app.setPalette(dark_palette)

# Ask the user to select a folder and get its path
folder_path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder')

# Create a new folder called "MySongs" on the desktop
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
new_folder_path = os.path.join(desktop_path, 'MySongs')
os.makedirs(new_folder_path, exist_ok=True)

# Create a PyQt window for the progress bar
window = QtWidgets.QWidget()
window.setWindowTitle('Copying files')
window.setFixedSize(300, 80)
layout = QtWidgets.QVBoxLayout()
layout.setContentsMargins(10, 10, 10, 10)
progress_bar = QtWidgets.QProgressBar()
progress_bar.setRange(0, 100)
layout.addWidget(progress_bar)
window.setLayout(layout)


# Define a function to update the progress bar
def update_progress(percent):
    progress_bar.setValue(percent)
    app.processEvents()

# Define a function to copy a file and show the progress
def copy_file_with_progress(src_path, dest_path):
    src_size = os.stat(src_path).st_size
    progress = 0
    block_size = 1024 * 1024 # Copy files in 1 MB chunks
    with open(src_path, 'rb') as src_file:
        with open(dest_path, 'wb') as dest_file:
            while True:
                data = src_file.read(block_size)
                if not data:
                    break
                dest_file.write(data)
                progress += len(data)
                percent = int(progress / src_size * 100)
                update_progress(percent)

# Recursively search for MP3 files in nested folders
AUDIO_FILE_EXTENSIONS = (".3gp",    ".aa",    ".aac",    ".aax",    ".act",    ".aiff",    ".alac",    ".amr",    ".ape",    ".au",    ".awb",    ".dss",    ".dvf",    ".flac",    ".gsm",    ".iklax",    ".ivs",    ".m4a",    ".m4b",    ".m4p",    ".mmf",    ".mp3",    ".mpc",    ".msv",    ".nmf",    ".ogg",    ".oga",    ".mogg",    ".opus",    ".ra",    ".rm",    ".raw",    ".rf64",    ".sln",    ".vox",    ".wav",    ".wma",    ".wv",    ".webm")


# Recursively search for audio files in nested folders
def find_audio_files(folder_path, audio_formats):
    total_files = 0
    for root, _, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.lower().endswith(audio_formats):
                total_files += 1

    # Create the progress bar for the overall progress
    window = QtWidgets.QWidget()
    window.setWindowTitle('Copying files')
    window.setWindowIcon(QtGui.QIcon("ppy.png"))
    window.setFixedSize(400,200)
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)


    image_path = 'ppy.png'  # Replace with your image file path
    image = QtGui.QPixmap(image_path)
    image = image.scaled(100, 100, QtCore.Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

    # Create a QHBoxLayout for the image and text labels
    hbox = QtWidgets.QHBoxLayout()

    # Create a QLabel widget for the image and set its size
    image_label = QtWidgets.QLabel()
    image_label.setPixmap(image)
    image_label.setFixedSize(image.size())

    # Create a QLabel widget for the text label
    text_label = QtWidgets.QLabel()
    text_label.setText("Copying Files.")
    text_label.setFont(QFont("MV Boli", 15))
    text_label.setStyleSheet("color: pink; background-color: black;")

    # Add the image and text labels to the QHBoxLayout
    hbox.addWidget(image_label, alignment=QtCore.Qt.AlignLeft)
    hbox.addStretch()
    hbox.addWidget(text_label, alignment=QtCore.Qt.AlignCenter)
    hbox.addStretch()

    # Set the stretch factor of the first and last stretch to 1
    hbox.setStretch(0, 1)
    hbox.setStretch(3, 1)

    # Add the QHBoxLayout to the main layout
    layout.addLayout(hbox)

    # Define a function to update the text label
    def update_label():
        text = text_label.text()
        if text.endswith("...."):
            text = "Copying Files."
        else:
            text += "."
        text_label.setText(text)

    # Start the animation when the button is clicked
    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(1000)  # Update label every second

    progress_bar = QtWidgets.QProgressBar()
    progress_bar.setRange(0, total_files)
    progress_bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid white;
            border-radius: 5px;
            background-color: black;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: pink;
            width: 20px;
        }
    """)
    layout.addWidget(progress_bar)
    window.setLayout(layout)
    window.show()

    # Copy the audio files to the new folder and update the progress bar
    progress = 0
    for root, _, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.lower().endswith(audio_formats):
                new_filepath = os.path.join(new_folder_path, filename)
                copy_file_with_progress(filepath, new_filepath)
                progress += 1
                progress_bar.setValue(progress)
                app.processEvents()

# Create the progress bar for the overall progress
start_time = time.time()
find_audio_files(folder_path,AUDIO_FILE_EXTENSIONS)

end_time = time.time()
#print(f'Total time taken: {round(end_time - start_time, 2)} seconds')

icon = QIcon("C:\\Users\\Rohit Sinha\\PycharmProjects\\OpenAI\\ppy.png")

msg_box = QtWidgets.QMessageBox()
msg_box.setIconPixmap(icon.pixmap(120,120))
msg_box.setWindowTitle("Copying files")
msg_box.setText(f'All songs have been copied to the new folder~~\n\nTotal time taken: {round(end_time - start_time, 2)}s')
ok_button = msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
msg_box.setStyleSheet("QLabel{color: pink; background-color: black;} QPushButton{background-color: black; color: pink;}"
                       "QPushButton:hover{background-color: pink;color - black}")
msg_box.setFont(QFont("MV Boli",12))
msg_box.setWindowIcon(QtGui.QIcon('ppy.png')) # Add your icon file path here
msg_box.exec_()

app.exit()
