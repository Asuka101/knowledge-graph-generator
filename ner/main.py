from ner import EntityRelationExtractor
from json2neo import JSONToNeo4jImporter

text_path = "./chapters/chapter_1.txt" # 文本路径
prompt_path = "./prompt.md" # 提示词路径
# 读取文本和提示词
with open(text_path, "r", encoding="utf-8") as f:
    text = f.read()
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()

extarctor = EntityRelationExtractor(api_key="AIzaSyBQF-QGdS4oH63Md9txR7sEwloxi7oCyN4", 
                                    http_proxy="http://localhost:7890", https_proxy="http://localhost:7890") # 初始化知识抽取器
extarctor.load(prompt, text) # 加载提示词和文本至抽取器
extarctor.extract_entities_relations() # 实体和关系抽取
extarctor.save("./data.json") # 保存知识抽取结果
importer = JSONToNeo4jImporter(neo4j_url="bolt://localhost:7687", username="neo4j", password="password") # 初始化导入器
importer.import_data("./data.json") # 导入知识抽取结果至Neo4j