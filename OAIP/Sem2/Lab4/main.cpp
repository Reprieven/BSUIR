#include<iostream>
#include<ctime>
using namespace std;
struct BiList 
{
	int info;
	BiList* next, * prev;
}*start,*finish,*t;

int Random(int max, int min) 
{
	return rand() % (max - min + 1) + min;
}

int FindMax() 
{
	BiList* t = start;
	int max = t->info;
	while (t != NULL) 
	{
		if (t->info > max) 
		{
			max = t->info;
		}
		t=t->next;
	}
	return max;
}

int FindMin()
{
	BiList* t = start;
	int min = t->info;
	while (t != NULL)
	{
		if (t->info < min)
		{
			min = t->info;
		}
		t = t->next;
	}
	return min;
}

void Swap() 
{
	int max = FindMax();
	int min = FindMin();
	for (BiList* t1 = start; t1 != NULL; t1 = t1->next) 
	{
		if (t1->info == max) 
		{
			for (BiList* t2 = start; t2 != NULL; t2 = t2->next) 
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

void Create_List(BiList** start, BiList** fin, int inf) 
{
    t = new BiList;
	t->info = inf;
	t->next = t->prev = NULL;
	*start = *fin = t;
}

void Add_List(int kod, BiList** start, BiList** fin, int inf) 
{
	t = new BiList;
	t->info = inf;
	if (kod == 0) 
	{
		t->prev = NULL;
		t->next = *start;
		(*start)->prev = t;
		*start = t;
	}
	else 
	{
		t->next = NULL;
		t->prev = *fin;
		(*fin)->next = t;
		*fin = t;
	}
}

void View_BiList(int kod, BiList* t) 
{
	cout << "Список:" << "\n";
	while(t!=NULL)
	{
		cout << t->info << endl;
		if (kod == 0) 
		{
			t = t->next;
		}
		else 
		{
			t = t->prev;
		}
	}
}

void Del_All(BiList** p) 
{
	while (p != NULL) 
	{
	 t = *p;
	 *p = (*p)->next;
	 delete t;
	}
}

int main() 
{
	srand(time(0));
	int max_rand, min_rand;
	cout << "Введите максимальное возможное случайное значение: ";
	cin >> max_rand;
	cout << "Введите минимальное возможное случайное значение: ";
	cin >> min_rand;
	int selection, kod;
	while (true) 
	{
		cout << "\nСоздать-1)\nДобавить-2)\nПросмотреть-3)\nУдалить-4)\nПоменять местами максимальный и минмальный элементы-5)\nВыйти-0):";
		cin >> selection;
		switch (selection) {
		case 1:
			if (start != NULL)
			{
				cout << "Список уже существует, очистите память" << "\n";
				break;
			}
			Create_List(&start, &finish, Random(max_rand, min_rand));
			cout << "Первый элемент списка со значением " << start->info << " создан" << endl;
			break;
		case 2:
			cout << "Добавить в конец списка-0)\nДобавить в начало списка-1)\n";
			cin >> kod;
			Add_List(kod, &start, &finish, Random(max_rand, min_rand));
			if (kod == 0) 
			{
				t = start;
			}
			else 
			{
				t = finish;
			}
			cout << "Элемент " << t->info << " добавлен в список" << "\n";
			break;
		case 3:
			if (start == NULL) 
			{
				cout << "В списке нет элементов" << "\n";
				break;
			}
			cout << "Просмотр списка с конца-0)\nПросмотр списка с начала-1)\n";
			cin >> kod;
			if (kod == 0) 
			{
				t =start;
			}
			else 
			{
				t = finish;
			}
			View_BiList(kod, t);
			break;
		case 4:
			Del_All(&start);
			cout << "Память очищена" << "\n";
			break;
		case 5:
			if (start==NULL)
			{
				cout << "Список пуст" << "\n";
				break;
			}
			if (start->next == NULL) 
			{
				cout << "В списке всего 1 элемент" << "\n";
				break;
			}
			Swap();
			cout << "Максимальный и минимальный элемент поменялись местами" << "\n";
			break;
		case 0:
			if (start != NULL) 
			{
				Del_All(&start);
			}
			return 0;
		}
	}
}
