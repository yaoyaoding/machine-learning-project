#include <bits/stdc++.h>
using namespace std;

string flabelname = "train.csv";
string finname = "train.if.txt";
string foutname = "train.lf.txt";

map<string,int> idlabel;

vector<string> split(string text, char ch = ',') {
	vector<string> vc;
	string buf;
	for(int i = 0; i < (int)text.size(); i++) {
		if(text[i] == ch) {
			if(!buf.empty()) vc.push_back(buf);
			buf.clear();
		} else {
			buf.push_back(text[i]);
		}
	}
	if(!buf.empty()) vc.push_back(buf);
	return vc;
}
typedef int (*JudgeChar)(int c);
vector<string> split(string text, JudgeChar judger) {
	vector<string> vc;
	string buf;
	for(int i = 0; i < (int)text.size(); i++) {
		if(judger(text[i])) {
			if(!buf.empty()) vc.push_back(buf);
			buf.clear();
		} else {
			buf.push_back(text[i]);
		}
	}
	if(!buf.empty()) vc.push_back(buf);
	return vc;
}
void init_idlabel() {
	ifstream flabel = ifstream(flabelname);
	if(!flabel) {
		printf("flabel open failed\n");
		return;
	}
	string buf;
	getline(flabel, buf);
	while(getline(flabel, buf)) {
		vector<string> vc = split(buf);
		idlabel[vc[0]] = atoi(vc[1].c_str());
	}
}
void process() {
	ifstream fin = ifstream(finname);
	ofstream fout = ofstream(foutname);
	if(!fin || !fout) {
		printf("fin or fout open failed\n");
		return;
	}
	string buf;
	int nline = 0;
	while(getline(fin,buf)) {
		vector<string> vc = split(buf,isspace);
		printf("%d\n", nline++);
		for(int t = 0; t < (int)vc.size(); t++) {
			if(t == 0) {
				if(!idlabel.count(vc[0])) {
					cout << vc[0] << " not found" << endl;
					printf("fatal error\n");
					exit(0);
				}
				fout << idlabel[vc[0]] << " ";
			} else {
				fout << vc[t] << " ";
			}
		}
		fout << endl;
	}
}
int main() {
	init_idlabel();
	process();
}

