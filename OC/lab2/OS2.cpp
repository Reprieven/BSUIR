#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <vector>

using namespace std;

void printProcessInfo(const std::string& message) 
{
    pid_t pid = getpid();
    pid_t ppid = getppid();
    cout << message << " (PID: " << pid << ", PID родителя: " << ppid << ")" << endl;
}

int main() 
{
    vector<int> tree = {0, 0, 1, 2, 2, 3, 4, 6};

    pid_t pids[tree.size()];
    printProcessInfo("Основной процесс запущен");

    for (size_t i = 0; i < tree.size(); ++i) 
    {
        if (i == 0 || pids[tree[i]] == getpid()) 
        {
            pid_t pid = fork();
            if (pid == 0) 
            {
                printProcessInfo("Дочерний процесс " + std::to_string(i) + " запущен");

                pids[i] = getpid();
            } 
            else if (pid > 0) 
            {
                pids[i] = pid;
                wait(NULL);
            }
        }
    }

    if (pids[2] == getpid()) 
    {
        std::cout << "Процесс 2 выполняет команду ps:" << std::endl;
        execlp("ps", "ps", (char *)0);
        _exit(0);
    }

    printProcessInfo("Основной процесс завершает работу");
    return 0;
}