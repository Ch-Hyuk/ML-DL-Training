import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant

class JsonTreeModel(QAbstractItemModel):
    def __init__(self, data):
        super(JsonTreeModel, self).__init__()
        self.root_data = ('Root', data)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Elements"

    def rowCount(self, parent):
        if not parent.isValid():
            parent_data = self.root_data
        else:
            parent_data = parent.internalPointer()
        return len(parent_data[1])

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            return item[0]

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child = index.internalPointer()
        parent_data = self.get_parent(child)

        if parent_data == self.root_data:
            return QModelIndex()

        return self.createIndex(self.get_row(parent_data), 0, parent_data)

    def index(self, row, column, parent):
        if not parent.isValid():
            parent_data = self.root_data
        else:
            parent_data = parent.internalPointer()

        try:
            key, value = list(parent_data[1].items())[row]
            # 튜플 대신 새 객체를 생성하여 가비지 컬렉터의 중복 추적 문제 방지
            child = (key, value)
            return self.createIndex(row, column, child)
        except (IndexError, KeyError):
            return QModelIndex()

    def get_parent(self, child):
        for parent, data in self.iterate_items(self.root_data):
            if child in data.items():
                return (parent, data)
        return None

    def get_row(self, child):
        parent = self.get_parent(child)
        if parent:
            return list(parent[1].values()).index(child[1])
        return 0

    def iterate_items(self, item):
        stack = [item]
        while stack:
            parent, data = stack.pop()
            yield parent, data
            if isinstance(data, dict):
                stack.extend(data.items())

class MainWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.tree_view = QTreeView()
        self.model = JsonTreeModel(data)
        self.tree_view.setModel(self.model)
        self.tree_view.clicked.connect(self.on_item_clicked)

        self.setCentralWidget(self.tree_view)
        self.setWindowTitle("JSON Tree Viewer")
        self.resize(600, 400)

    def on_item_clicked(self, index):
        item = index.internalPointer()
        if isinstance(item[1], str):
            QMessageBox.information(self, "Item Value", f"The value is: {item[1]}")

def main():
    app = QApplication(sys.argv)

    with open('./file/tree_view_matadata.json', 'r') as file:
        data = json.load(file)

    main_window = MainWindow(data['Mata_Data'])
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()