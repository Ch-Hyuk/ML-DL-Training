import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, qApp, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5 import uic


import pandas as pd
import json

#from_class = uic.loadUiType("ui1.ui")[0]



class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Quit_button()
        self.menu_bar()
        self.initUI()

    #window 기본 setting
    def initUI(self):
        self.setWindowTitle('My Application')
        self.setWindowIcon(QIcon("C:/workspace/ML&DL/Application/img/test.png"))
        self.setGeometry(300, 300, 1000, 500)

        self.statusBar().showMessage('This is Statusbar')
        self.center()
        self.show()

    #center window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    #button method(quit)
    def Quit_button(self):
        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50,50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

    def open_json(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)", options=options)
        if fileName:
            df = pd.read_json(fileName)
            # Convert to Excel
            df.to_excel(fileName.replace('.json', '.xlsx'))
            self.status_label.setText(f'Converted {fileName} to Excel')

    def open_excel(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)", options=options)
        if fileName:
            df = pd.read_excel(fileName)
            # Convert to JSON
            df.to_json(fileName.replace('.xlsx', '.json'))
            self.status_label.setText(f'Converted {fileName} to JSON')

    #menu_bar
    def menu_bar(self):

        #exit Action data
        exitAction = QAction(QIcon("C:/workspace/ML&DL/Application/img/test2.png"), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        #file open Action data
        fileOpen = QAction('test', self)
        fileOpen.triggered.connect(self.open_json)

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)

        filemenu = menuBar.addMenu('&File')
        
        filemenu.addAction(exitAction)
        filemenu.addAction(fileOpen)

        edit_menu = menuBar.addMenu('&Edit')
        edit_menu.addAction(exitAction)



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())


QWidget.setLayout()