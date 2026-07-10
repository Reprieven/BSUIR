from generator import generate_string, choose_password
from visuals import *

length_str = int(input('Введите длину строки: '))
string = generate_string(length_str)
print(string)
start = int(input('Введите номер начального элемента для пароля: '))
length = int(input('Введите длину пароля: '))
password = choose_password(string, start, length)
print(password)
marginal_destr(password)
brutforce_distr(password)