import sqlite3
from typing import Text
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QCheckBox, QDialog, QLabel, QLineEdit, QMainWindow, QApplication, QMessageBox, QPushButton, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
import pandas as pd

class Window(QMainWindow):
    def __init(self, conn: sqlite3.Connection, curs: sqlite3.Cursor):

        #Database stuff
        super().cursor = curs
        self.connection = conn

        self.setWindowTitle("Main Menu")

        self.setGeometry(100, 100, 600, 300)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        # Labels

        # Title
        self.title = QLabel(self)
        self.title.setText("Choose an option")
        self.title.resize(250, 30)
        self.title.move(30, 10)