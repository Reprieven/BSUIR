#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <string>
#include <fstream>
#include <cstdlib>

// Мьютекс для синхронизации записи в лог-файл
std::mutex log_mutex;

// Функция для логирования
void log_message(const std::string& message) {
    std::lock_guard<std::mutex> guard(log_mutex);
    std::ofstream log_file("/tmp/download_log.txt", std::ios::app);
    if (log_file.is_open()) {
        log_file << message << std::endl;
    } else {
        std::cerr << "Ошибка при открытии лог-файла." << std::endl;
    }
}

// Функция для скачивания файла с использованием системного вызова wget
void download_image(const std::string& url) {
    // Логируем начало скачивания
    log_message("Начинаю скачивание: " + url);

    // Формируем команду для wget
    std::string command = "wget " + url;
    
    // Выполняем команду через системный вызов
    int result = std::system(command.c_str());

    // Логируем результат скачивания
    if (result == 0) {
        log_message("Скачивание успешно завершено: " + url);
    } else {
        log_message("Ошибка при скачивании: " + url);
    }
}

int main() {
    std::vector<std::thread> threads;

    while (true) {
        std::string url;
        std::cout << "Введите URL изображения для скачивания (или 'exit' для завершения): ";
        std::getline(std::cin, url);

        if (url == "exit") {
            break;
        }

        // Запускаем скачивание в отдельном потоке
        threads.push_back(std::thread(download_image, url));
    }

    // Ждем завершения всех потоков
    for (auto& t : threads) {
        t.join();
    }
      //https://images.app.goo.gl/sCv51rfmCsT3Upks5
    std::cout << "Завершено выполнение программы." << std::endl;
    return 0;
}