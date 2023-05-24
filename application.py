import sys
import json
import os
import subprocess
from main import main_start
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QAction, QMessageBox, \
    QPushButton, QGridLayout, QLayout, QProgressDialog, QMenuBar, QStatusBar, QLabel, QFileDialog, QComboBox



class MainWindow(QMainWindow):
    def __init__(self, main_func=None):
        super().__init__(parent=None)
        self.cache_json = {
            "box1": [],
            "box2": [],
            "box3": [],
            "box4": []
        }
        self.main_func = main_func
        self.home_path = os.path.realpath(__file__)
        self.setup_ui()

    def setup_ui(self):

        self.setObjectName("MainWindow")
        self.resize(600, 350)

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.setFont(font)
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setStyleSheet("font: 10pt \"Segoe UI\";")

        self.centralwidget = QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        # Begin button
        self.BeginButton_5 = QPushButton(self.centralwidget)
        self.BeginButton_5.clicked.connect(self.process_main)
        self.BeginButton_5.setGeometry(QtCore.QRect(225, 250, 150, 42))
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(10)
        size_policy.setHeightForWidth(self.BeginButton_5.sizePolicy().hasHeightForWidth())
        self.BeginButton_5.setSizePolicy(size_policy)
        self.BeginButton_5.setStyleSheet("")
        self.BeginButton_5.setObjectName("BeginButton_5")

        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 581, 186))
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.layoutWidget.sizePolicy().hasHeightForWidth())
        self.layoutWidget.setSizePolicy(size_policy)
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(24)
        self.gridLayout.setObjectName("gridLayout")

        # Predict label
        self.label_1_predict = QLabel(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_1_predict.sizePolicy().hasHeightForWidth())
        self.label_1_predict.setSizePolicy(size_policy)
        self.label_1_predict.setTextFormat(QtCore.Qt.RichText)
        self.label_1_predict.setScaledContents(False)
        self.label_1_predict.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_1_predict.setIndent(-1)
        self.label_1_predict.setOpenExternalLinks(False)
        self.label_1_predict.setObjectName("label_1_predict")
        self.gridLayout.addWidget(self.label_1_predict, 0, 0, 1, 1)

        self.combobox_1_predict = QComboBox(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.combobox_1_predict.sizePolicy().hasHeightForWidth())
        self.combobox_1_predict.setEditable(True)
        self.combobox_1_predict.setSizePolicy(size_policy)
        self.combobox_1_predict.setObjectName("combobox_1_predict")
        self.gridLayout.addWidget(self.combobox_1_predict, 0, 1, 1, 1)

        self.pushButton_1_predict = QPushButton(self.layoutWidget)
        self.pushButton_1_predict.clicked.connect(self.file_search_predict)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(10)
        size_policy.setHeightForWidth(self.pushButton_1_predict.sizePolicy().hasHeightForWidth())
        self.pushButton_1_predict.setSizePolicy(size_policy)
        self.pushButton_1_predict.setStyleSheet("")
        self.pushButton_1_predict.setObjectName("pushButton_1_predict")
        self.gridLayout.addWidget(self.pushButton_1_predict, 0, 2, 1, 1)

        # Video label
        self.label_2_video = QLabel(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_2_video.sizePolicy().hasHeightForWidth())
        self.label_2_video.setSizePolicy(size_policy)
        self.label_2_video.setTextFormat(QtCore.Qt.RichText)
        self.label_2_video.setScaledContents(False)
        self.label_2_video.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2_video.setIndent(-1)
        self.label_2_video.setOpenExternalLinks(False)
        self.label_2_video.setObjectName("label_2_video")
        self.gridLayout.addWidget(self.label_2_video, 1, 0, 1, 1)

        self.combobox_2_video = QComboBox(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.combobox_2_video.sizePolicy().hasHeightForWidth())
        self.combobox_2_video.setEditable(True)
        self.combobox_2_video.setSizePolicy(size_policy)
        self.combobox_2_video.setObjectName("combobox_2_predict")
        self.gridLayout.addWidget(self.combobox_2_video, 1, 1, 1, 1)

        # self.lineEdit_2_video = QLineEdit(self.layoutWidget)
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(self.lineEdit_2_video.sizePolicy().hasHeightForWidth())
        # self.lineEdit_2_video.setSizePolicy(size_policy)
        # self.lineEdit_2_video.setObjectName("lineEdit_2_video")
        # self.gridLayout.addWidget(self.lineEdit_2_video, 1, 1, 1, 1)

        self.pushButton_2_video = QPushButton(self.layoutWidget)
        self.pushButton_2_video.clicked.connect(self.file_search_video)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(10)
        size_policy.setHeightForWidth(self.pushButton_2_video.sizePolicy().hasHeightForWidth())
        self.pushButton_2_video.setSizePolicy(size_policy)
        self.pushButton_2_video.setStyleSheet("")
        self.pushButton_2_video.setObjectName("pushButton_2_video")
        self.gridLayout.addWidget(self.pushButton_2_video, 1, 2, 1, 1)

        # Markdown label
        self.label_3_markdown = QLabel(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_3_markdown.sizePolicy().hasHeightForWidth())
        self.label_3_markdown.setSizePolicy(size_policy)
        self.label_3_markdown.setTextFormat(QtCore.Qt.RichText)
        self.label_3_markdown.setScaledContents(False)
        self.label_3_markdown.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3_markdown.setIndent(-1)
        self.label_3_markdown.setOpenExternalLinks(False)
        self.label_3_markdown.setObjectName("label_3_markdown")
        self.gridLayout.addWidget(self.label_3_markdown, 2, 0, 1, 1)

        self.combobox_3_markdown = QComboBox(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.combobox_3_markdown.sizePolicy().hasHeightForWidth())
        self.combobox_3_markdown.setEditable(True)
        self.combobox_3_markdown.setSizePolicy(size_policy)
        self.combobox_3_markdown.setObjectName("combobox_3_predict")
        self.gridLayout.addWidget(self.combobox_3_markdown, 2, 1, 1, 1)

        # self.lineEdit_3_markdown = QLineEdit(self.layoutWidget)
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(self.lineEdit_3_markdown.sizePolicy().hasHeightForWidth())
        # self.lineEdit_3_markdown.setSizePolicy(size_policy)
        # self.lineEdit_3_markdown.setObjectName("lineEdit_3_markdown")
        # self.gridLayout.addWidget(self.lineEdit_3_markdown, 2, 1, 1, 1)

        self.pushButton_3_markdown = QPushButton(self.layoutWidget)
        self.pushButton_3_markdown.clicked.connect(self.file_search_markdown)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(10)
        size_policy.setHeightForWidth(self.pushButton_3_markdown.sizePolicy().hasHeightForWidth())
        self.pushButton_3_markdown.setSizePolicy(size_policy)
        self.pushButton_3_markdown.setStyleSheet("")
        self.pushButton_3_markdown.setObjectName("pushButton_3_markdown")
        self.gridLayout.addWidget(self.pushButton_3_markdown, 2, 2, 1, 1)

        # Save label
        self.label_4_symmetries_file = QLabel(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.label_4_symmetries_file.sizePolicy().hasHeightForWidth())
        self.label_4_symmetries_file.setSizePolicy(size_policy)
        self.label_4_symmetries_file.setTextFormat(QtCore.Qt.RichText)
        self.label_4_symmetries_file.setScaledContents(False)
        self.label_4_symmetries_file.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4_symmetries_file.setIndent(-1)
        self.label_4_symmetries_file.setOpenExternalLinks(False)
        self.label_4_symmetries_file.setObjectName("label_4_symmetries_file")
        self.gridLayout.addWidget(self.label_4_symmetries_file, 3, 0, 1, 1)

        self.combobox_4_symmetries_file = QComboBox(self.layoutWidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.combobox_4_symmetries_file.sizePolicy().hasHeightForWidth())
        self.combobox_4_symmetries_file.setEditable(True)
        self.combobox_4_symmetries_file.setSizePolicy(size_policy)
        self.combobox_4_symmetries_file.setObjectName("combobox_4_symmetries_file ")
        self.gridLayout.addWidget(self.combobox_4_symmetries_file, 3, 1, 1, 1)

        # self.lineEdit_4_symmetries_file = QLineEdit(self.layoutWidget)
        # size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(self.lineEdit_4_symmetries_file.sizePolicy().hasHeightForWidth())
        # self.lineEdit_4_symmetries_file.setSizePolicy(size_policy)
        # self.lineEdit_4_symmetries_file.setStyleSheet("border-color: rgb(56, 104, 106);")
        # self.lineEdit_4_symmetries_file.setObjectName("lineEdit_4_symmetries_file")
        # self.gridLayout.addWidget(self.lineEdit_4_symmetries_file, 3, 1, 1, 1)

        self.pushButton_4_symmetries_file = QPushButton(self.layoutWidget)
        self.pushButton_4_symmetries_file.clicked.connect(self.save_result_file)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(10)
        size_policy.setHeightForWidth(self.pushButton_4_symmetries_file.sizePolicy().hasHeightForWidth())
        self.pushButton_4_symmetries_file.setSizePolicy(size_policy)
        self.pushButton_4_symmetries_file.setStyleSheet("")
        self.pushButton_4_symmetries_file.setObjectName("pushButton_4_symmetries_file")
        self.gridLayout.addWidget(self.pushButton_4_symmetries_file, 3, 2, 1, 1)

        self.gridLayout.setColumnMinimumWidth(2, 100)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 23))
        self.menubar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.read_cache()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "paresis_detection"))
        self.BeginButton_5.setText(_translate("MainWindow", "Начать обработку"))
        self.pushButton_3_markdown.setText(_translate("MainWindow", "Поиск"))
        self.label_1_predict.setText(_translate("MainWindow", "Предиктор:"))
        self.label_2_video.setText(_translate("MainWindow", "Видео:"))
        self.pushButton_2_video.setText(_translate("MainWindow", "Поиск"))
        self.label_3_markdown.setText(_translate("MainWindow", "Разметка:"))
        self.label_4_symmetries_file.setText(_translate("MainWindow", "Сохранять в:"))
        self.pushButton_1_predict.setText(_translate("MainWindow", "Поиск"))
        self.pushButton_4_symmetries_file.setText(_translate("MainWindow", "Поиск"))

    def read_cache(self):
        if not os.path.isfile("cache.json"):
            return

        with open("cache.json", "r") as f:
            try:
                self.cache_json = json.load(f)
            except json.JSONDecodeError:
                return
        try:
            self.combobox_1_predict.addItems(self.cache_json['box1'])
            self.combobox_2_video.addItems(self.cache_json['box2'])
            self.combobox_3_markdown.addItems(self.cache_json['box3'])
            self.combobox_4_symmetries_file.addItems(self.cache_json['box4'])
        except KeyError:
            open("cache.json", "w").close()

    def write_cache(self):
        with open("cache.json", "w") as f:
            json.dump(self.cache_json, f)

    def file_search_predict(self):
        # Predict find button
        file_name = QFileDialog.getOpenFileName(self, "Select prediction model", self.home_path, "Dat Files (*.dat)")[0]
        if file_name in self.cache_json['box1']:
            self.cache_json["box1"].remove(file_name)
        self.cache_json['box1'].insert(0, file_name)
        self.combobox_1_predict.clear()
        self.combobox_1_predict.addItems(self.cache_json['box1'])
        if len(self.cache_json['box1']) > 4:
            self.cache_json['box1'].pop()

    def file_search_video(self):
        # Video find button
        file_name = QFileDialog.getOpenFileName(self, "Select video", self.home_path, "mp4 files (*.mp4)")[0]
        if file_name in self.cache_json['box2']:
            self.cache_json["box2"].remove(file_name)
        self.cache_json['box2'].insert(0, file_name)
        self.combobox_2_video.clear()
        self.combobox_2_video.addItems(self.cache_json['box2'])
        if len(self.cache_json['box2']) > 4:
            self.cache_json['box2'].pop()

    def file_search_markdown(self):
        # Markdown find button
        file_name = QFileDialog.getOpenFileName(self, "Select markdown file", self.home_path, "xlsx files (*.xlsx)")[0]
        if file_name in self.cache_json['box3']:
            self.cache_json["box3"].remove(file_name)
        self.cache_json['box3'].insert(0, file_name)
        self.combobox_3_markdown.clear()
        self.combobox_3_markdown.addItems(self.cache_json['box3'])
        if len(self.cache_json['box3']) > 4:
            self.cache_json['box3'].pop()

    def save_result_file(self):
        # Save path button
        file_name = QFileDialog.getExistingDirectory(self, "Select save path file", self.home_path,
                                                     QFileDialog.ShowDirsOnly)
        if file_name in self.cache_json['box4']:
            self.cache_json["box4"].remove(file_name)
        self.cache_json['box4'].insert(0, file_name)
        self.combobox_4_symmetries_file.clear()
        self.combobox_4_symmetries_file.addItems(self.cache_json['box4'])
        if len(self.cache_json['box4']) > 4:
            self.cache_json['box4'].pop()

    def process_main(self):
        predictor_file_path = str(self.combobox_1_predict.currentText())
        video_file_path = str(self.combobox_2_video.currentText())
        markup_file_path = str(self.combobox_3_markdown.currentText())
        save_to_files = str(self.combobox_4_symmetries_file.currentText())
        if predictor_file_path == '' or \
                video_file_path == '' or \
                markup_file_path == '' or \
                save_to_files == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Ошибка")
            msg.setInformativeText('Не все поля заполнены')
            msg.setWindowTitle("Ошибка")
            msg.exec_()
        else:
            self.main_func(predictor_file_path, video_file_path, markup_file_path, save_to_files)

    def closeEvent(self, e):
        # Close application
        self.write_cache()
        result = QMessageBox.question(self, "Подтверждение закрытия окна",
                                      "Вы действительно хотите закрыть окно?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if result == QMessageBox.Yes:
            e.accept()
            QWidget.closeEvent(self, e)
        else:
            e.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(main_func=main_start)
    main_window.show()
    sys.exit(app.exec_())
