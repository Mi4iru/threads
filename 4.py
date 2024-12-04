from threading import Thread


def particial_factorial(num, start, end):
    res = 1
    for i in range(start, end):
        res *= i
    global result
    global result_string
    result[num] = res
    result_string[num] = f"Thread number {num + 1} multiplication from: {start} to: {end} result: {res}"


THREADS_COUNT = int(input("Введите количество рабочих потоков: "))
result = [1] * THREADS_COUNT
result_string = [''] * THREADS_COUNT
threads = []

N = int(input('Введите целое число: '))
if N == 0 or N == 1:
    print(1)
    exit()

size = N // THREADS_COUNT

for i in range(THREADS_COUNT):
    if i == THREADS_COUNT - 1:
        threads.append(Thread(target=particial_factorial, args=(i, 1 + size * i, N + 1)))
    else:
        threads.append(Thread(target=particial_factorial, args=(i,  1 + size * i, size * (i + 1) + 1)))
    threads[-1].start()

for thread in threads:
    thread.join()

fact = 1
for i in result:
    fact *= i
print(fact)
for i in result_string:
    print(i)