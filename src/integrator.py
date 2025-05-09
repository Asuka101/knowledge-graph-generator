# description: 知识融合器
import os
import json
from collections import defaultdict, deque
from src.libs.llm import KnowledgeProcessor

class Integrator:
    def __init__(self):
        self.data_path = os.getenv("DATA_PATH")
        self.chapter_data_path = os.getenv("CHAPTER_DATA_PATH")
        self.chapter_name = os.getenv("CLEANED_NAME")
        self.data_name = os.getenv("DATA_NAME")
        self.filtered_data_name = os.getenv("FILTERED_DATA_NAME")

        # 提示词配置及完整路径
        self.prompt_path = os.getenv("PROMPT_PATH")
        self.prompt_name = os.getenv("PROMPT4INTEGRATOR_NAME")
        self.prompt_entities = os.getenv("PROMPT4INTEGRATOR_ENTITIES_NAME")
        self.prompt_relations = os.getenv("PROMPT4INTEGRATOR_RElATIONS_NAME")
        self.prompt_extension = os.getenv("PROMPT_TYPE")

        # API 配置
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL")
        self.base_url = os.getenv("BASE_URL")

        # 初始化知识处理器和转换器
        self.processor = None

    def load_prompt(self):
        # 加载提示词文件
        prompt_file = os.path.join(self.prompt_path, f"{self.prompt_name}{self.prompt_extension}")
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
        self.processor.load_prompt(prompt)

    def merge(self):
        print("开始合并知识抽取结果...")
        # 合并知识抽取结果
        data = {"entities": [], "relations": []}
        filtered_data = {"entities": [], "relations": []}
        data_file = os.path.join(self.data_path, f"{self.data_name}.json")
        filtered_data_file = os.path.join(self.data_path, f"{self.filtered_data_name}.json")

        # 遍历并合并目录中的所有 JSON 文件
        for filename in os.listdir(self.chapter_data_path):
            if filename.endswith(".json") and filename.split("_")[0] == self.chapter_name:
                file_path = os.path.join(self.chapter_data_path, filename)
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

    # 去重实体和关系
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
        
        # 第二步：更新关系中的ID
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

    # 过滤掉不连通的图
    def filter_connected_graph(self, data):
        # 构建无向图
        graph = defaultdict(set)
        entity_ids = set(entity["ID"] for entity in data["entities"])
        for rel in data["relations"]:
            graph[rel["source"]].add(rel["target"])
            graph[rel["target"]].add(rel["source"])

        # 找最大连通分量
        visited = set()
        components = []
        for eid in entity_ids:
            if eid not in visited:
                queue = deque([eid])
                comp = set()
                while queue:
                    node = queue.popleft()
                    if node not in visited:
                        visited.add(node)
                        comp.add(node)
                        queue.extend(graph[node] - visited)
                components.append(comp)
        if not components:
            print("无连通分量")
            return

        main_component = max(components, key=len)

        # 过滤实体和关系
        filtered_entities = [e for e in data["entities"] if e["ID"] in main_component]
        filtered_relations = [
            r for r in data["relations"]
            if r["source"] in main_component and r["target"] in main_component
        ]

        # 保存结果
        filtered_data = {"entities": filtered_entities, "relations": filtered_relations}
        return filtered_data

    def integrate(self):
        print("开始知识融合...")
        self.merge()
        # 初始化知识处理器
        self.processor = KnowledgeProcessor(api_key=self.api_key, model=self.model, base_url=self.base_url)
        self.load_prompt()
        source = os.path.join(self.data_path, f"{self.filtered_data_name}.json")
        target = os.path.join(self.data_path, f"{self.data_name}.json")
        
        # 读取用于知识融合的数据
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()
        
        self.processor.integrate(text, save_path=source, modify_json=True)
        with open(source, "r", encoding="utf-8") as f:
            filtered_data = f.read()
            filtered_data = json.loads(filtered_data)
        with open(target, "r", encoding="utf-8") as f:
            data = f.read()
            data = json.loads(data)

        filtered_data = self.filter_connected_graph(filtered_data)
        
        # 按ID将attributes赋值给filtered_data里的实体
        id2attributes = {entity["ID"]: entity.get("attributes") for entity in data["entities"]}
        for entity in filtered_data["entities"]:
            if entity["ID"] in id2attributes:
                entity["attributes"] = id2attributes[entity["ID"]]

        # 保存带attributes的新filtered_data
        with open(target, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)

        print(f"知识融合完成！")