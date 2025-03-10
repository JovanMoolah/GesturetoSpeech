# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIForHandGesturetest5.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSlider,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(911, 725)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(250, 10, 640, 480))
        self.Display = QLabel(self.widget)
        self.Display.setObjectName(u"Display")
        self.Display.setGeometry(QRect(0, 0, 640, 480))
        self.Display.setStyleSheet(u"")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(10, 10, 231, 481))
        self.gridLayoutWidget = QWidget(self.widget_2)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 231, 481))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.Translate = QPushButton(self.gridLayoutWidget)
        self.Translate.setObjectName(u"Translate")

        self.gridLayout.addWidget(self.Translate, 9, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 9, 0, 1, 1)

        self.pause = QPushButton(self.gridLayoutWidget)
        self.pause.setObjectName(u"pause")

        self.gridLayout.addWidget(self.pause, 13, 0, 1, 1)

        self.clear = QPushButton(self.gridLayoutWidget)
        self.clear.setObjectName(u"clear")

        self.gridLayout.addWidget(self.clear, 14, 0, 1, 1)

        self.Input_Language = QLabel(self.gridLayoutWidget)
        self.Input_Language.setObjectName(u"Input_Language")
        self.Input_Language.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Input_Language, 6, 0, 1, 1)

        self.Output_Voice = QLabel(self.gridLayoutWidget)
        self.Output_Voice.setObjectName(u"Output_Voice")
        self.Output_Voice.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Output_Voice, 11, 0, 1, 1)

        self.speak_start = QPushButton(self.gridLayoutWidget)
        self.speak_start.setObjectName(u"speak_start")

        self.gridLayout.addWidget(self.speak_start, 12, 0, 1, 1)

        self.speak_stop = QPushButton(self.gridLayoutWidget)
        self.speak_stop.setObjectName(u"speak_stop")

        self.gridLayout.addWidget(self.speak_stop, 12, 1, 1, 1)

        self.Pitch = QLabel(self.gridLayoutWidget)
        self.Pitch.setObjectName(u"Pitch")
        self.Pitch.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Pitch, 4, 0, 1, 1)

        self.Gesture = QComboBox(self.gridLayoutWidget)
        self.Gesture.setObjectName(u"Gesture")

        self.gridLayout.addWidget(self.Gesture, 2, 0, 1, 1)

        self.Rate = QLabel(self.gridLayoutWidget)
        self.Rate.setObjectName(u"Rate")
        self.Rate.setEnabled(True)
        self.Rate.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Rate, 3, 0, 1, 1)

        self.stop = QPushButton(self.gridLayoutWidget)
        self.stop.setObjectName(u"stop")

        self.gridLayout.addWidget(self.stop, 0, 1, 1, 1)

        self.pitch = QSlider(self.gridLayoutWidget)
        self.pitch.setObjectName(u"pitch")
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(85, 255, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(170, 255, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(127, 255, 63, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(42, 127, 0, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(56, 170, 0, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush6 = QBrush(QColor(255, 255, 255, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush6)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush2)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush7)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        self.pitch.setPalette(palette)
        self.pitch.setAutoFillBackground(False)
        self.pitch.setMinimum(-10)
        self.pitch.setMaximum(10)
        self.pitch.setTracking(True)
        self.pitch.setOrientation(Qt.Horizontal)
        self.pitch.setInvertedAppearance(False)
        self.pitch.setInvertedControls(False)
        self.pitch.setTickPosition(QSlider.NoTicks)

        self.gridLayout.addWidget(self.pitch, 4, 1, 1, 1)

        self.concurrentbut = QPushButton(self.gridLayoutWidget)
        self.concurrentbut.setObjectName(u"concurrentbut")

        self.gridLayout.addWidget(self.concurrentbut, 8, 1, 1, 1)

        self.Mapping = QLineEdit(self.gridLayoutWidget)
        self.Mapping.setObjectName(u"Mapping")
        self.Mapping.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Mapping, 2, 1, 1, 1)

        self.Concurrent = QLabel(self.gridLayoutWidget)
        self.Concurrent.setObjectName(u"Concurrent")
        self.Concurrent.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Concurrent, 8, 0, 1, 1)

        self.Volume = QLabel(self.gridLayoutWidget)
        self.Volume.setObjectName(u"Volume")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Volume.sizePolicy().hasHeightForWidth())
        self.Volume.setSizePolicy(sizePolicy)
        self.Volume.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Volume, 5, 0, 1, 1)

        self.Output_Langauge = QLabel(self.gridLayoutWidget)
        self.Output_Langauge.setObjectName(u"Output_Langauge")
        self.Output_Langauge.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Output_Langauge, 10, 0, 1, 1)

        self.output_language = QComboBox(self.gridLayoutWidget)
        self.output_language.setObjectName(u"output_language")

        self.gridLayout.addWidget(self.output_language, 10, 1, 1, 1)

        self.start = QPushButton(self.gridLayoutWidget)
        self.start.setObjectName(u"start")

        self.gridLayout.addWidget(self.start, 0, 0, 1, 1)

        self.volume = QSlider(self.gridLayoutWidget)
        self.volume.setObjectName(u"volume")
        self.volume.setMaximum(20)
        self.volume.setValue(10)
        self.volume.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.volume, 5, 1, 1, 1)

        self.Input_Voice = QLabel(self.gridLayoutWidget)
        self.Input_Voice.setObjectName(u"Input_Voice")
        self.Input_Voice.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Input_Voice, 7, 0, 1, 1)

        self.rate = QSlider(self.gridLayoutWidget)
        self.rate.setObjectName(u"rate")
        self.rate.setMinimum(-10)
        self.rate.setMaximum(10)
        self.rate.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.rate, 3, 1, 1, 1)

        self.output_voice = QComboBox(self.gridLayoutWidget)
        self.output_voice.setObjectName(u"output_voice")

        self.gridLayout.addWidget(self.output_voice, 11, 1, 1, 1)

        self.input_voice = QComboBox(self.gridLayoutWidget)
        self.input_voice.setObjectName(u"input_voice")

        self.gridLayout.addWidget(self.input_voice, 7, 1, 1, 1)

        self.input_language = QComboBox(self.gridLayoutWidget)
        self.input_language.setObjectName(u"input_language")

        self.gridLayout.addWidget(self.input_language, 6, 1, 1, 1)

        self.resume = QPushButton(self.gridLayoutWidget)
        self.resume.setObjectName(u"resume")

        self.gridLayout.addWidget(self.resume, 13, 1, 1, 1)

        self.Stream_Source = QLineEdit(self.gridLayoutWidget)
        self.Stream_Source.setObjectName(u"Stream_Source")
        self.Stream_Source.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.Stream_Source, 1, 1, 1, 1)

        self.Synchronize = QPushButton(self.gridLayoutWidget)
        self.Synchronize.setObjectName(u"Synchronize")

        self.gridLayout.addWidget(self.Synchronize, 14, 1, 1, 1)

        self.Stream_Type = QComboBox(self.gridLayoutWidget)
        self.Stream_Type.setObjectName(u"Stream_Type")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Stream_Type.sizePolicy().hasHeightForWidth())
        self.Stream_Type.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.Stream_Type, 1, 0, 1, 1)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(10, 500, 881, 191))
        self.horizontalLayoutWidget = QWidget(self.widget_3)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 29, 881, 161))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.inputted_text = QPlainTextEdit(self.horizontalLayoutWidget)
        self.inputted_text.setObjectName(u"inputted_text")
        self.inputted_text.setStyleSheet(u"font: 18pt \"MS Shell Dlg 2\";\n"
"")
        self.inputted_text.setBackgroundVisible(False)
        self.inputted_text.setCenterOnScroll(False)

        self.horizontalLayout.addWidget(self.inputted_text)

        self.translated_text = QPlainTextEdit(self.horizontalLayoutWidget)
        self.translated_text.setObjectName(u"translated_text")
        self.translated_text.setStyleSheet(u"font: 18pt \"MS Shell Dlg 2\";")

        self.horizontalLayout.addWidget(self.translated_text)

        self.horizontalLayoutWidget_2 = QWidget(self.widget_3)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, 881, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Inputted = QLabel(self.horizontalLayoutWidget_2)
        self.Inputted.setObjectName(u"Inputted")
        self.Inputted.setStyleSheet(u"font: 12pt \"MS Shell Dlg 2\";")
        self.Inputted.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.Inputted)

        self.Translated = QLabel(self.horizontalLayoutWidget_2)
        self.Translated.setObjectName(u"Translated")
        self.Translated.setStyleSheet(u"font: 12pt \"MS Shell Dlg 2\";")
        self.Translated.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.Translated)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 911, 18))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Display.setText("")
        self.Translate.setText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Translate", None))
        self.pause.setText(QCoreApplication.translate("MainWindow", u"Pause  Speak", None))
        self.clear.setText(QCoreApplication.translate("MainWindow", u"Clear ", None))
        self.Input_Language.setText(QCoreApplication.translate("MainWindow", u"Input Language", None))
        self.Output_Voice.setText(QCoreApplication.translate("MainWindow", u"Translated Voice", None))
        self.speak_start.setText(QCoreApplication.translate("MainWindow", u"Start Speak", None))
        self.speak_stop.setText(QCoreApplication.translate("MainWindow", u"Stop Speak", None))
        self.Pitch.setText(QCoreApplication.translate("MainWindow", u"Pitch", None))
        self.Rate.setText(QCoreApplication.translate("MainWindow", u"Rate", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"Stop Stream", None))
#if QT_CONFIG(tooltip)
        self.pitch.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.pitch.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.concurrentbut.setText(QCoreApplication.translate("MainWindow", u"Off", None))
        self.Mapping.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.Concurrent.setText(QCoreApplication.translate("MainWindow", u"Concurrent", None))
        self.Volume.setText(QCoreApplication.translate("MainWindow", u"Volume", None))
        self.Output_Langauge.setText(QCoreApplication.translate("MainWindow", u"Translated Language", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start Stream", None))
        self.Input_Voice.setText(QCoreApplication.translate("MainWindow", u"Input Voice", None))
        self.resume.setText(QCoreApplication.translate("MainWindow", u"Resume Speak", None))
        self.Stream_Source.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.Synchronize.setText(QCoreApplication.translate("MainWindow", u"Synchronize", None))
        self.inputted_text.setPlainText("")
        self.translated_text.setPlainText("")
        self.Inputted.setText(QCoreApplication.translate("MainWindow", u"Input Language", None))
        self.Translated.setText(QCoreApplication.translate("MainWindow", u"Translated Language", None))
    # retranslateUi

