# Description: 从 JSON 文件导入数据到 Neo4j 数据库
from libs.json2neo import JSONToNeo4jImporter

data_path = "./data" # 导入数据路径
data_name = "data" # 数据名称
data_range = range(9) # 导入数据下标

importer = JSONToNeo4jImporter(neo4j_url="bolt://localhost:7687", username="neo4j", password="password") # 初始化 JSON 数据导入器

# 逐章导入 JSON 数据到 Neo4j
for data_index in data_range:
    json_filepath = f"{data_path}/{data_name}_{data_index}.json" # 合成 JSON 文件路径
    importer.import_data(json_filepath) # 导入 JSON 数据到 Neo4j