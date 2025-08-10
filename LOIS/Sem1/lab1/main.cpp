/*Лабораторная работа №1
Выполнил студент группы 321701
Климков М. П.
Вариант 3

Главный файл программы содержащий точку входа (функцию main())
19.04.2025
*/

#include"Parser.h"
#include"Validation.h"
#include"Counter.h"
#include<iostream>
#include<string>
#include<chrono>
using namespace std;

int main() 
{
    int choice = 1;
    while(choice==1)
    {
        string expression = "";
        cout << "Введите формулу сокращённого языка логики высказываний:\n";
        cin>>expression;
        auto start = chrono::high_resolution_clock::now();
        bool is_valid_operations_symbols = validate_logic_operations(expression);
        expression = parse_expression(expression);
        if(!is_valid_formula(expression) || !is_valid_operations_symbols)
        {
            cout << "Формула не является формулой сокращенного языка логики высказываний\n";
        }
        else
        {
            expression = make_lower_case(expression);
            if (isUnsatisfiable(expression)) 
            {
                cout << "Формула невыполнима\n";
            }
            else 
            {
                cout << "Формула выполнима\n";
            }
        }
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double>duration = end - start;
        cout<<"Время выполнения программы: "<<duration.count()<<endl;
        cout << "Ввести формулу еще раз:\n";
        cout << "1)Да\n";
        cout<<"2)Нет\n";
        cin>>choice;
    }
}