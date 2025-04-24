# Description: 知识抽取器
import os
import threading
from dotenv import load_dotenv
from libs.llm import KnowledgeProcessor

class Extractor:
    def __init__(self):
        load_dotenv()  # 加载环境变量
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # 待处理文本（已清理文本）配置及完整路径
        self.source_path = os.path.abspath(os.path.join(self.base_dir, os.getenv("CLEANED_PATH")))
        self.source_filename = os.getenv("CLEANED_NAME")
        self.source_extension = os.getenv("CLEANED_TYPE")

        # 抽取后数据（知识数据）配置及完整路径
        self.target_path = os.path.abspath(os.path.join(self.base_dir, os.getenv("DATA_PATH")))
        self.target_filename = os.getenv("CLEANED_NAME")

        # 提示词配置及完整路径
        self.prompt_path = os.path.abspath(os.path.join(self.base_dir, os.getenv("PROMPT_PATH")))
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
        if os.path.exists(self.source_path):
            self.source_indices = sorted(
                [int(f.split('_')[-1].split('.')[0]) for f in os.listdir(self.source_path)
                 if f.startswith(self.source_filename) and f.endswith(self.source_extension)]
            )
        else:
            self.source_indices = []

        # 初始化知识抽取器
        self.processor = KnowledgeProcessor(api_key=self.api_key, model=self.model, base_url=self.base_url)

    def load_prompt(self):
        # 加载提示词文件
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"提示词路径 {self.prompt_path} 不存在")
        prompt_file = os.path.join(self.prompt_path, f"{self.prompt_filename}{self.prompt_extension}")
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
        self.processor.load_prompt(prompt)

    def process_chapter(self, idx):
        # 构造待处理文件及抽取后保存文件路径
        source = os.path.join(self.source_path, f"{self.source_filename}_{idx}{self.source_extension}")
        if not os.path.exists(source):
            print(f"待处理文件 {source} 不存在")
            return
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()
        target_file = os.path.join(self.target_path, f"{self.target_filename}_{idx}.json")
        self.processor.extract(text, save_path=target_file)

    def extract(self):
        print("开始知识抽取...")
        self.load_prompt()
        threads = []
        for idx in self.source_indices:
            t = threading.Thread(target=self.process_chapter, args=(idx,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print("知识抽取完成!")

if __name__ == "__main__":
    extractor = Extractor()
    extractor.extract()