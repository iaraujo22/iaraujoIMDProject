import sqlite3
from PySide6.QtWidgets import QWidget, QPushButton, QListWidget, QApplication, QListWidgetItem, QMessageBox, QLabel, QDialog
import pyqtgraph as pg
import sys

class Window(QWidget):
    def __init(self):
        super().__init__()
        '''
        #Database tools
        self.cursor = curs
        self.connection = conn
        #self.data = data_to_show
        '''

        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 600, 300)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowTitle("IMDB")
        # Title
        self.title = QLabel(self)
        self.title.setText("Choose an option")
        self.title.resize(250, 30)
        self.title.move(30, 10)

        # Buttons

        # Update Data Button
        self.update_button = QPushButton(self)
        self.update_button.setText("Update")
        self.update_button.resize(180, 30)
        self.update_button.move(30, 50)
        self.update_button.clicked.connect(self)

        # Visualize Data Button
        self.visualize_button = QPushButton(self)
        self.visualize_button.setText("Visualize")
        self.visualize_button.resize(180, 30)
        self.visualize_button.move(30, 100)
        self.visualize_button.clicked.connect(self)

    def update_button_clicked(self):
        conn = self.connection
        curs = self.cursor()
        self.cam = UpdateWindow(conn, curs)
        self.cam.show()
        self.close()

    def visualize_button_clicked(self):
        conn = self.connection
        curs = self.cursor()
        self.cam = VisualizeWindow(conn, curs)
        self.cam.show()
        self.close()

class UpdateWindow(QDialog):
    def __init__(self, conn):
        super().__init__()
        #Database
        self.cursor = curs
        self.connection = conn

        self.setWindowTitle("Update")
        self.setGeometry(100, 100, 600, 300)
        self.setup_update_ui()
        self.show()

    def setup_update_ui(self):
        self.update_title = QLabel(self)
        self.update_title.setText("Update")

class VisualizeWindow(QDialog):
    def __init__(self, conn):
        super().__init__()
        #Database
        self.cursor = curs
        self.connection = conn

        self.setWindowTitle("Visualize")
        self.setGeometry(100, 100, 600, 300)
        self.setup_visualize_ui()
        self.show()

    def setup_visualize_ui(self):
            self.update_title = QLabel(self)
            self.update_title.setText("Choose an Option")
            self.title.resize(250, 30)
            self.title.move(30, 10)

            #Movie Button
            self.visualize_button = QPushButton(self)
            self.visualize_button.setText("Movies")
            self.visualize_button.resize(180, 30)
            self.visualize_button.move(30, 100)
            self.visualize_button.clicked.connect(self)

            #Tv Show Button
            self.visualize_button = QPushButton(self)
            self.visualize_button.setText("TV Show")
            self.visualize_button.resize(180, 30)
            self.visualize_button.move(30, 100)
            self.visualize_button.clicked.connect(self)