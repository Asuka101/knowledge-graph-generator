import json
from datetime import datetime

import openai
from dotenv import load_dotenv
from openai import OpenAI

from aiprompt.prompt import role_prompt_templates
import os

def load_env():
    dotenv_file= ".env.ai"
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), dotenv_file))

load_env()

openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key=openai.api_key,
    base_url=os.getenv('OPENAI_BASE_URL')
)
model=os.getenv('OPENAI_MODEL')
max_tokens= int(os.getenv('OPENAI_MAX_TOKENS'))
role_name=os.getenv('OPENAI_ROLE_NAME')
temp=float(os.getenv('OPENAI_TEMPERATURE'))
top_p=float(os.getenv('OPENAI_TOP_P'))

# a=client.models.list()
# print(a)

def get_role_prompt():
    """
    获取角色扮演提示词
    :param role_name: 角色名称
    :param user_question: 用户具体问题
    :return: 完整的提示词
    """
    if role_name not in role_prompt_templates:
        raise ValueError(f"未知的角色名称：{role_name}")
    
    return f"{role_prompt_templates[role_name]}"


def generate_role_text(prompt,encoded_string):
    """
    # 根据指定角色生成文本
    :param role_name: 角色名称
    :param user_question: 用户问题
    :param model: 使用的模型，默认为全局model
    :param max_tokens: 最大token数，默认1000
    :return: 生成的文本内容
    """
    # 获取角色提示词
    sysprompt = get_role_prompt()
    # 调用生成函数
    return generate_text(sysprompt,prompt,encoded_string)

def generate_text(sysprompt, prompt,encoded_string):
    while True:  # 添加循环以便重试
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": sysprompt},
                    {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_base64",
                            "image_base64": {
                                "data": encoded_string
                            }
                        }
                        ]
                     }

                ],
                stream=False,
                max_tokens=max_tokens,
                temperature=temp,
                top_p=top_p
            )
            return response.choices[0].message.content
        except json.decoder.JSONDecodeError:  # 捕获 JSONDecodeError
            print(f"发生 JSONDecodeError，正在重试...: {datetime.now()}")  # 打印错误信息和当前时间
            continue  # 继续循环重试
        except Exception as e:  # 捕获其他异常
            print(f"发生其他错误: {e}")
            break  # 退出循环




