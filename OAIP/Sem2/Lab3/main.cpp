#include<iostream>
#include<ctime>
using namespace std;
struct Stack 
{
	int info;
	Stack* next;
}*start,*inf;

Stack* PushStack(Stack* p, int inf) 
{
	Stack* t = new Stack;
	t->info = inf;
	t->next = p;
	return t;
}

void View(Stack* p) 
{
	Stack* t = p;
	while (t != NULL) 
	{
		cout << " " << t->info << endl;
		t = t->next;
	}
}

void Dell_All(Stack** p)
{
	Stack* t;
	while (*p != NULL) 
	{
		t = *p;
		*p = (*p)->next;
		delete t;
	}
}

int random(int min, int max) 
{
	return rand() % (max - min + 1) + min;
}

int SearchMax(Stack* p) 
{
	int max = p->info;
	Stack* t = p;
	while (t != NULL) 
	{
		if (t->info > max) 
		{
			max = t->info;
		}
		t = t->next;
	}
	return max;
}

int SearchMin(Stack* p) 
{
	int min = p->info;
	Stack* t = p;
	while (t != NULL) 
	{
		if (t->info < min) 
		{
			min = t->info;
		}
		t=t->next;
	}
	return min;
}

void Swap(Stack* p) 
{
	if (p == NULL) return;
	int max = SearchMax(start);
	int min = SearchMin(start);
	for (Stack* t1=p; t1 != NULL; t1 = t1->next) 
	{
		if (t1->info == max)
		{
			for (Stack* t2 = p; t2 != NULL; t2 = t2->next) 
			{
				if (t2->info == min) 
				{
					t1->info = min;
					t2->info = max;
					return;
				}
			}
		}
	}
}

int main() 
{
	setlocale(0, " ");
	int max_rand, min_rand;
	cout << "Введите максимальное возможное случайное значение: ";
	cin >> max_rand;
	cout << "Введите минимальное возможное случайное значение: ";
	cin >> min_rand;
	int inf, n, kod;
	while (true) 
	{
		cout << "\nСоздать-1)\nДобавить-2)\nПросмотреть-3)\nУдалить-4)\nПоменять местами максимальный и минмальный элементы-5)\nВыйти-0):";
		cin >> kod;
		switch (kod) 
		{
		case 1: case 2:
			if (kod == 1 && start != NULL) 
			{
				cout << "Освободите память" << endl;
				break;
			}
			cout << "Ввести количество эелементов ";
			cin >> n;
			for (int i = 1; i <= n; i++) {
				inf = random(min_rand, max_rand);
				start = PushStack(start, inf);
			}
			if (kod == 1)
			{
				cout << "Создался стек на " << n <<" элементов" << endl;
			}
			else
			{
				cout << "Добавлено " << n <<" элементов" << endl;
			}
			break;
		case 3:
			if (!start) 
			{
				cout << "Стек пуст" << endl;
				break;
			}
			cout << "----Стек----" << endl;
			View(start);
			break;
		case 4:
			Dell_All(&start);
			cout << "Память очищена" << endl;
			break;
		case 5:
			if (!start) 
			{
				cout << "Стек пуст" << endl;
				break;
			}
			if (start->next==NULL) {
				cout << "В стеке всего 1 элемент" << endl;
				break;
			}
			Swap(start);
			cout << "Максимальный и минимальный элементы поменялись местами" << endl;
			break;
		case 0:
			if (start != NULL) 
			{
				Dell_All(&start);
			}
			exit(0);
			break;

		}

	}
}