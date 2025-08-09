#include<iostream>
#include<cstring>
using namespace std;
void sort(char line[], int length) 
{
	for (int i = 4; i < 15 && i < length; i++) 
	{
		cout << line[i];
	}
	cout << endl;
	for (int i = length - 1; i >= 0; i--)
	{
		if (line[i] == ' ') 
		{
			for (int j = i + 1; j < length; j++) 
			{
				cout << line[j];
			}
			cout<<endl;
			break;

		}
	}
}
int main() {
	const int MAXL = 1000;
	char line[MAXL];
	cout << "Введите строку(Максимум 1000 элементов):" << endl;
	cin.getline(line, MAXL);
	int length = strlen(line);
	if (length < 15) 
	{
		cout << "Ошибка,слишком мало символов в строке" << endl;
	}
	else 
	{
		sort(line, length);
	}

}
