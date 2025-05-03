# description: 文本转换器
import os
import fitz  # PyMuPDF
import base64
from src.libs.ocr import recognize_image, cookies
import concurrent.futures

class PDF2TextbookConverter:
    def __init__(self):
        # PDF 相关配置
        self.textbook_path = os.getenv("TEXTBOOK_PATH")
        self.textbook_name = os.getenv("TEXTBOOK_NAME")
        self.textbook_extension = os.getenv("TEXTBOOK_TYPE")

        # 图片相关配置
        self.image_path = os.getenv("IMAGE_PATH")
        self.image_name = os.getenv("IMAGE_NAME")
        self.image_extension = os.getenv("IMAGE_TYPE")

        # 文本输出相关
        self.page_path = os.getenv("PAGE_PATH")
        self.page_name = os.getenv("page_NAME")
        self.page_extension = os.getenv("page_TYPE")


    def pdf2images(self):
        print("开始PDF转图片...")
        pdf_file = os.path.join(self.textbook_path, f"{self.textbook_name}{self.textbook_extension}")
        with fitz.open(pdf_file) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=300)
                img_filename = os.path.join(self.image_path, f"{self.image_name}_{page_num + 1}{self.image_extension}")
                pix.save(img_filename)
                print(f"保存图片: {self.image_name}_{page_num + 1}{self.image_extension}")
        print("所有页面已成功转换为图片")

    def process_image(self, i):
        image_file = os.path.join(self.image_path, f"{self.image_name}_{i}{self.image_extension}")
        page_file = os.path.join(self.page_path, f"{self.page_name}_{i}{self.page_extension}")
        complete = 0
        while complete == 0:
            try:
                with open(image_file, "rb") as img_f:
                    encoded_string = base64.b64encode(img_f.read()).decode('utf-8')
                with open(page_file, 'w', encoding='utf-8') as out_f:
                    gpt_answer = recognize_image(encoded_string, i % len(cookies))
                    out_f.write(f"{gpt_answer['result']}\n")
                    print(f"图片 {i} 转换成功！")
                    complete = 1
            except Exception as e:
                print(f"处理图片 {i} 发生错误: {e}")
                complete = 0
                continue

    def images2text(self, image_indices=None):
        print("开始图片转文本...")
        os.makedirs(self.page_path, exist_ok=True)
        if image_indices is None:
            # 自动检测图片数量
            image_indices = []
            for fname in os.listdir(self.image_path):
                if fname.startswith(self.image_name) and fname.endswith(self.image_extension):
                    try:
                        idx = int(fname.replace(self.image_name + "_", "").replace(self.image_extension, ""))
                        image_indices.append(idx)
                    except Exception:
                        continue
            image_indices.sort()

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(cookies)) as executor:
            executor.map(self.process_image, image_indices)

        print("图片转文本完成!")

    def convert(self):
        self.pdf2images()
        self.images2text()