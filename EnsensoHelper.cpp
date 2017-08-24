
#include "EnsensoHelper.h"
#include "nxLib.h"
#include <fstream>
#include <chrono>

#define ISNAN(X) (X != X)

NxLibItem camera;

int EnsensoHelper::InitializeCamera()
{
	int result = 0;

	try{
		printf("Opening NxLib and waiting for cameras to be detected\n");
		nxLibInitialize(true);

		NxLibItem root; // Reference to the API tree root

		// Create an object referencing the camera's tree item, for easier access:
		camera = root[itmCameras][itmBySerialNo][0];
		if (!camera.exists() || (camera[itmType] != valStereo)) {
			printf("Please connect a single stereo camera to your computer\n");
		}

		std::string serial = camera[itmSerialNumber].asString();
		printf("Opening camera %s\n", serial.c_str());
		NxLibCommand open(cmdOpen); // When calling the 'execute' method in this object, it will synchronously execute the command 'cmdOpen'
		open.parameters()[itmCameras] = serial; // Set parameters for the open command
		open.execute();
		
		// Set the exposure to 5ms
		camera[itmParameters][itmCapture][itmAutoExposure] = false;
		camera[itmParameters][itmCapture][itmExposure] = 5;
		
	}
	catch(NxLibException& e) {
		printf("An NxLib API error with code %d (%s) occurred while accessing item %s.\n", e.getErrorCode(), e.getErrorText().c_str(), e.getItemPath().c_str());
		if (e.getErrorCode() == NxLibExecutionFailed) printf("/Execute:\n%s\n", NxLibItem(itmExecute).asJson(true).c_str());
	}
	catch(...){
		printf("You done goofed son");
	}
				
	return result;

//	return camera;
}


int EnsensoHelper::TakeImages(string imageID, string ts)
{		
	int result = 0;
	
	std::stringstream ss;

	// Save images
	NxLibCommand saveImage(cmdSaveImage);

	// Execute the 'Capture', 'ComputeDisparityMap' and 'ComputePointMap' commands
	printf("Grabbing an image\n");
	NxLibCommand (cmdCapture).execute(); // Without parameters, most commands just operate on all open cameras
	printf("Computing the disparity map\n"); // This is the actual, computation intensive stereo matching task
	NxLibCommand (cmdComputeDisparityMap).execute();
	printf("Generating point map from disparity map\n"); // This converts the disparity map into XYZ data for each pixel
	NxLibCommand (cmdComputePointMap).execute();
	printf("Rectifying image\n");
	NxLibCommand (cmdRectifyImages).execute();	

	// Get info about the computed point map and copy it into a std::vector
	std::vector<float> pointMap; int width, height;
	camera[itmImages][itmPointMap].getBinaryDataInfo(&width, &height, 0,0,0,0);
	camera[itmImages][itmPointMap].getBinaryData(pointMap, 0);

	// Compute average Z value
	//printf("The average z value in the point map is %.1fmm.\n", computeAverageZ(pointMap, width, height));

	// rectified left	
	saveImage.parameters()[itmNode] = camera[itmImages][itmRectified][itmLeft].path;
	saveImage.parameters()[itmFilename] = "DataSet/" + imageID + "_" + ts + "_EnsensoLeft.png";
	saveImage.execute();
	// rectified right
	saveImage.parameters()[itmNode] = camera[itmImages][itmRectified][itmRight].path;
	saveImage.parameters()[itmFilename] = "DataSet/" + imageID + "_" + ts + "_EnsensoRight.png";
	saveImage.execute();


	return result;
}

int EnsensoHelper::ShutdownCamera()
{
	int result = 0;
	printf("Closing camera\n");
	NxLibCommand (cmdClose).execute();
	printf("Closing NxLib\n");
	nxLibFinalize();
	return result;
}



BOOST_PYTHON_MODULE(EnsensoHelper)
{

	/*int InitializeCameras();
	int TakeImages();
	int ShutdownCameras();
	EnsensoHelper(){;};*/

	class_<EnsensoHelper>("EnsensoHelper")
	.def("InitializeCamera", &EnsensoHelper::InitializeCamera)
	.def("TakeImages", &EnsensoHelper::TakeImages)
	.def("ShutdownCamera", &EnsensoHelper::ShutdownCamera)
	;
}
