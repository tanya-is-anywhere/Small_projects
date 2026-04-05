import re

in_cal = input("Введите выражение: ")
def calculate_with_priority(expression):
    try:
        numbers = list(map(float, re.split(r'[\+\-\*/^]', expression)))
        ops = re.findall(r'[\+\-\*/^]', expression)
        i = 0
        while i < len(ops):
            if ops[i] in ['*', '/']:
                if ops[i] == '*':
                    numbers[i] = numbers[i] * numbers[i + 1]
                else:
                    if numbers[i + 1] == 0:
                        raise ZeroDivisionError("Деление на ноль!")
                    numbers[i] = numbers[i] / numbers[i + 1]
                del numbers[i + 1]
                del ops[i]
            else:
                i += 1
        result = numbers[0]
        for i, op in enumerate(ops):
            if op == '+':
                result += numbers[i + 1]
            elif op == '-':
                result -= numbers[i + 1]
        return result
    except ZeroDivisionError:
        print("На ноль делить нельзя!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")



print(calculate_with_priority(in_cal))
