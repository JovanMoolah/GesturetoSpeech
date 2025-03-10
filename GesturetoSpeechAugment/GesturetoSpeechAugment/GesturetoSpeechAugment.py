
from re import S

import ultralytics

import supervision as sv

import cv2

import random

from ultralytics import YOLO

from roboflow import Roboflow

from matplotlib import pyplot as plt

import albumentations as A

import numpy as np

import os

from sklearn.model_selection import train_test_split

from tqdm import tqdm

import os




#Uncomment to download Dataset from Roboflow 
'''
rf = Roboflow(api_key="rnDx69TSkP9qRvzAtngq")
project = rf.workspace("mkjahf").project("kjldovpnqbd")
version = project.version(27)
dataset = version.download("yolov8")
          
'''            
 



#Uncomment to start Augmentation pipeline for dataset
'''
#Define Augmentations for dataset
          
global h 
h = 640                #Size of image based on dataset image sizwe

global numaug
numaug = 1             #Multiplier for Augments


imagefold = r'T:\Current Data\kjldovpnqbd37outb_latest\train\images'                               #input folder that contains dataset images
antfold = r'T:\Current Data\kjldovpnqbd37outb_latest\train\labels'                                 #ouput folder for labels of the augmented data
outfold = r'F:\PythonDataFast\PoseTestingLaterVersion\PoseTestingLaterVersion\kjldovpnqbd38out'    #ouput folder for images of the augmented data


#datasets were transformed separately and then combined
#-------------------------------------------------------------------------------------------------------------------------------
#outfold = r'F:\PythonDataFast\PoseTestingLaterVersion\PoseTestingLaterVersion\kjldovpnqbd37outb'

#housefolder = r'F:\PythonDataFast\PoseTestingLaterVersion\PoseTestingLaterVersion\House_Room_Dataset'

housefolder= r'T:\Current Data\Combined_Dataset_latest'

#colourfolder = r'F:\PythonDataFast\PoseTestingLaterVersion\PoseTestingLaterVersion\Colour Dataset'

#colorclassificationfoler = r'F:\PythonDataFast\PoseTestingLaterVersion\PoseTestingLaterVersion\ColorClassification'

#colourfolder= r'F:\PythonDataFast\PoseTestingLaterVersion\PoseTestingLaterVersion\Colour-Null-1'
#-------------------------------------------------------------------------------------------------------------------------

LISTROOM = []
LISTCOL = []

#def resize_img():                                     #Resize images in folder                 

   # output = r'F:\PythonDataFast\PoseTestingLaterVersion\PoseTestingLaterVersion\Resized_ColorClassification_Dataset'
    #for room in os.listdir (colorclassificationfoler ):
       # roomfolder = os.path.join(colorclassificationfoler , room)
        #for roomtype in os.listdir(roomfolder):
          #  if not roomtype.endswith(".jpg"):
           #     continue
            #image_path = os.path.join(roomfolder, roomtype)
            #image = cv2.imread(image_path)
            #resized_image = cv2.resize(image, (640, 640))
            
            #os.makedirs(output, exist_ok=True)
            #filename = os.path.basename(image_path)
            #output_path = os.path.join(output, filename)
           # cv2.imwrite(output_path, resized_image)

           # print(f"Resized image saved to {output_path}")
#resize_img()


for room in os.listdir (housefolder):                              #Append images to List in numpy format
        roomfolder = os.path.join(housefolder, room)
        for roomtype in os.listdir(roomfolder):
            if not roomtype.endswith(".jpg"):
                continue
            image_path = os.path.join(roomfolder, roomtype)
 
            Ref = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
            LISTROOM.append(Ref)

            #print (Ref)

#for room in os.listdir (colourfolder):                          #Appends images to List in numpy format
   #     roomfolder = os.path.join(colourfolder, room)
      #  for roomtype in os.listdir(roomfolder):
        #    if not roomtype.endswith(".jpg"):
         #       continue
         #   image_path = os.path.join(roomfolder, roomtype)
 
         #   Refcol = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
           # LISTCOL.append(Refcol)
       

#Augmentation Transoforms Parameters 
#Check https://github.com/albumentations-team/albumentations for more information about tranforms                       
transform = A.Compose([
    A.ShiftScaleRotate(shift_limit= (0,0), rotate_limit=(0,0),scale_limit=(-0.3, 0),border_mode = cv2.BORDER_REPLICATE, p=0.5), 
    A.Affine(scale=(0.7,1), shear= (-5,5), mode = 1, p=0.3),
    A.GaussianBlur(blur_limit = (1, 3), p=0.25),
    A.GaussNoise(var_limit= (5.0, 15.0), p=0.25),
    A.RandomBrightnessContrast(brightness_limit=(-0.1, 0.1), contrast_limit =(-0.1, 0.1), p=0.25),
    A.HueSaturationValue (hue_shift_limit = (-15, 15), sat_shift_limit = (-15, 15), val_shift_limit = (-10, 10),  p= 0.25),
    A.HistogramMatching (reference_images=LISTROOM, read_fn=lambda x: x, p=0.5, blend_ratio=(0.1, 0.5))  
     

    #A.TemplateTransform(templates=LISTROOM, img_weight=0.5, template_weight= 0.75, p=1)        #The above transforms should be commented when using this transform


], bbox_params=A.BboxParams(format='yolo', label_fields=['classlabels'], min_visibility=0.2),
   keypoint_params=A.KeypointParams(format='xy', remove_invisible=False))
   


def transformdata(image_files, imagefold, antfold, outfold):      #Function to transform data 
  numaug
  h
  
  imgdir = os.path.join(outfold, 'images')                        #Creates image and label file directories
  os.makedirs(imgdir, exist_ok=True)
  
  labeldir = os.path.join(outfold, 'labels')
  os.makedirs(labeldir, exist_ok=True)
  
  for imgname in tqdm(image_files):                               #Save information from original files
       imgpath = os.path.join(imagefold, imgname)     
       antpath = os.path.join(antfold, os.path.splitext(imgname)[0] + '.txt') 
       
       image = cv2.imread(imgpath)                                 #Read image files 
       bboxes = []                                                 #Initialize empty variables
       classlabels = []
       keypoints = []
       with open(antpath, 'r') as f:                               #Read label files
           for line in f:
                 data = list(map(float, line.strip().split()))     #Split data 
                 if len(data) == 68:                               #Checks if their is 68 labels in label file
                      class_id = int (data[0])                     #First label is the class name
                      classlabels.append(class_id)
                      #bbox = data[1:5]                            #Labels 2 to 5 is Box width, height, X, Y coordinates
                      bbox = [(data[1]), (data[2]), (data[3]), (data[4])]
                      bboxes.append(bbox)
                      keypoint_data = data[5:]                      #Labels 6 to 68 is the 21 keypoints devided into X,Y coordinates and visibilty status
                      for i in range(0, len(keypoint_data), 3):     
                           kdata = [h*keypoint_data[i], h*keypoint_data[i+1], keypoint_data[i+2]]  
                           keypoints.append (kdata)                  
                 else:
                   print("invalid format")
        
       for i in range(numaug):
          augmented = transform(image=image, classlabels=classlabels, bboxes=bboxes, keypoints=keypoints)   #Transofrm the data with transform function
          image = augmented['image']                                                                        #Paste and write the saved information to the label files for transformed data        
          classlabels = augmented['classlabels']
          bboxes = augmented['bboxes']
          keypoints = augmented['keypoints']
      
          augimgpath = os.path.join(imgdir, f"{os.path.splitext(imgname)[0]}_aug_{i}.jpg")
          cv2.imwrite( augimgpath, image)
      
          auglabpath = os.path.join(labeldir, f"{os.path.splitext(imgname)[0]}_aug_{i}.txt")
          with open(auglabpath, 'w') as f:
               for label,bbox in zip(classlabels, bboxes):
                    x, y, width, height = bbox
                    f.write(f"{label} {x} {y} {width} {height} ")
               for kp in keypoints:
                     #for i in range (0, len(kp), 1):
                       #for val in kp:
                       #val = kp[0]/360, kp[1]/360, kp[2]
                       #f.write(f"{val} ")
                        f.write(f"{kp[0]/h} ")
                        f.write(f"{kp[1]/h} ")
                        f.write(f"{kp[2]} ")

            
def augment(imagefold, antfold, outfold):                               #Splits dataset in train,test,val and then call transform function
  files = []
  for f in os.listdir(imagefold):
    files.append(f)
      
  train, test = train_test_split(files, test_size=0.2, random_state=0)
  train, val = train_test_split(train, test_size=0.125, random_state=0)

  #train, test = train_test_split(files, test_size=0.000001, random_state=0)        #Puts all images in train dataset
  #train, val = train_test_split(train, test_size=0.000001, random_state=0)
       
  trainout = os.path.join(outfold,'train')
  os.makedirs(trainout, exist_ok=True)
  print("Train Images")
  transformdata(train, imagefold, antfold, trainout)

  valout = os.path.join(outfold, 'val')
  os.makedirs(valout, exist_ok=True)
  print("Valid Images")
  transformdata(val, imagefold, antfold, valout)

  testout = os.path.join(outfold, 'test')
  os.makedirs(testout, exist_ok=True)
  print("Test Images")
  transformdata(test, imagefold, antfold, testout)
    

augment(imagefold, antfold, outfold)                                #Start Augmentation
'''




#Uncomment to test and visualize augments for one image
'''
#image = cv2.imread('test.jpg')                                     #Show original image 
#cv2.imshow("NAME", image)
#cv2.waitKey(0)

KEYPOINT_COLOR = (0, 255, 0) # Green

def vis_keypoints(image, keypoints, xx,yy, ww, hh, color=KEYPOINT_COLOR, diameter=5):      #Function to map bounding box and keypoints coordinates on image
    image = image.copy()

    for (x, y) in keypoints:
        cv2.circle(image, (int(x), int(y)), diameter, (0, 255, 0), -1)

    cv2.rectangle(image, (int (xx-ww/2), int (yy-hh/2)),  (int (xx+ww/2), int(yy+hh/2)) , (255,255,255), 2)     
    plt.figure(figsize=(8, 8))
    plt.axis('off')
    plt.imshow(image)
    plt.show()
   

image = cv2.imread('test.jpg')                                   #Load image file  
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
h, w, _ = image.shape


bboxes = []
classlabels = []
keypoints = []

with open('test.txt', 'r') as f:                                 #Load label file   
    for line in f:
            data = list(map(float, line.strip().split()))
            if len(data) == 68: 
                class_id = int (data[0])
                classlabels.append(class_id)
                bbox = data[1:5]
                bboxes.append(bbox)
                keypoint_data = data[5:]
                for i in range(0, len(keypoint_data), 3):
                    kdata = [keypoint_data[i], keypoint_data[i+1],keypoint_data[i+2]]  
                    keypoints.append (kdata) 

keypoints = [(h*a, h*b) for a, b, c in keypoints]  
box = bboxes[0]  
xx,yy, ww, hh = box
print (bboxes)
print (w)
xx = h*xx
yy = h*yy
ww = h*ww
hh = h*hh
vis_keypoints(image, keypoints, xx,yy,ww,hh)                      #Show orgianl image with bouding box and keypoints

                                                                   
transform = A.Compose([                                           #Test Augments
     A.ShiftScaleRotate(shift_limit= (0,0), rotate_limit=(0,0),scale_limit=(-0.4, 0),border_mode = cv2.BORDER_REPLICATE, p=0),   
     A.Affine(scale=1, shear= (-15,15), mode = 1, p=1)],
     keypoint_params=A.KeypointParams(format='xy')   
)

transformed = transform(image=image, keypoints=keypoints)
vis_keypoints(transformed['image'], transformed['keypoints'], xx,yy,ww,hh)  #Show transformed image with bounding box and keypoints     
'''




