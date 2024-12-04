from concurrent.futures import ThreadPoolExecutor


def func(words):
    d = {}
    for i in words:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1
    return d


f = open('input.txt', 'r')
s = []
for j in [i.rstrip() for i in f.readlines()]:
    for word in j.split():
        s.append(word)
THREADS_COUNT = 5
threads = []


with ThreadPoolExecutor() as executor:
    data = []
    total = {}
    for i in range(THREADS_COUNT):
        data.append(s[i::THREADS_COUNT])
    results = executor.map(func, data)
    for result in results:
        for key in result.keys():
            if key in total.keys():
                total[key] += result[key]
            else:
                total[key] = result[key]
    for key in sorted(total, key=lambda k: total[k]):
        print(key, total[key])
