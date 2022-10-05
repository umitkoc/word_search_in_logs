from functools import partial
from glob import glob
from os import path, system
from threading import Thread
from PyQt6.QtCore import QTimer 

from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 500)
        self.search_input()
        self.search_button()
        self.files = []
        self.timer=QTimer(self)

    def search_input(self):
        self.input_search = QLineEdit(self)
        self.input_search.resize(600, 30)
        self.input_search.move(20, 20)
        self.input_search.setPlaceholderText("word1,word2,word3...")

    def search_button(self):
        self.button_search = QPushButton(self)
        self.button_search.resize(100, 30)
        self.button_search.move(640, 20)
        self.button_search.setText("Search")
        self.button_search.setStyleSheet("color:white;background-color:red")
        self.button_search.clicked.connect(self.find_file)
    def find_file(self):
        self.loading()
        for i in self.files:
            i.deleteLater()
        self.files = []
        x = 0
        y = 1
        for file in glob(path.join(".", "*.log")):
            step = 0
            for word in self.input_search.text().split(","):
                for item in open(f"{file}", "r").readlines():
                    
                    if item.lower().find(word) > 0:
                        step += 1
                        break
            if len(self.input_search.text().split(",")) == step:
                if x > 9:
                    y += 1
                    x = 0
                x += 1
                self.create_file(file, x, y)
        for i in self.files:
            i.show()
        self.button_search.setText("Search")
        self.button_search.setDisabled(False)
    def loading(self):
        self.button_search.setText("Loading")
        self.button_search.setDisabled(True)

    def create_file(self, files="", x=0, y=0):
        self.button_file = QPushButton(f"{files.split('.')[1]}", self)
        self.button_file.resize(120, 120)
        self.button_file.move(130*x, 130*y)
        self.button_file.clicked.connect(partial(self.open_file, files))
        self.button_file.setStyleSheet("background-color:gray;color:black;")
        self.files.append(self.button_file)

    def open_file(self, files=""):
        system(f"notepad-plus-plus {files}")


if __name__ == "__main__":
    app = QApplication([])
    main = Main()
    main.show()
    exit(app.exec())
