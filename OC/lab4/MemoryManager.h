#include <iostream>
#include <unordered_map>
#include <list>
#include <cstring>
#include <cstdlib>


struct Segment
 {
    int id;            
    size_t size;       
    void* address;     
    bool inMemory;     

    Segment(int id, size_t size) : id(id), size(size), address(nullptr), inMemory(false) {}
    Segment() : id(0), size(0), address(nullptr), inMemory(false) {}
};


class MemoryManager 
{
private:
    size_t physicalMemorySize;  
    size_t usedMemory;        

    std::list<int> lruQueue;   
    std::unordered_map<int, Segment> segmentTable; 

public:
    MemoryManager(size_t physicalMemorySize) : physicalMemorySize(physicalMemorySize), usedMemory(0) {}

    void addSegment(int id, size_t size) 
    {
        if (segmentTable.find(id) != segmentTable.end()) 
        {
            std::cerr << "Сегмент с ID " << id << " уже существует.\n";
            return;
        }
        segmentTable[id] = Segment(id, size);
        std::cout << "Сегмент " << id << " добавлен в виртуальную память (размер: " << size << " байт).\n";
    }

   
    void loadSegment(int id) 
    {
        if (segmentTable.find(id) == segmentTable.end()) 
        {
            std::cerr << "Сегмент с ID " << id << " не существует.\n";
            return;
        }

        Segment& segment = segmentTable[id];
        if (segment.inMemory) 
        {
            std::cout << "Сегмент " << id << " уже находится в физической памяти.\n";
            updateLRU(id);
            return;
        }

       
        if (segment.size > physicalMemorySize) 
        {
            std::cerr << "Сегмент " << id << " слишком велик для физической памяти.\n";
            return;
        }

        while (usedMemory + segment.size > physicalMemorySize)
         {
            evictSegment();
        }

       
        segment.address = malloc(segment.size);
        if (!segment.address) 
        {
            std::cerr << "Не удалось выделить память для сегмента " << id << ".\n";
            return;
        }
        memset(segment.address, 0, segment.size); 
        segment.inMemory = true;
        usedMemory += segment.size;
        lruQueue.push_front(id);

        std::cout << "Сегмент " << id << " загружен в физическую память (размер: " << segment.size << " байт).\n";
    }


    void evictSegment() 
    {
        if (lruQueue.empty()) 
        {
            std::cerr << "Физическая память пуста, нечего выгружать.\n";
            return;
        }

        int idToEvict = lruQueue.back(); 
        lruQueue.pop_back();

        Segment& segment = segmentTable[idToEvict];
        if (segment.inMemory) 
        {
            free(segment.address); 
            segment.address = nullptr;
            segment.inMemory = false;
            usedMemory -= segment.size;

            std::cout << "Сегмент " << idToEvict << " выгружен из физической памяти.\n";
        }
    }

    void updateLRU(int id) 
    {
        lruQueue.remove(id);
        lruQueue.push_front(id);
    }

    void displayMemoryState() 
    {
        std::cout << "\n--- Состояние памяти ---\n";
        std::cout << "Использованная память: " << usedMemory << " / " << physicalMemorySize << " байт\n";
        std::cout << "Сегменты в физической памяти: ";
        for (int id : lruQueue) 
        {
            std::cout << id << " ";
        }
        std::cout << "\n------------------------\n";
    }

    ~MemoryManager()
    {
        for (auto& [id, segment] : segmentTable)
        {
            if (segment.inMemory) 
            {
                free(segment.address);
            }
        }
    }
};