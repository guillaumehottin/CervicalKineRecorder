#pragma once
#include "stdafx.h"
#include "acquire.h"
#include <fstream>
#include <iostream>
#include <windows.h>
#include "writeInFile.h"
#include "convertToRetour.h"
#include <sstream>
#include <boost\thread\thread.hpp>
#include "time.h"
#include <OVR_CAPI.h>
#include <msclr\marshal_cppstd.h>
#include "saveAcq.h"
#include "ssttringToChar.h" ; 



//using namespace std; 
using namespace System;
using namespace System::ComponentModel;
using namespace System::Collections;
using namespace System::Windows::Forms;
using namespace DataVisualization::Charting;
using namespace System::Drawing;
using namespace System::Threading;
using namespace Runtime::InteropServices;



/// <summary>
/// Summary for MyForm
/// </summary>
public ref class AcqForm : public Form
{
public:
	AcqForm(void)
	{
		InitializeComponent();
		//
		//TODO: Add the constructor code here
		//
	}
	// Set the current patient name //
	void setNom(String^ n) { nom = n; }

	// Set the current patient surname //
	void setPrenom(String ^p) { prenom = p; }

	// Set the current patient age //
	void setAge(String ^a) { age = a; }

	// Print name,surname, age in the nameBox //
	void printNoms(String^ p, String^ n) {
		this->nameBox->Text = p + " " + n + " " + age + " ans";
	}

protected:
	/// <summary>
	/// Clean up any resources being used.
	/// </summary>
	~AcqForm()
	{
		if (components)
		{
			delete components;
		}
	}

		/////////////////////////////////
		//    Declaration of charts    //
		/////////////////////////////////
private: Chart^  chart1;
private: Chart^  chart2;
private: Chart^  chart3;


		 /////////////////////////////////
		 //    Declaration of buttons   //
		 /////////////////////////////////
private: Button^  acquireButton;
private: Button^  browseButton;
private: Button^  clearButton;
private: Button^  saveButton;
private: Button^  removeLastButton;


		 /////////////////////////////////
		 //   Declaration of textboxes  //
		 /////////////////////////////////
private: TextBox^  xyBox;
private: ComboBox^  typeBox;
private: TextBox^  nameBox;
private: TextBox^  commentsBox;
private: TextBox^  commentsShow;


		 //   Declaration of booleans  //
private: bool canSave = false;
private: bool canCursor = false;
private: bool fromCharge = false;

		 //  Declaration of strings   //
		 static String^ path = "";
		 static String^ prenom;
		 static String^ age;
private: String^ nomCharge;
private: String^ fileName;
		 static String^ nom;

		 //Declaration of acquistion Thread//
private: Thread^ ackThr = gcnew Thread(gcnew ThreadStart(acquire));;

		 //  Declaration of app icon  //
private: System::Drawing::Icon^ icon = System::Drawing::Icon::ExtractAssociatedIcon("icone.ico");



private:
	/// <summary>
	/// Required designer variable.
	/// </summary>
	System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code
	/// <summary>
	/// Required method for Designer support - do not modify
	/// the contents of this method with the code editor.
	/// </summary>

	void InitializeComponent(void)
	{
		ChartArea^  chartArea1 = (gcnew ChartArea());
		Legend^  legend1 = (gcnew Legend());
		ChartArea^  chartArea2 = (gcnew ChartArea());
		Legend^  legend2 = (gcnew Legend());
		ChartArea^  chartArea3 = (gcnew ChartArea());
		Legend^  legend3 = (gcnew Legend());
		ComponentResourceManager^  resources = (gcnew ComponentResourceManager(AcqForm::typeid));
		this->chart1 = (gcnew Chart());
		this->chart2 = (gcnew Chart());
		this->chart3 = (gcnew Chart());
		this->acquireButton = (gcnew Button());
		this->browseButton = (gcnew Button());
		this->xyBox = (gcnew TextBox());
		this->typeBox = (gcnew ComboBox());
		this->clearButton = (gcnew Button());
		this->saveButton = (gcnew Button());
		this->removeLastButton = (gcnew Button());
		this->nameBox = (gcnew TextBox());
		this->commentsBox = (gcnew TextBox());
		this->commentsShow = (gcnew TextBox());
		(cli::safe_cast<ISupportInitialize^>(this->chart1))->BeginInit();
		(cli::safe_cast<ISupportInitialize^>(this->chart2))->BeginInit();
		(cli::safe_cast<ISupportInitialize^>(this->chart3))->BeginInit();
		this->SuspendLayout();
		// 
		// chart1
		// 
		chartArea1->Name = L"ChartArea1";
		this->chart1->ChartAreas->Add(chartArea1);
		this->chart1->Cursor = Cursors::Cross;
		legend1->Name = L"Legend1";
		this->chart1->Legends->Add(legend1);
		this->chart1->Location = Point(56, 457);
		this->chart1->Margin = System::Windows::Forms::Padding(2);
		this->chart1->Name = L"chart1";
		this->chart1->Size = System::Drawing::Size(740, 316);
		this->chart1->TabIndex = 0;
		this->chart1->Text = L"chart1";
		this->chart1->MouseMove += gcnew MouseEventHandler(this, &AcqForm::chart1_MouseMove);
		// 
		// chart2
		// 
		chartArea2->Name = L"ChartArea1";
		this->chart2->ChartAreas->Add(chartArea2);
		this->chart2->Cursor = Cursors::Cross;
		legend2->Name = L"Legend2";
		this->chart2->Legends->Add(legend2);
		this->chart2->Location = Point(56, 40);
		this->chart2->Margin = System::Windows::Forms::Padding(2);
		this->chart2->Name = L"chart2";
		this->chart2->Size = System::Drawing::Size(740, 346);
		this->chart2->TabIndex = 1;
		this->chart2->Text = L"chart2";
		this->chart2->MouseMove += gcnew MouseEventHandler(this, &AcqForm::chart2_MouseMove);
		// 
		// chart3
		// 
		chartArea3->Name = L"ChartArea1";
		this->chart3->ChartAreas->Add(chartArea3);
		this->chart3->Cursor = Cursors::Cross;
		legend3->Name = L"Legend3";
		this->chart3->Legends->Add(legend3);
		this->chart3->Location = Point(836, 457);
		this->chart3->Margin = System::Windows::Forms::Padding(2);
		this->chart3->Name = L"chart3";
		this->chart3->Size = System::Drawing::Size(664, 316);
		this->chart3->TabIndex = 2;
		this->chart3->Text = L"chart3";
		this->chart3->MouseMove += gcnew MouseEventHandler(this, &AcqForm::chart3_MouseMove);
		// 
		// acquireButton
		// 
		this->acquireButton->BackColor = SystemColors::Control;
		this->acquireButton->FlatAppearance->BorderColor = Color::Black;
		this->acquireButton->Location = Point(836, 40);
		this->acquireButton->Margin = System::Windows::Forms::Padding(2);
		this->acquireButton->Name = L"acquireButton";
		this->acquireButton->Size = System::Drawing::Size(135, 55);
		this->acquireButton->TabIndex = 3;
		this->acquireButton->Text = L"Acquisition Start";
		this->acquireButton->UseVisualStyleBackColor = false;
		this->acquireButton->Click += gcnew System::EventHandler(this, &AcqForm::acquireButton_Click);
		// 
		// browseButton
		// 
		this->browseButton->Location = Point(836, 136);
		this->browseButton->Margin = System::Windows::Forms::Padding(2);
		this->browseButton->Name = L"browseButton";
		this->browseButton->Size = System::Drawing::Size(135, 54);
		this->browseButton->TabIndex = 4;
		this->browseButton->Text = L"Charger fichier";
		this->browseButton->UseVisualStyleBackColor = true;
		this->browseButton->Click += gcnew System::EventHandler(this, &AcqForm::browseButton_Click);
		// 
		// textBox1
		// 
		this->xyBox->Cursor = Cursors::Arrow;
		this->xyBox->Font = (gcnew System::Drawing::Font(L"Microsoft Sans Serif", 11));
		this->xyBox->Location = Point(836, 211);
		this->xyBox->Margin = System::Windows::Forms::Padding(2);
		this->xyBox->Multiline = true;
		this->xyBox->Name = L"textBox1";
		this->xyBox->ReadOnly = true;
		this->xyBox->Size = System::Drawing::Size(171, 46);
		this->xyBox->TabIndex = 5;
		this->xyBox->MouseClick += gcnew MouseEventHandler(this, &AcqForm::xyBox_MouseClick);
		this->xyBox->MouseEnter += gcnew System::EventHandler(this, &AcqForm::xyBox_MouseEnter);
		// 
		// comboBox1
		// 
		this->typeBox->DropDownStyle = ComboBoxStyle::DropDownList;
		this->typeBox->FormattingEnabled = true;
		this->typeBox->Items->AddRange(gcnew cli::array< System::Object^  >(3) { L"Lacet", L"Tangage", L"Roulis" });
		this->typeBox->Location = Point(836, 101);
		this->typeBox->Margin = System::Windows::Forms::Padding(2);
		this->typeBox->Name = L"comboBox1";
		this->typeBox->Size = System::Drawing::Size(92, 21);
		this->typeBox->TabIndex = 6;
		this->typeBox->Tag = L"";
		// 
		// clearButton
		// 
		this->clearButton->Location = Point(982, 136);
		this->clearButton->Margin = System::Windows::Forms::Padding(2);
		this->clearButton->Name = L"clearButton";
		this->clearButton->Size = System::Drawing::Size(73, 55);
		this->clearButton->TabIndex = 7;
		this->clearButton->Text = L"Effacer toutes les courbes";
		this->clearButton->UseVisualStyleBackColor = true;
		this->clearButton->Click += gcnew System::EventHandler(this, &AcqForm::clearButton_Click);
		// 
		// saveButton
		// 
		this->saveButton->Location = Point(982, 40);
		this->saveButton->Margin = System::Windows::Forms::Padding(2);
		this->saveButton->Name = L"saveButton";
		this->saveButton->Size = System::Drawing::Size(73, 55);
		this->saveButton->TabIndex = 8;
		this->saveButton->Text = L"Enregistrer";
		this->saveButton->UseVisualStyleBackColor = true;
		this->saveButton->Click += gcnew System::EventHandler(this, &AcqForm::saveButton_Click);
		// 
		// removeLastButton
		// 
		this->removeLastButton->Location = Point(1073, 40);
		this->removeLastButton->Margin = System::Windows::Forms::Padding(2);
		this->removeLastButton->Name = L"removeLastButton";
		this->removeLastButton->Size = System::Drawing::Size(98, 55);
		this->removeLastButton->TabIndex = 9;
		this->removeLastButton->Text = L"Effacer dernière courbe";
		this->removeLastButton->UseVisualStyleBackColor = true;
		this->removeLastButton->Click += gcnew System::EventHandler(this, &AcqForm::removeLastButton_Click);
		// 
		// textBox3
		// 
		this->nameBox->BorderStyle = BorderStyle::None;
		this->nameBox->Cursor = Cursors::Arrow;
		this->nameBox->Font = (gcnew System::Drawing::Font(L"Microsoft Sans Serif", 12, FontStyle::Bold));
		this->nameBox->Location = Point(1176, 40);
		this->nameBox->Margin = System::Windows::Forms::Padding(2);
		this->nameBox->Name = L"textBox3";
		this->nameBox->ReadOnly = true;
		this->nameBox->Size = System::Drawing::Size(230, 19);
		this->nameBox->TabIndex = 11;
		this->nameBox->TextAlign = HorizontalAlignment::Center;
		// 
		// commentsBox
		// 
		this->commentsBox->ForeColor = SystemColors::WindowFrame;
		this->commentsBox->Location = Point(1073, 136);
		this->commentsBox->Margin = System::Windows::Forms::Padding(2);
		this->commentsBox->Name = L"commentsBox";
		this->commentsBox->Size = System::Drawing::Size(230, 20);
		this->commentsBox->TabIndex = 12;
		this->commentsBox->Text = L"Commentaires";
		this->commentsBox->GotFocus += gcnew System::EventHandler(this, &AcqForm::commentsBox_GotFocus);
		// 
		// commentsShow
		// 
		this->commentsShow->BackColor = SystemColors::Control;
		this->commentsShow->Location = Point(836, 276);
		this->commentsShow->Margin = System::Windows::Forms::Padding(2);
		this->commentsShow->Multiline = true;
		this->commentsShow->Name = L"commentsShow";
		this->commentsShow->ReadOnly = true;
		this->commentsShow->Size = System::Drawing::Size(570, 103);
		this->commentsShow->TabIndex = 13;
		this->commentsShow->MouseClick += gcnew MouseEventHandler(this, &AcqForm::commentsShow_MouseClick);
		this->commentsShow->MouseEnter += gcnew System::EventHandler(this, &AcqForm::commentsShow_MouseEnter);
		// 
		// MyForm1
		// 
		this->AutoScaleDimensions = SizeF(6, 13);
		this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
		this->AutoScroll = true;
		this->ClientSize = System::Drawing::Size(1447, 686);
		this->Controls->Add(this->commentsShow);
		this->Controls->Add(this->commentsBox);
		this->Controls->Add(this->nameBox);
		this->Controls->Add(this->removeLastButton);
		this->Controls->Add(this->saveButton);
		this->Controls->Add(this->clearButton);
		this->Controls->Add(this->typeBox);
		this->Controls->Add(this->xyBox);
		this->Controls->Add(this->browseButton);
		this->Controls->Add(this->acquireButton);
		this->Controls->Add(this->chart3);
		this->Controls->Add(this->chart2);
		this->Controls->Add(this->chart1);
		this->Cursor = Cursors::Default;
		this->Icon = icon;
		this->Margin = System::Windows::Forms::Padding(2);
		this->Name = L"MyForm1";
		this->Text = L"Cervical Kinématic Recorder";
		this->WindowState = FormWindowState::Maximized;
		this->FormClosing += gcnew FormClosingEventHandler(this, &AcqForm::AcqForm_FormClosing);
		(cli::safe_cast<ISupportInitialize^>(this->chart1))->EndInit();
		(cli::safe_cast<ISupportInitialize^>(this->chart2))->EndInit();
		(cli::safe_cast<ISupportInitialize^>(this->chart3))->EndInit();
		this->ResumeLayout(false);
		this->PerformLayout();

	}
#pragma endregion

	//*************************************************************************************************************//
	//*************************************************************************************************************//

	/////////////////////////////////
	/////////////////////////////////
	//Definition of buttons actions//
	/////////////////////////////////
	/////////////////////////////////


	//Action when clicking the acquireButton (Acquisition) 
	//Acquire datas from the OR
private: System::Void acquireButton_Click(System::Object^  sender, System::EventArgs^  e) {
	clear();
	//Impossible to launch an acquisition if no move is selected
	if (this->typeBox->SelectedItem == nullptr) {
		this->xyBox->Text = "Aucun mouvement selectionné";
	}
	//when a move is selected
	else {
		//make the move choice box read-only
		typeBox->Enabled = false;
		//change titles of the charts depending on the chosen move
		printTitles(typeBox->Text); 
	}

	Retour_t retour;
	//when you want to start acquisition
	if ((acquireButton->Text) == "Acquisition Start") {
		if (this->typeBox->SelectedItem == nullptr) {
			this->xyBox->Text = "Aucun mouvement selectionné";
		}
		else {
			acquireButton->Text = "Acquistion Stop";
			//Get datas from the OR
			ackThr->Start();
		}
	}
	//when you want to stop acquistion
	else {
		acquireButton->Text = "Acquisition Start";
		//stop the acquistion thread
		ackThr->Abort();
		//shut down the OR
		ovr_Shutdown();
		ackThr = gcnew Thread(gcnew ThreadStart(acquire));;
		//Stocking datas in a orpl file
		std::ifstream fichier("tmp.orpl");
		retour = convertToRetour(fichier);
		canSave = true;
		//Ploting datas 
		plot(retour);


	}
}

//*************************************************************************************************************//
//*************************************************************************************************************//


//Action when clicking the browseButton (Charger fichier)
//Browse a file thanks to an explorer
private: System::Void browseButton_Click(System::Object^  sender, System::EventArgs^  e) {
	xyBox->Text = "";
	//impossible to browse a file when no move is selected
	if (this->typeBox->SelectedItem == nullptr) {
		this->xyBox->Text = "Aucun mouvement selectionné";
	}
	else {
		//make the move choice box read-only
		typeBox->Enabled = false;
		String^ path3 = path;
		//launch a file explorer
		Thread^ thr = gcnew Thread(gcnew ThreadStart(openFile));
		openExplorer(thr);
		thr->Join();
		const char* path2 = sstringToChar(path); 

		if (path != path3) {
			//check if the move of the file is the same as the move selected in the box
			if ((path->Substring(path->LastIndexOf(" ") + 1)) != (typeBox->Text + ".orpl")) {
				xyBox->Text = "Mouvement incompatible";
				path = "";
				clear();
			}
			else {
				std::ifstream fichier(path2);
				int i = path->LastIndexOf("\\");
				//get the name
				String^ s1 = path->Substring(i + 1);
				fileName = s1->Substring(0, s1->IndexOf("."));
				fileName = fileName->Substring(4, 16);


				String^ sansFichier = path->Substring(0, i);
				int j = sansFichier->LastIndexOf("\\");
				String^ sansFichier2 = sansFichier->Substring(j + 1);
				//name of the person whom file is browsed
				nomCharge = sansFichier2->Substring(0, sansFichier2->IndexOf("_"));
				//add the person name in order to show it on the chart 
				fileName = nomCharge + " " + fileName;
				fileName = fileName->Replace("_", ":");

				//****************Comments part******************//


				String^ test = commentsBox->Text;
				//path to the commentsFile and conversion to char 
				String^ commentsPath = sansFichier + "\\commentaires.txt";
				const char* commentsPathChar = sstringToChar(commentsPath); 
				//search for comments
				std::ifstream commentsFile;
				commentsFile.open(commentsPathChar);
				//search string = title of the acquisition file
				String^ searchString = s1->Substring(0, s1->IndexOf("."));
				//convert the searchstring
				const char* searchChar = sstringToChar(searchString); 
				std::string search = std::string(searchChar);
				std::string line;
				size_t pos;
				//search file name in the comment file
				bool commentFound = false;
				while (commentsFile.good()) {
					getline(commentsFile, line);
					pos = line.find(search);
					//if found, show the comment in the comment box 
					if (pos != std::string::npos) {
						commentsShow->Text += nomCharge + " " + gcnew String(line.c_str()) + "\r\n";
					}
				}

				fromCharge = true;
				//Convert in a Retour_t type
				Retour_t retour = convertToRetour(fichier);
				//Plotting
				this->chart1->Titles->Clear();
				this->chart2->Titles->Clear();
				this->chart3->Titles->Clear();
				//change titles of the charts depending on the chosen move
				printTitles(typeBox->Text); 
				plot(retour);
				path = "";
			}
		}
	}
}


//*************************************************************************************************************//
//*************************************************************************************************************//

//Action when clicking the clearButton (Clear)
//Clear all the datas from the different charts
private: System::Void clearButton_Click(System::Object^  sender, System::EventArgs^  e) {
	//if an acquisition was made and not saved, open a warning pop
	if (canSave) {
		System::Windows::Forms::DialogResult answer = MessageBox::Show("Attention l'acquisition n'a pas été enregistrée voulez vous l'enregistrer avant de l'effacer ?", "Warning", MessageBoxButtons::YesNoCancel, MessageBoxIcon::Question);
		//if the user clicks on yes, save the file and clear
		if (answer == System::Windows::Forms::DialogResult::Yes) {
			save();
			clear();
			std::remove("tmp.orpl");
			canSave = false;
		}
		//else, if he clicked on no just clear the charts
		else if (answer == System::Windows::Forms::DialogResult::No) {
			clear();
			std::remove("tmp.orpl");
			canSave = false;
		}
	}
	//if there is no unsaved acquisition, clear the charts
	else {
		clear();
		std::remove("tmp.orpl");
		canSave = false;
	}
}

		 //*************************************************************************************************************//
		 //*************************************************************************************************************//


//Action when clicking the saveButton (Enregistrer)
//Saving datas into a orpl file through an explorer
private: System::Void saveButton_Click(System::Object^  sender, System::EventArgs^  e) {
	if (canSave) {
		save();
	}
}

		 //*************************************************************************************************************//
		 //*************************************************************************************************************//



//Action when clicking on removeLastButton (Retirer la derniere courbe)
//Remove the last curve drawn on the different charts
private: System::Void removeLastButton_Click(System::Object^  sender, System::EventArgs^  e) {
	//if an acquisition was made and not saved, open a warning pop
	if (canSave && this->chart1->Series->Count == 1) {
		System::Windows::Forms::DialogResult answer = MessageBox::Show("Attention l'acquisition n'a pas été enregistrée voulez vous l'enregistrer avant de l'effacer ?", "Warning", MessageBoxButtons::YesNoCancel, MessageBoxIcon::Question);
		//if the user clicks on yes, save the file
		if (answer == System::Windows::Forms::DialogResult::Yes) {
			save();
			this->chart1->Series->RemoveAt(this->chart1->Series->Count - 1);
			this->chart2->Series->RemoveAt(this->chart2->Series->Count - 1);
			this->chart3->Series->RemoveAt(this->chart3->Series->Count - 1);
			canSave = false;
			commentsShow->Text = commentsShow->Text->Substring(0, commentsShow->Text->LastIndexOf("\r\n"));
			typeBox->Enabled = true;


		}
		//else clear the last serie on the charts
		else if (answer == System::Windows::Forms::DialogResult::No) {
			this->chart1->Series->RemoveAt(this->chart1->Series->Count - 1);
			this->chart2->Series->RemoveAt(this->chart2->Series->Count - 1);
			this->chart3->Series->RemoveAt(this->chart3->Series->Count - 1);
			canSave = false;
			typeBox->Enabled = true;



		}
		else if (answer == System::Windows::Forms::DialogResult::Cancel) {
			//if the user cancels, the movement still can not be changed 
			typeBox->Enabled = false;
		}

	}
	else {
		if (this->chart1->Series->Count > 1) {
			this->chart1->Series->RemoveAt(this->chart1->Series->Count - 1);
			this->chart2->Series->RemoveAt(this->chart2->Series->Count - 1);
			this->chart3->Series->RemoveAt(this->chart3->Series->Count - 1);
			//erase the last comment 
			int lastIndex = commentsShow->Text->LastIndexOf("\r\n");
			commentsShow->Text = commentsShow->Text->Substring(0, lastIndex);
			lastIndex = commentsShow->Text->LastIndexOf("\r\n");
			commentsShow->Text = commentsShow->Text->Substring(0, lastIndex);
		}

		else {
			clear();
		}
		if (this->chart1->Series->Count == 0) {
			clear();

		}
	}
}





		 ////////////////////////////////////////////////////////
		 ////////////////////////////////////////////////////////
		 //Functions needed for the definition of button action//
		 ////////////////////////////////////////////////////////
		 ////////////////////////////////////////////////////////



//Saving file method
//Creates the file name with time, name, surname, age and writes 
private: System::Void save() {
	//call saveAcq to generate file name and write acquistion in tmp file 
	String^ genericfileName =  saveAcq(nom, prenom, age, typeBox->Text);
	//convert to char 
	const char* genFileNamechar = sstringToChar(genericfileName); 

	//               Comments part                   //

	//convert the commentsBox txt into char 
	const char* commentairechar = sstringToChar(commentsBox->Text);
	//get the path to the comments file 
	const char* pathcomms = sstringToChar(nom + "_" + prenom + "_" + age + "\\" + "commentaires.txt");
	//load the comments file
	std::ofstream comms(pathcomms, std::ios::out | std::ios::app);
	if (comms) {
		//If a comment has been written
		if (commentsBox->Text != "Commentaires") {
			//write it it the comments file and in the commentsShow box
			comms << genFileNamechar << " : " << commentairechar << std::endl;
			commentsShow->Text += nom + " " + genericfileName + " : " + commentsBox->Text + "\r\n";
		}
		//If not
		else {
			//write "" in the comments file and in the commentsShow box 
			comms << genFileNamechar << " : " << "" << std::endl;
			commentsShow->Text += nom + " " + genericfileName + " : " + "" + "\r\n";
		}
		comms.close();
	}

	//Restore the commentsBox : text+font color
	commentsBox->Text = "Commentaires";
	commentsBox->ForeColor = SystemColors::WindowFrame;

	//delete the tmp file
	std::remove("tmp.orpl");
	//there is no unsaved acquistion anymore 
	canSave = false;
}


//Clearing all datas from the charts
private: void clear() {
	//Clear all the charts from series and titles
	this->chart1->Series->Clear();
	this->chart2->Series->Clear();
	this->chart3->Series->Clear();
	this->chart3->Titles->Clear();
	this->chart1->Titles->Clear();
	this->chart2->Titles->Clear();

	//the user can not cursor on charts anymore
	canCursor = false;
	//the movement type can be changed again
	typeBox->Enabled = true;
	//erase comments showed
	commentsShow->Text = "";
	//restore the comments box : text+font color
	commentsBox->Text = "Commentaires";
	commentsBox->ForeColor = SystemColors::WindowFrame;
	//empty the path
	path = "";
}


//Plot the datas in the different charts
private: void plot(Retour_t retour) {

	int rows = retour.size;
	//create new series 
	Series^  serie1 = (gcnew Series());
	Series^  serie2 = (gcnew Series());
	Series^  serie3 = (gcnew Series());

	//add them in the charts
	serie1->ChartArea = L"ChartArea1";
	serie1->ChartType = SeriesChartType::Spline;
	serie1->Legend = L"Legend1";
	serie1->Name = L"serie1";
	this->chart1->Series->Add(serie1);

	serie2->ChartArea = L"ChartArea1";
	serie2->ChartType = SeriesChartType::Spline;
	serie2->Legend = L"Legend2";
	serie2->Name = L"serie2";
	this->chart2->Series->Add(serie2);

	serie3->ChartArea = L"ChartArea1";
	serie3->ChartType = SeriesChartType::Spline;
	serie3->Legend = L"Legend3";
	serie3->Name = L"serie3";
	this->chart3->Series->Add(serie3);

	//if data comes from an acquistion (not browsed)
	if (!fromCharge) {
		//get the current date 
		time_t date = time(0);
		String^ time = gcnew String(ctime(&date));
		int timeSize = time->Length;
		time = time->Remove(timeSize - 1, 1);
		time = time->Substring(4, 16);
		//create the filename : name of patient and time 
		fileName = nom + " " + time;
	}
	fromCharge = false;


	for (int i = 0; i < rows; ++i) {
		// Begin trunc
		int yaw = 100.0 * retour.yaw[i];
		int pitch = 100.0 * retour.pitch[i];
		int roll = 100.0 * retour.roll[i];
		double yaw2 = yaw / 100.0;
		double pitch2 = pitch / 100.0;
		double roll2 = roll / 100.0;
		//end trunc

		//Add points to series depending on the movement type selected 
		if (this->typeBox->SelectedItem->Equals(L"Lacet")) {

			serie1->Name = fileName;
			serie1->Points->AddXY(yaw2, pitch2);
			serie2->Name = fileName;
			serie2->Points->AddXY(yaw2, roll2);
			serie3->Name = fileName;
			serie3->Points->AddXY(roll2, pitch2);
		}
		if (this->typeBox->SelectedItem->Equals(L"Tangage")) {
			serie1->Name = fileName;
			serie1->Points->AddXY(pitch2, yaw2);
			serie2->Name = fileName;
			serie2->Points->AddXY(pitch2, roll2);
			serie3->Name = fileName;
			serie3->Points->AddXY(roll2, pitch2);
		}
		if (this->typeBox->SelectedItem->Equals(L"Roulis")) {
			serie1->Name = fileName;
			serie1->Points->AddXY(roll2, pitch2);
			serie2->Name = fileName;
			serie2->Points->AddXY(roll2, yaw2);
			serie3->Name = fileName;
			serie3->Points->AddXY(yaw2, pitch2);
		}
		//a curve is present, the user can use the cursor on it 
		canCursor = true;
	}
}


//Open an explorer (used in the buttons that needs to open an explorer)
private: System::Void openExplorer(Thread^ thr) {
	thr->SetApartmentState(ApartmentState::STA);
	thr->Start();
}


//Open a file
private: static System::Void openFile() {
	OpenFileDialog^ openFileDialog1 = gcnew OpenFileDialog;
	String^ id = "\\" + nom + "_" + prenom + "_" + age;

	openFileDialog1->InitialDirectory = Environment::CurrentDirectory + id;;
	openFileDialog1->Filter = "orpl files (*.orpl)|*.orpl";
	openFileDialog1->FilterIndex = 2;
	openFileDialog1->RestoreDirectory = false;

	if (openFileDialog1->ShowDialog() == System::Windows::Forms::DialogResult::OK) {
		// get the path to the selected file 
		path = openFileDialog1->FileName;
	}
}


private: System::Void printTitles(String^ type) {

	if (type->Equals(L"Lacet")) {
		this->chart1->Titles->Add("Tangage/Lacet");
		this->chart2->Titles->Add("Roulis/Lacet");
		this->chart3->Titles->Add("Tangage/Roulis");
	}

	if (type->Equals(L"Tangage")) {
		this->chart1->Titles->Add("Lacet/Tangage");
		this->chart2->Titles->Add("Roulis/Tangage");
		this->chart3->Titles->Add("Lacet/Roulis");
	}

	if (type->Equals(L"Roulis")) {
		this->chart1->Titles->Add("Tangage/Roulis");
		this->chart2->Titles->Add("Lacet/Roulis");
		this->chart3->Titles->Add("Tangage/Lacet");

	}
}






		 //////////////////////////////////////////////////////////////////////////////
		 //////////////////////////////////////////////////////////////////////////////
		 //Functions used to print the position of the cursor in the different charts//
		 //////////////////////////////////////////////////////////////////////////////
		 //////////////////////////////////////////////////////////////////////////////

private: System::Void printXY(Chart^ chart, MouseEventArgs^  e) {
	Point mousePoint = Point(e->X, e->Y);
	double x = chart->ChartAreas[0]->AxisX->PixelPositionToValue(e->X);
	double y = chart->ChartAreas[0]->AxisY->PixelPositionToValue(e->Y);
	chart->ChartAreas[0]->CursorX->Interval = 0.0;
	chart->ChartAreas[0]->CursorY->Interval = 0.0;
	chart->ChartAreas[0]->CursorX->SetCursorPixelPosition(mousePoint, true);
	chart->ChartAreas[0]->CursorY->SetCursorPixelPosition(mousePoint, true);
	this->xyBox->Text = "x : " + round(100 * x) / 100 + "\r\ny : " + round(100 * y) / 100;
}

//For chart1
private: System::Void chart1_MouseMove(System::Object^  sender, MouseEventArgs^  e) {
	if (canCursor) {
		printXY(this->chart1,e); 
	}
}

//For chart2
private: System::Void chart2_MouseMove(System::Object^  sender, MouseEventArgs^  e) {
	if (canCursor) {
		printXY(this->chart2, e); 
	}
}

//For chart3
private: System::Void chart3_MouseMove(System::Object^  sender, MouseEventArgs^  e) {
	if (canCursor) {
		printXY(this->chart3, e); 
	}
}


		 //////////////////////////////////////////////////////////////////////////////
		 //////////////////////////////////////////////////////////////////////////////
		 //                          Graphic details functions                       //
		 //////////////////////////////////////////////////////////////////////////////
		 //////////////////////////////////////////////////////////////////////////////


//Cancels the closing of the form when the user clicks on the red cross and hide it instead (otherwise it can not be opened again)
private: System::Void AcqForm_FormClosing(System::Object^  sender, FormClosingEventArgs^  e) {
	//cancel the closing of the form
	e->Cancel = true;
	//hide it instead and clear the graphs 
	clear();
	this->Hide();
}


//Erase the "Comments" string when the user clicks in the commentsBox and change the font color to Black
private: System::Void commentsBox_GotFocus(System::Object^ sender, System::EventArgs^ e) {
	commentsBox->Clear();
	commentsBox->ForeColor = SystemColors::WindowText;
}

//Transform the edit cursor into arrow cursor when mouse enters the xyBox
private: System::Void xyBox_MouseEnter(System::Object^  sender, System::EventArgs^  e) {
	xyBox->Cursor = Cursors::Arrow;
}

//Transform the edit cursor into arrow cursor when mouse enters the commentsShow box
private: System::Void commentsShow_MouseEnter(System::Object^  sender, System::EventArgs^  e) {
	this->commentsShow->Cursor = Cursors::Arrow;
}

//Hide the edit cursor in the xyBox
private: System::Void xyBox_MouseClick(System::Object^  sender, MouseEventArgs^  e) {
	HideCaret((HWND)xyBox->Handle.ToPointer());
}

//Hide the edit cursor in the commentsShow box
private: System::Void commentsShow_MouseClick(System::Object^  sender, MouseEventArgs^  e) {
	HideCaret((HWND)commentsShow->Handle.ToPointer());
}
};

