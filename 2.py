from threading import Thread, Lock
from math import sqrt, ceil


def search_primes(begin, end, lock):
    primes = []
    for i in range(begin, end):
        is_prime = True
        for j in range(2, ceil(sqrt(i))):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    lock.acquire()
    global result
    result += primes
    lock.release()


N, M = map(int, input('Введите диапазон для поиска простых чисел: ').split())
THREADS_COUNT = 10
lock =Lock()
size = (M - N + 1) // THREADS_COUNT
size_last = (M - N + 1) - size * (THREADS_COUNT - 1)
result = []

threads = []
for i in range(THREADS_COUNT):
    if i == THREADS_COUNT - 1:
        threads.append(Thread(target=search_primes, args=(N + size * i, M + 1, lock)))
    else:
        threads.append(Thread(target=search_primes, args=(N + size * i, N + size * (i + 1), lock)))
    threads[-1].start()

for thread in threads:
    thread.join()
print(*sorted(result))
