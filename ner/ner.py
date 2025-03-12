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
    请分析以下数据结构与算法课程教材文本，提取以下信息，并以JSON格式输出：

    1. 实体识别：
    - 识别文本中涉及的知识点实体，包括：
        - 数据结构（例如：数组、链表、栈、队列、树、图等）
        - 算法（例如：排序算法、查找算法、图算法、动态规划等）
        - 概念（例如：时间复杂度、空间复杂度、递归、迭代等）
        - 定理（例如：主定理、霍尔定理等）
        - 公式（例如：递归公式、计算公式等）
        - 模型（例如：哈希表模型、二叉树模型等）
        - 评价指标（例如：效率、稳定性、正确性等）
        - 性能（例如：最好情况、最坏情况、平均情况等）

    2. 属性抽取：
    - 为每个知识点实体抽取以下属性：
        - ID（唯一标识符）
        - 名称
        - 掌握程度（例如：初级、中级、高级）
        - 难度（例如：简单、中等、困难）

    3. 关系抽取：
    - 识别实体之间的以下关系：
        - 包含关系（例如：树包含子节点）
        - 并列关系（例如：冒泡排序和选择排序）
        - 相等关系（例如：两个算法等价）
        - 先后关系（例如：算法的执行步骤）
        - 上下关系（例如：父节点和子节点）
        - 因果关系（例如：某种操作导致某种结果）
        - 时空关系（例如：算法的时间复杂度和空间复杂度）
        - 从属关系（例如：某个算法属于某个算法类别）
        - 继承关系（例如：子类继承父类）
        - 相关关系（例如：两个算法解决相似问题）
    - 为每个关系抽取以下属性：
        - 强度（例如：强相关、弱相关）
        - 方向（例如：A包含B，B被A包含）

    请严格按照以下JSON格式输出结果：

    {
    "entities": [
        {
        "entity_type": "知识点",
        "entity_name": "实体名称",
        "entity_id": "唯一标识符",
        "attributes": {
            "掌握程度": "初级/中级/高级",
            "难度": "简单/中等/困难",
            "规模大小": "适用于数据集",
            "存放位置": "适用于教学资源"
        }
        },
        ...
    ],
    "relationships": [
        {
        "relation_type": "关系类型",
        "entity1_id": "实体1的唯一标识符",
        "entity2_id": "实体2的唯一标识符",
        "attributes": {
            "强度": "强相关/弱相关",
            "方向": "方向描述"
        }
        },
        ...
    ]
    }

    以下是数据结构与算法课程教材文本：
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