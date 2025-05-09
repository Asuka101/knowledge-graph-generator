# description: 数据清理器
import os
from src.libs.preprocessor import Preprocessor

class Cleaner:
    def __init__(self):
        # 原始数据配置及完整路径
        self.source_path = os.getenv("CHAPTER_PATH")
        self.source_filename = os.getenv("CHAPTER_NAME")
        self.source_extension = os.getenv("CHAPTER_TYPE")

        # 清理后数据配置及完整路径
        self.target_path = os.getenv("CLEANED_PATH")
        self.target_filename = os.getenv("CLEANED_NAME")
        self.target_extension = os.getenv("CLEANED_TYPE")

        # 停用词配置及完整路径
        self.stopwords_path = os.getenv("STOPWORDS_PATH")
        self.stopwords_filename = os.getenv("STOPWORDS_NAME")
        self.stopwords_extension = os.getenv("STOPWORDS_TYPE")

        # 确保输出目录存在
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)

    def read_stopwords(self):
        # 读取停用词
        stopwords_file = os.path.join(self.stopwords_path, f"{self.stopwords_filename}{self.stopwords_extension}")
        with open(stopwords_file, "r", encoding="utf-8") as file:
            return file.read().splitlines()

    def clean(self, use_stopwords=False):
        print("开始清理文本...")
        # 处理源目录下所有文件
        files = [f for f in os.listdir(self.source_path) if f.endswith(self.source_extension)]
        files.sort()
        for index, file_name in enumerate(files, start=1):
            source_file = os.path.join(self.source_path, file_name)
            target_file = os.path.join(self.target_path, f"{self.target_filename}_{index}{self.target_extension}")
            try:
                with open(source_file, "r", encoding="utf-8") as file:
                    text = file.read()
                text = Preprocessor.remove_specific_characters(text)
                text = Preprocessor.remove_empty_lines(text)
                if use_stopwords:
                    text = Preprocessor.delete_stopwords(text, self.read_stopwords())
                text = Preprocessor.remove_whitespace(text)
                head = text.splitlines()[0] if text.splitlines() else text
                with open(target_file, "w", encoding="utf-8") as file:
                    file.write(text)
                print(f"[{head}]：文本已清理!")
            except FileNotFoundError:
                print(f"文件 {file_name} 未找到!")
                raise
            except Exception as e:
                print(f"处理文件 {file_name} 时出错: {e}")
                raise
        print("文本清理完成!")