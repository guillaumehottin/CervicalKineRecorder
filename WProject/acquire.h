#pragma once
#include <vector>
#include <OVR_CAPI.h>

struct Retour_t { int size; std::vector<double> yaw; std::vector<double> pitch; std::vector<double> roll; };

System::Void acquire();
double Quat_To_Pitch(ovrQuatf orient);
double Quat_To_Yaw(ovrQuatf orient);
double Quat_To_Roll(ovrQuatf orient);