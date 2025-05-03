# description: 主程序
from src.converter import PDF2TextbookConverter
from src.cleaner import Cleaner
from src.merger import ChapterMerger
from src.extractor import Extractor
from src.integrator import Integrator
from src.store import StoreManager
import os

def main(chapter_pages):
    print("知识图谱构建程序启动成功！")

    # 初始化教材目录
    textbook_path = os.getenv("TEXTBOOK_PATH")
    if not os.path.exists(textbook_path):
        os.makedirs(textbook_path)
    image_path = os.getenv("IMAGE_PATH")
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    page_path = os.getenv("PAGE_PATH")
    if not os.path.exists(page_path):
        os.makedirs(page_path)
    chapter_path = os.getenv("CHAPTER_PATH")
    if not os.path.exists(chapter_path):
        os.makedirs(chapter_path)
    cleaned_path = os.getenv("CLEANED_PATH")
    if not os.path.exists(cleaned_path):
        os.makedirs(cleaned_path)
    
    # 模块初始化
    converter = PDF2TextbookConverter()
    merger = ChapterMerger(chapter_pages=chapter_pages)
    cleaner = Cleaner()
    extractor = Extractor()
    integrator = Integrator()
    store = StoreManager()

    # 工作流
    converter.convert()
    merger.process_chapters()
    cleaner.clean()
    extractor.extract()
    integrator.integrate()
    store.import_data()
    store.convert()
    print("程序已退出！")
