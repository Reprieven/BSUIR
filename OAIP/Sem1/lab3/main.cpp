#include<iostream>
#include<cmath>
using namespace std;
int factorial(int &r) 
{
	int fact = 1;
	int i = 1;
	if (r == 0)
		return 1;
	else 
	{
		while (i <= r)
		{
			fact = fact * i;
			i++;
		}
		return fact;
	}

}

double Sum(double &x,int &n) 
{
	int k = 0;
	double Sx = 0;
	while (k <= n) 
	{
		Sx = Sx + ((2 * k + 1) * pow(x, 2 * k) / factorial(k));
		k++;
	}
	return Sx;
} 

double FuncY(double &x) 
{
	double Yx = (1 + 2 * x * x) * exp(x * x);
	return Yx;
}


int main() 
{
	int n =0;
	double e,x;
	cout << "Vvedite x,x{0.1,1.5}:";
	cin >> x;
	e = fabs(Sum(x, n) - FuncY(x));
	while (e >=0.001) 
	{
		n++;
		e = fabs(Sum(x, n) - FuncY(x));
	}
	cout <<"n="<< n << endl;
	cout <<"Sx="<< Sum(x, n) << endl;
	cout <<"Yx="<< FuncY(x) << endl;
	cout<<"|Sx-Yx|="<<e << endl;

}