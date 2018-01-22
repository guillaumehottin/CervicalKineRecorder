#pragma once

#include "resource.h"
#include "AcqForm.h"
#include "Home.h"

ref struct Globals {
	static AcqForm^ form = gcnew AcqForm;
	static Home^ home = gcnew Home; 
}; 