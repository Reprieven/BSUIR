#include <string>
#include <vector>
#include <unordered_set>
#include <unordered_map>  
#include <stack>
using namespace std;
int Prior(char op);
bool applyOp(bool a, bool b, char op) ;
string toReversePolishNotation(const string& expr);
bool evaluateExpression(const string& rpn, const vector<bool>& values, const unordered_set<char>& vars);
bool isUnsatisfiable(const string& expr);