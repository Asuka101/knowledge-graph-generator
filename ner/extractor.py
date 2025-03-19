# Description: 从文本中抽取知识并保存
from libs.ner import EntityRelationExtractor

chapter_path = "./textbook/chapters/chapter" # 文本路径
prompt_path = "./prompt.md" # 提示词路径
data_path = "./data/data" # 保存路径
chapter_name = "chapter" # 章节名称
data_name = "data" # 数据名称
chapter_type = "txt" # 文本类型
data_type = "json" # 数据类型
extarctor = EntityRelationExtractor(api_key="AIzaSyBQF-QGdS4oH63Md9txR7sEwloxi7oCyN4", model="gemini-2.0-flash",
                                    http_proxy="http://localhost:7890", https_proxy="http://localhost:7890") # 初始化知识抽取器
chapter_indices = range(9) # 章节列表

# 加载提示词
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()
extarctor.load_prompt(prompt)

# 逐章节抽取知识并保存
for i in chapter_indices:
    text_path = f"{chapter_path}/{chapter_name}_{i}.{chapter_type}"
    # 读取文本
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    extarctor.extract_entities_relations(text) # 实体和关系抽取
    extarctor.save(f"{data_path}/{data_name}_{i}.{data_type}") # 保存知识抽取结果