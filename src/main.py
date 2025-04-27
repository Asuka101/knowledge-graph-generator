# description: 主程序
from src.converter import PDF2TextbookConverter
from src.cleaner import Cleaner
from src.merger import ChapterMerger
from src.extractor import Extractor
from src.integrator import Integrator
from src.importer import Importer

def main():
    # 模块初始化
    converter = PDF2TextbookConverter()
    cleaner = Cleaner()
    merger = ChapterMerger(chapter_pages=[18, 65, 111, 148, 195, 229, 266, 290, 322])
    extractor = Extractor()
    integrator = Integrator()
    importer = Importer()

    # 工作流
    converter.convert()
    cleaner.clean()
    merger.process_chapters()
    extractor.extract()
    integrator.integrate()
    importer.import_data()