# Description: 数据导入器
import os
from dotenv import load_dotenv
from libs.json2neo import JSONToNeo4jImporter

class Importer:
    def __init__(self):
        load_dotenv()  # 加载环境变量
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # 汇总数据文件配置及完整路径（待导入的 JSON 文件）
        self.source_path = os.path.abspath(os.path.join(self.base_dir, os.getenv("DATA_PATH")))
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
        # 汇总数据导入
        json_file = os.path.join(self.source_path, f"{self.source_filename}.json")
        self.importer.import_data(json_file)
        print(f"汇总数据已导入：{json_file}")

if __name__ == "__main__":
    importer = Importer()
    importer.import_data() 
    print("数据导入完成！")