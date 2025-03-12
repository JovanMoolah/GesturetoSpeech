import ultralytics
from ultralytics import YOLO
import torch

#Checks if CUDA GPU is available
#If GPU is not availabel, download Torch libaray instead to use cpu for training
'''
if torch.cuda.is_available():
    print("GPU is available")
else:
    print("GPU is not available")   
'''

#Trains pretrained model with dataset
model = YOLO('yolov8x-pose.yaml').load('yolov8x-pose.pt')
if __name__ == '__main__':
    results = model.train(data=r'F:\kjldovpnqbd38out\data.yaml', epochs=75, imgsz=576, plots=True, batch=16, translate = 0, erasing = 0, scale =1) 

#Resume training or validate model
'''
model = YOLO (r'L:\Python Data\PoseTesting\PoseTesting\runs\detect\train5\weights\best.pt')
if __name__ == '__main__':
    #results = model.train(resume=True) # Resume training
    metrics = model.val()
'''
