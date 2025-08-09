#include<iostream>
#include<fstream>
#include<string>
using namespace std;
string shifr(string &line) 
{
	string subline1 = "си", subline2 = "ли", subline3 = "ти";
	string zamline1 = "иис", zamline2 = "иил", zamline3 = "иит";
	size_t pos;
	while ((pos = line.find(subline1)) != string::npos) 
	{
		line.replace(pos, 4, zamline1);
	}
	while ((pos = line.find(subline2)) != string::npos) 
	{
		line.replace(pos, 4, zamline2);
	}
	while ((pos = line.find(subline3)) != string::npos) 
	{
		line.replace(pos, 4, zamline3);
	}
	return line;
}
string deshifr(string &line) 
{
	string subline1 = "иис", subline2 = "иил", subline3 = "иит";
	string zamline1 = "си", zamline2 = "ли", zamline3 = "ти";
	size_t pos;
	while ((pos = line.find(subline1)) != string::npos) 
	{
		line.replace(pos, 6, zamline1);
	}
	while ((pos = line.find(subline2)) != string::npos) 
	{
		line.replace(pos, 6, zamline2);
	}
	while ((pos = line.find(subline3)) != string::npos) 
	{
		line.replace(pos, 6, zamline3);
	}
	return line;

}
string vvod_sh(string &line) 
{
	ofstream vvod;
	vvod.open("example.txt");
	if (vvod.is_open()) 
	{
		vvod << shifr(line) << endl;
	}
	vvod.close();
	return shifr(line);
}
string vivod_desh(string line) 
{
	ifstream vivod("example.txt");
	if (vivod.is_open()) 
	{
		getline(vivod, line);
		cout << deshifr(line) << endl;
	}
	vivod.close();
	return deshifr(line);
}
string vvod_desh(string line) 
{
	ofstream vvod_deshifr;
	vvod_deshifr.open("shifr.txt", ios::app);
	if (vvod_deshifr.is_open())
	{
		vvod_deshifr << deshifr(line) << endl;
	}
	vvod_deshifr.close();
	return deshifr(line);
}
int main() 
{
	string line;
	cout << "Введите строку:" << endl;
	getline(cin, line);
	vvod_sh(line);
	vivod_desh(vvod_sh(line));
	vvod_desh(vvod_sh(line));
}
