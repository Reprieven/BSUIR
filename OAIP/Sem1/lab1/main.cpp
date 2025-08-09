#include<iostream>
#include<cmath> 
using namespace std;
int main()
{
	double B, x, z, y;
	    cout << "Введите x:" << endl;
	    cin >> x;
		cout << "Введите y:" << endl;
		cin >> y;
		cout << "Введите z:" << endl;
		cin >> z;

		if ((10 * (cbrt(x) + pow(x, y + 2))) < 0) 
		{
			cout << "Error-negative number under the root,try again!" << endl;
		}

		else if (z > 1 || z < -1) 
		{
			cout << "Error-wrong z!" << endl;
		}

		else 
		{
			B = sqrt(10 * (cbrt(x) + pow(x, y + 2))) * (pow(asin(z), 2) - fabs(x - y));
			cout << "B=" << B << endl;
		}
}

