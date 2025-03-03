import fitz  # PyMuPDF

# 打开 PDF 文件
with fitz.open('textbook.pdf') as doc:
    # 遍历每一页
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # 将 PDF 页面转换为图像，pixmap 是图像对象
        pix = page.get_pixmap(dpi=300)
        
        # 保存图像为 PNG 格式
        pix.save(f'page_{page_num + 1}.png')

print("所有页面已成功转换为图片")
