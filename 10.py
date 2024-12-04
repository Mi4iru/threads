import threading
from threading import Thread, Lock
from random import randint
from time import sleep


class ParkingSpace():
    def __init__(self):
        self.capacity = 5
        self.current = 0

    def parking(self):
        if self.current < self.capacity:
            self.current += 1
            return True
        else:
            return False

    def exit(self, condition):
        self.current -= 1
        with condition:
            condition.notify()

    def statistics(self):
        return self.current, self.capacity


def car_run(parking, num, condition):
    time_arrive = randint(1, 47)
    time_parking = randint(1, 48 - time_arrive)
    sleep(time_arrive / 2)
    if parking.parking():
        result = parking.statistics()
        print(f'Машина {num} припарковалась, занято: {result[0]}/{result[1]}')
        sleep(time_parking / 2)
        parking.exit(condition)
        result = parking.statistics()
        print(f'Машина {num} покинула парковку, занято: {result[0]}/{result[1]}')
    else:
        print(f'Машина {num} попыталась припарковаться, но свободных мест нет')
        with condition:
            condition.wait()
        parking.parking()
        result = parking.statistics()
        print(f'Машина {num} припарковалась, занято: {result[0]}/{result[1]}')
        sleep(time_parking / 2)
        parking.exit(condition)
        result = parking.statistics()
        print(f'Машина {num} покинула парковку, занято: {result[0]}/{result[1]}')


cars = []
parking_space = ParkingSpace()
lock = Lock()
condition = threading.Condition(lock=lock)
for i in range(20):
    car = Thread(target=car_run, args=(parking_space, i + 1, condition))
    car.start()
    cars.append(car)

for i in cars:
    i.join()
