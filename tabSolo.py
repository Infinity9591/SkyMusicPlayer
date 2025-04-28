import json
import os
import threading
import time
import pygetwindow
from PySide6.QtCore import Signal, QTimer, QThread
from PySide6.QtWidgets import QWidget, QFileDialog, QLineEdit
from pynput.keyboard import Controller

from demo import Ui_MainWindow  # Nếu Tab1Widget chỉ dùng 1 phần thì nên cắt bớt import

keyboard = Controller()

key_maps = {
    '1Key0': 'y', '1Key1': 'u', '1Key2': 'i', '1Key3': 'o', '1Key4': 'p',
    '1Key5': 'h', '1Key6': 'j', '1Key7': 'k', '1Key8': 'l', '1Key9': ';',
    '1Key10': 'n', '1Key11': 'm', '1Key12': ',', '1Key13': '.', '1Key14': '/',
    '2Key0': 'y', '2Key1': 'u', '2Key2': 'i', '2Key3': 'o', '2Key4': 'p',
    '2Key5': 'h', '2Key6': 'j', '2Key7': 'k', '2Key8': 'l', '2Key9': ';',
    '2Key10': 'n', '2Key11': 'm', '2Key12': ',', '2Key13': '.', '2Key14': '/'
}

sky = None

class KeyPressThread(threading.Thread):
    def __init__(self, note_time, note_key):
        super().__init__()
        self.note_time = note_time
        self.note_key = note_key

    def run(self):
        if self.note_key in key_maps:
            keyboard.press(key_maps[self.note_key])
            time.sleep(0.02)
            keyboard.release(key_maps[self.note_key])
        else:
            print("Skipped: Key not found in mapping")

class SongPlayerThread(QThread):
    log_signal = Signal(str)

    def __init__(self, song_data):
        super().__init__()
        self.song_data = song_data

    def run(self):
        song_notes = self.song_data['songNotes']
        start_time = time.perf_counter()
        pause_time = 0

        for i, note in enumerate(song_notes):
            if sky and sky.isActive:
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
                while not (sky and sky.isActive):
                    time.sleep(1)
                paused_time_end = time.perf_counter()
                pause_time += paused_time_end - paused_time_start
                self.log_signal.emit("▶ Resuming song...")

        self.log_signal.emit(f"✅ Finished playing {self.song_data['name']}")

class ClickableLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if folder:
            self.setText(folder)

class Tab1Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        global sky
        windows = pygetwindow.getWindowsWithTitle("Sky")
        for window in windows:
            if window.title == "Sky":
                sky = window

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.is_counting_down = False

        self.folder_path = ""
        self.song_data = ""

        parent = self.ui.lineEditFolder.parent()
        parent_2 = self.ui.lineEditFolder_2.parent()

        self.ui.lineEditFolder.setVisible(False)
        self.ui.lineEditFolder_2.setVisible(False)

        self.lineEditCustom = ClickableLineEdit(parent)
        self.lineEditCustom_2 = ClickableLineEdit(parent_2)
        self.lineEditCustom.setGeometry(self.ui.lineEditFolder.geometry())
        self.lineEditCustom_2.setGeometry(self.ui.lineEditFolder_2.geometry())
        self.lineEditCustom.setPlaceholderText("Click to choose folder")
        self.lineEditCustom_2.setPlaceholderText("Click to choose folder")

        self.ui.pushButtonSelectFolder.clicked.connect(self.show_files_in_folder)
        self.ui.pushButtonPlay.clicked.connect(self.on_button_click)
        self.ui.pushButtonCancel.clicked.connect(self.cancel_song)
        self.ui.pushButtonDetectWindow.clicked.connect(self.focus_sky_window)
        self.ui.listWidgetFiles.clicked.connect(self.show_infor)

        self.ui.tabWidget.setCurrentIndex(0)

    # Các hàm (copy y nguyên trong MainWindow của bạn):
    def update_sky_window(self):
        global sky
        windows = pygetwindow.getWindowsWithTitle("Sky")
        for window in windows:
            if window.title == "Sky":
                sky = window
                return True
        sky = None
        return False

    def focus_sky_window(self):
        if not self.update_sky_window():
            self.ui.plainTextEditLogs.clear()
            self.ui.plainTextEditLogs.appendPlainText("❌ Can't find Sky window.")
            return

        try:
            sky.activate()
            self.ui.plainTextEditLogs.clear()
            self.ui.plainTextEditLogs.appendPlainText("✅ Focused to Sky Window.")
        except:
            try:
                sky.minimize()
                sky.restore()
                sky.activate()
                self.ui.plainTextEditLogs.clear()
                self.ui.plainTextEditLogs.appendPlainText("✅ Focused to Sky Window (restore).")
            except Exception as e:
                self.ui.plainTextEditLogs.clear()
                self.ui.plainTextEditLogs.appendPlainText(f"❌ Can't focus: {e}")

    def on_button_click(self):
        if self.start_play():
            self.start_countdown()
        else:
            self.ui.plainTextEditLogs.clear()
            self.ui.plainTextEditLogs.appendPlainText("⛔ Can't play song.")

    def start_countdown(self):
        if self.is_counting_down:
            return
        self.is_counting_down = True
        self.countdown = 3
        self.ui.plainTextEditLogs.clear()
        self.timer.start(1000)
        return False

    def update_countdown(self):
        if self.countdown > 0:
            self.ui.plainTextEditLogs.appendPlainText(f"Playing song in {self.countdown}")
            self.countdown -= 1
        else:
            self.timer.stop()
            self.is_counting_down = False
            song_name = self.song_data[0]["name"]
            self.ui.plainTextEditLogs.appendPlainText(f"▶ Start song {song_name}!")
            self.play_song()

    def cancel_song(self):
        if hasattr(self, 'player_thread') and self.player_thread.isRunning():
            self.player_thread.terminate()
            self.player_thread.wait()

        self.ui.plainTextEditLogs.clear()
        self.ui.lineEditFolder.setText("")
        self.ui.plainTextEditLogs.appendPlainText("⏸ Canceling song")
        self.timer.stop()
        self.is_counting_down = False
        self.countdown = 3
        self.ui.plainTextEditLogs.appendPlainText(f"Countdown reset to {self.countdown}")

    def show_infor(self):
        self.ui.plainTextInfor.clear()
        item = self.ui.listWidgetFiles.currentItem().text()
        try:
            with open(f'{self.folder_path}/{item}', 'r', encoding="utf-8") as file:
                data = json.load(file)
        except:
            with open(f'{self.folder_path}/{item}', 'r', encoding="utf-16") as file:
                data = json.load(file)

        song_name = data[0]["name"] if data[0]["name"] is not None else "Unknown"
        bpm = data[0].get('bpm', 'Unknown')
        author = data[0].get('author', 'Unknown')
        instruments = data[0].get('instruments', 'Unknown')

        self.ui.plainTextInfor.appendPlainText("Name: " + song_name)
        self.ui.plainTextInfor.appendPlainText("Author: " + author)
        self.ui.plainTextInfor.appendPlainText("BPM: " + str(bpm))

        self.ui.plainTextInfor.appendPlainText("Instrument: ")
        if isinstance(instruments, list):
            unique_instruments = set(inst['name'] for inst in instruments)
            self.ui.plainTextInfor.appendPlainText(", ".join(unique_instruments))
        else:
            self.ui.plainTextInfor.appendPlainText(instruments)

    def show_files_in_folder(self):
        self.folder_path = self.lineEditCustom.text()
        if not self.folder_path or not os.path.isdir(self.folder_path):
            self.ui.listWidgetFiles.clear()
            self.ui.listWidgetFiles.addItems(["❌ Folder is invalid."])
            return

        files = os.listdir(self.folder_path)
        if not files:
            self.ui.listWidgetFiles.clear()
            self.ui.listWidgetFiles.addItems(["📁 Folder has no files."])
            return

        only_files = [f for f in files if os.path.isfile(os.path.join(self.folder_path, f))]
        self.ui.listWidgetFiles.clear()
        self.ui.listWidgetFiles.addItems(only_files)

    def start_play(self):
        item = self.ui.listWidgetFiles.currentItem().text()
        try:
            with open(f'{self.folder_path}/{item}', 'r', encoding="utf-8") as file:
                self.song_data = json.load(file)
            return True
        except FileNotFoundError:
            self.ui.plainTextEditLogs.clear()
            self.ui.plainTextEditLogs.appendPlainText("Song not found.")
            return False
        except UnicodeDecodeError:
            with open(f'{self.folder_path}/{item}', 'r', encoding="utf-16") as file:
                self.song_data = json.load(file)
            return True

    def play_song(self):
        self.player_thread = SongPlayerThread(self.song_data[0])
        self.player_thread.log_signal.connect(self.ui.plainTextEditLogs.appendPlainText)
        self.player_thread.start()
