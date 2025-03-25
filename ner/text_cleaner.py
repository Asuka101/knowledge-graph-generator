import re
import string

chapter_index = range(1, 9)
original_text_path = "./textbook/chapters/chapter"
original_text_type = ".txt"
cleaned_text_path = "./textbook/cleaned_chapters/chapter"
cleaned_text_type = ".txt"

# 定义移除标点符号的函数
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# 定义移除特殊字符的函数
def remove_special_characters(text):
    # 保留中文、英文、数字和空格
    return re.sub(r"[^\w\s\u4e00-\u9fa5]", "", text)

def remove_specific_characters(text):
    # 列出需要移除的字符
    characters_to_remove = r"\$#{}\*\\"
    return re.sub(f"[{characters_to_remove}]", "", text)

def remove_invisible_characters(text):
    return text.replace("\n", "").replace("\t", "").strip()

# 定义移除英文字符的函数
def remove_english_characters(text):
    # 匹配所有英文字符（大小写）
    return re.sub(r"[a-zA-Z]", "", text)

for i in chapter_index:
    with open(f"{original_text_path}_{i}{original_text_type}", "r", encoding="utf-8") as file:
        text = file.read()

    new_text = remove_specific_characters(text)
    with open(f"{cleaned_text_path}_{i}{cleaned_text_type}", "w", encoding="utf-8") as file:
        file.write(new_text)
    print(f"文本已清理并保存到 {cleaned_text_path.split('/')[-1]}_{i}{cleaned_text_type} 文件中。")