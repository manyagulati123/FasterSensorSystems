#include "Spinnaker.h"
#include "SpinGenApi/SpinnakerGenApi.h"
#include <iostream>
#include <sstream>
#include <boost/python.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
using namespace boost::python;
using namespace Spinnaker;
using namespace Spinnaker::GenApi;
using namespace Spinnaker::GenICam;
using namespace std;

// Use the following enum and global static variable to select whether a 
// software or hardware trigger is used.
enum triggerType
{
	SOFTWARE,
	HARDWARE
};


struct GigECameraHelper {

	const triggerType chosenTrigger = SOFTWARE;
	SystemPtr system; 
	CameraList camList;
	unsigned int numCameras;	
public:
	int InitializeCameras();
	int TakeImages(string imageID, string ts);
	int ShutdownCameras();
	//GigECameraHelper(std::string s){;};

private:
	int _ConfigureTrigger(CameraPtr pCam);
	int _GrabNextImageByTrigger(CameraPtr pCam, ImagePtr & pResultImage);
	int _PrintDeviceInfo(CameraPtr pCam, int number);
	int _ResetTrigger(CameraPtr pCam);

	int _InitSingleCamera(CameraPtr pCam, int i);
	int _ShutDownSingleCamera(CameraPtr pCam);
	int _CaptureImageSingleCamera(CameraPtr pCam);		
};


