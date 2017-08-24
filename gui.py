import tkinter as tk
import PIL.Image, PIL.ImageTk
from tkinter import *
from tkinter import messagebox
import os
import sys
import cv2
import glob
import shutil
import fileinput
import xml.etree.ElementTree as ET



DSPath = "DataSet/"
DoublesPath = "DataSet/Doubles/"
SinglesPath = "DataSet/Singles/"
XMLPath = "DataSet/XML/"
cAPath="DataSet/Classes/classA.txt"
cBPath="DataSet/Classes/classB.txt"
g1PathA="DataSet/Classes/GigE1A.txt"
g2PathA="DataSet/Classes/GigE2A.txt"
g3PathA="DataSet/Classes/GigE3A.txt"
ePathA="DataSet/Classes/EnsensoA.txt"
kPathA="DataSet/Classes/KinectA.txt"
g1PathB="DataSet/Classes/GigE1B.txt"
g2PathB="DataSet/Classes/GigE2B.txt"
g3PathB="DataSet/Classes/GigE3B.txt"
ePathB="DataSet/Classes/EnsensoB.txt"
kPathB="DataSet/Classes/KinectB.txt"
ClassFile_A = open("DataSet/Classes/classA.txt",'a')
ClassFile_B = open("DataSet/Classes/classB.txt",'a')
GigE1file_A = open("DataSet/Classes/GigE1A.txt",'a')
GigE2file_A = open("DataSet/Classes/GigE2A.txt",'a')
GigE3file_A = open("DataSet/Classes/GigE3A.txt",'a')
KinectFile_A = open("DataSet/Classes/KinectA.txt",'a')
EnsensoFile_A = open("DataSet/Classes/EnsensoA.txt",'a')
GigE1file_B = open("DataSet/Classes/GigE1B.txt",'a')
GigE2file_B = open("DataSet/Classes/GigE2B.txt",'a')
GigE3file_B = open("DataSet/Classes/GigE3B.txt",'a')
KinectFile_B = open("DataSet/Classes/KinectB.txt",'a')
EnsensoFile_B = open("DataSet/Classes/EnsensoB.txt",'a')
mismatchFile = open("mismatch.txt",'w')
with open("ID.txt",'r') as idFile:
    IDlist = idFile.readlines()
IDlist = [x.strip() for x in IDlist]
doneIDlist=[]
currentImages=[]
currentID=''


def closeFiles():
    ClassFile_A.close()
    ClassFile_B.close()
    GigE1file_A.close()
    GigE2file_A.close()
    GigE3file_A.close()
    KinectFile_A.close()
    EnsensoFile_A.close()
    GigE1file_B.close()
    GigE2file_B.close()
    GigE3file_B.close()
    KinectFile_B.close()
    EnsensoFile_B.close()
    idFile.close()

def removeFile(item, path):
    try:
        os.remove(path+"/"+item)
    except FileNotFoundError:
        print(item+" not found in "+path)


def replaceLine(fileName, imgID, text, instances):
    countLines=0
    f = fileinput.input(fileName,inplace=True)
    for line in f:
        if(line.startswith(imgID)):
            countLines+=1
            sys.stdout.write(text)
            #if(countLines==instances):
                #break
        else:
            sys.stdout.write(line)

    f.close()

def encodeXML(ID, coder, value, numPieces, boxesPresent, bagsPresent):
    if(value==1):
        encodedVal = 'True'
    else:
        encodedVal = 'False'

    match_string = XMLPath+str(ID)+"_"+'*'
    XML_file = glob.glob(match_string)
    print(XML_file)
    print(coder)
    print(value)
    if(len(XML_file)>0):
        XML_file = XML_file[0]
        tree = ET.parse(XML_file)
        root = tree.getroot()
        ImageTag= root.find('Image')
        ClassificationTag = ImageTag.find('Classification')
        if(coder==1):
            coderTag = ClassificationTag.find('First_Coder')
        else:
            coderTag = ClassificationTag.find('Second_Coder')
        Multifeed = coderTag.find('Multifeed')
        Number_Pieces = coderTag.find('NumOfPieces')
        BoxesPresent = coderTag.find('BoxesPresent')
        BagsPresent = coderTag.find('BagsPresent')
        Multifeed.text = encodedVal
        Number_Pieces.text = numPieces
        BoxesPresent.text = boxesPresent
        BagsPresent.text = bagsPresent
        tree.write(XML_file)
    else:
        print("No file matched!")



value=0
def incrementCount():
    global value
    retVal = value
    value=value+1
    return retVal

def decrementCount():
    global value
    value = value-1
    return value

def main():

    root = Tk()
    root.title("Multifeed Image Data Classification")
    frame = Frame(root,height=680, width=1020)#1120)
    imageFile = "black15.jpg"
    img = PIL.ImageTk.PhotoImage(PIL.Image.open(imageFile).resize((300,300)))
    GigE1Label = Label(frame,image=img,height=300,width=300, relief=SUNKEN)
    GigE1Label.pack(expand = False)
    GigE2Label = Label(frame,image=img,height=300,width=300, relief= SUNKEN)
    GigE2Label.pack(expand = False)
    GigE3Label = Label(frame,image=img,height=300,width=300, relief= SUNKEN)
    GigE3Label.pack(expand = False)
    KinectLabel = Label(frame,image=img,height=300,width=300, relief= SUNKEN)
    KinectLabel.pack(expand = False)
    EnsensoLabel = Label(frame,image=img,height=300,width=300, relief=SUNKEN)
    EnsensoLabel.pack(expand = False)
    GigE1Label.place(x=20,y=20)
    GigE2Label.place(x=360,y=20)
    GigE3Label.place(x=700,y=20)
    KinectLabel.place(x=20,y=330)
    EnsensoLabel.place(x=700,y=330)

    def startProcess():
        coderRB1['state'] = 'disabled'
        coderRB2['state'] = 'disabled'
        coderButton['state'] = 'disabled'
        startButton['state'] = 'normal'


    def loadPrevious():
        decrementCount()
        decrementCount()
        loadImage()

    def loadNext():
        loadImage()

    def loadImage():
        root.bind("d", keyD)
        root.bind("s", keyS)
        root.bind("<Return>", keyEnter)
        startButton['state'] = 'disabled'
        count=incrementCount()
        print(count)
        classifyButton['state']='normal'
        rb1['state'] = 'normal'
        rb2['state'] = 'normal'
        category.set(None)
        if(count>=1):
            previousButton['state']='normal'
        else:
            previousButton['state'] = 'disabled'
        if(count<len(IDlist)):
            nextButton['state']='normal'
        else:
            nextButton['state']='disabled'
        global currentID
        if(count<len(IDlist)):
            codedImageNumber['text']=str(count)
            remImageNumber['text']=str(len(IDlist)-count)
            currentID = IDlist[count]
            match=DSPath+currentID+"_"+'*'
            print(match)
            imageList = glob.glob(match)
            print(imageList)
            if(len(imageList)==0):
                messagebox.showinfo('Information',"No images with such an ID")
                startButton['state']='disabled'
                classifyButton['state'] = 'disabled'
                rb1['state'] = 'disabled'
                rb2['state'] = 'disabled'
                return
        else:
            codedImageNumber['text'] = str(count)
            remImageNumber['text'] = str(len(IDlist) - count)
            messagebox.showinfo('Information', "No more images to classify")
            startButton['state'] = 'disabled'
            classifyButton['state'] = 'disabled'
            rb1['state'] = 'disabled'
            rb2['state'] = 'disabled'
            coderRB1['state']='normal'
            coderRB2['state']='normal'
            coder.set(None)
            coderButton['state']='normal'
            global value
            value = 0
            return

        global currentImages
        currentImages=imageList
        for item in imageList:
            print(item)
            img = PIL.ImageTk.PhotoImage(PIL.Image.open(str(item)).resize((300, 300)))
            pathList = str(item).split('/')
            imageName = pathList[1]
            print(imageName)
            cameraName = imageName.split('_')[3]
            print(imageName)
            camera = cameraName.split('.')[0]
            if (camera == 'Kinect'):
                kinectType = imageName.split('_')[4]
                kinectType = kinectType.split('.')[0]
            if(camera=='GigE1'):
                GigE1Label.configure(image=img)
                GigE1Label.image=img
            elif(camera=='GigE2'):
                GigE2Label.configure(image=img)
                GigE2Label.image= img
            elif (camera == 'GigE3'):
                GigE3Label.configure(image=img)
                GigE3Label.image = img
            elif(camera=='Kinect' and kinectType =='depth'):
                KinectLabel.configure(image=img)
                KinectLabel.image=img
            elif(camera=='Ensenso'):
                EnsensoLabel.configure(image=img)
                EnsensoLabel.image=img
            else:
                print("No such camera")

    def quit():
        closeFiles()
        sys.exit(0)



    Pieces = StringVar()
    boxes = StringVar()
    bags = StringVar()

    def popUp():

        def closePopUp(event=None):
            top.destroy()

        top = Toplevel(root)
        top.title("Enter Details")
        L1 = Label(top, text="Number of\n Pieces").grid(row=1, column=1)
        #E1 = Entry(top, width=3, bd=5, textvariable=Pieces).grid(row=1, column=2)
        choices = {'1','2','3','4','More than 4'}
        option = OptionMenu(top, Pieces, *choices).grid(row=1,column=2)
        Pieces.set('1')
        L2 = Label(top, text="Boxes Present?").grid(row=2, column=1)
        rbBox1 = Radiobutton(top, bd=5, text="  Yes  ",variable=boxes, value='Yes',relief=RIDGE).grid(row=2, column=2)
        rbBox2 = Radiobutton(top, bd=5, text="  No  ",variable=boxes, value='No',relief=RIDGE).grid(row=2, column=3)
        boxes.set('Yes')
        #E2 = Entry(top, bd=5, textvariable=boxes).grid(row=2, column=3)
        L3 = Label(top, text="Bags Present?").grid(row=3, column=1)
        rbBag1 = Radiobutton(top, bd=5, text="  Yes  ", variable=bags, value='Yes', relief=RIDGE).grid(row=3, column=2)
        rbBag2 = Radiobutton(top, bd=5, text="  No  ", variable=bags, value='No', relief=RIDGE).grid(row=3, column=3)
        bags.set('No')
        #E3 = Entry(top, bd=5, textvariable=bags).grid(row=4, column=3)
        B = Button(top, text="   OK   ", command=closePopUp).grid(row=5, column=2)
        top.bind("<Return>",closePopUp)
        top.geometry('265x150+435+420')
        top.focus_force()

    def compareLabels():
        coder.set(3)
        closeFiles()
        for imageID in IDlist:
            match_string = XMLPath + str(imageID) + "_" + '*'
            XML_file = glob.glob(match_string)
            print(XML_file)
            if (len(XML_file) > 0):
                XML_file = XML_file[0]
                tree = ET.parse(XML_file)
                root = tree.getroot()
                ImageTag = root.find('Image')
                ClassificationTag = ImageTag.find('Classification')
                coderATag = ClassificationTag.find('First_Coder')
                coderBTag = ClassificationTag.find('Second_Coder')
                mA = coderATag.find('Multifeed')
                mB = coderBTag.find('Multifeed')
                '''Number_Pieces_A = coderATag.find('NumOfPieces')
                BoxesPresent_A = coderATag.find('BoxesPresent')
                BagsPresent_A = coderATag.find('BagsPresent')
                Number_Pieces_B = coderBTag.find('NumOfPieces')
                BoxesPresent_B = coderBTag.find('BoxesPresent')
                BagsPresent_B = coderBTag.find('BagsPresent')'''
                print(mA.text)
                print(mB.text)
                multifeed_A = mA.text
                multifeed_B = mB.text
                if(multifeed_A != multifeed_B):
                    mismatchFile.write(imageID+"\n")
            else:
                print("No XML file with such an ID")
        mismatchFile.close()
        loadMismatch()

    def loadMismatch():
        global IDlist
        global doneIDlist
        doneIDlist=IDlist
        with open("mismatch.txt", 'r') as mismatch_file:
            IDlist = mismatch_file.readlines()
        IDlist = [x.strip() for x in IDlist]
        print("IDLIST:")
        print(IDlist)
        global value
        value=0
        loadImage()

    numDoubles = StringVar()
    numSingles = StringVar()
    doublesFirst = StringVar()
    def autoClassify():
        coderRB1['state'] = 'disabled'
        coderRB2['state'] = 'disabled'
        coderButton['state'] = 'disabled'
        auto['state']='disabled'

        def autoClassification():
            top.destroy()
            doublesCode=1
            singlesCode=2
            numDoubleImages = int(numDoubles.get())*6
            numSingleImages = int(numSingles.get())*6
            answer = doublesFirst.get()
            if (answer == 'y' or answer == 'Y'):
                firstSet = numDoubleImages
                firstGroup = ", Doubles\n"
                secondGroup = ", Singles\n"
                firstPath = DoublesPath
                secondPath = SinglesPath
                firstValue= doublesCode
                secondValue=singlesCode
            else:
                firstSet = numSingleImages
                firstGroup = ", Singles\n"
                secondGroup = ", Doubles\n"
                firstPath = SinglesPath
                secondPath = DoublesPath
                firstValue = singlesCode
                secondValue = doublesCode

            listing = os.listdir(DSPath)
            imageCount=0
            for image in listing:
                if(image.endswith(".jpg")):
                    print(str(image))
                    imageCount+=1
                    if(imageCount<=firstSet):
                        print(firstGroup)
                        shutil.copy(DSPath+str(image), firstPath)
                        writeClass = str(image) + firstGroup
                        classValue=firstValue
                    else:
                        print(secondGroup)
                        shutil.copy(DSPath+str(image), secondPath)
                        writeClass = str(image) + secondGroup
                        classValue=secondValue
                    ClassFile_A.write(writeClass)
                    ClassFile_B.write(writeClass)

                    if(imageCount%6==0):
                        encodeXML(image.split('_')[0], 1,classValue,"auto","auto","auto")
                        encodeXML(image.split('_')[0], 2,classValue, "auto", "auto", "auto")
            messagebox.showinfo('Information', "Auto-coding is completed!")
            quit()

        top = Toplevel(root)
        top.title("Enter Details")
        L1 = Label(top, text="Number of Doubles Instances").grid(row=1, column=1)
        E1 = Entry(top, bd=5, textvariable=numDoubles).grid(row=1, column=3)
        L2 = Label(top, text="Number of Singles Instances").grid(row=2, column=1)
        E2 = Entry(top, bd=5, textvariable=numSingles).grid(row=2, column=3)
        L3 = Label(top, text="Doubles first? (y/n)").grid(row=3, column=1)
        E3 = Entry(top, bd=5, textvariable=doublesFirst).grid(row=3, column=3)
        B = Button(top, text="OK", command=autoClassification).grid(row=4, column=2)

    def classify():
        #top.destroy()
        classifyButton['state'] = 'disabled'
        rb1['state'] = 'disabled'
        rb2['state'] = 'disabled'
        global currentImages
        coderValue = coder.get()
        classifiedValue = category.get()
        numPieces = Pieces.get()
        boxesPresent = boxes.get()
        bagsPresent = bags.get()
        Pieces.set('')
        boxes.set('')
        bags.set('')
        writeClass = ""
        print(numPieces)
        print(boxesPresent)
        print(bagsPresent)
        print(category.get())
        global currentID
        if(coderValue!=1 and coderValue!=2):
            encodeXML(currentID, 1, classifiedValue, numPieces, boxesPresent, bagsPresent)
            encodeXML(currentID, 2, classifiedValue, numPieces, boxesPresent, bagsPresent)
        else:
            encodeXML(currentID, coderValue, classifiedValue, numPieces, boxesPresent, bagsPresent)
        for item in currentImages:
            print(item)
            pathList = str(item).split('/')
            imageName = pathList[1]
            print(imageName)
            cameraName = imageName.split('_')[3]
            print(cameraName)
            camera = cameraName.split('.')[0]
            if (camera == 'Kinect'):
                kinectType = imageName.split('_')[4]
                kinectType = kinectType.split('.')[0]


            if(classifiedValue==1):
                print("Doubles")
                print(currentImages)
                shutil.copy(item,DoublesPath)
                removeFile(pathList[1],SinglesPath)
                writeClass = imageName+", Doubles\n"

            else:
                print("Singles")
                shutil.copy(item,SinglesPath)
                removeFile(pathList[1], DoublesPath)
                writeClass = imageName + ", Singles\n"

            print(writeClass)
            if(coderValue==1):
                ClassFile_A.write(writeClass)
            elif(coderValue==2):
                ClassFile_B.write(writeClass)
            else:
                replaceLine(cAPath,imageName,writeClass, 6)
                replaceLine(cBPath,imageName,writeClass, 6)


            if (camera == 'GigE1'):
                if(coderValue==1):
                    GigE1file_A.write(writeClass)
                elif(coderValue==2):
                    GigE1file_B.write(writeClass)
                else:
                    replaceLine(g1PathA, imageName, writeClass, 1)
                    replaceLine(g1PathB, imageName, writeClass, 1)
            elif(camera == 'GigE2'):
                if (coderValue == 1):
                    GigE2file_A.write(writeClass)
                elif(coderValue == 2):
                    GigE2file_B.write(writeClass)
                else:
                    replaceLine(g2PathA, imageName, writeClass, 1)
                    replaceLine(g2PathB, imageName, writeClass, 1)
            elif (camera == 'GigE3'):
                if (coderValue == 1):
                    GigE3file_A.write(writeClass)
                elif(coderValue == 2):
                    GigE3file_B.write(writeClass)
                else:
                    replaceLine(g3PathA, imageName, writeClass, 1)
                    replaceLine(g3PathB, imageName, writeClass, 1)
            elif (camera == 'Kinect' and kinectType == 'depth'):
                if (coderValue == 1):
                    KinectFile_A.write(writeClass)
                elif(coderValue == 2):
                    KinectFile_B.write(writeClass)
                else:
                    replaceLine(kPathA, imageName, writeClass, 1)
                    replaceLine(kPathB, imageName, writeClass, 1)
            elif (camera == 'Ensenso'):
                if (coderValue == 1):
                    EnsensoFile_A.write(writeClass)
                elif(coderValue == 2):
                    EnsensoFile_B.write(writeClass)
                else:
                    replaceLine(ePathA, imageName, writeClass, 1)
                    replaceLine(ePathB, imageName, writeClass, 1)
            else:
                print("No such camera")
        loadImage()


    def keyD(event):
        category.set(1)
        popUp()

    def keyS(event):
        category.set(2)
        popUp()

    def keyEnter(event):
        classify()


    coderLabel = Label(frame, text="Coder: Identify yourself")
    coderLabel.place(x=430,y=340)
    coder = IntVar()
    coderRB1 = Radiobutton(frame, text="A",variable=coder, value=1,relief=RIDGE, bg="thistle2")
    coderRB2 = Radiobutton(frame, text="B", variable=coder, value=2, relief=RIDGE, bg="thistle2")
    coderRB1.place(x=428,y=365)
    coderRB2.place(x=550,y=365)
    coderButton = Button(frame, text="Done", height=1, width=7, relief = RAISED, bg="firebrick3", command=startProcess)
    coderButton.place(x=465, y=360)
    compButton = Button(frame, text="Compare \n Labels", height=2, width=9, relief=RAISED, bg="green4", command=compareLabels)
    compButton.place(x=365, y=400)
    startButton = Button(frame,text="Load \n Images", height=2,width=9,relief=RAISED,bg="green4", state=DISABLED,command=loadImage)
    startButton.place(x=460,y=400)
    auto = Button(frame,text="Auto \n Classify", height=2,width=9,relief=RAISED,bg="green4",command=autoClassify)
    auto.place(x=555,y=400)
    category = IntVar()
    question = Label(frame, text="Choose the class and click on Classify")
    question.place(x=394,y=465)
    rb1 = Radiobutton(frame, text="Doubles",variable=category, value=1,relief=RIDGE, bg="thistle2",state=DISABLED, command=popUp)
    rb1.place(x=415,y=490)
    rb2 = Radiobutton(frame, text="No Doubles",variable=category, value=2,relief=RIDGE, bg="thistle2",state=DISABLED, command=popUp)
    rb2.place(x=515,y=490)

    previousButton = Button(frame,text="Previous", height=1,width=8,relief=RAISED,bg="purple3",state=DISABLED,command=loadPrevious)
    previousButton.place(x=360,y=537)
    classifyButton = Button(frame,text="Classify", height=2,width=10,relief=RAISED,bg="SkyBlue1",state=DISABLED,command=classify)
    classifyButton.place(x=452,y=530)

    nextButton = Button(frame, text="Next", height=1, width=8, relief=RAISED, bg="purple3", state=DISABLED, command=loadNext)
    nextButton.place(x=560, y=537)
    codedImageLabel = Label(frame,text="Coded Sets",height=1,width=15,relief=RIDGE)
    codedImageLabel.place(x=330,y=585)
    codedImageNumber = Label(frame,text="-", height=1,width=7,relief=SUNKEN,bg="gold2")
    codedImageNumber.place(x=442,y=585)
    remImageLabel = Label(frame, text="Remaining Sets", height=1, width=15, relief=RIDGE)
    remImageLabel.place(x=500, y=585)
    remImageNumber = Label(frame, text="-", height=1, width=7, relief=SUNKEN, bg="gold2")
    remImageNumber.place(x=612, y=585)
    exitButton = Button(frame, text="Exit", height=1,width=10, relief=RAISED,bg="red",command=quit)
    exitButton.place(x=455,y=620)
    frame.pack(fill=BOTH, expand =True,side=TOP)

    root.mainloop()

if __name__ == '__main__':
    main()
