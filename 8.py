import os
import threading
from threading import Thread
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from threading import *


def dir_filter(directory):
    files_l = []
    dirs_l = []
    for f in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, f)):
            files_l.append(f)
        else:
            dirs_l.append(os.path.join(directory, f))
    return files_l, dirs_l





directory = "C:\\THUNDEROBOT"
pattern = ".exe"
dirs_queue = Queue()
dirs_queue.put(directory)
files_list = []
MAX_THREADS_COUNT = 5
curr_threads_count = 0
lock = Lock()
threads = []

with ThreadPoolExecutor() as executor:
    futures = []
    while not dirs_queue.empty() or len(futures) != 0:
        #print(curr_threads_count)
        while curr_threads_count < MAX_THREADS_COUNT and (not dirs_queue.empty() or len(futures) != 0):
            if dirs_queue.empty():
                break
            directory = dirs_queue.get()
            futures.append(executor.submit(dir_filter, directory))
            curr_threads_count += 1
        for future in futures:
            if future.done():
                curr_threads_count -= 1
                files, dirs = future.result()
                files_list += files
                for dir in dirs:
                    dirs_queue.put(dir)
                futures.remove(future)
    print(*filter(lambda z: z.endswith(pattern), files_list), sep='\n')