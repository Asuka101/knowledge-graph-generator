# description: 合并多个 JSON 文件中的 "entities" 和 "relations" 字段
import os
import json

def merge_json_files(input_folder, output_file):
    merged_data = {"entities": [], "relations": []}

    # 遍历文件夹中的所有 JSON 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    # 合并 "entities" 和 "relations"
                    if "entities" in data:
                        merged_data["entities"].extend(data["entities"])
                    if "relations" in data:
                        merged_data["relations"].extend(data["relations"])
                except json.JSONDecodeError as e:
                    print(f"文件 {filename} 解析失败: {e}")

    # 将合并后的数据写入输出文件
    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(merged_data, output, ensure_ascii=False, indent=4)
    print(f"合并完成，结果已保存到 {output_file}")

# 使用示例
input_folder = "./data"  # 输入文件夹路径
output_file = "./data/data.json"  # 输出文件路径
merge_json_files(input_folder, output_file)