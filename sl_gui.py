import os.path
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from save_and_load import save, load, config_path, read_config


# source_path, save_path, config,

class SL(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 10))

        s_btn = QPushButton("存档", self)
        l_btn = QPushButton("读档", self)
        source_path_btn = QPushButton("默认存档位置", self)
        save_path_btn = QPushButton("保存存档位置", self)

        s_btn.clicked.connect(self.save)
        l_btn.clicked.connect(self.load)
        source_path_btn.clicked.connect(self.config_source_path)
        save_path_btn.clicked.connect(self.config_save_path)

        hbox = QHBoxLayout()
        hbox.addWidget(s_btn)
        hbox.addWidget(l_btn)

        hbox.addWidget(source_path_btn)
        hbox.addWidget(save_path_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("SL")
        self.show()

    def save(self):
        config = read_config()
        source_path = config.get("config", "source_path")
        save_path = config.get("config", "save_path")
        if not source_path or not save_path:
            self.err_event()
        else:
            save()

    def load(self):
        config = read_config()
        source_path = config.get("config", "source_path")
        save_path = config.get("config", "save_path")
        if not source_path or not save_path:
            self.err_event()
        else:
            load()

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
            open_path = "~"
        if os.path.isdir(_path):
            open_path = _path
        return open_path

    def err_event(self):
        reply = QMessageBox.question(self, "Message", "配置文件错误", QMessageBox.Close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = SL()
    sys.exit(app.exec_())
