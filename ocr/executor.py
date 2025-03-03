import base64
import logging
import os

from ocr import recognize_image,cookies

# 设置日志记录
logging.basicConfig(filename='generate_md.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

images_path = "./images"
images_name = "page"
images_index = [330]
outputs_path = "./textbook"
concat_file = "./textbook.txt"


def convert(images_path, images_name, images_index, outputs_path, concat_file):
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
    with open(concat_file, "w", encoding="utf-8") as outfile:
        # 遍历 390 个文件
        for i in range(1, 391):  # 从 1 到 390
            # 生成文件名
            filename = f"{images_name}_{i}.txt"
            filepath = os.path.join(outputs_path, filename)

            # 检查文件是否存在
            if not os.path.exists(filepath):
                logging.error(f"File {filename} does not exist, skip")
                continue

            # 读取文件内容并写入输出文件
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n")  # 可选：在文件之间添加空行

convert(images_path, images_name, images_index, outputs_path, concat_file)

# def test(question,image_path):
#     logging.info("正在调用gpt")
#     # 将图片路径编码为base64字符串
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#         # print(encoded_string)
#     # gpt_answer = generate_role_text(question, encoded_string)
#     gpt_answer = recognize_image(encoded_string)
#     print("gpt: %s", gpt_answer)
#     logging.info("gpt: %s", gpt_answer)

# test("请大致描述一下图片内容","test_2.png")



