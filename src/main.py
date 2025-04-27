# description: 主程序
from src.converter import PDF2TextbookConverter
# from src.cleaner import Cleaner
# from src.merger import ChapterMerger
# from src.extractor import Extractor
# from src.integrator import Integrator
# from src.importer import Importer
from dotenv import load_dotenv
import os

def main():
    print("知识图谱构建程序启动成功！")
    
    load_dotenv()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    textbook_path = os.path.abspath(os.path.join(base_dir, os.getenv("TEXTBOOK_PATH")))
    if not os.path.exists(textbook_path):
        os.makedirs(textbook_path)
    image_path = os.path.abspath(os.path.join(base_dir, os.getenv("IMAGE_PATH")))
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    page_path = os.path.abspath(os.path.join(base_dir, os.getenv("PAGE_PATH")))
    if not os.path.exists(page_path):
        os.makedirs(page_path)
    chapter_path = os.path.abspath(os.path.join(base_dir, os.getenv("CHAPTER_PATH")))
    if not os.path.exists(chapter_path):
        os.makedirs(chapter_path)
    cleaned_path = os.path.abspath(os.path.join(base_dir, os.getenv("CLEANED_PATH")))
    if not os.path.exists(cleaned_path):
        os.makedirs(cleaned_path)
    
    try:
        # 模块初始化
        converter = PDF2TextbookConverter()
        # merger = ChapterMerger(chapter_pages=[18, 65, 111, 148, 195, 229, 266, 290, 322])
        # cleaner = Cleaner()
        # extractor = Extractor()
        # integrator = Integrator()
        # importer = Importer()

        # 工作流
        converter.convert()
        # merger.process_chapters()
        # cleaner.clean()
        # extractor.extract()
        # integrator.integrate()
        # importer.import_data()
        # print("知识图谱构建完成！")

    except Exception as e:
        print(f"知识图谱构建程序错误退出！")