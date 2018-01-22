#pragma once
#include "stdafx.h"
#include "AcqForm.h"
#include "msclr/marshal.h"
#include <string>



	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace System::Threading;
	using namespace Runtime::InteropServices;
	using namespace msclr::interop;

	/// <summary>
	/// Summary for Home
	/// </summary>
	public ref class Home : public System::Windows::Forms::Form
	{
	public:
		Home(void){
			InitializeComponent();
			//
			//TODO: Add the constructor code here
			//
		}
		String^ getNom() {
			return nom;
		}
		String^ getPrenom() {
			return prenom;
		}

		String^ getAge() {
			return age; 
		}
	protected:
		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		~Home()
		{
			if (components)
			{
				delete components;
			}
		}


	private: System::Windows::Forms::Button^  newProfileButton;
	static String^ path = "";
	static String^ nom = "";
	static String^ prenom = "";
	static String^ age = ""; 
	private: bool isNotReady = true;
	public: System::Drawing::Icon^ icon = System::Drawing::Icon::ExtractAssociatedIcon("icone.ico");

	private: System::Windows::Forms::TextBox^  prenomBox;
	private: System::Windows::Forms::TextBox^  nomBox;
	private: System::Windows::Forms::Button^  ackButton;
	private: System::Windows::Forms::Button^  browseProfileButton;
	private: System::Windows::Forms::TextBox^  infoBox;
	private: System::Windows::Forms::TextBox^  ageBox;

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
			System::ComponentModel::ComponentResourceManager^  resources = (gcnew System::ComponentModel::ComponentResourceManager(Home::typeid));
			this->ackButton = (gcnew System::Windows::Forms::Button());
			this->prenomBox = (gcnew System::Windows::Forms::TextBox());
			this->nomBox = (gcnew System::Windows::Forms::TextBox());
			this->newProfileButton = (gcnew System::Windows::Forms::Button());
			this->browseProfileButton = (gcnew System::Windows::Forms::Button());
			this->infoBox = (gcnew System::Windows::Forms::TextBox());
			this->ageBox = (gcnew System::Windows::Forms::TextBox());
			this->SuspendLayout();
			// 
			// ackButton
			// 
			this->ackButton->Location = System::Drawing::Point(176, 191);
			this->ackButton->Margin = System::Windows::Forms::Padding(2);
			this->ackButton->Name = L"ackButton";
			this->ackButton->Size = System::Drawing::Size(142, 53);
			this->ackButton->TabIndex = 5;
			this->ackButton->Text = L"Acquisition";
			this->ackButton->UseVisualStyleBackColor = true;
			this->ackButton->Click += gcnew System::EventHandler(this, &Home::ackButton_Click);
			// 
			// prenomBox
			// 
			this->prenomBox->ForeColor = System::Drawing::SystemColors::WindowFrame;
			this->prenomBox->Location = System::Drawing::Point(392, 38);
			this->prenomBox->Name = L"prenomBox";
			this->prenomBox->Size = System::Drawing::Size(100, 20);
			this->prenomBox->TabIndex = 4;
			this->prenomBox->Text = L"Prénom";
			this->prenomBox->GotFocus += gcnew System::EventHandler(this, &Home::prenomBox_GotFocus);
			// 
			// nomBox
			// 
			this->nomBox->ForeColor = System::Drawing::SystemColors::WindowFrame;
			this->nomBox->Location = System::Drawing::Point(392, 76);
			this->nomBox->Name = L"nomBox";
			this->nomBox->Size = System::Drawing::Size(100, 20);
			this->nomBox->TabIndex = 3;
			this->nomBox->Text = L"Nom";
			this->nomBox->GotFocus += gcnew System::EventHandler(this, &Home::nomBox_GotFocus);
			// 
			// newProfileButton
			// 
			this->newProfileButton->Location = System::Drawing::Point(176, 38);
			this->newProfileButton->Margin = System::Windows::Forms::Padding(2);
			this->newProfileButton->Name = L"newProfileButton";
			this->newProfileButton->Size = System::Drawing::Size(142, 55);
			this->newProfileButton->TabIndex = 0;
			this->newProfileButton->Text = L"Nouveau profil";
			this->newProfileButton->UseVisualStyleBackColor = true;
			this->newProfileButton->Click += gcnew System::EventHandler(this, &Home::newProfileButton_Click);
			// 
			// browseProfileButton
			// 
			this->browseProfileButton->Location = System::Drawing::Point(176, 113);
			this->browseProfileButton->Margin = System::Windows::Forms::Padding(2);
			this->browseProfileButton->Name = L"browseProfileButton";
			this->browseProfileButton->Size = System::Drawing::Size(142, 55);
			this->browseProfileButton->TabIndex = 6;
			this->browseProfileButton->Text = L"Charger profil";
			this->browseProfileButton->UseVisualStyleBackColor = true;
			this->browseProfileButton->Click += gcnew System::EventHandler(this, &Home::browseProfileButton_Click);
			// 
			// infoBox
			// 
			this->infoBox->BackColor = System::Drawing::SystemColors::ButtonFace;
			this->infoBox->BorderStyle = System::Windows::Forms::BorderStyle::None;
			this->infoBox->Location = System::Drawing::Point(392, 156);
			this->infoBox->Margin = System::Windows::Forms::Padding(2);
			this->infoBox->Name = L"infoBox";
			this->infoBox->ReadOnly = true;
			this->infoBox->Size = System::Drawing::Size(206, 13);
			this->infoBox->TabIndex = 7;
			this->infoBox->MouseClick += gcnew System::Windows::Forms::MouseEventHandler(this, &Home::infoBox_MouseClick);
			this->infoBox->MouseEnter += gcnew System::EventHandler(this, &Home::infoBox_MouseEnter);
			// 
			// ageBox
			// 
			this->ageBox->ForeColor = System::Drawing::SystemColors::WindowFrame;
			this->ageBox->Location = System::Drawing::Point(392, 113);
			this->ageBox->Name = L"ageBox";
			this->ageBox->Size = System::Drawing::Size(100, 20);
			this->ageBox->TabIndex = 8;
			this->ageBox->Text = L"Age";
			this->ageBox->GotFocus += gcnew System::EventHandler(this, &Home::ageBox_GotFocus);
			// 
			// Home
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(658, 406);
			this->Controls->Add(this->ageBox);
			this->Controls->Add(this->infoBox);
			this->Controls->Add(this->browseProfileButton);
			this->Controls->Add(this->nomBox);
			this->Controls->Add(this->prenomBox);
			this->Controls->Add(this->newProfileButton);
			this->Controls->Add(this->ackButton);
			this->Icon = icon;
			this->Margin = System::Windows::Forms::Padding(2);
			this->Name = L"Home";
			this->Text = L"Cervical Kinématic Recorder";
			this->FormClosing += gcnew System::Windows::Forms::FormClosingEventHandler(this, &Home::Home_FormClosing);
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion
		
	private: System::Void newProfileButton_Click(System::Object^  sender, System::EventArgs^  e) {
		if ((!prenomBox->Text->Equals("Prénom")) && (!nomBox->Text->Equals("Nom")) && (!prenomBox->Text->Equals("")) && (!nomBox->Text->Equals("")) && (!ageBox->Text->Equals("Age")) && (!ageBox->Text->Equals("")) ){
			prenom = prenomBox->Text;
			nom = nomBox->Text;
			age = ageBox->Text; 
			System::IO::Directory::CreateDirectory(nom + "_" + prenom + "_" + age);		
			this->infoBox->Text = "Profil créé : " + prenom + " " + nom + " " + age + " ans"; 
		}
		else {
			this->infoBox->Text = "Tous les champs ne sont pas remplis"; 
		}

	}
	
	private: System::Void Home_FormClosing(System::Object^  sender, System::Windows::Forms::FormClosingEventArgs^  e) {
		//cancel the closing of the form
		e->Cancel = true;
		//hide it instead and clear the graphs 
		//this->Hide();
		exit(0);
	}

private: System::Void prenomBox_GotFocus(System::Object^ sender, System::EventArgs^ e) {
	prenomBox->Clear();
	prenomBox->ForeColor = System::Drawing::SystemColors::WindowText;
}

	private: System::Void nomBox_GotFocus(System::Object^ sender, System::EventArgs^ e) {
		nomBox->Clear();
		nomBox->ForeColor = System::Drawing::SystemColors::WindowText;
	}

	private: System::Void ageBox_GotFocus(System::Object^ sender, System::EventArgs^ e) {
		ageBox->Clear();
		ageBox->ForeColor = System::Drawing::SystemColors::WindowText;
	}

	private: System::Void openExplorer(Thread^ thr) {
		thr->SetApartmentState(ApartmentState::STA);
		thr->Start();
	}

	private: static System::Void openFolder() {
		FolderBrowserDialog^ openFolderDialog = gcnew FolderBrowserDialog(); 

		openFolderDialog->SelectedPath = Environment::CurrentDirectory;


		if (openFolderDialog->ShowDialog() == System::Windows::Forms::DialogResult::OK) {
			// do your stuff
			path = openFolderDialog->SelectedPath; 
		}
	}

private: System::Void ackButton_Click(System::Object^  sender, System::EventArgs^  e) {
	if ((!prenom->Equals("")) && (!nom->Equals(""))) {
		AcqForm^ form = gcnew AcqForm();
		form->setNom(this->getNom());
		form->setPrenom(this->getPrenom());
		form->setAge(this->getAge()); 
		form->printNoms(this->getPrenom(), this->getNom());
		prenomBox->Text = "Prénom";
		nomBox->Text = "Nom";
		ageBox->Text = "Age";
		nomBox->ForeColor = System::Drawing::SystemColors::WindowFrame;
		prenomBox->ForeColor = System::Drawing::SystemColors::WindowFrame;
		ageBox->ForeColor = System::Drawing::SystemColors::WindowFrame;
		nom = "";
		prenom = ""; 
		age = ""; 
		this->infoBox->Clear(); 
		form->Show();
	}
	else {
		this->infoBox->Text = "Aucun profil selectionné"; 
	}
}
private: System::Void browseProfileButton_Click(System::Object^  sender, System::EventArgs^  e) {
	String^ path3 = path;
	Thread^ thr = gcnew Thread(gcnew ThreadStart(openFolder));
	openExplorer(thr);
	thr->Join();

	if (path != path3) {
		String^ name  = splitPath(path); 
		int i = name->IndexOf("_");
		String^ prenomage = name->Substring(i+1); 
		nom = name->Substring(0,i); 
		int j = prenomage->IndexOf("_"); 
		prenom = prenomage->Substring(0, j);
		age = prenomage->Substring(j+1); 
		nomBox->Text = nom;
		prenomBox->Text = prenom;
		ageBox->Text = age; 
		nomBox->ForeColor = System::Drawing::SystemColors::WindowText;
		prenomBox->ForeColor = System::Drawing::SystemColors::WindowText;	
		ageBox->ForeColor = System::Drawing::SystemColors::WindowText;
		this->infoBox->Text = "Profil chargé : " + prenom + " " + nom + " " + age + " ans"; 
	}

}
//get the name from the folder path 
String^ splitPath(String^ s) {
			 int last = s->LastIndexOf("\\");
			 String^ name = s->Substring(last + 1); 
			 return name;

}

//when the mouse enters the infobox, replace the edit cursor by an arrow cursor
private: System::Void infoBox_MouseEnter(System::Object^  sender, System::EventArgs^  e) {
	this->infoBox->Cursor = System::Windows::Forms::Cursors::Arrow; 
}
private: System::Void infoBox_MouseClick(System::Object^  sender, System::Windows::Forms::MouseEventArgs^  e) {
	HideCaret((HWND)infoBox->Handle.ToPointer());
}
};

