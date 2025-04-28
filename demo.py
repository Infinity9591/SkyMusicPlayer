# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'demo.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(817, 639)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(290, 20, 251, 51))
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 130, 121, 31))
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(12)
        self.label_2.setFont(font1)
        self.lineEditFolder = QLineEdit(self.centralwidget)
        self.lineEditFolder.setObjectName(u"lineEditFolder")
        self.lineEditFolder.setGeometry(QRect(170, 140, 481, 22))
        self.pushButtonSelectFolder = QPushButton(self.centralwidget)
        self.pushButtonSelectFolder.setObjectName(u"pushButtonSelectFolder")
        self.pushButtonSelectFolder.setGeometry(QRect(670, 140, 101, 24))
        font2 = QFont()
        font2.setFamilies([u"Consolas"])
        font2.setPointSize(10)
        self.pushButtonSelectFolder.setFont(font2)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 190, 121, 31))
        self.label_3.setFont(font1)
        self.listWidgetFiles = QListWidget(self.centralwidget)
        self.listWidgetFiles.setObjectName(u"listWidgetFiles")
        self.listWidgetFiles.setGeometry(QRect(170, 200, 251, 191))
        self.plainTextEditLogs = QPlainTextEdit(self.centralwidget)
        self.plainTextEditLogs.setObjectName(u"plainTextEditLogs")
        self.plainTextEditLogs.setGeometry(QRect(170, 420, 611, 191))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(30, 420, 121, 31))
        self.label_4.setFont(font1)
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(20, 480, 131, 131))
        self.groupBox_3.setFont(font1)
        self.pushButtonPlay = QPushButton(self.groupBox_3)
        self.pushButtonPlay.setObjectName(u"pushButtonPlay")
        self.pushButtonPlay.setGeometry(QRect(10, 40, 101, 24))
        self.pushButtonPlay.setFont(font2)
        self.pushButtonCancel = QPushButton(self.groupBox_3)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setGeometry(QRect(10, 90, 101, 24))
        self.pushButtonCancel.setFont(font2)
        self.pushButtonDetectWindow = QPushButton(self.centralwidget)
        self.pushButtonDetectWindow.setObjectName(u"pushButtonDetectWindow")
        self.pushButtonDetectWindow.setGeometry(QRect(640, 80, 131, 24))
        self.pushButtonDetectWindow.setFont(font2)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(460, 200, 71, 31))
        self.label_5.setFont(font1)
        self.plainTextInfor = QPlainTextEdit(self.centralwidget)
        self.plainTextInfor.setObjectName(u"plainTextInfor")
        self.plainTextInfor.setEnabled(False)
        self.plainTextInfor.setGeometry(QRect(550, 200, 231, 191))
        self.plainTextInfor.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SkyAutoMusic", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sky Auto Music", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Select folder", None))
        self.pushButtonSelectFolder.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Files", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Action", None))
        self.pushButtonPlay.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.pushButtonDetectWindow.setText(QCoreApplication.translate("MainWindow", u"Detect Sky Window", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Infor", None))
    # retranslateUi

