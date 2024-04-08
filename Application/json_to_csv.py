import os
import json
import pandas as pd

class JsonToCsvConverter:
    def __init__(self, json_file_path, csv_file_path, fields=None):
        """
        json_file_path: JSON 파일의 경로
        csv_file_path: 생성될 CSV 파일의 경로
        fields: CSV로 변환할 때 포함할 필드의 리스트. None이면 모든 필드를 포함.
        """
        self.json_file_path = json_file_path
        self.csv_file_path = csv_file_path
        self.fields = fields


    #json file load
    def load_json(self):
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    #convert json -> csv
    def convert(self):
        data = self.load_json()

        # 'fields'가 정의되지 않은 경우, JSON의 첫 번째 요소에서 키를 필드로 사용
        if not self.fields:
            self.fields = list(data[0].keys()) if data else []

        # 데이터 프레임 생성
        df = pd.DataFrame(data, columns=self.fields)

        # CSV 파일로 저장
        df.to_csv(self.csv_file_path, index=False, encoding='utf-8-sig')

        print(f'File converted and saved to {self.csv_file_path}')

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'file/json_file.json')
csv_path = os.path.join(script_dir, 'file/csv_file.csv')

# 필드 리스트 (옵션). None을 전달하면 JSON 파일의 모든 필드를 포함합니다.
fields = ['field1', 'field2', 'field3']

# 변환기 인스턴스 생성 및 변환 실행
converter = JsonToCsvConverter(json_path, csv_path, fields)
converter.convert()