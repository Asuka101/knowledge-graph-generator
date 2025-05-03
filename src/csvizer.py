# description: CSV 转换器
import os
from src.libs.json2csv import JSONToCSVConverter

class CSVizer:
    def __init__(self):
        # 汇总数据文件配置及完整路径
        self.data_path = os.getenv("DATA_PATH")
        self.data_name = os.getenv("DATA_NAME")
        self.csv_path = os.getenv("CSV_PATH")
        self.entities_name = os.getenv("ENTITIES_NAME")
        self.relations_name = os.getenv("RELATIONS_NAME")

        # CSV 转换器初始化
        self.converter = JSONToCSVConverter()

    def convert(self):
        print("开始转换 JSON 数据为 CSV 格式...")
        json_file = os.path.join(self.data_path, f"{self.data_name}.json")
        entities_file = os.path.join(self.csv_path, f"{self.entities_name}.csv")
        relations_file = os.path.join(self.csv_path, f"{self.relations_name}.csv")
        self.converter.load_json(json_file)
        self.converter.convert(entities_file, relations_file)
        print(f"转换完成!")