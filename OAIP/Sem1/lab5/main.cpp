#include<iostream>
using namespace std;
double funcSchet(double** arr, int rows) 
{
	int cols = rows;
	int indCol = 0, indRow = 0;
	double multipl = 0;
	double min = arr[0][0];
	for (int i=0; i < rows; i++) 
	{
		for (int j=0; j < cols; j++) 
		{
			if (arr[i][j] < min) 
			{
				min = arr[i][j];
				indCol = j;
			}
		}
	}
    double max = arr[0][0];
	for (int i=0; i < rows; i++) 
	{
		for (int j=0; j < cols; j++) 
		{
			if (arr[i][j] > max) 
			{
				max = arr[i][j];
				indRow = i;
			}
		}
	}
	for (int i = 0,j = 0; i < rows; i++, j++) 
	{
		multipl += arr[i][indCol] * arr[indRow][j];

	}
	return multipl;


}
int main() {
	int rows, cols;
	cout << "Введите размер матрицы:" << endl;
	cin >> rows;
	cols = rows;
	double** arr = new double* [rows];
	for (int i = 0; i < rows; i++) 
	{
		arr[i] = new double[cols];
	}
	if (cin.fail()) 
	{
		cout << "Ошибка,введите цифры" << endl;
	}
	else 
	{
		cout << "Введите элементы матрицы:" << endl;
		for (int i = 0; i < rows; i++) 
		{
			for (int j = 0; j < cols; j++) 
			{
				cin >> arr[i][j];
			}
		}
		if (cin.fail()) 
		{
			cout << "Ошибка,введите цифры" << endl;
		}
		else 
		{
			cout << "Скалярное произведение=" << funcSchet(arr, rows) << endl;
		}
	}
	for (int i = 0; i < rows; i++)
		delete[] arr[i];
	delete[]arr;
}