import re
import sys
import math
from typing import Dict, List, Any, Union
from pathlib import Path

class ConfigParser:
    def __init__(self):
        self.constans: Dict[str, float] = {}

        self.one_line_comment = re.compile(r'\|\|.*')
        self.big_comment = re.compile(r'<!--.*?-->', re.DOTALL)
        self.number = re.compile(r'0[xX][0-9a-fA-F]+')
        self.array = re.compile(r'\[\s*(.*?)\s*\]')
        self.dict = re.compile(r'table\(\s*(.*?)\s*\)', re.DOTALL)
        self.key_value = re.compile(r'([a-zA-Z][a-zA-Z0-9]*)\s*=>\s*(.*?)(?:,|$)')
        self.string = re.compile(r'"([^"]*)"')
        self.const_decl = re.compile(r'([a-zA-Z][a-zA-Z0-9]*)\s*<-\s*(.*?);')
        self.constant_eval = re.compile(r'!\{(.+?)\}')

if __name__ == "__main__":
    parser = ConfigParser()
    print("ConfigParser инициализирован")
