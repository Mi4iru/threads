from threading import Thread, Lock


def particial_sort(num, arr):
    global result
    result[0][num] = sorted(arr)

def merge_arrs(num, arr1, arr2, lock):
    res = []
    i = 0
    j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            res += [arr1[i]]
            i += 1
        else:
            res += [arr2[j]]
            j += 1
    if i == len(arr1):
        res += arr2[j:]
    else:
        res += arr1[i:]
    global result
    lock.acquire()
    result[num + 1].append(res)
    lock.release()


THREADS_COUNT = int(input("Введите количество потоков: "))
array = list(map(int, input('Введите массив: ').split()))
threads = []
lock = Lock()
result = [[0] * THREADS_COUNT]

for i in range(THREADS_COUNT):
    threads.append(Thread(target=particial_sort, args=(i, array[i::THREADS_COUNT])))
    threads[-1].start()

for thread in threads:
    thread.join()

i = 0
while len(result[i]) > 1:
    threads = []
    if len(result[i]) % 2 == 1:
        result.append([result[i][0]])
    else:
        result.append([])
    for j in range(len(result[i]) % 2, len(result[i]), 2):
        threads.append(Thread(target=merge_arrs,
                              args=(i, result[i][j], result[i][j + 1], lock)))
    for thread in threads:
        thread.start()
        thread.join()
    i += 1

print(' '.join([str(i) for i in result[-1][0]]))