# Description: 知识抽取类 (支持调用任意大语言模型的API)
from openai import OpenAI
import threading

class KnowledgeProcessor:
    def __init__(self, api_key, model, base_url):
        if not api_key:
            raise ValueError("API 密钥不能为空")
        if not model:
            raise ValueError("模型名称不能为空")
        if not base_url:
            raise ValueError("base_url不能为空")
        self.api_key = api_key       # API 密钥
        self.model = model             # 模型名称 
        self.base_url = base_url         # API 地址
        self.prompt = None             # 提示词
        self.lock = threading.Lock()  # 线程锁

        # 设置模型生成参数
        self.generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
        }

    # 发送消息
    def send_message(self, content, client):
        try:
            if self.prompt is None:
                raise ValueError("提示词尚未加载请重试")
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": self.prompt},
                          {"role": "user", "content": content}],
                temperature=self.generation_config["temperature"],
                top_p=self.generation_config["top_p"],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"向大语言模型发送消息失败: {e}")
            raise

    # 加载提示词
    def load_prompt(self, prompt):
        try:
            with self.lock:
                self.prompt = prompt
            print(f"提示词加载成功!")
        except Exception as e:
            print(f"加载提示词失败: {e}")
            raise

    # 设置生成参数
    def set_config(self, temperature=None, top_p=None):
        if temperature is not None:
            if not (0 <= temperature <= 1):
                raise ValueError("模型温度必须在0到1之间")
            with self.lock:
                self.generation_config["temperature"] = temperature
        if top_p is not None:
            if not (0 <= top_p <= 1):
                raise ValueError("top_p必须在0到1之间")
            with self.lock:
                self.generation_config["top_p"] = top_p

    # 知识抽取
    def extract(self, text, save_path, modify_json=True):
        try:
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            head = text.splitlines()[0] if text.splitlines() else text
            print(f"[{head}]：正在抽取实体、关系和属性...")
            response_text = self.send_message(content=text, client=client)
            # 保存结果
            with open(save_path, "w", encoding="utf-8") as f:
                if modify_json:
                    f.write(self.json_modify(response_text))
                else:
                    f.write(response_text)
            print(f"[{head}]：知识抽取成功!结果已保存到: {save_path}")
        except Exception as e:
            print(f"知识抽取失败: {e}")
            raise

    # 知识融合
    def integrate(self, text, save_path, modify_json=True):
        try:
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            print("正在进行知识融合...")
            response_text = self.send_message(content=text, client=client)
            # 保存结果
            with open(save_path, "w", encoding="utf-8") as f:
                if modify_json:
                    f.write(self.json_modify(response_text))
                else:
                    f.write(response_text)
            print(f"知识融合成功!结果已保存到: {save_path}")
        except Exception as e:
            print(f"知识融合失败: {e}")
            raise

    # 保证结果格式正确
    def json_modify(self, text):
        lines = text.splitlines()
        if len(lines) > 2 and lines[0].startswith("```json") and lines[-1].endswith("```"):
            return "\n".join(lines[1:-1])
        return text