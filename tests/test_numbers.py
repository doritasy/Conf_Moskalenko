import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ConfigParser

def test_parse_number():
    print("Тест парсинга чисел")
    
    parser = ConfigParser()
    
    tests = [
        ("0x10", 16),
        ("0xFF", 255),
        ("0x1A", 26),
        ("0XFF", 255),
        ("0x0", 0),
        ("0x3E8", 1000),
    ]
    
    print("\n1. Шестнадцатеричные числа:")
    for text, expected in tests:
        result = parser.parse_number(text)
        if result == expected:
            print(f"{text} -> {result}")
        else:
            print(f"{text}: получили {result}, ожидали {expected}")
    
    tests = [
        ("42", 42.0),
        ("3.14", 3.14),
        ("100", 100.0),
        ("0", 0.0),
        ("-10", -10.0),
    ]
    
    print("\n2. Десятичные числа:")
    for text, expected in tests:
        result = parser.parse_number(text)
        if result == expected:
            print(f"{text} -> {result}")
        else:
            print(f"{text}: получили {result}, ожидали {expected}")
    
    print("\n3. Некорректные числа (должны вернуть 0):")
    bad_tests = ["abc", "12a", "", "  "]
    for text in bad_tests:
        result = parser.parse_number(text)
        if result == 0.0:
            print(f"{text!r} -> {result}")
        else:
            print(f"{text!r}: получили {result}, ожидали 0.0")
    
    print("\n4. Числа с пробелами:")
    tests = [("  0x10  ", 16), (" 42 ", 42.0), ("\t0xFF\n", 255)]
    for text, expected in tests:
        result = parser.parse_number(text)
        if result == expected:
            print(f"{text!r} -> {result}")
        else:
            print(f"{text!r}: получили {result}, ожидали {expected}")
    
    print("\n5. Шестнадцатеричные через parse_value:")
    tests = [("0x10", 16), ("0xFF", 255), ("0x1A", 26)]
    for text, expected in tests:
        result = parser.parse_value(text)
        if result == expected:
            print(f"{text} -> {result}")
        else:
            print(f"{text}: получили {result}, ожидали {expected}")
    
    print("\n6. Константы с hex значениями:")
    parser.constans["test_value"] = 0x64
    result = parser.get_constant_value("test_value")
    if result == 100:
        print("Константа 0x64 правильно равна 100")
    else:
        print(f"Константа: получили {result}, ожидали 100")
    
    result = parser.parse_value("test_value")
    if result == 100:
        print("Константа через parse_value = 100")
    else:
        print(f"Константа через parse_value: получили {result}")
    
    print("\nТесты завершены")

if __name__ == "__main__":
    test_parse_number()
