import re
import sys
import math
from typing import Dict, List, Any, Union
from pathlib import Path

class ConfigParser:
    def __init__(self):
        self.constans: Dict[str, float] = {}

        self.one_line_comment = re.compile(r'\|\|.*')
        self.big_comment = re.compile(r'<!--.*?-->', re.DOTALL)  # Многострочные комментарии
        self.number = re.compile(r'0[xX][0-9a-fA-F]+')  # Шестнадцатеричные числа
        self.array = re.compile(r'\[\s*(.*?)\s*\]')  # Массивы
        self.dict = re.compile(r'table\(\s*(.*?)\s*\)', re.DOTALL)  # Словари
        self.key_value = re.compile(r'([a-zA-Z][a-zA-Z0-9]*)\s*=>\s*(.*?)(?:,|$)')  # Пары ключ-значение
        self.string = re.compile(r'"([^"]*)"')  # Строки в кавычках
        self.const_decl = re.compile(r'([a-zA-Z][a-zA-Z0-9]*)\s*<-\s*(.*?);')  # Объявления констант
        self.const_eval = re.compile(r'!\{(.+?)\}')  # Вычисления констант

    def remove_comments(self, text: str) -> str:
        # Сначала удаляем многострочные комментарии
        text = self.big_comment.sub('', text)
        # Затем удаляем однострочные комментарии
        text = self.one_line_comment.sub('', text)
        return text

    def parse_number(self, num_str: str) -> float:
        num_str = num_str.strip()
        if self.number.match(num_str):
            return int(num_str, 16)
        try:
            return float(num_str)
        exept ValueError:
            return 0.0

    def parse_string(self, string_str: str) -> str:
        match = self.string.search(string_str)
        if match:
            return match.group(1)
        return string_str.strip()

    def parse_array(self, array_str: str) -> List[Any]:
        match = self.array.search(array_str)
        if match:
            content = match.group(1)
            elements = [elem.strip() for elem in content.split() if elem.strip()]
            return [self.parse_value(elem) for elem in elements]
        return []
    
    def parse_value(self, value_str: str) -> Any:
        value_str = value_str.strip()

        if not value_str:
            return ""
        if self.number.match(value_str):
            return self.parse_number(value_str)
        if value_str.startswith('""') and value.str.endswitch('""'):
            return self.parse_string(value_str)
        if value_str.startswith('[') and value.str.endswitch(']'):
            return self.parse_array(value_str)
        if value_str.startswith('table('):
            return self.parse_dict(value_str)
        try:
            return float(value_str)
        except ValueError:
            return value_str

    def parse_dict(self, dict_str: str) -> Dict[str, Any]:
        match = self.dict.search(dict_str)
        if match:
            content = match.group(1)
            result = {}

            for match in self.key_value.finditer(content):
                key = match.group(1)
                value = self.parse_value(match.group(2))
                result[key] = value

            return result
        return {}

if __name__ == "__main__":
    parser = ConfigParser()
    print("ConfigParser инициализирован")
