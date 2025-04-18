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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(556, 594)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 10, 221, 51))
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 200, 49, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 70, 49, 16))
        self.lineEditFolder = QLineEdit(self.centralwidget)
        self.lineEditFolder.setObjectName(u"lineEditFolder")
        self.lineEditFolder.setGeometry(QRect(30, 110, 401, 21))
        self.btnSelectFolder = QPushButton(self.centralwidget)
        self.btnSelectFolder.setObjectName(u"btnSelectFolder")
        self.btnSelectFolder.setGeometry(QRect(450, 110, 75, 24))
        self.pushButtonPlay = QPushButton(self.centralwidget)
        self.pushButtonPlay.setObjectName(u"pushButtonPlay")
        self.pushButtonPlay.setGeometry(QRect(140, 370, 75, 24))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(30, 160, 49, 16))
        self.comboBoxCodec = QComboBox(self.centralwidget)
        self.comboBoxCodec.setObjectName(u"comboBoxCodec")
        self.comboBoxCodec.setGeometry(QRect(30, 240, 101, 22))
        self.plainTextEditLog = QPlainTextEdit(self.centralwidget)
        self.plainTextEditLog.setObjectName(u"plainTextEditLog")
        self.plainTextEditLog.setGeometry(QRect(30, 430, 491, 131))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(30, 390, 49, 16))
        self.listWidgetListFiles = QListWidget(self.centralwidget)
        self.listWidgetListFiles.setObjectName(u"listWidgetListFiles")
        self.listWidgetListFiles.setGeometry(QRect(170, 160, 351, 192))
        self.pushButtonCancel = QPushButton(self.centralwidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setGeometry(QRect(380, 370, 75, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sky Auto Music", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sky Auto Music", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Codec", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.btnSelectFolder.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.pushButtonPlay.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    # retranslateUi

