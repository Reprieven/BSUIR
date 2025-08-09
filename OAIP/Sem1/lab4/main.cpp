#include<iostream>
using namespace std;
void FuncSort(double* arr,int &size) 
{
	double Zamena = 0;
	for (int i = 0; i <size ; i++)
	{
		for (int j = 1; j < size; j++)
			if (arr[j-1] >= arr[j]) 
			{
				Zamena = arr[j-1];
				arr[j-1] = arr[j];
				arr[j] = Zamena;
			}
		
	}
}

int main() 
{
	int sizeX,sizeY,sizeZ;
	cout << "Введите размер массива X:";
	cin >> sizeX;
	if (cin.fail()) 
	{
		cout << "Ошибка,нужно ввести числа" << endl;
	}
	double* arrX = new double[sizeX];
	cout << "Введите элементы X:" << endl;
	for (int i = 0; i < sizeX; i++) 
	{
		cin >> arrX[i];
	}
	if (cin.fail()) 
	{
		cout << "Ошибка,нужно ввести числа" << endl;
	}
	FuncSort(arrX,sizeX);
	cout << "Введите размер массива Y:";
	cin >> sizeY;
	if (cin.fail()) 
	{
		cout << "Ошибка,нужно ввести числа" << endl;
	}
	double* arrY = new double[sizeY];
	cout << "Введите элементы Y:" << endl;
	for (int i = 0; i < sizeY; i++) 
	{
		cin >> arrY[i];
	}
	if (cin.fail()) 
	{
		cout << "Ошибка,нужно ввести числа" << endl;
	}
	FuncSort(arrY,sizeY);
	sizeZ = sizeX + sizeY;
	double* arrZ = new double[sizeZ];
	for (int i=0; i < (sizeZ - sizeX); i++) 
	{
		arrZ[i] = arrY[i];
	}
	for (int i=0; i < (sizeZ - sizeY); i++) 
	{
		arrZ[i+sizeY] = arrX[i];
	}
	FuncSort(arrZ,sizeZ);
	cout << "Массив Z:";
	for(int i=0; i<sizeZ; i++) 
	{
		cout << arrZ[i] << ",";
	}
	delete[] arrX;
	delete[]arrY;
	delete[]arrZ;
}
