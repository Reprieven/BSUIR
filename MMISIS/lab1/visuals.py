import string
from matplotlib import pyplot as plt
import numpy as np
from brute_force import bruteforce_count_time
def marginal_destr(password: str):
    symbols = list(string.ascii_letters)+list(string.digits)
    counts = [password.count(i) for i in symbols]
    y = np.arange(0, len(password)/10)
    plt.bar(symbols, counts)
    plt.title('Частное распределение')
    plt.xlabel('Символ')
    plt.ylabel('Количество повторений')
    plt.yticks(y)
    plt.show()


def brutforce_distr(password: str):
    timespans = bruteforce_count_time(password)
    length = len(password)
    x = np.arange(1, length+1,1)
    plt.plot(x, timespans)
    plt.title('Распределение времени брутфорса в зависимости от длины пароля')
    plt.xlabel('Кол-во символов')
    plt.ylabel('Время брутфорса')
    plt.xticks(x)
    plt.show()
