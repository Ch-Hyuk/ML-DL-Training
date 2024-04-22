import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, qApp, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QLabel, QInputDialog, QTreeView
from PyQt5.QtGui import QIcon,QStandardItem, QStandardItemModel
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5 import uic


import pandas as pd
import json
from pymongo import MongoClient

#from_class = uic.loadUiType("ui1.ui")[0]


#Database Tree viewer
class DBTreeView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()

        # tree view setting
        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Key', 'Value'])
        self.tree_view.setModel(self.model)

        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        # data load from Database
        self.load_data()

    def load_secure_json(self):
        with open ("./file/secure_data.json", "r") as f:
            data = json.load(f)

        Cluster_name = data["Cluster_name"]
        DB_id = data["DATABASE"]["DB_id"]
        DB_ps = data["DATABASE"]["DB_password"]
        DB_name = data["DATABASE"]["DB_name"]
        DB_col_name = data["DATABASE"]["Collection_name"]

        Address = "mongodb+srv://"+DB_id+":"+DB_ps+"@"+Cluster_name+".otujyun.mongodb.net/"

        return Address, DB_name, DB_col_name
    

    def load_data(self):
        Address, DB_name, Col_name = self.load_secure_json()
        client = MongoClient(Address)
        db = client[DB_name]
        collection = db[Col_name]

        # 컬렉션의 모든 문서를 불러옴
        documents = collection.find()
        for doc in documents:
            parent = QStandardItem(QIcon("./img/test2.png"), str(doc['name']))  # 문서 ID에 폴더 아이콘 사용
            for key, value in doc.items():
                if key == '_id':
                    continue
                key_item = QStandardItem(QIcon("./img/test.png"), str(key))
                value_item = QStandardItem(QIcon("./img/test.png"), str(value))
                key_item.setEditable(False)  # 키 아이템을 읽기 전용으로 설정
                value_item.setEditable(False)  # 값 아이템을 읽기 전용으로 설정
                parent.appendRow([key_item, value_item])
            self.model.appendRow(parent)

        self.tree_view.expandAll()  # 모든 노드 확장


#Application Class
class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    #window 기본 setting
    def initUI(self):
        self.setWindowTitle('My Application')
        self.setWindowIcon(QIcon("./img/test.png"))
        self.setGeometry(300, 300, 1000, 500)
        self.statusBar().showMessage('This is Statusbar')


        self.mongoTreeView = DBTreeView()
        self.setCentralWidget(self.mongoTreeView)
        self.Quit_button()
        self.text_submit_button()
        self.menu_bar()
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
        btn.move(300,50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

    #button method(text)
    def text_submit_button(self):
        btn = QPushButton('Submit', self)
        btn.setToolTip('This is a <b>SubmitButton</b> widget')
        btn.move(400,50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.text_dialog)


    def text_dialog(self):
        label = QLabel(self)
        label.setStyleSheet('background-color : green')
        label.setGeometry(10, 10, 200, 30)

        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Text Input')
        if ok:
            label.setText(text)


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
        exitAction = QAction(QIcon("./img/test2.png"), 'Exit', self)
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
