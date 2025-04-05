# description: 文本预处理类
import re
import string
import jieba

class Preprocessor:
    def __init__():
        pass

    @staticmethod
    def print_top_tokens(text):
        """ 打印词频前20的非标点词 """
        words = jieba.lcut(text) # 分词
        print(f"总词数：{len(words)}")

        # 统计词频
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        print("词频前20的词：")
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"{word}: {count}")

    @staticmethod
    def delete_stopwords(text, stopwords):
        # 分词
        words = jieba.lcut(text)

        # 去除停用词
        filtered_words = [word for word in words if word not in stopwords]

        # 将处理后的词语连接成字符串
        filtered_text = " ".join(filtered_words)
        return filtered_text
    
    @staticmethod
    def remove_punctuation(text):
        """移除标点符号"""
        return re.sub(r"[{}]+".format(re.escape(string.punctuation)), "", text)

    @staticmethod
    def remove_special_characters(text):
        """移除特殊字符，保留中文、英文、数字和空格"""
        return re.sub(r"[^\w\s\u4e00-\u9fa5]", "", text)

    @staticmethod
    def remove_specific_characters(text):
        """移除特定字符"""
        characters_to_remove = r"\$#{}\*\\"
        return re.sub(f"[{characters_to_remove}]", "", text)

    @staticmethod
    def remove_invisible_characters(text):
        """移除不可见字符"""
        return text.replace("\n", "").replace("\t", "").strip()

    @staticmethod
    def remove_english_characters(text):
        """移除英文字符"""
        return re.sub(r"[a-zA-Z]", "", text)
    
    @staticmethod
    def remove_numbers(text):
        """移除数字"""
        return re.sub(r"\d+", "", text)
    
    @staticmethod
    def remove_chinese_characters(text):
        """移除中文字符"""
        return re.sub(r"[\u4e00-\u9fa5]", "", text)
    
    @staticmethod
    def remove_whitespace(text):
        """移除多余的空格"""
        return text.replace(" ", "")
    
    @staticmethod
    def remove_empty_lines(text):
        """移除空行"""
        return "\n".join([line for line in text.splitlines() if line.strip()])