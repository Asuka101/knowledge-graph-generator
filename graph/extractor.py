# Description: 从文本中抽取知识并保存
from libs.ner import EntityRelationExtractor

# 文本路径和名称
chapter_path = "./textbook/cleaned_chapters/chapter" # 文本路径
chapter_type = ".txt" # 文本类型

# 提示词路径和名称
prompt_path = "./prompt/prompt" # 提示词路径
prompt_type = ".md" # 提示词类型

# 数据保存路径和名称
data_path = "./data/data" # 保存路径
data_type = ".json" # 数据类型

extarctor = EntityRelationExtractor(api_key="AIzaSyBQF-QGdS4oH63Md9txR7sEwloxi7oCyN4", model="gemini-2.5-pro-exp-03-25",
                                    http_proxy="http://localhost:7890", https_proxy="http://localhost:7890") # 初始化知识抽取器
chapter_indices = range(1, 9) # 章节列表

# 加载提示词
with open(f"{prompt_path}{prompt_type}", "r", encoding="utf-8") as f:
    prompt = f.read()
extarctor.load_prompt(prompt)

# 逐章节抽取知识并保存
for i in chapter_indices:
    text_path = f"{chapter_path}_{i}{chapter_type}"
    # 读取文本
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    extarctor.extract_entities_relations(text) # 实体和关系抽取
    extarctor.save(f"{data_path}_{i}{data_type}") # 保存知识抽取结果