import requests
import os

# 获取cookie列表
with open(os.getenv("OCR_COOKIES"), 'r', encoding='utf-8') as f:
    cookies = [line.strip() for line in f if line.strip()]

def recognize_image(base64_image, cookie_index):
    """
    调用OCR API识别图片内容
    :param base64_image: 图片的base64编码字符串
    :return: API返回的识别结果
    """

    url = 'https://ocr.doublefenzhuan.me/api/recognize/base64'
    headers = {
        'Content-Type': 'application/json',
        "x-custom-cookie": cookies[cookie_index],
    }
    data = {
        "base64Image": base64_image
    }

    # 禁用代理
    proxies = {
        "http": None,
        "https": None,
    }

    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    return response.json()

