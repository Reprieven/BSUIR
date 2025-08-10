#include<iostream>
#include<string>
using namespace std;

struct Customer
{
	string FIO;
	int purch_num;
};

struct Node
{
	Customer info;
	int height;
	Node* left, * right;
	Node(int i, string Name)
	{
		info.FIO = Name;
		info.purch_num = i;
		left = right = 0;
		height = 1;
	}
};


int Height(Node* p)
{
	if (p != nullptr)
	{
		return p->height;
	}
	else return 0;
}

int BalanceFactor(Node* p)
{
	return Height(p->right) - Height(p->left);
}

void FixHeight(Node* p)
{
	int hl = Height(p->left);
	int hr = Height(p->right);
	if (hl > hr)
	{
		p->height = hl + 1;
	}
	else
	{
		p->height = hr + 1;
	}
}

Node* RotateRight(Node* p)
{
	Node* q = p->left;
	p->left = q->right;
	q->right = p;
	FixHeight(p);
	FixHeight(q);
	return q;
}

Node* RotateLeft(Node* q)
{
	Node* p = q->right;
	q->right = p->left;
	p->left = q;
	FixHeight(q);
	FixHeight(p);
	return p;
}

Node* Balance(Node* p)
{
	FixHeight(p);
	if (BalanceFactor(p) == 2)
	{
		if (BalanceFactor(p->right) < 0)
		{
			p->right = RotateRight(p->right);
		}
		return RotateLeft(p);
	}
	if (BalanceFactor(p) == -2)
	{
		if (BalanceFactor(p->left) > 0)
		{
			p->left = RotateLeft(p->left);
		}
		return RotateRight(p);
	}
	return p;
}

Node* Add_Key(Node* p, int key, string FIO)
{
	if (p == nullptr)
	{
		return new Node(key, FIO);
	}
	if (key < p->info.purch_num)
	{
		p->left = Add_Key(p->left, key, FIO);
	}
	else
	{
		p->right = Add_Key(p->right, key, FIO);
	}
	return Balance(p);
}

Node* FindMin(Node* p)
{
	if (p->left != nullptr)
	{
		return FindMin(p->left);
	}
	else return p;
}

Node* RemoveMin(Node* p)
{
	if (p->left == nullptr)
	{
		return p->right;
	}
	p->left = RemoveMin(p->left);
	return Balance(p);
}

Node* Remove(Node* p, int key)
{
	if (p == nullptr) return 0;
	if (key < p->info.purch_num)
	{
		p->left = Remove(p->left, key);
	}
	else if (key > p->info.purch_num)
	{
		p->right = Remove(p->right, key);
	}
	else
	{
		Node* q = p->left;
		Node* t = p->right;
		delete p;
		if (t == nullptr)
		{
			return q;
		}
		Node* min = FindMin(t);
		min->right = RemoveMin(t);
		min->left = q;
		return Balance(min);
	}
	return Balance(p);
}

void  ViewUp(Node* p)
{
	if (p == nullptr)
	{
		return;
	}
	else
	{
		ViewUp(p->left);
		cout << p->info.purch_num << " ";
		ViewUp(p->right);
	}
}

void ViewReverse(Node* p) 
{
	if (p == nullptr) 
	{
		return;
	}
	else 
	{
		ViewReverse(p->left);
		ViewReverse(p->right);
		cout << p->info.purch_num << " ";
	}
}

void ViewStraight(Node* p) 
{
	if (p == nullptr) 
	{
		return;
	}
	else
	{
		cout << p->info.purch_num << " ";
		ViewStraight(p->left);
		ViewStraight(p->right);
	}
}


void Search(Node* p, int key)
{
	if (p == nullptr)
	{
		cout << "Такого элемента нет\n";
		return;
	}
	else if (key == p->info.purch_num)
	{
		cout << p->info.FIO << '\n';
		cout << p->info.purch_num << '\n';
	}
	else if (key > p->info.purch_num)
	{
		Search(p->right, key);
	}
	else
	{
		Search(p->left, key);
	}
}

void LeftMaxRemove(Node* p)
{
	Node* max = p->left;
	Node* t = p->left;
	int key_max = p->left->info.purch_num;
	if (t == nullptr)
	{
		cout << "В левой ветви нет элементов\n";
		return;
	}
	while (t->right != nullptr)
	{
		max = t->right;
		key_max = t->right->info.purch_num;
		t = t->right;
	}
	while (max->left != nullptr)
	{
		Remove(p, max->left->info.purch_num);
	}
	Remove(p, key_max);
}

int main()
{
	int size, choice = -1,view_choice=-1;
	int key;
	bool cycle = true;
	string add_FIO;
	Node* root = NULL;
	cout << "Введите количество покупателей: ";
	cin >> size;
	cout << '\n';
	Customer* list = new Customer[size];
	for (int i = 0; i < size; i++)
	{
		cin.ignore(1000, '\n');
		cout << "Введите ФИО (Фамилию Имя Отчество) " << i + 1 << " покупателя\n";
		getline(cin, list[i].FIO);
		cout << "Введите номер покупки " << i + 1 << " покупателя\n";
		cin >> list[i].purch_num;
	}
	for (int i = 0; i < size; i++)
	{
		root = Add_Key(root, list[i].purch_num, list[i].FIO);
	}
	while (cycle)
	{
		cout << "Просмотреть дерево-1)\nУдалить элемент из дерева по ключу-2)\nНайти элемент по ключу-3)\n";
		cout << "Добавить элемент в дерево - 4)\nУдалить из левой ветви дерева узел с максимальным значением ключа-5)\nВыйти - 6)\n";
		cin >> choice;
		switch (choice)
		{
		case 1:
			cout << "Выберете способ обхода дерева:\nПрямой-1)\nОбратный-2)\nВ порядке возрастания ключа-3)\n";
			cin >> view_choice;
			
			switch (view_choice) 
			{
			case 1:
				cout << "-----Дерево-----\n";
				ViewStraight(root);
				cout << '\n';
				break;
			case 2:
				cout << "-----Дерево-----\n";
				ViewReverse(root);
				cout << '\n';
				break;
			case 3:
				cout << "-----Дерево-----\n";
				ViewUp(root);
				cout << '\n';
				break;
			default:
				cout << "Неверное введенное значение\n";
				break;
			}
			break;
		case 2:
			cout << "Введите ключ элемента\n";
			cin >> key;
			root=Remove(root, key);///
			cout << "Элемент удален из дерева\n\n";
			break;
		case 3:
			cout << "Введите ключ элемента для поиска\n";
			cin >> key;
			cout << "Результат поиска:\n";
			Search(root, key);
			cout << '\n';
			break;
		case 4:
			cin.ignore(1000, '\n');
			cout << "Введите ФИО(Фамилию Имя Отчество) покупателя\n";
			getline(cin, add_FIO);
			cout << "Введите номер покупки\n";
			cin >> key;
			root=Add_Key(root, key, add_FIO);
			break;
		case 5:
			LeftMaxRemove(root);
			break;
		case 6:
			cycle = false;
			break;
		default:
			cout << "Некоректный ввод, введите значение от 1 до 5\n";
			break;
		}
	}
	delete[]list;
}