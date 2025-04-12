# Description: 从文本中抽取知识并保存
from libs.ner import KnowledgeExtractor
import threading

# 文本路径和名称
chapter_path = "./textbook/cleaned_chapters/chapter" # 文本路径
chapter_type = ".txt" # 文本类型

# 提示词路径和名称
prompt_path = "./prompt/prompt4extractor" # 提示词路径
prompt_type = ".md" # 提示词类型

# 数据保存路径和名称
data_path = "./data/chapter" # 保存路径
data_type = ".json" # 数据类型

# API 密钥
gemini_key = "AIzaSyBQF-QGdS4oH63Md9txR7sEwloxi7oCyN4" # Gemini API 密钥

# 模型名称
gemini_model = "gemini-2.5-pro-exp-03-25" # Gemini 模型名称
gemini_flash_model = "gemini-2.0-flash"

# API 地址
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/" # Gemini API 地址

extarctor = KnowledgeExtractor(api_key=gemini_key, model=gemini_flash_model, base_url=gemini_url) # 初始化知识抽取器
chapter_indices = range(1, 9) # 章节列表

# 加载提示词
with open(f"{prompt_path}{prompt_type}", "r", encoding="utf-8") as f:
    prompt = f.read()
extarctor.load_prompt(prompt)

# 章节处理线程
def process_chapter(i):
    text_path = f"{chapter_path}_{i}{chapter_type}"
    # 读取文本
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    extarctor.extract(text, save_path=f"{data_path}_{i}{data_type}")  # 知识抽取

# 创建线程并启动
threads = []
for i in chapter_indices:
    t = threading.Thread(target=process_chapter, args=(i,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()