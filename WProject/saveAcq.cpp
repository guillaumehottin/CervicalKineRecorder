#include "stdafx.h"
#include <fstream>
#include <iostream>
#include "ssttringToChar.h"
#include "writeInFile.h"
#include "convertToRetour.h"
#include "time.h"
#include <msclr\marshal_cppstd.h>

using namespace System;
using namespace System::Data;
using namespace Runtime::InteropServices;

System::String^ saveAcq(String^ name, String^ surname, String^ age, String^ type) {
	//get the time
	time_t date = time(0);
	System::String^ time = gcnew System::String(ctime(&date));
	int timeSize = time->Length;
	time = time->Remove(timeSize - 1, 1);
	time = time->Replace(":", "_");
	//create the filename with time, move type and extension
	System::String^ genericfileName = time + " - " + type;
	const char* genFileNamechar = (const char*)(Marshal::StringToHGlobalAnsi(genericfileName)).ToPointer();
	System::String^ fileName = time + " - " + type + ".orpl";
	const char* path = (const char*)(Marshal::StringToHGlobalAnsi(name + "_" + surname + "_" + age + "\\" + fileName)).ToPointer();
	//conversion en retour
	Retour_t retour = convertToRetour(std::ifstream("tmp.orpl"));
	//write the file
	writeInFile(retour, path);
	return genericfileName;
}
