import json

def print_json_structure(data, indent=0):
    """ JSON 데이터 구조를 재귀적으로 출력하는 함수 """
    space = ' ' * (indent * 4)  # 들여쓰기를 위한 공백 생성
    if isinstance(data, dict):  # 데이터가 딕셔너리인 경우
        print(f"{space}Object with {len(data)} properties:")
        for key, value in data.items():
            print(f"{space}  - {key}:", end=" ")
            print_json_structure(value, indent + 1)
    elif isinstance(data, list):  # 데이터가 리스트인 경우
        print(f"{space}Array with {len(data)} items:")
        for item in data:
            print_json_structure(item, indent + 1)
    else:  # 데이터가 기본 타입인 경우 (문자열, 숫자, 등)
        print(f"{space}{type(data).__name__}")

def analyze_json_file(file_path):
    """ JSON 파일을 로드하고 구조를 출력하는 함수 """
    with open(file_path, 'r') as file:
        data = json.load(file)
        print_json_structure(data)

# 사용 예
file_path = 'c:/workspace/ML&DL/Application/file/Submodel_Technical_Data.json'  # 분석할 JSON 파일 경로
analyze_json_file(file_path)