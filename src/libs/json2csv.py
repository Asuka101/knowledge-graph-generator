import json
import pandas as pd

class JSONToCSVConverter:
    def __init__(self):
        self.json = None
        self.entites = None
        self.relations = None

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
                    "名称": entity["name"]
                }
                row.update(entity.get("attributes", {}))
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


    def convert(self, entities_path, relations_path):
        # 导出实体和关系到csv（临时文件或指定路径）
        self.convert_entities()
        self.convert_relations()
        # 构建ID到名称的映射字典
        if "ID" in self.entities.columns and "名称" in self.entities.columns:
            id_name_map = self.entities.set_index("ID")["名称"].to_dict()
            # 用map直接映射并拼接
            for col in ["源实体", "目标实体"]:
                self.relations[col] = self.relations[col].map(id_name_map)
        try:
            self.entities.to_csv(entities_path, index=False, encoding="utf-8")
            self.relations.to_csv(relations_path, index=False, encoding="utf-8")
        except Exception as e:
            print(f"保存 CSV 文件时发生错误: {e}")
            raise