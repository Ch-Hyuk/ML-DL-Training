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

    #menu_bar
    def menu_bar(self):
        exitAction = QAction(QIcon("C:/workspace/ML&DL/Application/img/test2.png"), 'Exit', self)
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