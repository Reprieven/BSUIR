#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/sem.h>
#include <sys/wait.h>
#include <cstdlib>
#include <ctime>

const int SHM_SIZE = sizeof(int);
const char* outputFile = "output.txt";

union semun {
    int val;
    struct semid_ds* buf;
    unsigned short* array;
};

void semaphore_wait(int sem_id) {
    struct sembuf op = {0, -1, 0};
    semop(sem_id, &op, 1);
}

void semaphore_signal(int sem_id) {
    struct sembuf op = {0, 1, 0};
    semop(sem_id, &op, 1);
}

void generate_numbers(int* shared_memory, int sem_id1, int sem_id2) {
    std::srand(std::time(nullptr));

    for (int i = 0; i < 10; i++) {
        int number = std::rand() % 100;
        *shared_memory = number;


        semaphore_signal(sem_id1);
        semaphore_signal(sem_id2);

        sleep(1);
    }
}

void process1(int* shared_memory, int sem_id) 
{
    for (int i = 0; i < 10; i++) {
        semaphore_wait(sem_id);
        std::cout << "Process1: " << *shared_memory << std::endl;
    }
}

void process2(int* shared_memory, int sem_id) {
    std::ofstream file(outputFile);

    for (int i = 0; i < 10; i++) {
        semaphore_wait(sem_id);
        file << "Process2: " << *shared_memory << std::endl;
    }

    file.close();
}

int main() {
    pid_t pid1, pid2;
    int shm_id = shmget(IPC_PRIVATE, SHM_SIZE, IPC_CREAT | 0666);
    int* shared_memory = static_cast<int*>(shmat(shm_id, nullptr, 0));

    int sem_id1 = semget(IPC_PRIVATE, 1, IPC_CREAT | 0666);
    int sem_id2 = semget(IPC_PRIVATE, 1, IPC_CREAT | 0666);

    semun sem_union;
    sem_union.val = 0;
    semctl(sem_id1, 0, SETVAL, sem_union);
    semctl(sem_id2, 0, SETVAL, sem_union);

    pid1 = fork();
    if (pid1 == 0) {
        process1(shared_memory, sem_id1);
        return 0;
    }

    pid2 = fork();
    if (pid2 == 0) {
        process2(shared_memory, sem_id2);
        return 0;
    }

    generate_numbers(shared_memory, sem_id1, sem_id2);

    wait(nullptr);
    wait(nullptr);

    shmdt(shared_memory);
    shmctl(shm_id, IPC_RMID, nullptr);
    semctl(sem_id1, 0, IPC_RMID, sem_union);
    semctl(sem_id2, 0, IPC_RMID, sem_union);

    return 0;
}