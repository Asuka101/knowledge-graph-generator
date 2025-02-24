import os
import requests
import json
from dotenv import load_dotenv
import time
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class KnowledgeExtractor:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        
    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, min=2, max=10))
    def extract_knowledge(self, text):
        """调用DeepSeek API进行知识抽取"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        prompt = f"""请从以下教材内容中提取知识图谱三元组，格式为JSON：
        {text}
        
        返回格式示例：
        {{
            "entities": ["概念1", "概念2", "概念3"],
            "relationships": [
                {{"source": "概念1", "target": "概念2", "type": "包含"}},
                {{"source": "概念2", "target": "概念3", "type": "前提"}}
            ]
        }}
        """
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        if response.status_code == 200:
            return json.loads(response.json()['choices'][0]['message']['content'])
        else:
            logger.error(f"API请求失败: {response.text}")
            raise Exception(f"API请求失败: {response.text}") 

    def batch_extract(self, text_chunks):
        """批量处理文本分块"""
        all_entities = set()
        all_relationships = []
        
        for chunk in text_chunks:
            try:
                data = self.extract_knowledge(chunk)
                # 合并结果
                all_entities.update(data.get('entities', []))
                all_relationships.extend(data.get('relationships', []))
                time.sleep(1)  # 避免速率限制
            except Exception as e:
                print(f"处理分块时出错: {str(e)}")
                continue
                
        return {
            "entities": list(all_entities),
            "relationships": self._deduplicate_relationships(all_relationships)
        }
    
    def _deduplicate_relationships(self, relationships):
        """去重关系"""
        seen = set()
        unique_rels = []
        for rel in relationships:
            key = (rel['source'], rel['target'], rel['type'])
            if key not in seen:
                seen.add(key)
                unique_rels.append(rel)
        return unique_rels 