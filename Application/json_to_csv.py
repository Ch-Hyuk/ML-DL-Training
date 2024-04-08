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

    def load_json(self):
        """JSON 파일을 로드하고 데이터를 반환합니다."""
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def convert(self):
        """JSON 데이터를 CSV로 변환합니다."""
        data = self.load_json()

        # 'fields'가 정의되지 않은 경우, JSON의 첫 번째 요소에서 키를 필드로 사용
        if not self.fields:
            self.fields = list(data[0].keys()) if data else []

        # 데이터 프레임 생성
        df = pd.DataFrame(data, columns=self.fields)

        # CSV 파일로 저장
        df.to_csv(self.csv_file_path, index=False, encoding='utf-8-sig')

        print(f'File converted and saved to {self.csv_file_path}')
