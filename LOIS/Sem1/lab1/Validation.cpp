/*Лабораторная работа №1
Выполнил студент группы 321701
Климков М. П.
Вариант 3

Файл проверяющий является ли введенная строка формулой 
сокращенного языка логики выссказываний 
19.04.2025*/

#include"Validation.h"
#include<iostream>
#include<set>
using namespace std;
int count_operations_num(std::string expr)
{
    int operations_num = 0;
    for (int i = 0; i < expr.length(); i++)
    {
        if (expr[i] == '&' || expr[i] == '|' || 
            expr[i] == '!' || expr[i] == '>' || 
            expr[i] == '~')
        {
            operations_num++;
        }
    }
    return operations_num;
}

bool validate_logic_operations(std::string expr)
{
    for (int i = 0; i < expr.length(); i++)
    {
        if (expr[i] == '>' && i != 0 && expr[i - 1] != '-')
        {
            return false;
        }
        else if (expr[i] == '&' || expr[i] == '|')
        {
            return false;
        }
    }
    return true;
}

int count_brackets_num(std::string expr)
{
    int brackets_num = 0;
    for (int i = 0; i < expr.length(); i++)
    {
        if (expr[i] == '(' || expr[i] == ')')
        {
            brackets_num++;
        }
    }
    return brackets_num;
}

int count_formulas(std::string expr)
{
    int formulas_num = 0;
    for (int i = 0; i < expr.length(); i++)
    {
        if (isalpha(expr[i]) || expr[i] == '1' || expr[i] == '0')
        {
            formulas_num++;
        }
    }
    return formulas_num;
}

bool check_extra_symbols(std::string expr)
{
    std::string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ10&|!>~()";
    for (int i = 0; i < expr.length(); i++)
    {
        if (alphabet.find(expr[i]) == std::string::npos)
        {
            return false;
        }
    }
    return true;
}

bool check_brackets(std::string expr)
{
    if (count_brackets_num(expr) != (count_operations_num(expr) * 2))
    {
        return false;
    }
    int brackets_depth = 0;
    for (int i = 0; i < expr.length(); i++)
    {
        if (expr[i] == '(')
            brackets_depth++;

        else if (expr[i] == ')')
            brackets_depth--;

        if (brackets_depth < 0)
        {
            return false;
        }
    }
    return brackets_depth==0;
}


bool check_operations_structure(std::string expr)
{
    if ((count_formulas(expr)-1) > count_operations_num(expr))
    {
        return false;
    }
    for (int i = 0; i < expr.size(); ++i)
    {
        if (expr[i] == '!') 
        {
            if (i + 1 >= expr.size() || !(isalpha(expr[i+1]) || expr[i+1] == '('||expr[i+1]=='1'||expr[i+1]=='0')) 
            {
                return false;
            }
        } 
        else if (expr[i] == '&' || expr[i] == '|' || expr[i] == '>' || expr[i] == '~') 
        {
            if (i == 0 || i + 1 >= expr.size() || 
            !(isalpha(expr[i-1]) || expr[i-1] == ')' || expr[i-1]=='1'||expr[i-1]=='0') ||
            !(isalpha(expr[i+1]) || expr[i+1] == '(' || expr[i+1]=='1'||expr[i+1]=='0'))
            {
                return false;
            }
        }
    }
    return true;
}

bool is_valid_subformula(std::string expr)
{   
    return check_operations_structure(expr)&& check_brackets(expr);
}

bool is_valid_formula(std::string expr)
{   
    if(!is_valid_subformula(expr) || !check_extra_symbols(expr))
    {
        return false;
    }
    for(int i = 0;i<expr.length();i++)
    {
        if(expr[i]=='(')
        {
            int brackets_depth = 0;
            std::string subformula = "";
            for(int j = i;j<expr.length();j++)
            {
                if(expr[j]=='(')
                    brackets_depth++;
                else if(expr[j]==')')
                    brackets_depth--;
                subformula+=expr[j];
                if(brackets_depth==0)
                    break;
            }
            if(!is_valid_subformula(subformula))
            {
                return false;
            }
        }
    }
    return true;
}
