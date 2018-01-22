#include "acquire.h"
#include <fstream>
#include <vector>
#include <string>
#include "convertToRetour.h"

Retour_t convertToRetour(std::ifstream &file) {
	Retour_t retour;
	char str[255];
	std::vector<double> parsedLine; 
	if (file.getline(str, 255)) {
		while (file.getline(str, 255)) {
			parsedLine = splitLine(str);
			retour.yaw.push_back(parsedLine[0]);
			retour.pitch.push_back(parsedLine[1]);
			retour.roll.push_back(parsedLine[2]);

			retour.size = retour.roll.size();
		}
		//else : erreur ? 
	}
	return retour; 

}

std::vector<double> splitLine(char str[]) {
	std::string s(str); 
	std::string::size_type sz;
	std::vector<double> retour; 
	std::string delimiter = " ";
	std::string y = s.substr(0, s.find(delimiter));
	s.erase(0, s.find(delimiter) + delimiter.length());
	std::string p = s.substr(0, s.find(delimiter));
	s.erase(0, s.find(delimiter) + delimiter.length());
	std::string r = s; 
	retour.push_back(std::stod(y,&sz));
	retour.push_back(std::stod(p,&sz));
	retour.push_back(std::stod(r,&sz)); 
	return retour; 

}

