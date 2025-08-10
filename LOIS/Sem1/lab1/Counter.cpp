/*Лабораторная работа №1
Выполнил студент группы 321701
Климков М. П.
Вариант 3

Файл выполняющий интерпретацию формулы языка логики выссказываний
19.04.2025*/

#include"Counter.h"
int Prior(char op) {
    switch (op) {
        case '!': return 5;
        case '&': return 4;
        case '|': return 3;
        case '>': return 2;
        case '~': return 1;
        case '(': return 0;
        default: return -1;
    }
}

bool applyOp(bool a, bool b, char op) {
    switch (op) {
        case '&': return a && b;
        case '|': return a || b;
        case '>': return !a || b;
        case '~': return a == b;
        default: return false;
    }
}

string toReversePolishNotation(const string& expr) {
    stack<char> opStack;
    string output;
    int length = expr.length();

    for (int i = 0; i < length; i++) {
        char ch = expr[i];
        if (isalpha(ch) || ch == '0' || ch == '1') {
            output += ch;
        } else if (ch == '(') {
            opStack.push(ch);
        } else if (ch == ')') {
            while (!opStack.empty() && opStack.top() != '(') {
                output += opStack.top();
                opStack.pop();
            }
            if (!opStack.empty()) opStack.pop();
        } else if (Prior(ch) != -1) {
            while (!opStack.empty() && Prior(opStack.top()) >= Prior(ch)) {
                output += opStack.top();
                opStack.pop();
            }
            opStack.push(ch);
        }
    }

    while (!opStack.empty()) {
        output += opStack.top();
        opStack.pop();
    }

    return output;
}

bool evaluateExpression(const string& rpn, const vector<bool>& values, const unordered_set<char>& vars) {
    stack<bool> evalStack;
    unordered_map<char, bool> varValues;
    int rpnLength = rpn.length();
    int varIndex = 0;

    for (char var = 'a'; var <= 'z'; var++) {
        if (vars.count(var)) {
            varValues[var] = values[varIndex];
            varIndex++;
        }
    }
    varValues['0'] = false;
    varValues['1'] = true;

    for (int i = 0; i < rpnLength; i++) {
        char ch = rpn[i];
        if (isalpha(ch) || ch == '0' || ch == '1') {
            evalStack.push(varValues[ch]);
        } else if (ch == '!') {
            bool val = evalStack.top();
            evalStack.pop();
            evalStack.push(!val);
        } else {
            bool b = evalStack.top(); evalStack.pop();
            bool a = evalStack.top(); evalStack.pop();
            evalStack.push(applyOp(a, b, ch));
        }
    }

    return evalStack.top();
}

bool isUnsatisfiable(const string& expr) {
    unordered_set<char> variables;
    int exprLength = expr.length();

    for (int i = 0; i < exprLength; i++) {
        char ch = expr[i];
        if (isalpha(ch)) variables.insert(ch);
    }

    string rpn = toReversePolishNotation(expr);
    int varCount = variables.size();

    for (int i = 0; i < (1 << varCount); i++) {
        vector<bool> values;
        for (int j = 0; j < varCount; j++) {
            values.push_back((i >> (varCount - 1 - j)) & 1);
        }

        if (evaluateExpression(rpn, values, variables)) {
            return false;
        }
    }

    return true;
}

