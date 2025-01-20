import pandas as pd
import requests
from pandas import DataFrame


class DataLoader:
    @staticmethod
    def load_csv(file_path: str) -> DataFrame:
        return pd.read_csv(file_path)

    @staticmethod
    def load_json(file_path: str) -> DataFrame:
        return pd.read_json(file_path)

    @staticmethod
    def load_api(url: str) -> DataFrame:
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            raise Exception(f"API request failed with status code {response.status_code}")

    def __init__(self, file_path: str, file_type: str):
        if file_type == 'csv':
            self.data = DataLoader.load_csv(file_path)
        elif file_type == 'json':
            self.data = DataLoader.load_json(file_path)
        else:
            self.data = DataLoader.load_api(file_path)

    def get_data(self):
        return self.data
