
#include "GigECameraHelper.h"
#include<fstream>
#include <chrono>

// This function configures the camera to use a trigger. First, trigger mode is 
// ensured to be off in order to select the trigger source. Trigger mode is 
// then enabled, which has the camera capture only a single image upon the 
// execution of the chosen trigger.
int GigECameraHelper::_ConfigureTrigger(CameraPtr pCam)
{
	int result = 0;
	try
	{
		if (chosenTrigger == SOFTWARE)
		{
			cout << "Software trigger chosen..." << endl;
		}
		else
		{
			cout << "Hardware trigger chosen..." << endl;
		}

		//
		// Ensure trigger mode off
		//
		// *** NOTES ***
		// The trigger must be disabled in order to configure whether the source
		// is software or hardware.
		//
		if (pCam->TriggerMode == NULL || pCam->TriggerMode.GetAccessMode() != RW)
		{
			cout << "Unable to disable trigger mode. Aborting..." << endl;
			return -1;
		}

		pCam->TriggerMode.SetValue(TriggerMode_Off);

		//
		// Select trigger source
		//
		// *** NOTES ***
		// The trigger source must be set to hardware or software while trigger 
		// mode is off.
		//
		// Set the trigger source to software
		if (pCam->TriggerSource == NULL || pCam->TriggerSource.GetAccessMode() != RW)
		{
			cout << "Unable to set trigger mode (node retrieval). Aborting..." << endl;
			return -1;
		}

		pCam->TriggerSource.SetValue(TriggerSource_Software);

		//
		// Turn trigger mode on
		//
		// *** LATER ***
		// Once the appropriate trigger source has been set, turn trigger mode 
		// back on in order to retrieve images using the trigger.
		//
		if (pCam->TriggerMode == NULL || pCam->TriggerMode.GetAccessMode() != RW)
		{
			cout << "Unable to disable trigger mode. Aborting..." << endl;
			return -1;
		}

		pCam->TriggerMode.SetValue(TriggerMode_On);

		cout << "Trigger mode turned back on..." << endl << endl;
	}
	catch (Spinnaker::Exception &e)
	{
		cout << "Error: " << e.what() << endl;
		result = -1;
	}

	return result;
}

// This function retrieves a single image using the trigger. In this example, 
// only a single image is captured and made available for acquisition - as such,
// attempting to acquire two images for a single trigger execution would cause 
// the example to hang. This is different from other examples, whereby a 
// constant stream of images are being captured and made available for image
// acquisition.
int GigECameraHelper::_GrabNextImageByTrigger(CameraPtr pCam, ImagePtr & pResultImage)
{
	int result = 0;
	try
	{				
		// Execute software trigger
		/*if (pCam->TriggerSoftware == NULL || pCam->TriggerSoftware.GetAccessMode() != WO)
		{
			cout << "Unable to execute trigger..." << endl;
			return -1;
		}*/

		pCam->TriggerSoftware.Execute();
		// Retrieve the next received image
		pResultImage = pCam->GetNextImage();
	}
	catch (Spinnaker::Exception &e)
	{
		cout << "Error: " << e.what() << endl;
		result = -1;
	}
	return result;
}

// This function returns the camera to a normal state by turning off trigger 
// mode.
int GigECameraHelper::_ResetTrigger(CameraPtr pCam)
{
	int result = 0;
	try
	{
		//
		// Turn trigger mode back off
		//
		// *** NOTES ***
		// Once all images have been captured, it is important to turn trigger
		// mode back off to restore the camera to a clean state.
		//
		if (pCam->TriggerMode == NULL || pCam->TriggerMode.GetAccessMode() != RW)
		{
			cout << "Unable to disable trigger mode. Aborting..." << endl;
			return -1;
		}
		pCam->TriggerMode.SetValue(TriggerMode_Off);
	}
	catch (Spinnaker::Exception &e)
	{
		cout << "Error: " << e.what() << endl;
		result = -1;
	}

	return result;
}

// This function prints the device information of the camera from the transport
// layer; please see NodeMapInfo example for more in-depth comments on printing
// device information from the nodemap.
int GigECameraHelper::_PrintDeviceInfo(CameraPtr pCam, int number)
{
	int result = 0;

	cout << endl << "*** DEVICE INFORMATION ***" << endl << endl;
	try
	{
		INodeMap & nodeMap = pCam->GetTLDeviceNodeMap();

		FeatureList_t features;
		CCategoryPtr category = nodeMap.GetNode("DeviceInformation");
		if (IsAvailable(category) && IsReadable(category))
		{
      string name = "GigE"+to_string(number+1)+".txt";
      ofstream myfile;
      myfile.open(name);
			category->GetFeatures(features);
      
			FeatureList_t::const_iterator it;
			for (it = features.begin(); it != features.end(); ++it)
			{
				CNodePtr pfeatureNode = *it;
				cout << pfeatureNode->GetName() << " : ";
        
				CValuePtr pValue = (CValuePtr)pfeatureNode;
        if(pfeatureNode->GetName()== "DeviceID")
        {
          myfile<<pValue->ToString()<<"\n";
        }
        if(pfeatureNode->GetName()== "DeviceVersion")
        {
          myfile<<pValue->ToString()<<"\n";
        }
        if(pfeatureNode->GetName()== "GevDeviceIPAddress")
        {
          myfile<<pValue->ToString()<<"\n";
        }
        if(pfeatureNode->GetName()== "GevDevicePort")
        {
          myfile<<pValue->ToString()<<"\n";
        }
        
				cout << (IsReadable(pValue) ? pValue->ToString() : "Node not readable");
				cout << endl;
			}
      myfile<<"N/A"<<"\n";
      myfile<<"N/A"<<"\n";
      //rename(myfile, name);
		}
		else
		{
			cout << "Device control information not available." << endl;
		}
	}
	catch (Spinnaker::Exception &e)
	{
		cout << "Error: " << e.what() << endl;
		result = -1;
	}

	return result;
}

// This function acquires and saves 10 images from a device; please see
// Acquisition example for more in-depth comments on the acquisition of images.
int GigECameraHelper::_CaptureImageSingleCamera(CameraPtr pCam)
{
	int result = 0;
	try
	{		
		// Get device serial number for filename
		/*gcstring deviceSerialNumber("");

		if (pCam->DeviceSerialNumber != NULL && pCam->DeviceSerialNumber.GetAccessMode() == RO)
		{
			deviceSerialNumber = pCam->DeviceSerialNumber.GetValue();

			cout << "Device serial number retrieved as " << deviceSerialNumber << "..." << endl;
		}
		cout << endl;*/

		try
		{
			// Retrieve next image by trigger
			ImagePtr pResultImage = NULL;
			auto t1 = std::chrono::high_resolution_clock::now();
			//clock_t begin = clock();	
			result = result | _GrabNextImageByTrigger(pCam, pResultImage);
			//clock_t end = clock();
			auto t2 = std::chrono::high_resolution_clock::now();
			std::cout << "f() took "
				<< std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count()
				<< " milliseconds\n";
			//double timeInMS =  end-begin;  //(((double)end - begin)/(CLOCKS_PER_SECc/1000.0));
			//printf("_GrabNextImageByTrigger: %f\n", timeInMS);


			// Ensure image completion
			if (pResultImage->IsIncomplete())
			{
				cout << "Image incomplete with image status " << pResultImage->GetImageStatus() << "..." << endl << endl;
			}
			else
			{
				// Print image information
				//cout << "Grabbed image " << ", width = " << pResultImage->GetWidth() << ", height = " << pResultImage->GetHeight() << endl;

				// Convert image to mono 8
				//ImagePtr convertedImage = pResultImage->Convert(PixelFormat_Mono8);

				// Create a unique filename
				ostringstream filename;

				filename << "TriggerQS-";
				/*if (deviceSerialNumber != "")
				{
					filename << deviceSerialNumber.c_str() << "-";
				}*/
				filename << "_End_" << ".jpg";

				// Save image
				//pResultImage->Save(filename.str().c_str());

				cout << "Image saved at " << filename.str() << endl;
			}

			// Release image
			pResultImage->Release();

			cout << endl;
		}
		catch (Spinnaker::Exception &e)
		{
			cout << "Error: " << e.what() << endl;
			result = -1;
		}		
		// End acquisition
		//pCam->EndAcquisition();
	}
	catch (Spinnaker::Exception &e)
	{
		cout << "Error: " << e.what() << endl;
		result = -1;
	}

	return result;
}

// This function acts as the body of the example; please see 
// NodeMapInfo_QuickSpin example for more in-depth comments on setting 
// up cameras.
int GigECameraHelper::_ShutDownSingleCamera(CameraPtr pCam)
{
	int result = 0;

	try
	{	
		// End acquisition
		pCam->EndAcquisition();

		// Reset trigger
		result = result | _ResetTrigger(pCam);

		// Deinitialize camera
		pCam->DeInit();
	}
	catch (Spinnaker::Exception &e)
	{
		cout << "Error: " << e.what() << endl;
		result = -1;
	}

	return result;
}

// This function acts as the body of the example; please see 
// NodeMapInfo_QuickSpin example for more in-depth comments on setting 
// up cameras.
int GigECameraHelper::_InitSingleCamera(CameraPtr pCam, int i)
{
	int result = 0;

	try
	{

		// Initialize camera
		pCam->Init();
		// Print device info
		result = _PrintDeviceInfo(pCam,i);
		// Configure trigger
		result = result | _ConfigureTrigger(pCam);

		// Set acquisition mode to continuous
		if (pCam->AcquisitionMode == NULL || pCam->AcquisitionMode.GetAccessMode() != RW)
		{
			cout << "Unable to set acquisition mode to continuous. Aborting..." << endl << endl;
			return -1;
		}

		pCam->AcquisitionMode.SetValue(AcquisitionMode_Continuous);

		cout << "Acquisition mode set to continuous..." << endl;

		// Begin acquiring images
		pCam->BeginAcquisition();		
	}
	catch (Spinnaker::Exception &e)
	{
		cout << "Error: " << e.what() << endl;
		result = -1;
	}

	return result;
}


int GigECameraHelper::InitializeCameras()
{
	int result = 0;

	// Print application build information
	cout << "Application build date: " << __DATE__ << " " << __TIME__ << endl << endl;
	
	// Retrieve singleton reference to system object
	system = System::GetInstance();

	// Retrieve list of cameras from the system
	camList = system->GetCameras();

	numCameras = camList.GetSize();

	cout << "Number of cameras detected: " << numCameras << endl << endl;

	//// Finish if there are no cameras
	if (numCameras == 0)
	{
		// Clear camera list before releasing system
		camList.Clear();

		// Release system
		system->ReleaseInstance();

		cout << "Not enough cameras!" << endl;
		cout << "Done! Press Enter to exit..." << endl;
		getchar();

		return -1;
	}

	// Run example on each camera

	for (unsigned int i = 0; i < numCameras; i++)
	{
		cout << "Init Camera:" << i << endl << endl;
		result = result | _InitSingleCamera(camList.GetByIndex(i), i);		
	}
	return result;
}


int GigECameraHelper::TakeImages(string imageID, string ts)
{

	auto t1 = std::chrono::high_resolution_clock::now();
		
	int result = 0;
	
	cout << "Taking images..." << endl;	
	CameraPtr pCam;
	for (unsigned int i = 0; i < numCameras; i++)
	{				
		pCam = camList.GetByIndex(i);
		pCam->TriggerSoftware.Execute();
		// Retrieve the next received image		
		//cout << "Obtain Images from Camera No:" << i << "..." << endl;
		//result = result | _CaptureImageSingleCamera(camList.GetByIndex(i));		
	}
	
	ImagePtr pResultImage = NULL;

	for (unsigned int i = 0; i < numCameras; i++)
	{				
		pCam = camList.GetByIndex(i);		
		pResultImage = pCam->GetNextImage();

		// Print image information
				cout << "Grabbed image " << ", width = " << pResultImage->GetWidth() << ", height = " << pResultImage->GetHeight() << endl;

				// Convert image to mono 8
				//ImagePtr convertedImage = pResultImage->Convert(PixelFormat_Mono8);

				// Create a unique filename
				ostringstream filename;
        
        int j = i+1;
        //string fname = "DataSet/"+imageID+"_"+ts+"_GigE"+j+".jpg";
        filename << "DataSet/"<<imageID<<"_"<<ts<<"_GigE"<<j<<".jpg";
				//filename << fname; //"TriggerQS-";
				/*if (deviceSerialNumber != "")
				{
					filename << deviceSerialNumber.c_str() << "-";
				}*/
				//filename << "" <<i<< ".jpg";

				// Save image
				pResultImage->Save(filename.str().c_str());

				cout << "Image saved at " << filename.str() << endl;

	}	


	
	auto t2 = std::chrono::high_resolution_clock::now();
	std::cout << "capturing time  took "
		<< std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count()
		<< " milliseconds\n";
	//printf("time spent capturing images: %f\n", timeInMS);

	
	cout << "Done taking images..." << endl;
	return result;
}

// This function acts as the body of the example; please see 
// NodeMapInfo_QuickSpin example for more in-depth comments on setting 
// up cameras.
//int RunSingleCamera(CameraPtr pCam)
//{
//	int result = 0;
//
//	try
//	{
//		// Initialize camera
//		pCam->Init();
//
//		// Print device info
//		result = PrintDeviceInfo(pCam);
//
//		// Configure trigger
//		result = result | ConfigureTrigger(pCam);
//
//		// Acquire images
//		result = result | AcquireImages(pCam);
//
//		// Reset trigger
//		result = result | ResetTrigger(pCam);
//
//		// Deinitialize camera
//		pCam->DeInit();
//	}
//	catch (Spinnaker::Exception &e)
//	{
//		cout << "Error: " << e.what() << endl;
//		result = -1;
//	}
//
//	return result;
//}


int GigECameraHelper::ShutdownCameras()
{
	int result = 0;
	
	//// Finish if there are no cameras
	if (numCameras == 0)
	{
		// Clear camera list before releasing system
		camList.Clear();

		// Release system
		system->ReleaseInstance();

		cout << "Not enough cameras!" << endl;
		cout << "Done! Press Enter to exit..." << endl;
		getchar();

		return -1;
	}

	// Run example on each camera
	for (unsigned int i = 0; i < numCameras; i++)
	{
		cout << endl << "Shutdown Cameras" << i << "..." << endl;
		
		result = result | _ShutDownSingleCamera(camList.GetByIndex(i));
	}

	// Clear camera list before releasing system
	camList.Clear();

	// Release system
	system->ReleaseInstance();

	cout << endl << "Done! Press Enter to exit..." << endl;	

	return result;
}



BOOST_PYTHON_MODULE(GigECameraHelper)
{

	/*int InitializeCameras();
	int TakeImages();
	int ShutdownCameras();
	GigECameraHelper(){;};*/

	class_<GigECameraHelper>("GigECameraHelper")
	.def("InitializeCameras", &GigECameraHelper::InitializeCameras)
	.def("TakeImages", &GigECameraHelper::TakeImages)
	.def("ShutdownCameras", &GigECameraHelper::ShutdownCameras)
	;
}
