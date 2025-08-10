#include<iostream>
#include<fstream>
#include<string>
#include<vector>
using namespace std;

struct Student
{
	string FIO;
	string group;
	string address;
	vector<int>marks;
};

//функция подсчета среднего балла за экзамены 
double CountAverage(const vector<int>& marks)
{
	double sum = 0;
	for (int i = 0; i < marks.size(); i++)
	{
		sum += marks[i];
	}
	return sum / marks.size();
}

//функция изменения значений
void Swap(Student& one, Student& two)
{
	Student buf = one;
	one = two;
	two = buf;
}

void heapfy(vector<Student>& students, int size, int i)
{
	int largest = i;
	int left = 2 * i + 1;
	int right = 2 * i + 2;

	if (left<size && students[left].FIO>students[largest].FIO)
	{
		largest = left;
	}

	if (right<size && students[right].FIO>students[largest].FIO)
	{
		largest = right;
	}

	if (largest != i)
	{
		Swap(students[i], students[largest]);
		heapfy(students, size, largest);
	}

}

int Separation(vector<Student>& students, int low, int high, string pivot)
{
	int i = low;
	int j = low;
	while (i <= high)
	{
		if (students[i].FIO > pivot)
		{
			i++;
		}
		else
		{
			Swap(students[i], students[j]);
			i++;
			j++;
		}
	}
	return j - 1;
}

//функция добавления элемента в список
void InFile()
{
	bool cycle = true;
	ofstream fin("Students.txt", ios_base::app);
	Student student;
	if (!fin.is_open())
	{
		cout << "Не удалось открыть файл" << endl;
		return;
	}
	int marks_count = 0;
	int mark;
	cout << "Введите ФИО (Фамилия Имя Отчество) студента" << endl;
	cin.ignore(1000, '\n');
	getline(cin, student.FIO);
	cout << "Введите группу студента" << endl;
	cin >> student.group;
	cout << "Введите адрес проживания студента" << endl;
	cin.ignore(1000, '\n');
	getline(cin, student.address);
	cout << "Введите количество оценок за экзамены" << endl;
	cin >> marks_count;
	cout << "Введите оценки за экзамены" << endl;
	for (int j = 0; j < marks_count; j++)
	{
		cin >> mark;
		student.marks.push_back(mark);
	}

	fin << student.FIO << "\n" << student.group << "\n" << student.address << "\n";
	for (int l = 0; l < marks_count; l++)
	{
		fin << student.marks[l] << " ";
	}
	fin << "\n";
	cout << endl;
	fin.close();
}

//функция считывания элементов из списка 
void OutFile(vector<Student>& studentOutput)
{
	studentOutput.clear();
	ifstream fout("Students.txt");
	if (!fout.is_open())
	{
		cout << "Не удалось открыть файл или файла не существует" << endl;
		return;
	}
	while (fout.peek() != '\n' && !fout.eof())
	{
		Student student;
		getline(fout, student.FIO);
		getline(fout, student.group);
		getline(fout, student.address);
		int mark;
		while (fout >> mark)
		{
			student.marks.push_back(mark);
		}
		fout.clear();
		studentOutput.push_back(student);
	}
	fout.close();

}

//функция изменения информации об элементе в списке 
void Update(vector<Student>& students)
{
	bool cycle = true;
	int choice = -1;
	int pos = -1;
	cout << "Введите номер абитуриента в списке, информацию о котором хотите изменить ";
	cin >> pos;
	cout << endl;
	while (cycle)
	{
		if (pos <= 0)
		{
			cin.clear();
			cin.ignore(1000, '\n');
			cout << "Некоректное значение выбора студента\n";
			cout << "Введите номер абитуриента в списке, информацию о котором хотите изменить ";
			cin >> pos;
		}
		else
		{
			cout << "Выберете что хотите изменить:" << endl;
			cout << "ФИО(Фамилия Имя Отчество)-1)\nГруппу-2)\nАдрес-3)\nОценки-4)\nЗавершить изменение-5)\n";
			cin >> choice;
			switch (choice)
			{
			case 1:
				cout << "Введите новое ФИО\n";
				cin.ignore(1000, '\n');
				getline(cin, students[pos - 1].FIO);
				break;
			case 2:
				cout << "Введите новую группу\n";
				cin.ignore(1000,'\n');
				getline(cin, students[pos - 1].group);
				break;
			case 3:
				cout << "Введите новый адрес\n";
				cin.ignore(1000, '\n');
				getline(cin, students[pos - 1].group);
				break;
			case 4:
				cout << "Введите новые оценки за экзамены\n";
				for (int i = 0; i < students[pos - 1].marks.size(); i++)
				{
					cin >> students[pos - 1].marks[i];
				}
				break;
			case 5:
				cycle = false;
				break;
			}

			ofstream fin("Students.txt");
			if (!fin.is_open())
			{
				cout << "Не удалось открыть файл" << endl;
				return;
			}
			for (int i = 0; i < students.size(); i++)
			{
				fin << students[i].FIO << "\n" << students[i].group << "\n" << students[i].address << "\n";
				for (int j = 0; j < students[i].marks.size(); j++)
				{
					fin << students[i].marks[j] << " ";
				}
				fin << "\n";
			}
			fin.close();
		}
	}
}

//удаление элемента из списка
void Delete(vector<Student>& students)
{
	int pos;
	bool cycle = true;
	int choice = -1;
		cout << "Введите номер абитуриента в списке, информацию о котором хотите удалить: ";
		cin >> pos;
		cout << endl;
		students.erase(students.begin() + (pos-1));
	ofstream fin("Students.txt");
	if (!fin.is_open())
	{
		cout << "Не удалось открыть файл для удаления" << endl;
		return;
	}
	for (int i = 0; i < students.size(); i++)
	{
		fin << students[i].FIO << "\n" << students[i].group << "\n" << students[i].address << "\n";
		for (int j = 0; j < students[i].marks.size(); j++)
		{
			fin << students[i].marks[j] << " ";
		}
		fin << "\n";
	}
	fin.close();
}

//просмотр списка
void View(vector<Student>& students)
{
	int maxFIO = 30;
	int maxAddress = 45;
	int maxGroup = 10;
	int count_space = 0;
	cout << "-----Список-----" << endl;
	for (int i = 0; i < students.size(); i++)
	{
		cout << students[i].FIO;
		for (int j = 0; j < maxFIO - ((students[i].FIO.length() - 2) / 2+2);j++) 
		{
			cout << " ";
		}

		cout << students[i].group;
		for (int j = 0; j < maxGroup - students[i].group.length(); j++) 
		{
			cout << " ";
		}

		cout << students[i].address;
		count_space = 0;

		for (int j = 0; j < students[i].address.length(); j++)
		{
			if (students[i].address[j] == ' ' || students[i].address[j] == '.'||(students[i].address[j]>='0'&& students[i].address[j]<='9'))
			{
				count_space++;
			}
		}

		for (int j = 0; j < maxAddress - ((students[i].address.length() - count_space) / 2+count_space); j++) 
		{
			cout << " ";
		}

		for (int j = 0; j < students[i].marks.size(); j++) 
		{
			cout << students[i].marks[j] << " ";
		}
		cout <<"\n\n";
	}
}

//линейный поиск
void LinSearch(vector<Student>& students)
{
	ofstream fin("Result.txt");
	if (!fin.is_open())
	{
		cout << "Не удалось открыть файл" << endl;
		return;
	}
	for (int i = 0; i < students.size(); i++)
	{
		if (CountAverage(students[i].marks) >= 8.5 && students[i].address.find("Минск ") != students[i].address.npos)
		{
			fin << students[i].FIO << "\n";
			cout << students[i].FIO << "\n";
		}
	}
	fin.close();
}

//бинарный поиск
void BinSearch(vector<Student>& students)
{
	ofstream fin("Result.txt");
	if (!fin.is_open())
	{
		cout << "Не удалось открыть файл" << endl;
		return;
	}
	int low = 0;
	int high = students.size() - 1;
	for (int i = 0; i < students.size(); i++)
	{
		Student lfor;
		if (CountAverage(students[i].marks) >= 8.5 && students[i].address.find("Минск ") != students[i].address.npos)
		{
			lfor = students[i];
		}
		while (low <= high)
		{
			int mid = (low + high) / 2;
			string guess = students[mid].FIO;
			if (guess == lfor.FIO)
			{
				fin << students[mid].FIO << "\n";
				cout << students[mid].FIO << "\n";
				break;
			}
			else if (guess > lfor.FIO)
			{
				high = mid - 1;
			}
			else
			{
				low = mid + 1;
			}
		}
		low = 0;
		high = students.size() - 1;

	}
	fin.close();
}

void BubbleSort(vector<Student>& students)
{
	Student bus;
	for (int i = 0; i < students.size() - 1; i++)
	{
		for (int j = i + 1; j < students.size(); j++)
		{
			if (students[i].FIO < students[j].FIO)
			{
				Swap(students[i], students[j]);
			}
		}
	}
}

void HeapSort(vector<Student>& students)
{
	int size = students.size();
	for (int i = size / 2 - 1; i >= 0; i--)
	{
		heapfy(students, size, i);
	}
	for (int i = size - 1; i >= 0; i--)
	{
		Swap(students[0], students[i]);

		heapfy(students, i, 0);
	}
}

void QuickSort(vector<Student>& students, int low, int high)
{
	if (low < high)
	{
		string pivot = students[high].FIO;
		int pos = Separation(students, low, high, pivot);

		QuickSort(students, low, pos - 1);
		QuickSort(students, pos + 1, high);
	}
}

int main()
{
	bool sorted = false;
	int choice = -1;
	bool cycle = true;
	vector<Student>studentOutput;
	OutFile(studentOutput);
	if (studentOutput.size() == 0)
	{
		cout << "Файл пуст" << endl;
	}
	else
	{
		cout << "Файл получен" << endl;
	}
	while (cycle)
	{
		cout << "1)Изменить информацию об абитуриентах в списке\n2)Удалить абитуриента из списка\n3)Добавить абитуриента в список\n";
		cout << "4)Посмотреть список\n5)Отсортировать список в обратном алфавитном порядке методом BubbleSort\n";
		cout << "6)Отсортировать список в алфавитном порядке методом HeapSort\n";
		cout << "7)Отсортировать список в алфавитном порядке методом QuickSort\n";
		cout << "8)Найти и вывести в файл Result.txt всех абитуриентов, проживающих в г.Минске и имеющих средний балл не меньше 8.5 методом линейного поиска\n";
		cout << "9)Найти и вывести в файл Result.txt всех абитуриентов, проживающих в г. Минске и имеющих средний балл не меньше 8.5 методом бинарного поиска\n";
		cout << "10)Выйти\n";
		cin >> choice;
		switch (choice)
		{
		case 1:
			Update(studentOutput);
			break;
		case 2:
			Delete(studentOutput);
			break;
		case 3:
			InFile();
			OutFile(studentOutput);
			break;
		case 4:
			View(studentOutput);
			break;
		case 5:
			BubbleSort(studentOutput);
			View(studentOutput);
			sorted = false;
			break;
		case 6:
			HeapSort(studentOutput);
			View(studentOutput);
			sorted = true;
			break;
		case 7:
			QuickSort(studentOutput,0,studentOutput.size()-1);
			View(studentOutput);
			sorted = true;
			break;
		case 8:
			if (!sorted)
			{
				cout << "Список не отсортирован. Для получения корректного результата отсортируйте список" << endl;
				break;
			}
			else
			{
				LinSearch(studentOutput);
				cout << "В файл Result.txt добавлены ФИО абитуриентов" << endl;
				break;
			}
		case 9:
			if (!sorted)
			{
				cout << "Список не отсортирован. Для получения корректного результата отсортируйте список" << endl;
				break;
			}
			else
			{
				BinSearch(studentOutput);
				cout << "В файл Result.txt добавлены ФИО абитуриентов" << endl;
				break;
			}
		case 10:
			cycle = false;
			break;
		}
	}
}