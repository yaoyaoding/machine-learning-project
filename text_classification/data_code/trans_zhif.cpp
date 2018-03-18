#include <bits/stdc++.h>
using namespace std;

string fdictname = "combined_words.txt";
string finname = "idy.zh.if.txt";
string foutname = "idy.if.txt";

map<string,string> dict;

void init_dict() {
	ifstream fdict = ifstream(fdictname);
	if(!fdict) {
		printf("fdict open failed\n");
		return;
	}
	string word, id;
	while(fdict >> word >> id) {
		dict[word] = id;
	}
}
vector<string> split(string text) {
	vector<string> vc;
	string buf;
	for(int i = 0; i < (int)text.size(); i++) {
		if(isspace(text[i])) {
			if(!buf.empty()) vc.push_back(buf);
			buf.clear();
		} else {
			buf.push_back(text[i]);
		}
	}
	if(!buf.empty()) vc.push_back(buf);
	return vc;
}
void process() {
	ifstream fin = ifstream(finname);
	ofstream fout = ofstream(foutname);
	if(!fin || !fout) {
		printf("fin or fout open failed\n");
		return;
	}
	string id;
	string text;
	int nline = 0;
	while(fin >> id) {
		nline++;
		if(nline % 3000 == 0) printf("%d\n",nline);
		fout << id << " ";
		getline(fin, text);
		vector<string> vc = split(text);
		map<int,int> mp;
		for(auto s : vc) {
			if(dict.count(s) == 0) continue;
			mp[atoi(dict[s].c_str())]++;
		}
		if(!mp.empty()) {
			for(auto pr : mp) {
				fout << pr.first << ":" << 1 << " ";
			}
		} else {
			fout << "0:0 ";
		}
		fout << endl;
	}
	fin.close();
	fout.close();
}
int main() {
	printf("init_dict...\n");
	init_dict();
	printf("process...\n");
	process();
}


