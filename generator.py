# description: 知识图谱构建程序
import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.main import main

if __name__ == "__main__":
    main(chapter_pages=[18, 65, 111, 148, 195, 229, 266, 290, 322])