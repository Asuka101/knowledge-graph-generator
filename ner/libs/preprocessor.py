import re
import string

class Preprocessor:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def remove_punctuation(text):
        """移除标点符号"""
        return text.translate(str.maketrans("", "", string.punctuation))

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

    def clean_text(self, text):
        """按顺序应用所有清理规则"""
        text = self.remove_punctuation(text)
        text = self.remove_special_characters(text)
        text = self.remove_specific_characters(text)
        text = self.remove_invisible_characters(text)
        text = self.remove_english_characters(text)
        return text