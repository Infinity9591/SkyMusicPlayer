import json
import os
import socket
import threading
import time

import psutil
import pygetwindow
from PySide6.QtCore import Signal, QTimer, QThread
from PySide6.QtNetwork import QHostInfo, QHostAddress
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit
from pynput.keyboard import Controller

from demo import Ui_MainWindow

sky = None

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

class ServerThread(QThread):
    log_signal = Signal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.is_running = True

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        self.log_signal.emit(f"Server đang lắng nghe tại {self.host}:{self.port}")

        while self.is_running:
            try:
                server_socket.settimeout(1.0)  # Thêm timeout để không kẹt vĩnh viễn
                client_socket, addr = server_socket.accept()
                self.log_signal.emit(f"Client {addr[0]} đã kết nối.")

                data = client_socket.recv(1024)
                self.log_signal.emit(f"Nhận được: {data.decode('utf-8')}")

                client_socket.sendall(b"Server da nhan duoc du lieu")
                client_socket.close()
            except socket.timeout:
                continue  # Không có ai connect thì quay lại vòng lặp
            except Exception as e:
                self.log_signal.emit(f"Lỗi server: {e}")
                break

        server_socket.close()
        self.log_signal.emit("Server đã dừng.")

    def stop(self):
        self.is_running = False

class ClientThread(QThread):
    log_signal = Signal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.is_running = True

    def run(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.log_signal.emit(f"Đã kết nối tới server {self.host}:{self.port}")

            while self.is_running:
                try:
                    self.client_socket.settimeout(1.0)
                    data = self.client_socket.recv(1024)
                    if data:
                        self.log_signal.emit(f"Nhận từ server: {data.decode('utf-8')}")
                except socket.timeout:
                    continue
                except Exception as e:
                    self.log_signal.emit(f"Lỗi nhận dữ liệu: {e}")
                    break

            self.client_socket.close()
            self.log_signal.emit("Đã ngắt kết nối server.")

        except Exception as e:
            self.log_signal.emit(f"Lỗi kết nối: {e}")

    def stop(self):
        self.is_running = False

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

class ClickableLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if folder:
            self.setText(folder)

class MainWindow(QMainWindow):

    def closeEvent(self, event):
        if hasattr(self, 'server_thread') and self.server_thread.isRunning():
            self.server_thread.stop()
            self.server_thread.wait()

        if hasattr(self, 'client_thread') and self.client_thread.isRunning():
            self.client_thread.stop()
            self.client_thread.wait()

        event.accept()

    def __init__(self):
        super().__init__()
        global sky
        self.folder_path = ""
        self.song_data = ""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.is_counting_down = False
        windows = pygetwindow.getWindowsWithTitle("Sky")
        for window in windows:
            if window.title == "Sky":
                sky = window

        if sky == None:
            self.ui.plainTextEditLogs.appendPlainText(
                "Sky was not detected, please open Sky before playing songs.")

        parent = self.ui.lineEditFolder.parent()
        parent_2 = self.ui.lineEditFolder_2.parent()
        self.ui.lineEditFolder.setVisible(False)
        self.ui.lineEditFolder_2.setVisible(False)
        self.ui.pushButtonCreateServer.setVisible(False)
        self.ui.pushButtonJoinServer.setVisible(False)

        self.lineEditCustom = ClickableLineEdit(parent)
        self.lineEditCustom_2 = ClickableLineEdit(parent_2)
        self.lineEditCustom.setGeometry(self.ui.lineEditFolder.geometry())
        self.lineEditCustom_2.setGeometry(self.ui.lineEditFolder_2.geometry())
        self.lineEditCustom.setPlaceholderText("Click to choose folder")
        self.lineEditCustom_2.setPlaceholderText("Click to choose folder")

        self.ui.lineEditFolder.mousePressEvent
        self.ui.pushButtonSelectFolder.clicked.connect(self.show_files_in_folder)
        self.ui.pushButtonPlay.clicked.connect(self.on_button_click)
        self.ui.pushButtonCancel.clicked.connect(self.cancel_song)
        self.ui.pushButtonDetectWindow.clicked.connect(self.focus_sky_window)
        self.ui.listWidgetFiles.clicked.connect(self.show_infor)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.comboBoxRole.addItems(["Chọn vai trò","server", "client"])
        self.ui.comboBoxRole.setCurrentIndex(0)
        self.ui.comboBoxRole.currentTextChanged.connect(self.on_role_changed)
        self.ui.pushButtonCreateServer.clicked.connect(self.start_server)
        self.ui.pushButtonJoinServer.clicked.connect(self.start_client)
        # self.ui.lineEditIP

    def on_role_changed(self, role):
        if role == "server":
            # Lấy địa chỉ IP của máy tính
            print(self.get_radminvpn_ip())
            ip = self.get_radminvpn_ip()
            self.ui.lineEditIP.setText(ip)
            self.ui.pushButtonCreateServer.setVisible(True)
            self.ui.pushButtonJoinServer.setVisible(False)
        if role == "client":
            self.ui.pushButtonCreateServer.setVisible(False)
            self.ui.pushButtonJoinServer.setVisible(True)

    def get_radminvpn_ip(self):
        addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in addrs.items():
            if "Radmin" in interface_name:
                for address in interface_addresses:
                    if address.family.name == 'AF_INET':
                        return address.address
        return None

    def start_server(self):
        port = 5000
        host = self.ui.lineEditIP.text()

        self.server_thread = ServerThread(host, port)
        self.server_thread.log_signal.connect(self.ui.plainTextEditLogs_2.appendPlainText)
        self.server_thread.start()

    def start_client(self):
        host = self.ui.lineEditIP.text()
        port = 5000

        self.client_thread = ClientThread(host, port)
        self.client_thread.log_signal.connect(self.ui.plainTextEditLogs_2.appendPlainText)
        self.client_thread.start()

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

        self.timer.stop()  # Dừng bộ đếm ngược
        self.is_counting_down = False
        self.countdown = 3  # Reset lại giá trị đếm ngược
        self.ui.plainTextEditLogs.appendPlainText(f"Countdown reset to {self.countdown}")

        if self.timer.isActive():
            self.timer.stop()
            self.countdown = 3

    def show_infor(self):
        self.ui.plainTextInfor.clear()
        item = self.ui.listWidgetFiles.currentItem().text()
        self.data = ""
        try:
            with open(f'{self.folder_path}/{item}', 'r', encoding="utf-8") as file:
                self.data = json.load(file)
            # return True
        except :
            with open(f'{self.folder_path}/{item}', 'r', encoding="utf-16") as file:
                self.data = json.load(file)
            # return True
        self.song_name = self.data[0]["name"] if self.data[0]["name"] is not None else "Unknown"
        self.bpm = self.data[0].get('bpm', 'Unknown')
        self.author = self.data[0].get('author', 'Unknown')
        self.instruments = self.data[0].get('instruments', 'Unknown')
        self.ui.plainTextInfor.appendPlainText("Name: " + self.song_name)
        self.ui.plainTextInfor.appendPlainText("Author: " + self.author)
        self.ui.plainTextInfor.appendPlainText("BPM: " + str(self.bpm))

        self.ui.plainTextInfor.appendPlainText("Instrument: ")
        if isinstance(self.instruments, list):
            unique_instruments = set(instrument['name'] for instrument in self.instruments)
            self.ui.plainTextInfor.appendPlainText(", ".join(unique_instruments))
        else:
            self.ui.plainTextInfor.appendPlainText(self.instruments)

    def show_files_in_folder(self ):
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
        except UnicodeDecodeError as e:
            with open(f'{self.folder_path}/{item}', 'r', encoding="utf-16") as file:
                self.song_data = json.load(file)
            return True

    def play_song(self):
        self.player_thread = SongPlayerThread(self.song_data[0])
        self.player_thread.log_signal.connect(self.ui.plainTextEditLogs.appendPlainText)
        self.player_thread.start()

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

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
