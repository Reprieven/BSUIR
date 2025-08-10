#include"Counter.h"
#include"Parser.h"
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <random>    
#include <chrono>

using namespace std;

int main() 
{
    vector<string> test_expr = 
    {
        "(A/\\(!A))",                          
        "((A->B)\\/(!(0->(C\\/((D->(!(A~B)))~1)))))",
        "((A\\/B)/\\((!A)/\\(!B)))",               
        "(!(P->(P->(Q~Q))))",                     
        "((Q\\/R)->((P\\/Q)->(P\\/R)))",           
        "((P/\\Q)~((!P)\\/(!R)))",                 
        "((P\\/(P/\\Q))~(!P))",                    
        "(!((!P)/\\(Q/\\(P\\/R))))",              
        "(!1)",                                   
        "(((!P)->P)->(R\\/Q))"                     
    };
    int answer = 0;
    bool answer_bool;
    bool correct_answer; 
    int result = 0;
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    shuffle(test_expr.begin(), test_expr.end(), mt19937(seed));
    vector<string> counter_expr;
    for(string expr : test_expr)
    {
        counter_expr.push_back(make_lower_case(parse_expression(expr)));
    }
    for (int i = 0; i < test_expr.size(); ++i) 
    {
        cout<<"Является ли формула сокращенного языка логики высказываний невыполнимой"<<endl;
        cout<<test_expr[i]<<endl;
        cout<<"1)Да\n";
        cout<<"2)Нет\n";
        cin>>answer;
        if(answer==1)
            answer_bool = true;
        else if(answer==2)
            answer_bool = false;
        else
            continue;
        correct_answer = isUnsatisfiable(counter_expr[i]);
        if(answer_bool == correct_answer)
            result++;
    }
    cout<<"Оценка за тест:"<<result<<endl;
}