#include<iostream>
#include<ctime>
#include<string>
using namespace std;
struct Product
{
	string name;
	int price;
	string date;
};

void TableAdd(Product prod, int M, Product* HashTable, int* RandomArr)
{
	int i = prod.price % 10;
	if (HashTable[i].price != -1)
	{
		for (int j = 0; HashTable[i].price != -1; j++)
		{
			i += RandomArr[j];
			if (i >= M)
			{
				i = 0;
			}
		}
	}
	HashTable[i] = prod;
}

int TableSearch(int price, int M, Product* HashTable, int* RandomArr)
{
	int i = price % 10;
	for (int j = 0; HashTable[i].price != -1; j++)
	{
		if (HashTable[i].price == price)
		{
			return i;
		}
		i += RandomArr[j];
		if (i >= M)
		{
			i = 0;
		}
	}
	return -1;
}

int main()
{
	srand(time(0));
	bool cycle = true;
	int key = 0, choice = 0, search = -1;
	const int SizeArr = 3;
	const int SizeHash = 10;

	Product list[SizeArr];
	for (int i = 0; i < SizeArr; i++)
	{
		cout << "Введите название " << i + 1 << " товара\n";
		getline(cin, list[i].name);
		cout << "Введите цену " << i + 1 << " товара\n";
		cin >> list[i].price;
		cin.ignore(1000, '\n');
		cout << "Введите день выпуска " << i + 1 << " товара\n";
		getline(cin, list[i].date);
	}

	Product HashTable[SizeHash];
	for (int i = 0; i < SizeHash; i++)
	{
		HashTable[i].price = -1;
	}

	int RandomArr[SizeHash];//???
	for (int i = 0; i < SizeHash; i++)
	{
		RandomArr[i] = rand() % 10;
	}

	for (int i = 0; i < SizeArr; i++)
	{
		TableAdd(list[i], SizeHash, HashTable, RandomArr);
	}

	while (cycle)
	{
		cout << "Найти элемент в таблице по ключу(цена)-1)\n" << "Завершить поиск-2)\n";
		cin >> choice;
		switch (choice)
		{
		case 1:
			cout << "Введите цену товара\n";
			cin >> key;
			cout << "Результат поиска:\n";
			if (key < 0)
			{
				cout << "Некорректная цена товара" << endl;
				break;
			}
			else
			{
				search = TableSearch(key, SizeHash, HashTable, RandomArr);
				if (search == -1)
				{
					cout << "Нет товара с такой ценой\n\n";
					break;
				}
				for (int i = 0; i < SizeArr; i++)
				{

				}
				cout << HashTable[search].name << "\n" << HashTable[search].price << "\n" << HashTable[search].date << "\n\n";
				break;
			}
		case 2:
			cycle = false;
			break;
		}
	}

	cout << "------Искодный массив------" << "\n";
	for (int i = 0; i < SizeArr; i++)
	{
		cout << list[i].name << "\n";
		cout << list[i].price << "\n";
		cout << list[i].date << "\n";
		cout << "\n";
	}
	cout << "------Хеш-таблица------" << "\n";
	for (int i = 0; i < SizeHash; i++)
	{
		if (HashTable[i].price == -1)
		{
			cout << "None" << "\n\n";
		}
		else
		{
			cout << HashTable[i].name << "\n";
			cout << HashTable[i].price << "\n";
			cout << HashTable[i].date << "\n\n";
		}
	}
}