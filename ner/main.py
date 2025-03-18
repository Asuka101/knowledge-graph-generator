from ner import EntityRelationExtractor
from json2neo import JSONToNeo4jImporter

chapter_path = "./chapters/chapter" # 文本路径
prompt_path = "./prompt.md" # 提示词路径
save_path = "./data/data" # 保存路径
extarctor = EntityRelationExtractor(api_key="AIzaSyBQF-QGdS4oH63Md9txR7sEwloxi7oCyN4", 
                                        http_proxy="http://localhost:7890", https_proxy="http://localhost:7890") # 初始化知识抽取器
importer = JSONToNeo4jImporter(neo4j_url="bolt://localhost:7687", username="neo4j", password="password") # 初始化导入器
chapters = range(9) # 章节列表

# 加载提示词
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()
extarctor.load_prompt(prompt)

# 逐章节抽取知识并导入到 Neo4j
for chapter in chapters:
    text_path = f"{chapter_path}_{chapter}.txt"
    # 读取文本
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    extarctor.extract_entities_relations(text) # 实体和关系抽取
    extarctor.save(f"{save_path}_{chapter}.json") # 保存知识抽取结果
    importer.import_data(f"{save_path}_{chapter}.json") # 导入数据到 Neo4j