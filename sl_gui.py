import os.path
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from save_and_load import save, load, config_path, read_config, init_config, SOURCE_PATH_NAME, SAVE_PATH_NAME


# source_path, save_path, config,

class SL(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        init_config()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 10))

        s_btn = QPushButton("存档", self)
        s_btn.setMinimumSize(200, 50)
        l_btn = QPushButton("读档", self)
        l_btn.setMinimumSize(200, 50)
        source_path_btn = QPushButton(f"{SOURCE_PATH_NAME}路径", self)
        save_path_btn = QPushButton(f"{SAVE_PATH_NAME}路径", self)

        s_btn.clicked.connect(self.save)
        l_btn.clicked.connect(self.load)
        source_path_btn.clicked.connect(self.config_source_path)
        save_path_btn.clicked.connect(self.config_save_path)

        vbox = QVBoxLayout()
        vbox.addWidget(s_btn)
        vbox.addWidget(l_btn)
        vbox.addWidget(source_path_btn)
        vbox.addWidget(save_path_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("SL")
        self.show()

    def save(self):
        try:
            save()
        except Exception as e:
            QMessageBox.question(self, "Message", str(e), QMessageBox.Close)

    def load(self):
        try:
            load()
        except Exception as e:
            QMessageBox.question(self, "Message", str(e), QMessageBox.Close)

    def config_source_path(self):
        config = read_config()
        source_path = config.get("config", "source_path")
        open_path = self.default_open_path(source_path)
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", open_path)
        if directory:
            config.set("config", "source_path", directory)
            config.write(open(config_path, "r+", encoding='utf8'))

    def config_save_path(self):
        config = read_config()
        save_path = config.get("config", "save_path")
        open_path = self.default_open_path(save_path)
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", open_path)
        if directory:
            config.set("config", "save_path", directory)
            config.write(open(config_path, "r+", encoding='utf8'))

    def default_open_path(self, _path):
        if sys.platform == "win32":
            open_path = os.getenv("appdata")
        else:
            open_path = os.getenv("HOME")
        if os.path.exists(_path):
            open_path = _path
        return open_path

    def err_event(self):
        QMessageBox.question(self, "Message", "配置文件错误", QMessageBox.Close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = SL()
    sys.exit(app.exec_())
