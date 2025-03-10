import google.generativeai as genai
import pandas as pd
import os

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

API_KEY = "AIzaSyBQF-QGdS4oH63Md9txR7sEwloxi7oCyN4"
input_filepath = "./textbook/page_36.txt" #输入文本路径
output_filepath = "extracted_data.csv" # 输出 CSV 文件路径

# 配置 Gemini API 密钥
genai.configure(api_key=API_KEY)

# 加载本地文本文件
def load_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# 调用 Gemini API 进行实体识别和关系抽取
def extract_entities_relations(text):
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    请从以下文本中提取实体和它们之间的关系，并以表格的形式输出，表格包含三列：实体1，关系，实体2。
    文本：
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

# 解析提取结果并保存为 CSV
def save_to_csv(extracted_data, output_filepath):
    # 将提取结果进行解析，转化为表格数据，如果gemini输出的是表格形式，可以进行pandas的read_csv方法直接读取。
    # 以下为示例，如果gemini输出的不是标准csv格式，需要按照输出格式进行解析。
    data = []
    lines = extracted_data.split('\n')
    for line in lines[2:]:
        items = line.split('|')
        if len(items) == 5:
            data.append([items[1].strip(), items[2].strip(), items[3].strip()])

    df = pd.DataFrame(data, columns=['实体1', '关系', '实体2'])
    df.to_csv(output_filepath, index=False, encoding='utf-8-sig')


text = load_text_file(input_filepath)
extracted_data = extract_entities_relations(text)
save_to_csv(extracted_data, output_filepath)

print(f"实体识别和关系抽取结果已保存到：{output_filepath}")