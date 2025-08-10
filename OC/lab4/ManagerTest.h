#include <gtest/gtest.h>
#include "MemoryManager.h"  

TEST(MemoryManagerTest, AddSegmentSuccessfully) {
    MemoryManager memoryManager(1024); // 1 КБ физической памяти
    memoryManager.addSegment(1, 256);
    EXPECT_NO_THROW(memoryManager.loadSegment(1));
};

TEST(MemoryManagerTest, AddDuplicateSegment) {
    MemoryManager memoryManager(1024);
    memoryManager.addSegment(1, 256);
    testing::internal::CaptureStderr(); // Захватываем поток ошибок
    memoryManager.addSegment(1, 256);
    std::string output = testing::internal::GetCapturedStderr();
    EXPECT_TRUE(output.find("Сегмент с ID 1 уже существует") != std::string::npos);
};

TEST(MemoryManagerTest, LoadSegmentIntoMemory) {
    MemoryManager memoryManager(1024);
    memoryManager.addSegment(1, 256);
    EXPECT_NO_THROW(memoryManager.loadSegment(1));
};

TEST(MemoryManagerTest, LoadSegmentTooLarge) {
    MemoryManager memoryManager(1024);
    memoryManager.addSegment(1, 2048); // Сегмент больше доступной памяти
    testing::internal::CaptureStderr(); // Захватываем поток ошибок
    memoryManager.loadSegment(1);
    std::string output = testing::internal::GetCapturedStderr();
    EXPECT_TRUE(output.find("Сегмент 1 слишком велик для физической памяти") != std::string::npos);
};

TEST(MemoryManagerTest, EvictSegment) {
    MemoryManager memoryManager(1024);
    memoryManager.addSegment(1, 256);
    memoryManager.addSegment(2, 256);
    memoryManager.loadSegment(1);
    memoryManager.loadSegment(2);
    memoryManager.evictSegment();
    EXPECT_NO_THROW(memoryManager.loadSegment(1));
};

TEST(MemoryManagerTest, UpdateLRU) {
    MemoryManager memoryManager(1024);
    memoryManager.addSegment(1, 256);
    memoryManager.addSegment(2, 256);
    memoryManager.loadSegment(1);
    memoryManager.loadSegment(2);
    memoryManager.updateLRU(1); // Обновляем LRU для сегмента 1
    testing::internal::CaptureStdout();
    memoryManager.displayMemoryState();
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_TRUE(output.find("Сегменты в физической памяти: 1 2") != std::string::npos);
};