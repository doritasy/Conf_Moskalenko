import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ConfigParser

def test_parse_array():
    print("Тест парсинга массивов")
    
    parser = ConfigParser()
    
    print("\n1. Числовые массивы:")
    tests = [
        ("[1 2 3]", [1, 2, 3]),
        ("[0x1 0x2 0x3]", [1, 2, 3]),
        ("[10 20 30]", [10, 20, 30]),
        ("[0]", [0]),
        ("[0xFF 0x10 0x0]", [255, 16, 0]),
    ]
    
    for text, expected in tests:
        result = parser.parse_array(text)
        if result == expected:
            print(f"{text} -> {result}")
        else:
            print(f"{text}: получили {result}, ожидали {expected}")
    
    print("\n2. Строковые массивы:")
    tests = [
        ('["hello" "world"]', ["hello", "world"]),
        ('["a" "b" "c"]', ["a", "b", "c"]),
        ('["test" "123"]', ["test", "123"]),
        ('[""]', [""]),
    ]
    
    for text, expected in tests:
        result = parser.parse_array(text)
        if result == expected:
            print(f"{text} -> {result}")
        else:
            print(f"{text}: получили {result}, ожидали {expected}")
    
    print("\n3. Смешанные массивы:")
    tests = [
        ('[1 "two" 0x3]', [1, "two", 3]),
        ('[0xA "hello" 20]', [10, "hello", 20]),
        ('["start" 0 0xFF "end"]', ["start", 0, 255, "end"]),
    ]
    
    for text, expected in tests:
        result = parser.parse_array(text)
        if result == expected:
            print(f"{text} -> {result}")
        else:
            print(f"{text}: получили {result}, ожидали {expected}")
    
    print("\n4. Пустые массивы и с пробелами:")
    tests = [
        ("[]", []),
        ("[   ]", []),
        ("[ 1  2   3 ]", [1, 2, 3]),
        ("[\t1\t2\t]", [1, 2]),
    ]
    
    for text, expected in tests:
        result = parser.parse_array(text)
        if result == expected:
            print(f"{text!r} -> {result}")
        else:
            print(f"{text!r}: получили {result}, ожидали {expected}")
    
    print("\n5. Массивы через parse_value:")
    tests = [
        ("[1 2 3]", [1, 2, 3]),
        ('["a" "b"]', ["a", "b"]),
        ('[0x1 "test"]', [1, "test"]),
    ]
    
    for text, expected in tests:
        result = parser.parse_value(text)
        if result == expected:
            print(f"{text} -> {result}")
        else:
            print(f"{text}: получили {result}, ожидали {expected}")
    
    print("\n6. Некорректные массивы (должны вернуть []):")
    bad_tests = ["[", "]", "1 2 3", "[1 2", "1 2 3]"]
    for text in bad_tests:
        result = parser.parse_array(text)
        if result == []:
            print(f"{text!r} -> []")
        else:
            print(f"{text!r}: получили {result}, ожидали []")
    
    print("\n7. Массивы с константами:")
    parser.constans["base"] = 10
    parser.constans["offset"] = 5
    result = parser.parse_array("[base offset]")
    if result == [10, 5]:
        print("Массив с константами: [10, 5]")
    else:
        print(f"Массив с константами: получили {result}, ожидали [10, 5]")
    
    print("\n8. Преобразование в TOML:")
    tests = [
        ([1, 2, 3], '[ 1, 2, 3 ]'),
        (["a", "b"], '[ "a", "b" ]'),
        ([0x10, "test"], '[ 16, "test" ]'),
        ([], '[  ]'),
    ]
    
    for arr, expected in tests:
        result = parser.to_toml_value(arr)
        if result == expected:
            print(f"{arr} -> {result}")
        else:
            print(f"{arr}: получили {result}, ожидали {expected}")
    
    print("\nТесты завершены")

if __name__ == "__main__":
    test_parse_array()
