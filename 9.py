import math
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from scipy.integrate import quad

def calculate_factorial(number):
    try:
        return f"Результат вычисления факториала {number}: {math.factorial(number)}"
    except Exception as e:
        return f"Ошибка: {e}"

def calculate_degree(base, exponent):
    try:
        return f"Результат вычисления {base} ** {exponent}: {base ** exponent}"
    except Exception as e:
        return f"Ошибка: {e}"

def calculate_integral(func, lower_limit, upper_limit):
    try:
        result = quad(func, lower_limit, upper_limit)
        return (f"Результат вычисления интеграла для функции {func} "
                f"с нижней границей {lower_limit} и верхней границей {upper_limit}: {result}")
    except Exception as e:
        return f"Ошибка {e}"

def distribution_of_threads(task):
    operation, args = task

    if operation == "factorial":
        result = calculate_factorial(args[0])
    elif operation == "degree":
        result = calculate_degree(args[0], args[1])
    else:
        result = calculate_integral(lambda x: x ** 2, args[0], args[1])

    return result


tasks = []
results = []
lock = threading.Lock()
print("Добро пожаловать в калькулятор. Доступные операции:")
print("1. Факториал: factorial <число>")
print("2. Возведение в степень: degree <основание> <показатель>")
print("3. Интеграл: integral <нижняя_граница> <верхняя_граница>")
print("Введите 'done' для завершения ввода.")


while True:
    user_input = input("Введите операцию: ").strip()
    if user_input.lower() == "done":
        break

    try:
        task = user_input.split()
        operation = task[0]
        if operation == "factorial":
            number = int(task[1])
            if number < 0:
                raise ValueError("Значение для подсчета факториала не может быть меньше нуля.")
            tasks.append((operation, (number, )))
        elif operation == "degree":
            base = float(task[1])
            exponent = float(task[2])
            tasks.append((operation, (base, exponent)))
        elif operation == "integral":
            lower_limit = float(task[1])
            upper_limit = float(task[2])
            tasks.append((operation, (lower_limit, upper_limit)))
        else:
            print("Неизвестная операция. Попробуйте снова.")
    except (IndexError, ValueError):
        print("Некорректный ввод.")

if not tasks:
    print("Нет операций для подсчета")
print(tasks)

with ThreadPoolExecutor(max_workers=3) as executor:
    future_list = []
    for task in tasks:
        future = executor.submit(distribution_of_threads, task)
        future_list.append(future)
    for f in as_completed(future_list):
        print(f.result())
