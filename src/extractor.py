# Description: 知识抽取器
import os
from src.libs.llm import KnowledgeProcessor
import concurrent.futures  # 导入线程池模块

class Extractor:
    def __init__(self):
        # 待处理文本（已清理文本）配置及路径
        self.source_path = os.getenv("CLEANED_PATH")
        self.source_filename = os.getenv("CLEANED_NAME")
        self.source_extension = os.getenv("CLEANED_TYPE")

        # 抽取后数据（知识数据）配置及路径
        self.target_path = os.getenv("DATA_PATH")
        self.target_filename = os.getenv("CLEANED_NAME")

        # 提示词配置及路径
        self.prompt_path = os.getenv("PROMPT_PATH")
        self.prompt_filename = os.getenv("PROMPT4EXTRACTOR_NAME")
        self.prompt_extension = os.getenv("PROMPT_TYPE")

        # API 配置
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL")
        self.base_url = os.getenv("BASE_URL")

        # 代理配置（可选）
        self.http_proxy = os.getenv("HTTP_PROXY")
        self.https_proxy = os.getenv("HTTPS_PROXY")
        if self.http_proxy and self.https_proxy:
            os.environ["HTTP_PROXY"] = self.http_proxy
            os.environ["HTTPS_PROXY"] = self.https_proxy

        # 根据 source_path 中对应文件名解析章节索引
        self.source_indices = sorted(
            [int(f.split('_')[-1].split('.')[0]) for f in os.listdir(self.source_path)
            if f.startswith(self.source_filename) and f.endswith(self.source_extension)]
        )

        # 初始化知识抽取器
        self.processor = KnowledgeProcessor(api_key=self.api_key, model=self.model, base_url=self.base_url)

    def load_prompt(self):
        # 加载提示词文件
        prompt_file = os.path.join(self.prompt_path, f"{self.prompt_filename}{self.prompt_extension}")
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
        self.processor.load_prompt(prompt)

    def process_chapter(self, idx):
        # 构造待处理文件及抽取后保存文件路径
        source = os.path.join(self.source_path, f"{self.source_filename}_{idx}{self.source_extension}")
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()
        target_file = os.path.join(self.target_path, f"{self.target_filename}_{idx}.json")
        self.processor.extract(text, save_path=target_file)

    def extract(self):
        print("开始知识抽取...")
        self.load_prompt()
        # 使用线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.process_chapter, self.source_indices)
        print("知识抽取完成!")