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
        except ValueError:
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
        if value_str in self.constants:
            return self.constants[value_str]
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

    def parse_constant_declaration(self, line: str):
        match = self.const_decl.search(line)
        if match:
            name = match.group(1)
            value_str = match.group(2)
            value = self.parse_value(value_str)
            if isinstance(value, (int, float)):
                self.constants[name] = value

    def evaluate_expression(self, expr: str) -> float:
        expr = expr.strip()

        if '+' in expr:
            parts = expr.split('+',1)
            left = self.get_constant_value(parts[0].strip())
            right = self.get_constant_value(parts[1].strip())
            return left - right
        if '-' in expr:
            parts = expr.split('-',1)
            left = self.get_constant_value(parts[0].strip())
            right = self.get_constant_value(parts[1].strip())
            return left - right
        if expr.startswith('abs(') and expr.endswith(')'):
            arg = expr[4:-1].strip()
            arg_value = self.get_constant_value(arg)
            return abs(arg_value)
        return self.get_constant_value(expr)

    def get_constant_value(self, name: str) -> float:
        name = name.strip()

        if name in self.constants:
            return self.constants[name]
        try:
            return float(name)
        except ValueError:
            if self.number.match(name):
                return int(name,16)
            return 0.0

    def process_constant_expressions(self, text: str)->str:
        def replace_match(match):
            expr = match.group(1)
            try:
                result = self.evaluate_expression(expr)
                return str(result)
            except:
                return "0"
        return self.const_eval.sub(replace_match, text)

    def to_toml_value(self, value: Any) -> str:
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value,bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            elements = [self.to_toml_value(elem) for elem in value]
            return f'[ {", ".join(elements)} ]'
        elif isinstance(value, decit):
            lines = []
            for k, v in value.items():
                lines.append(f'{k} = {self.to_toml_value(v)}')
            return '\n'.join(lines)
        else:
            return '""'

    def convert_to_toml(self, data: Dict[str, Any]) -> str:
        lines = []

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f'[{key}]')
                for sub_key, sub_value in value.items():
                    lines.append(f'{sub_key} = {self.to_toml_value(sub_value)}')
                lines.append('')
            else:
                lines.append(f'{key} = {self.to_toml_value(value)}')
        return '\n'.join(lines)

    def parse(self, input_text: str) -> Dict[str, Any]:
        cleaned_text = self.remove_comments(input_text)

        lines = cleaned_text.split('\n')
        result = {}

        other_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if '<-' in line:
                self.parse_constant_declaration(line)
            else:
                other_lines.append(line)

        for line in other_lines:
            line = self.process_constant_expressions(line)
            if not line.strip():
                continue
            if line.startswith('table('):
                dict_data = self.parse_dict(line)
                result.update(dict_data)
            elif line.startswith('[') and line.endswith(']'):
                array_data = self.parse_array(line)
                result['array'] = array_data
            elif '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = self.parse_value(parts[1].strip())
                    result[key] = value
        return result
    
def main():
    if len(sys.argv) != 3:
        print("Использование: python main.py <входной_файл> <выходной_файл>")
        print("Пример: python main.py config.txt output.toml")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not Path(input_file).exists():
        print(f"Ошибка: входной файл '{input_file}' не существует")
        sys.exit(1)
    
    try:
        print(f"Чтение входного файла: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            input_content = f.read()
        
        parser = ConfigParser()
        parsed_data = parser.parse(input_content)
        
        toml_output = parser.convert_to_toml(parsed_data)
        
        print(f"Запись результата в файл: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(toml_output)
        
        print(f"Конфигурация успешно преобразована:")
        print(f"Вход:  {input_file}")
        print(f"Выход: {output_file}")
        
    except Exception as e:
        print(f"Ошибка при обработке файлов: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
