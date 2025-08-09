#include<iostream>
#include<cmath>
using namespace std;

double min(double &x, double &y) 
{
	return (x < y)? x : y;
}

double max(double& x, double& y) 
{
	return (x > y)? x : y;
}
int main() {
	double x, y, z;
	cout << "Введите x:" << endl;
	cin >> x;
	cout<<"Введите y:" << endl;
	cin >> y;
    cout<<"Введите z:" << endl;
	cin >> z;
	if (max(min(y, z), min(x, y)) == 0) 
	{
		cout << "0 в знаменателе, введите другие числа";
	}
	else 
	{
		cout << "m=" << min(y, z) / max(min(y, z), min(x, y)) << endl;
	}

}