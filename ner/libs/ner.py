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
        self.configure_api() 

    # 配置 API 和代理
    def configure_api(self):
        try:
            genai.configure(api_key=self.api_key)
            if self.http_proxy and self.https_proxy:
                os.environ["HTTP_PROXY"] = self.http_proxy
                os.environ["HTTPS_PROXY"] = self.https_proxy
        except Exception as e:
            print(f"配置API或代理失败: {e}")
            raise

    # 加载prompt
    def load_prompt(self, prompt):
        try:
            self.prompt = prompt
            print(f"提示词加载成功!")
        except Exception as e:
            print(f"加载提示词失败: {e}")
            raise

    # 实体和关系抽取
    def extract_entities_relations(self, text):
        try:
            response = self.model.generate_content(f"{self.prompt}\n{text}")
            self.data = response.text
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