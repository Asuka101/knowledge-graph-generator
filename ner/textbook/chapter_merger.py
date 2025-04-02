# Description: 按章节合并教材文本
import os

#  需要合并的章节首页页码及尾页页码
chapter_pages = [1, 18, 65, 111, 148, 195, 229, 266, 290, 322]
input_dir = "./pages"
input_name = "page"
output_path = "./chapters"
output_name = "chapter"
output_type = ".txt"

def concat(input_dir, output_file, pages_index):
    # 打开输出文件
    with open(output_file, "w", encoding="utf-8") as outfile:
        # 遍历 390 个文件
        for i in pages_index:  # 从 1 到 390
            # 生成文件名
            filename = f"{input_name}_{i}.txt"
            filepath = os.path.join(input_dir, filename)

            # 检查文件是否存在
            if not os.path.exists(filepath):
                print(f"文件 {filename} 不存在，跳过")
                continue

            # 读取文件内容并写入输出文件
            with open(filepath, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n")  # 可选：在文件之间添加空行

    print(f"文件已合并到: {output_file}")

for i in range(0, 9):
    pages_index = range(chapter_pages[i], chapter_pages[i+1])
    output_file = f"{output_path}/{output_name}_{i}{output_type}"
    concat(input_dir, output_file, pages_index)