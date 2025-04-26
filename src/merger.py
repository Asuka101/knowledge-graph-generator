# Description: 按章节合并教材文本
import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class ChapterMerger:
    def __init__(self, chapter_pages):
        #  需要合并的章节首页页码及尾页页码
        self.chapter_pages = chapter_pages
        # 原始数据配置及完整路径
        self.input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.getenv("PAGE_PATH")))
        self.input_name = os.getenv("page_NAME")
        self.input_type = os.getenv("page_TYPE")
        # 合并后数据配置及完整路径
        self.output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.getenv("CHAPTER_PATH")))
        self.output_name = os.getenv("CHAPTER_NAME")
        self.output_type = os.getenv("CHAPTER_TYPE")
        self.chapters_edge = len(self.chapter_pages)

    def merge(self, output_file, pages_index):
        # 打开输出文件
        with open(output_file, "w", encoding="utf-8") as outfile:
            # 遍历文件
            for i in pages_index:
                # 生成文件名
                filename = f"{self.input_name}_{i}{self.input_type}"
                filepath = os.path.join(self.input_dir, filename)

                # 检查文件是否存在
                if not os.path.exists(filepath):
                    print(f"文件 {filename} 不存在，跳过")
                    continue

                # 读取文件内容并写入输出文件
                with open(filepath, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # 可选：在文件之间添加空行

        print(f"文件已合并到: {output_file}")

    def process_chapters(self):
        print("开始合并章节...")
        for i in range(1, self.chapters_edge):
            pages_index = range(self.chapter_pages[i-1], self.chapter_pages[i])
            output_file = os.path.join(self.output_path, f"{self.output_name}_{i}{self.output_type}")
            self.merge(output_file, pages_index)
        print("所有章节已成功合并!")

if __name__ == "__main__":
    merger = ChapterMerger()
    merger.process_chapters(chapter_pages=[18, 65, 111, 148, 195, 229, 266, 290, 322])