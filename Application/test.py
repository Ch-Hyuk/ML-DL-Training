# import tkinter as tk
# from tkinter import filedialog
# import os

# def open_file():
#     filepath = filedialog.askopenfilename()
#     if filepath:
#         # 여기에 파일을 열었을 때의 로직을 추가하세요
#         print(f"{filepath} 파일이 열렸습니다.")

# def calculate():
#     # 계산기 로직을 여기에 추가하세요
#     print("계산기 기능 실행")

# def modeling():
#     # 모델링 작업 로직을 여기에 추가하세요
#     print("모델링 작업 실행")


# if __name__ == '__main__':
#     print("Program Start")
#     app = tk.Tk()
#     app.title('멀티 기능 응용 프로그램')

#     btn_open_file = tk.Button(app, text='파일 열기', command=open_file)
#     btn_open_file.pack()

#     btn_calculate = tk.Button(app, text='계산기', command=calculate)
#     btn_calculate.pack()

#     btn_modeling = tk.Button(app, text='모델링 작업', command=modeling)
#     btn_modeling.pack()

#     app.mainloop()
#     print("Program Closed")

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, qApp, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Quit_button()
        self.menu_bar()
        self.initUI()

    #window 기본 setting
    def initUI(self):
        self.setWindowTitle('My Application')
        self.setWindowIcon(QIcon("C:/workspace/ML&DL/Application/test.png"))
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

    #menu_bar
    def menu_bar(self):
        exitAction = QAction(QIcon("C:/workspace/ML&DL/Application/test2.png"), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)

        filemenu = menuBar.addMenu('&File')
        filemenu.addAction(exitAction)

        edit_menu = menuBar.addMenu('&Edit')
        edit_menu.addAction(exitAction)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())


QWidget.setLayout()