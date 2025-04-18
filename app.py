import json
import os
import threading
import time
import pygetwindow
from PySide6.QtCore import Signal, QTimer, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from pynput.keyboard import Controller

from demo import Ui_MainWindow

windows = pygetwindow.getWindowsWithTitle("Sky")

sky = None

for window in windows:
    if window.title == "Sky":
        sky = window

def focusWindow():
    try:
        sky.activate()
    except:
        sky.minimize()
        sky.restore()

keyboard = Controller()

key_maps = {
    '1Key0': 'y',
    '1Key1': 'u',
    '1Key2': 'i',
    '1Key3': 'o',
    '1Key4': 'p',
    '1Key5': 'h',
    '1Key6': 'j',
    '1Key7': 'k',
    '1Key8': 'l',
    '1Key9': ';',
    '1Key10': 'n',
    '1Key11': 'm',
    '1Key12': ',',
    '1Key13': '.',
    '1Key14': '/',
    '2Key0': 'y',
    '2Key1': 'u',
    '2Key2': 'i',
    '2Key3': 'o',
    '2Key4': 'p',
    '2Key5': 'h',
    '2Key6': 'j',
    '2Key7': 'k',
    '2Key8': 'l',
    '2Key9': ';',
    '2Key10': 'n',
    '2Key11': 'm',
    '2Key12': ',',
    '2Key13': '.',
    '2Key14': '/'
}

class SongPlayerThread(QThread):
    log_signal = Signal(str)

    def __init__(self, song_data,):
        super().__init__()
        self.song_data = song_data

    def run(self):
        song_notes = self.song_data['songNotes']
        start_time = time.perf_counter()
        pause_time = 0

        for i, note in enumerate(song_notes):
            if sky.isActive:
                note_time = note['time']
                note_key = note['key']
                key_thread = KeyPressThread(note_time, note_key)
                key_thread.start()

                elapsed_time = time.perf_counter() - start_time - pause_time

                if i < len(song_notes) - 1:
                    next_note_time = song_notes[i + 1]['time']
                    wait_time = (next_note_time - note_time) / 1000
                    remaining_time = max(0, note_time / 1000 + wait_time - elapsed_time)
                    time.sleep(remaining_time)
            else:
                self.log_signal.emit("⏸ Sky is not focused, pausing...")
                paused_time_start = time.perf_counter()
                while not sky.isActive:
                    time.sleep(1)
                paused_time_end = time.perf_counter()
                pause_time += paused_time_end - paused_time_start
                self.log_signal.emit("▶ Resuming song...")

        self.log_signal.emit(f"✅ Finished playing {self.song_data['name']}")


class KeyPressThread(threading.Thread):
    def __init__(self, note_time, note_key):
        super().__init__()
        self.note_time = note_time
        self.note_key = note_key

    def run(self):
        if self.note_key in key_maps:
            keyboard.press(key_maps[self.note_key])
            time.sleep(0.02)  # short delay to ensure note is pressed
            keyboard.release(key_maps[self.note_key])  # release key
        else:
            print("Skipped: Key not found in mapping")

class ClickableLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if folder:
            self.setText(folder)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.folder_path = ""
        self.song_data = ""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.comboBoxCodec.addItem("utf-8")
        self.ui.comboBoxCodec.addItem("utf-16")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.is_counting_down = False

        self.ui.lineEditFolder.setVisible(False)

        self.lineEditCustom = ClickableLineEdit(self)
        self.lineEditCustom.setGeometry(self.ui.lineEditFolder.geometry())
        self.lineEditCustom.setText("Click to choose folder")
        self.ui.btnSelectFolder.clicked.connect(self.show_files_in_folder)
        self.ui.pushButtonPlay.clicked.connect(self.on_button_click)
        self.ui.pushButtonCancel.clicked.connect(self.cancel_song)
        if sky == None:
            self.ui.plainTextEditLog.appendPlainText(
                "Sky was not detected, please open Sky before playing songs.")
            # quit()

    def on_button_click(self):
        if self.start_play():
            self.start_countdown()
        else:
            self.ui.plainTextEditLog.clear()
            self.ui.plainTextEditLog.appendPlainText("⛔ Can't play song.")

    def start_countdown(self):
        if self.is_counting_down:
            return
        self.is_counting_down = True
        self.countdown = 3
        self.ui.plainTextEditLog.clear()
        self.timer.start(1000)
        return False

    def update_countdown(self):
        if self.countdown > 0:
            self.ui.plainTextEditLog.appendPlainText(f"Playing song in {self.countdown}")
            self.countdown -= 1
        else:
            self.timer.stop()
            self.is_counting_down = False
            self.ui.plainTextEditLog.appendPlainText("▶ Start!")
            self.play_song()

    def cancel_song(self):
        if hasattr(self, 'player_thread') and self.player_thread.isRunning():
            self.player_thread.terminate()
            self.player_thread.wait()


        self.ui.plainTextEditLog.clear()
        self.ui.comboBoxCodec.setCurrentIndex(0)
        self.ui.lineEditFolder.setText("")
        self.ui.plainTextEditLog.appendPlainText("⏸ Canceling song")

        if self.timer.isActive():
            self.timer.stop()
            self.countdown = 3

    def show_files_in_folder(self ):
        self.folder_path = self.lineEditCustom.text()
        if not self.folder_path or not os.path.isdir(self.folder_path):
            self.ui.listWidgetListFiles.clear()
            self.ui.listWidgetListFiles.addItems(["❌ Folder is invalid."])
            return

        files = os.listdir(self.folder_path)
        if not files:
            self.ui.listWidgetListFiles.clear()
            self.ui.listWidgetListFiles.addItems(["📁 Folder has no files."])
            return

        only_files = [f for f in files if os.path.isfile(os.path.join(self.folder_path, f))]

        self.ui.listWidgetListFiles.clear()
        self.ui.listWidgetListFiles.addItems(only_files)

    def start_play(self):
        self.ui.plainTextEditLog.appendPlainText('debug')
        item = self.ui.listWidgetListFiles.currentItem().text()
        codec = self.ui.comboBoxCodec.currentText()
        try:
            with open(f'{self.folder_path}/{item}', 'r', encoding=codec) as file:
                self.song_data = json.load(file)
            return True

        except FileNotFoundError:
            self.ui.plainTextEditLog.clear()
            self.ui.plainTextEditLog.appendPlainText("Song not found.")
            return False
        except UnicodeDecodeError as e:
            self.ui.plainTextEditLog.clear()
            self.ui.plainTextEditLog.appendPlainText(f"❌ Can't read file : {e}")
            return False

    def play_song(self):
        self.player_thread = SongPlayerThread(self.song_data[0])
        self.player_thread.log_signal.connect(self.ui.plainTextEditLog.appendPlainText)
        self.player_thread.start()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
