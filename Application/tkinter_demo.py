import tkinter as tk
from tkinter import filedialog
import os

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        # 여기에 파일을 열었을 때의 로직을 추가하세요
        print(f"{filepath} 파일이 열렸습니다.")

def calculate():
    # 계산기 로직을 여기에 추가하세요
    print("계산기 기능 실행")

def modeling():
    # 모델링 작업 로직을 여기에 추가하세요
    print("모델링 작업 실행")


if __name__ == '__main__':
    print("Program Start")
    app = tk.Tk()
    app.title('멀티 기능 응용 프로그램')

    btn_open_file = tk.Button(app, text='파일 열기', command=open_file)
    btn_open_file.pack()

    btn_calculate = tk.Button(app, text='계산기', command=calculate)
    btn_calculate.pack()

    btn_modeling = tk.Button(app, text='모델링 작업', command=modeling)
    btn_modeling.pack()

    app.mainloop()
    print("Program Closed")