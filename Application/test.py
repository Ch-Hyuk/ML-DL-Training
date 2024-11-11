import tkinter as tk
from tkinter import ttk

def on_tree_select(event):
    selected_item = tree.selection()[0]  # 선택된 아이템의 ID
    children = tree.get_children(selected_item)
    
    # Leaf 노드인 경우
    if not children:
        # 이미 데이터가 있는지 확인하고, 없다면 오른쪽 열에 데이터 표시
        if tree.set(selected_item, "Detail1") == "":
            # 예시 데이터를 설정
            tree.set(selected_item, "Detail1", "Detail 1")
            tree.set(selected_item, "Detail2", "Detail 2")
            tree.set(selected_item, "Detail3", "Detail 3")

# 기본 윈도우 생성
root = tk.Tk()
root.geometry("600x400")

# Treeview 생성 (여러 열 설정)
columns = ("MainItem", "Detail1", "Detail2", "Detail3")
tree = ttk.Treeview(root, columns=columns, show="headings")

# 열 헤더 설정
tree.heading("MainItem", text="Main Item")
tree.heading("Detail1", text="Detail 1")
tree.heading("Detail2", text="Detail 2")
tree.heading("Detail3", text="Detail 3")

# 트리뷰에 상위 노드 및 하위 노드 추가
parent1 = tree.insert("", "end", text="Parent 1", values=("Parent 1", "", "", ""))
leaf1 = tree.insert(parent1, "end", text="Leaf 1", values=("Leaf 1", "", "", ""))
leaf2 = tree.insert(parent1, "end", text="Leaf 2", values=("Leaf 2", "", "", ""))

parent2 = tree.insert("", "end", text="Parent 2", values=("Parent 2", "", "", ""))
leaf3 = tree.insert(parent2, "end", text="Leaf 3", values=("Leaf 3", "", "", ""))
leaf4 = tree.insert(parent2, "end", text="Leaf 4", values=("Leaf 4", "", "", ""))

# Treeview 선택 이벤트 바인딩
tree.bind("<<TreeviewSelect>>", on_tree_select)

# 트리뷰 배치
tree.pack(expand=True, fill="both")

root.mainloop()
