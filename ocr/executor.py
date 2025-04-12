import base64
import logging
from ocr import recognize_image,cookies

# 设置日志记录
logging.basicConfig(filename='generate_md.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

images_path = "./images" # 图片路径
images_name = "page" # 图片名称
images_index = [1] # 图片索引
outputs_path = "./textbook" # 输出路径
concat_file_path = "./textbook.txt" # 合并文件名


def convert(images_path, images_name, images_index, outputs_path):
    logging.info("正在调用llm")
    # 将图片路径编码为base64字符串
    for i in images_index:
        logging.info(f"Converting Image {i}......")
        image_path = f"{images_path}/{images_name}_{i}.png"  # 拼接图片路径
        output_path = f"{outputs_path}/{images_name}_{i}.txt"
        complete = 0
        while complete == 0:
            try:
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                with open(output_path, 'w', encoding='utf-8') as file:
                    # 调用 recognize_image 函数获取 gpt_answer
                    gpt_answer = recognize_image(encoded_string, i % cookies.len())
                    # 将 GPT 的回答写入文本文件
                    file.write(f"{gpt_answer['result']}\n")

                    # 记录日志
                    logging.info(f"Image {i} conversion is successful")
                    complete = 1


            except Exception as e:
                logging.error(f"Error processing image {i}: {e}")
                complete = 0
                continue

    logging.info(f"Conversion done")

convert(images_path, images_name, images_index, outputs_path)