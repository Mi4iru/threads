from threading import Thread


def func():
    pass


n = int(input("Сколько потоков необходимо создать? "))
threads_pool = []
for i in range(n):
    threads_pool.append(Thread(target=func))
    print(threads_pool[-1].name)