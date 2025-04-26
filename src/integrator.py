# description: 知识融合器
import os
import json
from collections import defaultdict
from dotenv import load_dotenv
from libs.llm import KnowledgeProcessor

class Integrator:
    def __init__(self):
        load_dotenv()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.abspath(os.path.join(self.base_dir, os.getenv("DATA_PATH")))
        self.chapter_name = os.getenv("CLEANED_NAME")
        self.data_name = os.getenv("DATA_NAME")
        self.filtered_data_name = os.getenv("FILTERED_DATA_NAME")
        self.data_type = os.getenv("DATA_TYPE")

        # 提示词配置及完整路径
        self.prompt_path = os.path.abspath(os.path.join(self.base_dir, os.getenv("PROMPT_PATH")))
        self.prompt_name = os.getenv("PROMPT4INTEGRATOR_NAME")
        self.prompt_entities = os.getenv("PROMPT4INTEGRATOR_ENTITIES_NAME")
        self.prompt_relations = os.getenv("PROMPT4INTEGRATOR_RElATIONS_NAME")
        self.prompt_extension = os.getenv("PROMPT_TYPE")

        # API 配置
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL")
        self.base_url = os.getenv("BASE_URL")

    def load_prompt(self):
        # 加载提示词文件
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"提示词路径 {self.prompt_path} 不存在")
        prompt_file = os.path.join(self.prompt_path, f"{self.prompt_name}{self.prompt_extension}")
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
        self.processor.load_prompt(prompt)

    def merge(self):
        print("开始合并知识抽取结果...")
        # 合并知识抽取结果
        data = {"entities": [], "relations": []}
        filtered_data = {"entities": [], "relations": []}
        data_file = os.path.join(self.path, f"{self.data_name}.json")
        filtered_data_file = os.path.join(self.path, f"{self.filtered_data_name}.json")

        # 遍历并合并目录中的所有 JSON 文件
        for filename in os.listdir(self.path):
            if filename.endswith(".json") and filename.split("_")[0] == self.chapter_name:
                file_path = os.path.join(self.path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    chapter = json.load(file)
                    if "entities" in data:
                        data["entities"].extend(chapter["entities"])
                    if "relations" in data:
                        data["relations"].extend(chapter["relations"])
        
        # 去重实体和关系
        data = self.deduplicate_entities(data)

        # 仅保留实体的ID、name、type字段
        filtered_entities = []
        for entity in data["entities"]:
            filtered_entity = {
                "ID": entity.get("ID"),
                "name": entity.get("name"),
                "type": entity.get("type")
            }
            filtered_entities.append(filtered_entity)
        filtered_data["entities"] = filtered_entities
        filtered_data["relations"] = data["relations"]  # 保留关系

        # 将合并后的数据写入输出文件
        with open(data_file, "w", encoding="utf-8") as output:
            json.dump(data, output, ensure_ascii=False, indent=4)
        with open(filtered_data_file, "w", encoding="utf-8") as output:
            json.dump(filtered_data, output, ensure_ascii=False, indent=4)
        print(f"数据合并完成!")

    def deduplicate_entities(self, data):
        # 创建一个字典来跟踪已经看到的实体（按名称和类型分组）
        seen_entities = defaultdict(list)
        
        # 用于存储需要保留的实体ID和它们的替代ID
        id_mapping = {}
        
        # 第一步：识别重复实体并建立ID映射
        new_entities = []
        for entity in data["entities"]:
            key = (entity["name"], entity["type"])
            if key in seen_entities:
                # 这是一个重复实体，记录ID映射
                original_id = seen_entities[key][0]["ID"]
                id_mapping[entity["ID"]] = original_id
            else:
                # 这是一个新实体，添加到已见列表和结果列表中
                seen_entities[key].append(entity)
                new_entities.append(entity)
                id_mapping[entity["ID"]] = entity["ID"]  # 映射到自身
        
        # 第二步：更新关系中的实体ID
        new_relations = []
        for relation in data["relations"]:
            # 创建关系的副本
            new_relation = relation.copy()
            
            # 更新源ID和目标ID
            if relation["source"] in id_mapping:
                new_relation["source"] = id_mapping[relation["source"]]
            if relation["target"] in id_mapping:
                new_relation["target"] = id_mapping[relation["target"]]
            
            # 只有当源和目标都保留时才保留这个关系
            if new_relation["source"] != new_relation["target"]:  # 避免自引用
                key = (new_relation["type"], new_relation["source"], new_relation["target"])
                if key not in new_relations:
                    new_relations.append(new_relation)
        
        # 构建去重后的JSON数据
        deduplicated_data = {
            "entities": new_entities,
            "relations": new_relations
        }
        
        return deduplicated_data

    def integrate(self):
        print("开始知识融合...")
        # 初始化知识处理器
        self.processor = KnowledgeProcessor(api_key=self.api_key, model=self.model, base_url=self.base_url)
        self.load_prompt()
        source = os.path.join(self.path, f"{self.filtered_data_name}.json")
        filtered = os.path.join(self.path, f"{self.filtered_data_name}.json")
        target = os.path.join(self.path, f"{self.data_name}.json")
        
        # 读取待融合的文件
        if not os.path.exists(source):
            print(f"文件 {source} 未找到。")
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()
        
        self.processor.integrate(text, save_path=filtered, modify_json=True)
        with open(filtered, "r", encoding="utf-8") as f:
            filtered_data = f.read()
            filtered_data = json.loads(filtered_data)
        with open(target, "r", encoding="utf-8") as f:
            data = f.read()
            data = json.loads(data)
        
        # 按ID将attributes赋值给filtered_data里的实体
        id2attributes = {entity["ID"]: entity.get("attributes") for entity in data["entities"]}
        for entity in filtered_data["entities"]:
            if entity["ID"] in id2attributes:
                entity["attributes"] = id2attributes[entity["ID"]]

        # 保存带attributes的新filtered_data
        with open(target, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)

        print(f"知识融合完成！")

if __name__ == "__main__":
    integrator = Integrator()
    integrator.merge()
    integrator.integrate()