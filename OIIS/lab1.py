import numpy as np
from matplotlib import pyplot as plt
fs = 1024 #частота дискретизации
T = 1 #длительность сигнала
N = 50 #частота сигнала
L = fs * T
t = [i/1000 for i in range(L)]
sin_signal = [np.sin(2*np.pi*N*ti) for ti in t]
cos_signal = [np.cos(2*np.pi*N*ti) for ti in t]

def my_fft(funcion_signals):
    N = len(funcion_signals)
    if N <= 1:
        return funcion_signals
    even = my_fft(funcion_signals[::2])
    odd = my_fft(funcion_signals[1::2])
    combined = [0]*N
    for k in range(N//2):
        factorial = np.exp(-2j*np.pi*k/N)*odd[k]
        combined[k] = (even[k] + factorial)
        combined[k + N // 2] = (even[k] - factorial)
    return combined


my_result_sin = my_fft(sin_signal)
numpy_result_sin = np.fft.fft(sin_signal)
my_result_cos = my_fft(cos_signal)
numpy_result_cos = np.fft.fft(cos_signal)
print(np.allclose(my_result_sin,numpy_result_sin))
print(np.allclose(my_result_cos,numpy_result_cos))

frequencies = np.fft.fftfreq(L, 1/fs)

half_L = L // 2
frequencies_half = frequencies[:half_L]

amplitude_spectrum_my = np.abs(my_result_sin)[:half_L]
amplitude_spectrum_numpy = np.abs(numpy_result_sin)[:half_L]

plt.plot(t, sin_signal)
plt.title('Исходный синусоидальный сигнал')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.show()
plt.plot(frequencies_half, amplitude_spectrum_my)
plt.title('Спектр')
plt.xlabel('Частота (Гц)')
plt.ylabel('Амплитуда')
plt.show()
plt.plot(frequencies_half, np.abs(amplitude_spectrum_my - amplitude_spectrum_numpy))
plt.title('Разница между реализациями')
plt.xlabel('Частота (Гц)')
plt.ylabel('Разница амплитуд')
plt.show()
