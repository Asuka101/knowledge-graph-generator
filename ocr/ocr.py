import requests


def recognize_image(base64_image):
    """
    调用OCR API识别图片内容
    :param base64_image: 图片的base64编码字符串
    :return: API返回的识别结果
    """
    url = 'https://ocr.doublefenzhuan.me/api/recognize/base64'
    headers = {
        'Content-Type': 'application/json',
        "x-custom-cookie": "acw_tc=b2f6c24c4ad73678826853048f07b5f1d5439988afab5645954302c5a2e30cef; x-ap=ap-southeast-1; cna=O8VCILKbpWACASrI5r32Wapc; xlly_s=1; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE2YWViYTlkLTg5ZmUtNDM1Ni05OWUwLTc3MTcyOTMxODJmNCIsImV4cCI6MTc0Mjk1NTYxNn0.JInZRlyw8BbGuoE8ksNAiT8GTolJnjjV-WTmw9pcPHE; SERVERID=1d359dbee252ae354fc7540962172fd2|1740363630|1740363571; SERVERCORSID=1d359dbee252ae354fc7540962172fd2|1740363630|1740363571; ssxmod_itna=eqUxRD9DgGe=D8Dh=WG8Du7xwxGrxWI4xGHDyx4YK0CDmxjKidKDUWqcbFDchhArAqDC0AGWrdSD0yGmDnqD82DQeDvYPq+0tS8n2RG3Q=ii2D1iBEmrvcYQAjlDp6k5r=qqmb4B3DExGk7AvimDiiax0rD0eDPxDYDG4DoxYDnx4DjxDdNFoIOKoDbxi3z4GC/6RAI4DFGl7+v3xD0xpskj+m1DDz1lM5K4h4I4Dr/13Yk7oKP59wD7y3DlpPTy2wnb6c1nO2=5KE3pYDXrtDvpojaUx=b/EImb+xiAeZm0pxP8xT7QGi3G5/D45hDq+D4Eo1iNK7D8iYYBHxr5uw+CxDiEwtCI0QNUDhxr+RhtcgoDctbWAxnKhjKSivwniQYed7DZ2rZjwzlwyBGs65P0DYCG8+NxD; ssxmod_itna2=eqUxRD9DgGe=D8Dh=WG8Du7xwxGrxWI4xGHDyx4YK0CDmxjKidKDUWqcbFDchhArAqDC0AGWrdmDDPoY7eIlb5DLiD4hEi+iixD/A4O3KqsvtDwBxpNdICj02KGYCqQ12KNQIt1=QZ679=0s/1I8hO0G7iiH2YmOTpGC=t0iVO2w7AFCFKq4/=FwFZvF6cYe/=TI9PwKe+II=fgsPmFwKG5khKvPVhiGWtYGMtiX688CVtjk3HB+ZZ5jfrc2Proc7hxLcKw49tw0Ou3U//12e4CzTrajtUzSh2/I/xKs2Zte41d/uV/C+KouBeArPqYe/QG52tMjvyPLdBNKExnn=x+G/DfE7x/BquQYPAXeaPT2KirKfQAxGLRB5zejYcL16Y=S61pN8+jvQpNptqiPdeTYnAs=uZYLnGjQORh+WQYnW4KcGp7fKXrWRlL7bIxaihC2M1N6aIMEP3giy0cjj6yOxn+NMrXXhPZjoXx3FEi2YWzaUx9fIrWdYdB7impDwOhq7IdQ6DUvXS5pUKZjauiWMm6pfbZ3KezaTZLxAA3qdxvrw9LQEKVeTMB5+fIxrgUQApRtZ4=icBFzrW4jWtPhnBxomTIPTxItHKnYeZ6Y3FfQGd1WePQD1QYdDb=tLujcP98jGdPG0x1D9h3unh9bkfGGcLrgmP6uYrXTBkxgsKx608f6Y1PSwZ2P8pyWDNTpeY0IyCDex6ZroiGi5ViM=sjqgDxiGPlWR9KcK7hAoeSDxnFzhAZPfmHnxlGAE+KGoIDmY6pDnITZPobNik=53zDnKqG+10FPeDEo3eQb5Wo2IHh+/nq9xYDo7DKDonxWEtQpMiNlqs+qnxagHb1hO5YDD; tfstk=gxTZGmaJmV3N9YLZn6b4Yl0oZuQOjND7bE6fiIAc1OXiBE_Vi9R4ChOXiZuVKNjvft613ZRvUXMSP4O96ZQiFYg5VH_xpaU0jZ2fKMflu1D0ABtk6ZQmdAKmNed9EfedlnbmTwfVMtbcmZXnTs5PnZXGmJqhZ9XcoKXGKwfA_s4csrbnTsBhnZbDnwD9fZb8LssigeyFPrVLVGBks9z0r7CcjYJgcyze-1SNSIXFO6TF_GWPv0sRCFvBiFTOvDECkBty3nvodl6M4_JFVhkz7LJOip76rjnOviY2u6KK3oWymCtJmMliSB7NQM5Nb5rc7nv9uGKaMbdhSpKReGmKp686PiWRYJDMOBWG4nJsprX64BvFVewQPaxJLESlrgzYH6jFKEKanoSG96WSTX-m3fKwAhKvpoEAXWCFFfjgDoIG96WSTXrYDGHdTTGGj; isg=BDs71f5F2PnuuORNyhRf0TdHyh-lkE-SNuqwIC3wFjpRjFZuvGEd4x6KpyzC46eK",
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