#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <sstream>

const int BLOCK_SIZE = 512; 
const int MAX_BLOCKS = 100; 
const std::string DISK_FILE = "virtual_disk.bin"; 
const std::string META_FILE = "metadata.txt";  

struct File {
    std::string name;
    int size; 
    std::vector<int> blocks;
};


std::unordered_map<std::string, File> files;
std::vector<bool> block_usage(MAX_BLOCKS, false);


void initializeDisk() {
    std::ofstream disk(DISK_FILE, std::ios::binary | std::ios::app);
    if (!disk) {
        std::cerr << "Не удалось инициализировать диск!" << std::endl;
        exit(1);
    }
    disk.close();
    std::ifstream meta(META_FILE);
    if (!meta) {
        std::ofstream metaOut(META_FILE); 
        metaOut.close();
    }
}

void saveMetadata() {
    std::ofstream meta(META_FILE, std::ios::trunc);
    for (const auto& [name, file] : files) {
        meta << file.name << " " << file.size;
        for (int block : file.blocks) {
            meta << " " << block;
        }
        meta << std::endl;
    }
    meta.close();
}

void loadMetadata() {
    std::ifstream meta(META_FILE);
    if (!meta) return;

    std::string line;
    while (std::getline(meta, line)) {
        std::istringstream iss(line);
        File file;
        iss >> file.name >> file.size;
        int block;
        while (iss >> block) {
            file.blocks.push_back(block);
            block_usage[block] = true;
        }
        files[file.name] = file;
    }
    meta.close();
}

void createFile(const std::string& name, const std::string& content) {
    if (files.find(name) != files.end()) {
        std::cerr << "Файл уже существует!" << std::endl;
        return;
    }

    File file;
    file.name = name;
    file.size = content.size();

    int required_blocks = (content.size() + BLOCK_SIZE - 1) / BLOCK_SIZE;
    for (int i = 0; i < MAX_BLOCKS && required_blocks > 0; ++i) {
        if (!block_usage[i]) {
            block_usage[i] = true;
            file.blocks.push_back(i);
            --required_blocks;
        }
    }

    if (required_blocks > 0) {
        std::cerr << "Недостаточно места на диске!" << std::endl;
        return;
    }

    std::ofstream disk(DISK_FILE, std::ios::binary | std::ios::in | std::ios::out);
    for (size_t i = 0; i < file.blocks.size(); ++i) {
        int block_num = file.blocks[i];
        disk.seekp(block_num * BLOCK_SIZE);
        disk.write(content.data() + i * BLOCK_SIZE, std::min(BLOCK_SIZE, static_cast<int>(content.size() - i * BLOCK_SIZE)));
    }
    disk.close();

    files[name] = file;
    saveMetadata();
}

void deleteFile(const std::string& name) {
    auto it = files.find(name);
    if (it == files.end()) {
        std::cerr << "Файл не найден!" << std::endl;
        return;
    }

    for (int block : it->second.blocks) {
        block_usage[block] = false;
    }
    files.erase(it);
    saveMetadata();
}

void readFile(const std::string& name) {
    auto it = files.find(name);
    if (it == files.end()) {
        std::cerr << "Файл не найден!" << std::endl;
        return;
    }

    File file = it->second;
    std::ifstream disk(DISK_FILE, std::ios::binary);
    std::string content;
    content.resize(file.size);

    for (size_t i = 0; i < file.blocks.size(); ++i) {
        int block_num = file.blocks[i];
        disk.seekg(block_num * BLOCK_SIZE);
        disk.read(&content[i * BLOCK_SIZE], std::min(BLOCK_SIZE, static_cast<int>(file.size - i * BLOCK_SIZE)));
    }
    disk.close();

    std::cout << "Содержимое файла \"" << name << "\": " << content << std::endl;
}

void copyFile(const std::string& source, const std::string& destination) {
    auto it = files.find(source);
    if (it == files.end()) {
        std::cerr << "Исходный файл не найден!" << std::endl;
        return;
    }

    if (files.find(destination) != files.end()) {
        std::cerr << "Файл с именем назначения уже существует!" << std::endl;
        return;
    }

    File sourceFile = it->second;
    std::ifstream disk(DISK_FILE, std::ios::binary);
    if (!disk) {
        std::cerr << "Ошибка открытия виртуального диска!" << std::endl;
        return;
    }

    std::string content;
    content.resize(sourceFile.size);
    for (size_t i = 0; i < sourceFile.blocks.size(); ++i) {
        int block_num = sourceFile.blocks[i];
        disk.seekg(block_num * BLOCK_SIZE);
        disk.read(&content[i * BLOCK_SIZE], std::min(BLOCK_SIZE, static_cast<int>(sourceFile.size - i * BLOCK_SIZE)));
    }
    disk.close();

    createFile(destination, content);

    std::cout << "Файл \"" << source << "\" успешно скопирован в \"" << destination << "\".\n";
}

void appendToFile(const std::string& name, const std::string& content) {
    auto it = files.find(name);
    if (it == files.end()) {
        std::cerr << "Файл не найден!" << std::endl;
        return;
    }
    File& file = it->second;
    std::string existingContent;

    std::ifstream disk(DISK_FILE, std::ios::binary);
    existingContent.resize(file.size);
    for (size_t i = 0; i < file.blocks.size(); ++i) {
        int block_num = file.blocks[i];
        disk.seekg(block_num * BLOCK_SIZE);
        disk.read(&existingContent[i * BLOCK_SIZE], std::min(BLOCK_SIZE, static_cast<int>(file.size - i * BLOCK_SIZE)));
    }
    disk.close();

    existingContent += content;
    deleteFile(name);
    createFile(name, existingContent); 
}

void moveFile(const std::string& source, const std::string& destination) {
    auto it = files.find(source);
    if (it == files.end()) {
        std::cerr << "Исходный файл не найден!" << std::endl;
        return;
    }

    if (files.find(destination) != files.end()) {
        std::cerr << "Файл с именем назначения уже существует!" << std::endl;
        return;
    }

    File file = it->second;
    files.erase(it);
    file.name = destination;
    files[destination] = file;
    saveMetadata();
}

void dumpDisk() {
    std::cout << "Содержимое диска:\n";
    for (const auto& [name, file] : files) {
        std::cout << "Файл: " << file.name << ", Размер: " << file.size << " байт, Блоки: ";
        for (int block : file.blocks) {
            std::cout << block << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    initializeDisk();
    loadMetadata();

    while (true) {
        std::cout << "\nМеню:\n";
        std::cout << "1. Создать файл\n";
        std::cout << "2. Удалить файл\n";
        std::cout << "3. Прочитать файл\n";
        std::cout << "4. Копировать файл\n";
        std::cout << "5. Переместить файл\n";
        std::cout << "6. Добавить содержимое в файл\n";
        std::cout << "7. Дамп содержимого диска\n";
        std::cout << "8. Выход\n";
        std::cout << "Ваш выбор: ";

        int choice;
        std::cin >> choice;

        std::string name, content, dest;
        switch (choice) {
            case 1:
                std::cout << "Введите имя файла: ";
                std::cin >> name;
                std::cout << "Введите содержимое файла: ";
                std::cin.ignore();
                std::getline(std::cin, content);
                createFile(name, content);
                break;
            case 2:
                std::cout << "Введите имя файла: ";
                std::cin >> name;
                deleteFile(name);
                break;
            case 3:
                std::cout << "Введите имя файла: ";
                std::cin >> name;
                readFile(name);
                break;
            case 4:
                std::cout << "Введите имя исходного файла: ";
                std::cin >> name;
                std::cout << "Введите имя файла назначения: ";
                std::cin >> dest;
                copyFile(name, dest);
                break;
            case 5:
                std::cout << "Введите имя исходного файла: ";
                std::cin >> name;
                std::cout << "Введите новое имя файла: ";
                std::cin >> dest;
                moveFile(name, dest);
                break;
            case 6:
                std::cout << "Введите имя файла: ";
                std::cin >> name;
                std::cout << "Введите содержимое для добавления: ";
                std::cin.ignore();
                std::getline(std::cin, content);
                appendToFile(name, content);
                break;
            case 7:
                dumpDisk();
                break;
            case 8:
                std::cout << "Выход из программы...\n";
                return 0;
            default:
                std::cerr << "Некорректный выбор, попробуйте снова.\n";
        }
    }
    return 0;
}

