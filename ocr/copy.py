import requests

def recognize_image(base64_image):
    """
    调用OCR API识别图片内容
    :param base64_image: 图片的base64编码字符串
    :return: API返回的识别结果
    """
    url = 'https://ocr.doublefenzhuan.me/api/recognize/base64'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjUzZTk0Nzg4LWMwM2QtNDY4Mi05OTNhLWE0ZDNjNGUyZDY0OSIsImV4cCI6MTczOTA3NTE0MX0.FtwG6xDLYd2rngWUhuldg56WXCiLSTL0RI6xJJQ4vHM",
        "base64Image": base64_image
    }
    
    # 禁用代理
    proxies = {
        "http": None,
        "https": None,
    }

    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    return response.json()

# 示例调用
if __name__ == "__main__":
    result = recognize_image("xxx")
    print(result)