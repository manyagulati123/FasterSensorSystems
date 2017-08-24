import subprocess
from subprocess import Popen
import datetime
import numpy as np
import time
import glob
import sys
import cv2
import xml.etree.ElementTree as ET
import os
import GigECameraHelper
import EnsensoHelper
g = EnsensoHelper.EnsensoHelper()
h = GigECameraHelper.GigECameraHelper()
from pylibfreenect2 import Freenect2, SyncMultiFrameListener, Freenect2Device
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
cameraList = ['Ensenso','GigE1','GigE2','GigE3','Kinect_depth']
KinectFilePath = "kinect.txt"
EnsensoFilePath = "ensenso.txt"
GigE1FilePath = "GigE1.txt"
GigE2FilePath = "GigE2.txt"
GigE3FilePath = "GigE3.txt"
IDFilePath = "ID.txt"

def writeToXML(date, time, timestamp, ID):
    root = ET.Element("root")
    KinectList=[]
    with open(KinectFilePath) as file:
        for line in file:
            KinectList.append(line)
    EnsensoList=[]
    with open(EnsensoFilePath) as file:
        for line in file:
            EnsensoList.append(line)
    GigE1List=[]
    with open(GigE1FilePath) as file:
        for line in file:
            GigE1List.append(line)
    GigE2List=[]
    with open(GigE2FilePath) as file:
        for line in file:
            GigE2List.append(line)
    GigE3List=[]
    with open(GigE3FilePath) as file:
        for line in file:
            GigE3List.append(line)
    doc = ET.SubElement(root, "Image", UniqueID= ID)
    ET.SubElement(doc, "Time").text = str(time)
    ET.SubElement(doc, "Date").text = str(date)
    ET.SubElement(doc, "SoftwareVersion").text = "Python 3.5"
    cls = ET.SubElement(doc, "Classification")
    coder1 = ET.SubElement(cls, "First_Coder")
    ET.SubElement(coder1, "Multifeed").text = " "
    ET.SubElement(coder1, "NumOfPieces").text = " "
    ET.SubElement(coder1, "BoxesPresent").text = " "
    ET.SubElement(coder1, "BagsPresent").text = " "
    
    coder2 = ET.SubElement(cls, "Second_Coder")
    ET.SubElement(coder2, "Multifeed").text = " "
    ET.SubElement(coder2, "NumOfPieces").text = " "
    ET.SubElement(coder2, "BoxesPresent").text = " "
    ET.SubElement(coder2, "BagsPresent").text = " "
    
    sensor1 = ET.SubElement(doc, "SensorInformation", Name="Ensenso")
    if(len(EnsensoList)==6):
      ET.SubElement(sensor1, "SerialNumber").text = EnsensoList[0]
      ET.SubElement(sensor1, "FirmwareVersion").text = EnsensoList[1]
      ET.SubElement(sensor1, "IPAddress").text = EnsensoList[2]
      ET.SubElement(sensor1, "USBPort").text = EnsensoList[3]
      ET.SubElement(sensor1, "Exposure").text = EnsensoList[4]
      ET.SubElement(sensor1, "Gain").text = EnsensoList[5]
    else:
      ET.SubElement(sensor1, "Error").text = "Some sensor details missing"
      
    sensor2 = ET.SubElement(doc, "SensorInformation", Name="Kinect")
    if(len(KinectList)==6):
      ET.SubElement(sensor2, "SerialNumber").text = KinectList[0]
      ET.SubElement(sensor2, "FirmwareVersion").text = KinectList[1]
      ET.SubElement(sensor2, "IPAddress").text = KinectList[2]
      ET.SubElement(sensor2, "USBPort").text = KinectList[3]
      ET.SubElement(sensor2, "Exposure").text = KinectList[4]
      ET.SubElement(sensor2, "Gain").text = KinectList[5]
    else:
      ET.SubElement(sensor2, "Error").text = "Some sensor details missing"

    sensor3 = ET.SubElement(doc, "SensorInformation", Name="GigE 1")
    if(len(GigE1List)==6):
      ET.SubElement(sensor3, "SerialNumber").text = GigE1List[0]
      ET.SubElement(sensor3, "FirmwareVersion").text = GigE1List[1]
      ET.SubElement(sensor3, "IPAddress").text = GigE1List[2]
      ET.SubElement(sensor3, "USBPort").text = GigE1List[3]
      ET.SubElement(sensor3, "Exposure").text = GigE1List[4]
      ET.SubElement(sensor3, "Gain").text = GigE1List[5]
    else:
      ET.SubElement(sensor3, "Error").text = "Some sensor details missing"
      
    sensor4 = ET.SubElement(doc, "SensorInformation", Name="GigE 2")
    if(len(GigE2List)==6):
      ET.SubElement(sensor4, "SerialNumber").text = GigE2List[0]
      ET.SubElement(sensor4, "FirmwareVersion").text = GigE2List[1]
      ET.SubElement(sensor4, "IPAddress").text = GigE2List[2]
      ET.SubElement(sensor4, "USBPort").text = GigE2List[3]
      ET.SubElement(sensor4, "Exposure").text = GigE2List[4]
      ET.SubElement(sensor4, "Gain").text = GigE2List[5]
    else:
      ET.SubElement(sensor4, "Error").text = "Some sensor details missing"
      
    sensor5 = ET.SubElement(doc, "SensorInformation", Name="GigE 3")
    if(len(GigE3List)==6):
      ET.SubElement(sensor5, "SerialNumber").text = GigE3List[0]
      ET.SubElement(sensor5, "FirmwareVersion").text = GigE3List[1]
      ET.SubElement(sensor5, "IPAddress").text = GigE3List[2]
      ET.SubElement(sensor5, "USBPort").text = GigE3List[3]
      ET.SubElement(sensor5, "Exposure").text = GigE3List[4]
      ET.SubElement(sensor5, "Gain").text = GigE3List[5]
    else:
      ET.SubElement(sensor5, "Error").text = "Some sensor details missing"
    # ET.SubElement(doc, "Time", name="blah").text = "some value1"
    # ET.SubElement(doc, "field2", name="asdfasd").text = "some value2"

    #root.append(doc)
    tree = ET.ElementTree(root)
    tree.write("DataSet/XML/"+ID+"_"+timestamp+".xml")


def writeIDtoFile(textfile, ID):
    textfile.write(str(ID)+"\n")


def displayImagesCaptured(Path, timestamp, ID):
    path = Path + ID +"_"+timestamp+"_"
    cv2.namedWindow('Ensenso', cv2.WINDOW_NORMAL)
    cv2.namedWindow('GigE1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('GigE2', cv2.WINDOW_NORMAL)
    cv2.namedWindow('GigE3', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Kinect', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Ensenso', 300,300)
    cv2.resizeWindow('GigE1', 300,300)
    cv2.resizeWindow('GigE2', 300,300)
    cv2.resizeWindow('GigE3', 300,300)
    cv2.resizeWindow('Kinect', 300,300)
    cv2.moveWindow('Ensenso', 0,20)
    cv2.moveWindow('GigE1', 300,400)
    cv2.moveWindow('GigE2', 500,20)
    cv2.moveWindow('GigE3', 800,400)
    cv2.moveWindow('Kinect', 1000,20)
    for camera in cameraList:
        imagePath = path+camera+".jpg"
        imageList = glob.glob(imagePath)
        print(imageList)
        for item in imageList:
            image = str(item)
            im = cv2.imread(image, -1)
            if(camera =='Ensenso'):
                cv2.imshow('Ensenso', im)
            elif(camera == 'GigE1'):
                cv2.imshow('GigE1', im)
            elif(camera == 'GigE2'):
                cv2.imshow('GigE2', im)
            elif(camera == 'GigE3'):
                cv2.imshow('GigE3', im)
            elif(camera == 'Kinect_depth'):
                cv2.imshow('Kinect', im)
                cv2.waitKey(3000)
        cv2.waitKey(4000)
    cv2.destroyAllWindows()


def captureKinect(device, serial,listener, timestamp, dID):
    ts = timestamp
    dataID = dID
    camera="Kinect"
    filename = dataID+"_"+ts+"_"+camera
    firmware = device.getFirmwareVersion()
    firmware = str(firmware).split("'")[1]
    # NOTE: must be called after device.start()
    registration = Registration(device.getIrCameraParams(),device.getColorCameraParams())
    undistorted = Frame(512, 424, 4)
    registered = Frame(512, 424, 4)
    frames = listener.waitForNewFrame()	
    color = frames["color"]
    ir = frames["ir"]	
    depth = frames["depth"]
    registration.apply(color, depth, undistorted, registered,bigdepth=None,color_depth_map=None)
    colorExposure = color.exposure
    depthExposure = depth.exposure
    irExposure = ir.exposure
    colorGain = color.gain
    depthGain = depth.gain
    irGain = ir.gain

    #key = cv2.waitKey(5000)
    cv2.imwrite('DataSet/'+filename+"_color.jpg", color.asarray())
    cv2.imwrite('DataSet/'+filename+"_depth.jpg", depth.asarray()%256)
    cv2.imwrite('DataSet/'+filename+"_RGBD.jpg", registered.asarray(np.uint8))
    listener.release(frames)
    with open("KinectDeviceID.txt") as file:
      deviceID = file.read() 
    process = subprocess.Popen("lsusb -v -d "+deviceID+"|grep \""+deviceID+"\"", stdout=subprocess.PIPE, shell=True)
    usb = process.stdout.readline()
    usb = str(usb).split("'")[1]
    usb = usb.split(':')[0]
    #print(usb)
    process.communicate()
    
    SensorDetails=[]
    SensorDetails.append(str(serial).split("'")[1])
    SensorDetails.append(firmware)
    SensorDetails.append("NA")
    SensorDetails.append(usb)
    SensorDetails.append("Color: "+str(colorExposure)+" Depth: "+str(depthExposure)+" IR: "+str(irExposure))
    SensorDetails.append("Color: "+str(colorGain)+" Depth: "+str(depthGain)+" IR: "+str(irGain))
    with open("kinect.txt",'w') as file:
      for item in SensorDetails:
         file.write(item+"\n")

def closeKinect(device):
    device.stop()
    device.close()
    
def main():
    t1=time.time()
    inputPath = "DataSet/"
    IDfile = open(IDFilePath,mode='a')
    try:
        from pylibfreenect2 import OpenCLPacketPipeline
        pipeline = OpenCLPacketPipeline()
        print("Using OpenCL")
        input()
    except:
        try:
            from pylibfreenect2 import OpenGLPacketPipeline
            pipeline = OpenGLPacketPipeline()
        except:
            from pylibfreenect2 import CpuPacketPipeline
            pipeline = CpuPacketPipeline()

    #print("Packet pipeline:", type(pipeline).__name__)
    # Create and set logger
    logger = createConsoleLogger(LoggerLevel.Debug)
    setGlobalLogger(logger)
    fn = Freenect2()
    num_devices = fn.enumerateDevices()
    if num_devices == 0:
        print("No device connected!")
        sys.exit(1)
    serial = fn.getDeviceSerialNumber(0)
    device = fn.openDevice(serial, pipeline=pipeline)
    
    #print("FirmwareVersion: "+ firmware)
    listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)
    # Register listeners
    device.setColorFrameListener(listener)
    device.setIrAndDepthFrameListener(listener)
    device.start()
    g.InitializeCamera()
    h.InitializeCameras()
    t2=time.time()
    print("Initialization before the loop "+str(t2-t1))
    while True:
        t3=time.time()
        t_ms = time.time()
        ts = datetime.datetime.now()

        print(t_ms)
        t_ms = t_ms * 1000
        t_ms = str(t_ms).split('.')[0]
        print(t_ms)
        imageID = t_ms

        print(str(ts).split('.')[0])
        ts = str(ts).split('.')[0]
        tsList1 = str(ts).split(' ')
        date = tsList1[0]
        tm = tsList1[1]
        print(tsList1)
        tsListTime = str(tsList1[1]).split(':')
        tsTime = str(tsListTime[0]) + "." + str(tsListTime[1]) + "." + str(tsListTime[2])
        print(tsTime)
        ts = str(tsList1[0]) + "_" + tsTime
        print(ts)
        t4=time.time()
        print("Starting part of the while loop: "+str(t4-t3))
        print("Press \'Enter\' to trigger the acquisition of images or \'q\' to Quit")
        key = input()
        print(key)
        if(not key):
            t5=time.time()
            captureKinect(device, serial, listener, ts, imageID)
            t0=time.time()
            g.TakeImages(imageID, ts)
            t9=time.time()
            h.TakeImages(imageID, ts)
            t6 = time.time()
            writeToXML(date, tm, ts, imageID)
            t7 = time.time()
            writeIDtoFile(IDfile,imageID)
            t8=time.time()
            '''ans = input("Display the images captured? (y/n)")
            if(ans=='y'):
                displayImagesCaptured(inputPath, ts, imageID)
            t9=time.time()'''
            print("Kinect Capture took "+str(t0-t5))
            print("Ensenso took "+str(t9-t0))
            print("GiGE took "+str(t6-t9))
            print("Writing to XML took "+str(t7-t6))
            print("Writing ID took "+ str(t8-t7))
            #print("Displaying images took "+str(t6-t5))
            print("Total time after pressing enter: "+str(t8-t5))
            print("Total loop time: "+str(t8-t3))
        elif(key =='q'):
            ta=time.time()
            closeKinect(device)
            g.ShutdownCamera()
            h.ShutdownCameras()
            tb=time.time()
            print("Close "+str(tb-ta))
            #print("Overall "+str(tb-t11))
            IDfile.close()
            sys.exit(0)
            break

if __name__ == '__main__':
    main()
