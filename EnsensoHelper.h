#include "nxLib.h"
#include <iostream>
#include <sstream>
#include <boost/python.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>

using namespace boost::python;
//using namespace nxLib;
using namespace std;

// Use the following enum and global static variable to select whether a 
// software or hardware trigger is used.
enum triggerType
{
	SOFTWARE,
	HARDWARE
};


struct EnsensoHelper {
	NxLibItem camera;
	//const triggerType chosenTrigger = SOFTWARE;
	//SystemPtr system; 
	//CameraList camList;
	//unsigned int numCameras;	
public:
	int InitializeCamera();
	int TakeImages(string imageID, string ts);
	int ShutdownCamera();

private:	
};


