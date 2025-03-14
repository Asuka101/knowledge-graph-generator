from py2neo import Graph, Node, Relationship
import json

neo4j_url = "bolt://localhost:7687" # Neo4j 服务器地址
username = "neo4j" # Neo4j 用户名
password = "password" # Neo4j 密码
json_file = "extracted_data.json" # JSON 文件路径

# 连接到 Neo4j 数据库
graph = Graph(neo4j_url, auth=(username, password))

# 读取 JSON 文件
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历 JSON 数据并创建节点和关系
for entity in data["entities"]:
    node = Node(entity["type"], name=entity["name"], **entity["attributes"])
    graph.create(node)

for relation in data["relations"]:
    source_node = graph.nodes.match(name=relation["source"]).first()
    target_node = graph.nodes.match(name=relation["target"]).first()
    if source_node and target_node:
        rel = Relationship(source_node, relation["type"], target_node, **relation["attributes"])
        graph.create(rel)

print("JSON 数据已成功导入到 Neo4j！")