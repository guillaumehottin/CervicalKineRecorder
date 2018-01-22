#include "acquire.h"
#include <fstream>
#include <iostream>
#include "writeInFile.h"

void writeInFile(Retour_t retour,const char* path) {
	int rows = retour.size; 
	std::ofstream fichier(path, std::ios::out | std::ios::trunc);
	if (fichier) {		
		fichier << "yaw pitch roll" << std::endl;
		for (int i = 0; i < rows; i++) {
			fichier << retour.yaw[i] << " " << retour.pitch[i] << " " << retour.roll[i] << std::endl;
		}
		fichier.close();
	}
	else { std::cerr << "impossible d'ouvrir le fichier" << std::endl; }
}


