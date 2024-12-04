import random
import threading
import time


class ATM:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    def withdraw_money(self, client, amount):
        with self.condition:
            while self.balance < amount:
                print(f'Клиент {client} запрашивает на снятие следующую сумму: {amount}.')
                time.sleep(1)
                print(f'Средств недостаточно.')
                self.condition.wait()

            print(f'Клиент {client} запрашивает на снятие следующую сумму: {amount}. Идет обработка.')
            time.sleep(1)
            self.balance -= amount
            print(f'Клиент {client} успешно снял следующую сумму: {amount}. Баланс счета: {self.balance}.')

    def top_up_balance(self, client, amount):
        with self.condition:
            self.balance += amount
            print(f'Клиент {client} пополнил баланс на сумму: {amount}. Баланс счета: {self.balance}.')
            self.condition.notify_all()


ATM = ATM(300)
clients_count = 2
threads = []

def withdraw(atm, client):
    for attempt in range(2):
        atm.withdraw_money(client, random.randint(150, 250))
        time.sleep(1)

def top_up(atm, client):
    for attempt in range(3):
        atm.top_up_balance(client, random.randint(50, 100))
        time.sleep(1)


for client in range(1, clients_count + 1):
    thread = threading.Thread(target=withdraw, args=(ATM, client))
    threads.append(thread)
    thread.start()

for client in range(clients_count + 1, clients_count + 3):
    thread = threading.Thread(target=top_up, args=(ATM, client))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
