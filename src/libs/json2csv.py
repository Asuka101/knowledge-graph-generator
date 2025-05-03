import json
import pandas as pd

class JSONToCSVConverter:
    def __init__(self):
        self.json = None
        self.entites = None
        self.relations = None
        self.data = None

    def load_json(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.json = json.load(f)
        except FileNotFoundError:
            print(f"文件 {json_path} 未找到")
            raise
        except json.JSONDecodeError:
            print(f"文件 {json_path} 解析错误")
            raise
        except Exception as e:
            print(f"加载 JSON 文件时发生错误: {e}")
            raise

    def convert_entities(self):
        entities_fields = [
            "实体类型", "ID", "名称", "难度", "内容", "存储开销", "核心特性",
            "时间复杂度", "空间复杂度", "设计思想", "适用场景"
        ]
        entities_data = []
        try:
            for entity in self.json["entities"]:
                row = {
                    "实体类型": entity["type"],
                    "ID": entity["ID"],
                    "名称": entity["name"],
                    "难度": entity["attributes"].get("难度", None),
                    "内容": entity["attributes"].get("内容", None),
                    "存储开销": entity["attributes"].get("存储开销", None),
                    "核心特性": entity["attributes"].get("核心特性", None),
                    "时间复杂度": entity["attributes"].get("时间复杂度", None),
                    "空间复杂度": entity["attributes"].get("空间复杂度", None),
                    "设计思想": entity["attributes"].get("设计思想", None),
                    "适用场景": entity["attributes"].get("适用场景", None),
                }
                entities_data.append(row)
            self.entities = pd.DataFrame(entities_data, columns=entities_fields)
        except KeyError as e:
            print(f"JSON 数据缺少必要字段: {e}")
            raise
        except Exception as e:
            print(f"转换实体数据时发生错误: {e}")
            raise

    def convert_relations(self):
        relations_fields = ["关系类型", "源实体", "目标实体"]
        relations_data = []
        try:
            for relation in self.json["relations"]:
                row = {
                    "关系类型": relation["type"],
                    "源实体": relation["source"],
                    "目标实体": relation["target"]
                }
                relations_data.append(row)
            self.relations = pd.DataFrame(relations_data, columns=relations_fields)
        except KeyError as e:
            print(f"JSON 数据缺少必要字段: {e}")
            raise
        except Exception as e:
            print(f"转换关系数据时发生错误: {e}")
            raise

    def merge(self):
        try:
            # 添加记录类型标识
            self.entities["记录类型"] = "实体"
            self.relations["记录类型"] = "关系"

            # 合并所有列（缺失值填充为NaN）
            self.data = pd.concat([self.entities, self.relations], ignore_index=True, sort=False)

            # 调整RecordType为首列
            cols = ["记录类型"] + [col for col in self.data.columns if col != "记录类型"]
            self.data = self.data[cols]
        except Exception as e:
            print(f"合并CSV数据时发生错误: {e}")
            raise


    def convert(self, csv_path):
        # 导出实体和关系到csv（临时文件或指定路径）
        self.convert_entities()
        self.convert_relations()
        # 合并并保存
        self.merge()
        try:
            self.data.to_csv(csv_path, index=False, encoding="utf-8")
        except Exception as e:
            print(f"保存 CSV 文件时发生错误: {e}")
            raise