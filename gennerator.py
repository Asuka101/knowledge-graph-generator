# description: 知识图谱构建程序
import sys
import os

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from src.main import main

if __name__ == "__main__":
    main()