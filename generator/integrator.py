# description: 知识融合器
import os
import json
from dotenv import load_dotenv
from libs.llm import KnowledgeProcessor

class Integrator:
    def __init__(self):
        load_dotenv()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.abspath(os.path.join(self.base_dir, os.getenv("DATA_PATH")))
        self.chapter_name = os.getenv("CLEANED_NAME")
        self.data_name = os.getenv("DATA_NAME")

        # 提示词配置及完整路径
        self.prompt_path = os.path.abspath(os.path.join(self.base_dir, os.getenv("PROMPT_PATH")))
        self.prompt_filename = os.getenv("PROMPT4INTEGRATO_NAME")
        self.prompt_extension = os.getenv("PROMPT_TYPE")

        # API 配置
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL")
        self.base_url = os.getenv("BASE_URL")

    def load_prompt(self):
        # 加载提示词文件
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"提示词路径 {self.prompt_path} 不存在")
        prompt_file = os.path.join(self.prompt_path, f"{self.prompt_filename}{self.prompt_extension}")
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
        self.processor.load_prompt(prompt)

    def merge(self):
        # 合并知识抽取结果
        merged_data = {"entities": [], "relations": []}
        output_file = os.path.join(self.path, f"{self.data_name}.json")

        # 遍历目录中的所有 JSON 文件
        for filename in os.listdir(self.path):
            if filename.endswith(".json") and filename.split("_")[0] == self.chapter_name:
                file_path = os.path.join(self.path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        data = json.load(file)
                        # 合并 "entities" 和 "relations"
                        if "entities" in data:
                            merged_data["entities"].extend(data["entities"])
                        if "relations" in data:
                            merged_data["relations"].extend(data["relations"])
                    except json.JSONDecodeError as e:
                        print(f"文件 {filename} 解析失败: {e}")

        # 将合并后的数据写入输出文件
        with open(output_file, "w", encoding="utf-8") as output:
            json.dump(merged_data, output, ensure_ascii=False, indent=4)
        print(f"数据合并完成，结果已保存到 {output_file}")

    def integrate(self):
        # 初始化知识处理器
        self.processor = KnowledgeProcessor(api_key=self.api_key, model=self.model, base_url=self.base_url)
        self.load_prompt()
        # 知识融合
        source = os.path(self.path, f"{self.data_name}.json")
        target = os.path(self.path, f"{self.data_name}.json")
        if not os.path.exists(source):
            print(f"文件 {source} 未找到。")
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()
        self.processor.integrate(text, save_path=target)

if __name__ == "__main__":
    integrator = Integrator()
    integrator.merge()
    integrator.integrate()