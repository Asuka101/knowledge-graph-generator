import os

# 设置文件路径
input_dir = "./textbook"  # 替换为你的文件目录
output_file = "./textbook.txt"  # 替换为输出文件路径

# 打开输出文件
with open(output_file, "w", encoding="utf-8") as outfile:
    # 遍历 390 个文件
    for i in range(1, 391):  # 从 1 到 390
        # 生成文件名
        filename = f"page_{i}.txt"
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