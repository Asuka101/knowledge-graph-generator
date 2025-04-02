# description: 数据清理脚本
from libs.preprocessor import Preprocessor

chapter_range = range(1, 9)
input_path = "./textbook/chapters/chapter"
input_type = ".txt"
output_path = "./textbook/cleaned_chapters/chapter"
output_type = ".txt"

for i in chapter_range:
    input_file = f"{input_path}_{i}{input_type}"
    output_file = f"{output_path}_{i}{output_type}"
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()
        cleaner = Preprocessor(text)
        cleaned_text = cleaner.clean_text(text)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(cleaned_text)

        print(f"文本已清理并保存到 {output_file}")
    except FileNotFoundError:
        print(f"文件 {input_file} 未找到，跳过。")
    except Exception as e:
        print(f"处理文件 {input_file} 时出错: {e}")