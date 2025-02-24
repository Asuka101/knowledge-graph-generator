from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(pdf_path):
    """提取PDF文本内容"""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return clean_text(text)

def clean_text(text):
    """清洗文本内容"""
    text = re.sub(r'\s+', ' ', text)  # 合并多余空格
    text = re.sub(r'[^\w\s.,;:!?（）《》]', '', text)  # 去除特殊字符
    return text.strip()

def split_into_chunks(text, chunk_size=3000):
    """将文本按语义分块"""
    # 按段落分割
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for para in paragraphs:
        if current_length + len(para) <= chunk_size:
            current_chunk.append(para)
            current_length += len(para)
        else:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_length = len(para)
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks 