from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt, QMimeData, QPoint, QPropertyAnimation
from PyQt5.QtGui import QDrag, QPixmap, QPainter
import sys

class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(item.text(0))
            drag.setMimeData(mimeData)

            # 선택된 항목의 픽스맵 생성
            pixmap = QPixmap(200, 30)  # 적당한 크기의 픽스맵 생성
            pixmap.fill(Qt.transparent)  # 배경을 투명하게 설정
            painter = QPainter(pixmap)
            painter.setPen(Qt.black)
            painter.setFont(self.font())
            painter.drawText(pixmap.rect(), Qt.AlignLeft, item.text(0))  # 텍스트를 픽스맵에 그림
            painter.end()

            drag.setPixmap(pixmap)

            # 드래그 시작 전에 선택 상태 해제
            self.setCurrentItem(None)

            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        target_item = self.itemAt(event.pos())
        dragged_item = self.currentItem()

        if target_item and dragged_item and target_item != dragged_item:
            # 부모가 같은지 확인
            dragged_item_parent = dragged_item.parent() or self.invisibleRootItem()
            target_item_parent = target_item.parent() or self.invisibleRootItem()

            if dragged_item_parent == target_item_parent:
                # 항목의 부모로부터 드래그된 항목을 제거하기 전에 복제
                dragged_item_clone = self.clone_item(dragged_item)
                target_index = target_item_parent.indexOfChild(target_item)
                
                # 새로운 위치로 항목 삽입
                target_item_parent.insertChild(target_index, dragged_item_clone)
                
                # 트리에서 기존 항목 삭제
                dragged_item_parent.removeChild(dragged_item)

                # 드롭된 후 항목 선택
                self.setCurrentItem(dragged_item_clone)

        event.accept()

    def clone_item(self, item):
        # 항목을 복제하는 함수 (자식 항목들도 함께 복제)
        clone = QTreeWidgetItem([item.text(0)])
        for i in range(item.childCount()):
            child_clone = self.clone_item(item.child(i))
            clone.addChild(child_clone)
        return clone

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Draggable Tree View with Correct Selection")
        self.setGeometry(100, 100, 1200, 600)

        # 메인 위젯
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 메인 레이아웃 (수평 분할)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 좌측 트리뷰 (계층적 데이터 표현)
        self.tree = TreeWidget()
        self.tree.setHeaderHidden(True)
        self.populate_tree()  # 트리 데이터 추가
        self.tree.itemClicked.connect(self.on_item_click)

        # 우측 상세 정보 영역
        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        self.create_detail_view()

        # Splitter 사용해 좌측 트리뷰와 우측 상세정보 분할
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.detail_widget)
        splitter.setSizes([300, 900])

        # 메인 레이아웃에 splitter 추가
        main_layout.addWidget(splitter)

        # 테마 색상 적용
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e8d5b5;
            }
            QTreeWidget {
                background-color: #aca9bb;
                color: white;
                font-size: 14px;
                border: none;
            }
            QTreeWidget::item {
                margin: 2px;
                padding: 5px;
                border: 1px solid #787586;  /* 테두리 효과 */
                border-radius: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #787586;
                color: white;
                border: 2px solid #e8d5b5; /* 선택된 항목 테두리 */
            }
            QLabel {
                font-size: 14px;
                color: #787586;
            }
            QLineEdit {
                background-color: #aca9bb;
                border: 1px solid #787586;
                color: white;
                font-size: 14px;
                padding: 5px;
            }
            QPushButton {
                background-color: #787586;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #aca9bb;
            }
        """)

    def populate_tree(self):
        # 트리의 루트 요소 생성
        root = QTreeWidgetItem(self.tree, ["Package"])
        
        # 하위 항목 추가
        env = QTreeWidgetItem(root, ["Environment"])
        admin_shells = QTreeWidgetItem(env, ["AdministrationShells"])
        aas = QTreeWidgetItem(admin_shells, ["AAS"])
        asset_info = QTreeWidgetItem(aas, ["Asset Information"])
        submodel = QTreeWidgetItem(env, ["All Submodels"])
        concept_descriptions = QTreeWidgetItem(env, ["ConceptDescriptions"])
        
        # 하위 항목에 추가 요소
        QTreeWidgetItem(submodel, ["SM"])
        QTreeWidgetItem(submodel, ["SMC"])
        
        # 트리 펼치기
        self.tree.expandAll()

    def create_detail_view(self):
        # 상세정보 레이아웃을 구성하는 요소들
        self.info_label = QLabel("Select an item from the tree to view details.")
        self.detail_layout.addWidget(self.info_label)

        # 상세정보 필드 예시
        self.id_short_label = QLabel("idShort:")
        self.id_short_input = QLineEdit()
        self.sync_button = QPushButton("Sync")

        # 레이아웃에 필드 추가
        self.detail_layout.addWidget(self.id_short_label)
        self.detail_layout.addWidget(self.id_short_input)
        self.detail_layout.addWidget(self.sync_button)

    def on_item_click(self, item, column):
        # 트리에서 항목을 클릭했을 때 상세 정보 업데이트
        selected_text = item.text(0)
        self.info_label.setText(f"Details for: {selected_text}")

        # 예시로 항목 이름에 따라 값을 업데이트
        if selected_text == "AAS":
            self.id_short_input.setText("AAS_Identifier")
        else:
            self.id_short_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
