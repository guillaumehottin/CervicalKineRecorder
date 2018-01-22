

using namespace System;
using namespace System::Data;
using namespace Runtime::InteropServices;

const char* sstringToChar(System::String^ s) { return (const char*)(Marshal::StringToHGlobalAnsi(s)).ToPointer(); }

