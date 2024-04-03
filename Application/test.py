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
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class MyApp1(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        #window 기본 setting
        self.setWindowTitle('Test App')
        self.setWindowIcon(QIcon("C:/workspace/ML&DL/Application/test.png"))
        self.setGeometry(300, 300, 1000, 500)
        
        #Quit button
        btn = QPushButton("Quit", self)
        btn.move(300, 300)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)
        
        
        
        self.show()

class MyApp2(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('This is Statusbar')

        self.setWindowTitle('Statusbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

class MyApp3(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon("C:/workspace/ML&DL/Application/test2.png"), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp3()
   sys.exit(app.exec_())


QWidget.setLayout()