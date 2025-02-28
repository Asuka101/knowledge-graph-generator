import base64
import logging

from ocr import recognize_image,cookies

# 设置日志记录
logging.basicConfig(filename='generate_md.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def convert(images_path, images_name, images_num, output_file):
    logging.info("正在调用llm")
    # 打开文本文件用于保存所有答案
    with open(output_file, 'w', encoding='utf-8') as file:
        # 将图片路径编码为base64字符串
        for i in range(1, images_num + 1):
            logging.info(f"Converting Image {i}......")
            image_path = f"{images_path}{images_name}_{i}.png"  # 拼接图片路径
            try:
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

                # 调用 recognize_image 函数获取 gpt_answer
                gpt_answer = recognize_image(encoded_string,i%len(cookies))
                # 将 GPT 的回答写入文本文件
                file.write(f"{gpt_answer['result']}\n")

                # 记录日志
                logging.info(f"Image {i} conversion is successful")

            except Exception as e:
                logging.error(f"Error processing image {i}: {e}")
                continue

    logging.info("Results have been saved in ：%s", output_file)


# 使用示例
convert("./textbook/", "page", 3, "textbook.txt")


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



