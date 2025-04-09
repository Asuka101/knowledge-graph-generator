# Description: 实体和关系抽取类
import google.generativeai as genai
import os

class EntityRelationExtractor:
    # 初始化
    def __init__(self, api_key, model, http_proxy=None, https_proxy=None):
        self.api_key = api_key # API 密钥
        self.http_proxy = http_proxy # HTTP 代理
        self.https_proxy = https_proxy # HTTPS 代理
        self.prompt = None # 提示词
        self.data = None # 提取结果
        self.model = genai.GenerativeModel(model)
        genai.configure(api_key=api_key)
        if self.http_proxy and self.https_proxy:
            os.environ["HTTP_PROXY"] = self.http_proxy
            os.environ["HTTPS_PROXY"] = self.https_proxy
        self.chat = self.model.start_chat()
        # 设置模型参数
        self.generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 40,
        }

    # 加载prompt
    def load_prompt(self, prompt):
        try:
            self.prompt = prompt
            response = self.chat.send_message(prompt)
            print(f"提示词加载成功!\n模型回复：{response.text}")
        except Exception as e:
            print(f"加载提示词失败: {e}")
            raise

    def set_config(self, temperature=None, top_p=None, top_k=None):
        """设置模型参数"""
        if temperature is not None:
            if temperature < 0 or temperature > 1:
                raise ValueError("模型温度必须在0到1之间")
            self.generation_config["temperature"] = temperature
        if top_p is not None:
            if top_p < 0 or top_p > 1:
                raise ValueError("top_p必须在0到1之间")
            self.generation_config["top_p"] = top_p
        if top_k is not None:
            if top_k < 0:
                raise ValueError("top_k必须大于等于0")
            if top_k > 100:
                raise ValueError("top_k必须小于等于100")
            self.generation_config["top_k"] = top_k

    # 实体和关系抽取
    def extract_entities_relations(self, text):
        try:
            print(f"正在抽取{text.splitlines()[0]}中的实体和关系...")
            response = self.chat.send_message(f"{text}", generation_config=self.generation_config)
            self.data = response.text
            print(f"实体和关系抽取成功!")
            return self.data
        except Exception as e:
            print(f"实体和关系抽取失败: {e}")
            raise

    # 保存知识抽取结果
    def save(self, save_path, modify_json=True):
        if modify_json:
            self.data = self.json_modify(self.data)
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.data)
            print(f"知识抽取结果已保存到: {save_path}")
        except Exception as e:
            print(f"保存文件失败: {e}")
            raise

    # 保证格式正确
    def json_modify(self, text):
        lines = text.splitlines()
        if len(lines) > 2:
            if lines[0].startswith("```json") and lines[-1].endswith("```"):
                return '\n'.join(lines[1:-1])
            return text
        else:
            return text