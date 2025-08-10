/*Лабораторная работа №1
Выполнил студент группы 321701
Климков М. П.
Вариант 3

Файл изменяющий введенную строку в строку удобную для обработки
19.04.2025
*/
#include"Parser.h"
#include<iostream>
std::string parse_expression(std::string expr)
{
    for(int i = 0;i<expr.length();i++)
    {
        if(expr[i]=='\\' && expr[i+1]=='/')
        {
            expr.replace(i,2,"|");
        }
        else if(expr[i]=='/' && expr[i+1]=='\\')
        {
            expr.replace(i,2,"&");
        }
        else if(expr[i]=='-' && expr[i+1]=='>')
        {
            expr.replace(i,2,">");
        }
    }
    return expr;
}

std::string make_lower_case(std::string expr)
{
    for(int i = 0;i<expr.length();i++)
    {
        expr[i] = std::tolower(expr[i]);
    }
    return expr;
}