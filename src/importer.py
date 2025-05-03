# Description: 数据导入器
import os
from src.libs.json2neo import JSONToNeo4jImporter

class Importer:
    def __init__(self):
        # 汇总数据文件配置及完整路径（待导入的 JSON 文件）
        self.source_path = os.getenv("DATA_PATH")
        self.source_filename = os.getenv("DATA_NAME")

        # Neo4j 配置（示例中部分参数固定，建议从环境变量读取）
        self.neo4j_url = os.getenv("NEO4J_URL")
        self.neo4j_username = os.getenv("NEO4J_USERNAME")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        self.importer = JSONToNeo4jImporter(
            neo4j_url=self.neo4j_url,
            username=self.neo4j_username,
            password=self.neo4j_password
        )

    def import_data(self):
        print("开始导入数据到 Neo4j...")
        # 汇总数据导入
        json_file = os.path.join(self.source_path, f"{self.source_filename}.json")
        self.importer.import_data(json_file)
        print(f"数据导入完成！")