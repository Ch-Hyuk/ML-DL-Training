# json 데이터 시각화 실험을 위한 copy 본

import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, qApp, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QLabel, QInputDialog, QTreeView, QSplitter
from PyQt5.QtGui import QIcon,QStandardItem, QStandardItemModel
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5 import uic


import pandas as pd
import json
from pymongo import MongoClient

#from_class = uic.loadUiType("ui1.ui")[0]


class DetailsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.details_label = QLabel("Select an item from the tree view")
        self.layout.addWidget(self.details_label)

    def update_details(self, text):
        self.details_label.setText(text)



#Database Tree viewer
class DataViewSection(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 300, 200)
        layout = QVBoxLayout()

        # tree view setting
        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)
        self.tree_view.header().hide()
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        # data load from Database
        self.load_data()

    def load_secure_json(self):
        with open ("./file/secure_data.json", "r") as f:
            data = json.load(f)

        Cluster_name = data["Cluster_name"]
        DB_id = data["DATABASE1"]["DB_id"]
        DB_ps = data["DATABASE1"]["DB_password"]
        DB_name = data["DATABASE1"]["DB_name"]
        DB_col_name = data["DATABASE1"]["Collection_name"]

        Address = "mongodb+srv://"+DB_id+":"+DB_ps+"@"+Cluster_name+".otujyun.mongodb.net/"

        return Address, DB_name, DB_col_name
    
    def add_items(self, parent, key, value):
        if isinstance(value, dict):  # 값이 딕셔너리인 경우, 중첩된 노드 처리
            parent_node = QStandardItem(QIcon("./icon/free-icon-app-2305920.png"), str(key))
            parent.appendRow(parent_node)
            for subkey, subvalue in value.items():
                self.add_items(parent_node, subkey, subvalue)
        else:
            # 기본 키-값 쌍을 처리, "key: value" 형식으로 표현
            item_text = f"{key}: {str(value)}"
            item = QStandardItem(QIcon("./icon/test.png"), item_text)
            item.setEditable(False)
            parent.appendRow(item)

    def load_data(self):
        Address, DB_name, Col_name = self.load_secure_json()
        client = MongoClient(Address)
        db = client[DB_name]
        collection = db[Col_name]

        # 컬렉션의 모든 문서를 불러옴
        documents = collection.find()
        for doc in documents:
            # 가정: 'Collection_001' 이 중첩된 문서 구조를 가지고 있다고 가정
            if 'Collection_001' in doc and isinstance(doc['Collection_001'], dict):
                parent = QStandardItem(QIcon("./img/test2.png"), str(doc['Collection_001']['Name']))
                for key, value in doc['Collection_001'].items():
                    if key == '_id':
                        continue
                    self.add_items(parent, key, value)
                self.model.appendRow(parent)

        self.tree_view.expandAll()

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
        #self.statusBar().showMessage('This is Statusbar')

        splitter = QSplitter(Qt.Horizontal, self)
        self.setCentralWidget(splitter)

        self.TreeView = DataViewSection()

        self.model = QStandardItemModel()
        self.TreeView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Tree Items'])

        self.details_view = DetailsView()

        splitter.addWidget(self.tree_view)
        splitter.addWidget(self.details_view)
        
        #self.Quit_button()
        #self.text_submit_button()
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
