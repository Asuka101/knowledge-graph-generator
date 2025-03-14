import google.generativeai as genai
import os

# 设置 HTTP 代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

API_KEY = "AIzaSyBQF-QGdS4oH63Md9txR7sEwloxi7oCyN4" # Gemini API 密钥
input_filepath = "./chapters/chapter_2.txt" #输入文本路径
prompt_path = "./prompt.md" # 提示词路径
output_filepath = "extracted_data.json" # 输出 JSON 文件路径

# 配置 Gemini API 密钥
genai.configure(api_key=API_KEY)

# 加载本地文本文件
def load_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# 调用 Gemini API 进行实体识别和关系抽取
def extract_entities_relations(text, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"{prompt}\n{text}"
    response = model.generate_content(prompt)
    return response.text

# 保存文件
def save_file(data, save_path):
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(data)

text = load_text_file(input_filepath) # 加载抽取文本
prompt = load_text_file(prompt_path) # 加载提示词
extracted_data = extract_entities_relations(text, prompt) # 实体识别和关系抽取
save_file(extracted_data, output_filepath) # 保存抽取结果

print(f"实体识别和关系抽取结果已保存到：{output_filepath}")