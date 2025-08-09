#include<iostream>
#include<cmath>
using namespace std;
double f(double &x) 
{

	double fx = 7 * pow(sin(x), 2);
	return fx;
}
double schetR(double &a, double &b)
{
	double e = 0.01;
	double c = (a + b) / 2;
	if (b - a < e)
		return c;
	double x1 = schetR(a, c), x2 = schetR(c, b);
	return f(x1) < f(x2) ? x1 : x2;
}
double schet(double a, double b) 
{
	double e = 0.001;
	int k = 1;
	float d = 0.002;
	while (true) 
	{
		double x1 = (a + b - d) / 2;
		double x2 = (a + b + d) / 2;
		if (f(x1) <= f(x2)) 
		{
			b = x1;
		}
		else 
		{
			a = x2;
		}
		e = (b - a - d) / pow(2, k + 1) + d / 2;
			k++;
		if (e < 0.001)
		{
			return (x1 + x2) / 2;
			break;
		}
	}
}

int main() 
{
	double first_value = 2;
	double second_value = 6;
	cout <<"Минимум рекурсивной функции:" << schetR(first_value, second_value) << endl;
	cout <<"Минимум обычной функции:" << schet(first_value, second_value) << endl;
	cout <<"Разность значений:" <<fabs(schetR(first_value, second_value) - schet(first_value, second_value))<< endl;
}