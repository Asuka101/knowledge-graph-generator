# Description: JSON 数据导入到 Neo4j 数据库
from py2neo import Graph, Node, Relationship
import json

class JSONToNeo4jImporter:
    def __init__(self, neo4j_url, username, password):
        self.neo4j_url = neo4j_url # Neo4j 数据库 URL
        self.username = username # 用户名
        self.password = password # 密码

        # 连接 Neo4j 数据库
        try:
            self.graph = Graph(self.neo4j_url, auth=(self.username, self.password))
        except Exception as e:
            print(f"连接 Neo4j 数据库失败: {e}")
            raise

    def import_data(self, json_filepath):
        # 读取 JSON 文件
        try:
            with open(json_filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"文件未找到: {json_filepath}")
            return False
        except json.JSONDecodeError:
            print(f"JSON 解码失败: {json_filepath}")
            return False
        except Exception as e:
            print(f"读取 JSON 文件失败: {e}")
            return False
        
        # 导入数据到 Neo4j
        try:
            for entity in data["entities"]:
                node = Node(entity["type"], id=entity["ID"], name=entity["name"], **entity["attributes"])
                self.graph.create(node)
            for relation in data["relations"]:
                source_node = self.graph.nodes.match(id=relation["source"]).first()
                target_node = self.graph.nodes.match(id=relation["target"]).first()
                if source_node and target_node:
                    rel = Relationship(source_node, relation["type"], target_node, id=relation["ID"])
                    self.graph.create(rel)
            print(f"{json_filepath.split('/')[-1]}已成功导入到 Neo4j！")
            return True
        except Exception as e:
            print(f"导入数据到 Neo4j 失败: {e}")
            return False