#include <OVR_CAPI.h>
#include <iostream>
#include <iomanip>
#include "acquire.h"
#include <boost/thread.hpp> 
#include <boost/date_time/posix_time/posix_time.hpp>
#include <vector>
#include <fstream>

//************************************************************************************************************//
// Acquire data from the rotation sensors of the Oculus, convert it into eulerian angles, tare it relatively  //
// to the first acquired value and put it in real tim in tmp.orpl                                            //
//************************************************************************************************************//
System::Void acquire()
{

	// ********************************************************** //
	//                Oculus initialization                       //
	// ********************************************************** //

	// Initialize the Oculus Library, a failure would probably mean incompatible Oculus runtime and SDK
	ovrResult result = ovr_Initialize(nullptr);
	if (OVR_FAILURE(result)) {
		exit(-1);
	}

	// Creation of a session of connection with the oculus to access sensor data
	ovrSession session = nullptr;
	ovrGraphicsLuid luid;
	result = ovr_Create(&session, &luid);

	//Close the connection if the session failed starting
	if (OVR_FAILURE(result))
	{
		ovr_Shutdown();
	}

	// ********************************************************** //
	//                Variables initialization                    //
	// ********************************************************** //

	// Sensor data of the Oculus
	ovrTrackingState ts;

	// Position of the oculus, may be used later on
	//ovrVector3f pos;

	// Orientation of the oculus
	ovrQuatf orient;

	// Length of the acquisition (60 secondes)
	int duree = 60;
	// Number of data collected per second (40 Hz)
	int nBperSec = 40;

	// Values of pitch yaw & roll at the first access of the sensor for the tare
	double pitch0 = 0;
	double yaw0   = 0;
	double roll0  = 0;

	// Values of pitch yaw & roll to be put in tmp.orpl
	double pitch  = 0;
	double yaw    = 0;
	double roll   = 0;

	// loop parameter
	int i = 0;

	// Output file to be filed in real time with the data collected
	std::ofstream fichier("tmp.orpl", std::ios::out | std::ios::trunc);
	fichier << "yaw pitch roll" << std::endl;

	// ********************************************************** //
	//                     Acquisition Loop                       //
	// ********************************************************** //
	while (i < duree*nBperSec)
	{
		ts = ovr_GetTrackingState(session, 0, true);

		//pos = ts.HeadPose.ThePose.Position;
		orient = ts.HeadPose.ThePose.Orientation;

		//////// Pitch value ////////
		pitch = Quat_To_Pitch(orient);
		// Tare initialization
		if (i == 0) {
			pitch0 = pitch;
		}
		// Tare
		pitch = pitch - pitch0;

		//////// Yaw value ////////
		yaw = Quat_To_Yaw(orient);
		// Tare initialization
		if (i == 0) {
			yaw0 = yaw;
		}
		// Tare
		yaw = yaw - yaw0;
		// Inversion for visualisation purposes on graph, so the angle move positively when moving the head to the right
		yaw = -yaw;

		//////// Roll value ////////
		roll = Quat_To_Roll(orient);
		// Tare initialization
		if (i == 0) {
			roll0 = roll;
		}
		// Tare
		roll = roll - roll0;

		// Writing values to the file
		fichier << yaw << " " << pitch << " " << roll << std::endl;

		i++;
		// Wait until next acquisition to maintain the number of value per second wanted
		boost::this_thread::sleep(boost::posix_time::milliseconds(1000 / nBperSec));
	}

	// Close the file and the connection to the oculus
	fichier.close(); 
	ovr_Destroy(session);
	ovr_Shutdown();
}

// Convert the quaternion orientation from the oculus to Pitch euler angle (y axis)
double Quat_To_Pitch(ovrQuatf orient) {

	double t0 = +2.0f * (orient.w * orient.x + orient.y * orient.z);
	double t1 = +1.0f - 2.0f * (orient.x * orient.x + orient.y * orient.y);

	return (180 / 3.14159265)*(std::atan2(t0, t1));
}

// Convert the quaternion orientation from the oculus to Yaw euler angle (z axis)
double Quat_To_Yaw(ovrQuatf orient) {

	double t = +2.0f * (orient.w * orient.y - orient.z * orient.x);
	t = t > 1.0f ? 1.0f : t;
	t = t < -1.0f ? -1.0f : t;
	return (180 / 3.14159265)*(std::asin(t));
}

// Convert the quaternion orientation from the oculus to Roll euler angle (x axis)
static double Quat_To_Roll(ovrQuatf orient) {

	double t0 = +2.0f * (orient.w * orient.z + orient.x *orient.y);
	double t1 = +1.0f - 2.0f * (orient.y * orient.y + orient.z * orient.z);

	return (180 / 3.14159265)*(std::atan2(t0, t1));
}
