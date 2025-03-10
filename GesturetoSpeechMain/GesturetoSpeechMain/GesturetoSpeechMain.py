
from re import S

import ultralytics

import supervision as sv

import cv2

import random

from ultralytics import YOLO

from roboflow import Roboflow

from matplotlib import pyplot as plt

import numpy as np

import torch

import os

from itertools import groupby

import argostranslate.package

import argostranslate.translate

import streamlink

import csv

import os

import sys

from PySide6.QtCore import Qt, QThread, Signal, Slot, QLocale, QSignalBlocker

from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap, QTextCursor

from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)

from PySide6.QtTextToSpeech import QTextToSpeech, QVoice


from UIForHand import Ui_MainWindow            #This file contains the configuration for the UI.

import pyperclip




#Download code for languages. Use https://github.com/argosopentech/argos-translate/blob/master/argostranslate/languages.csv to find codes 
#Download languages and voices from Windows Language settigns
'''
from_code = "en"
to_code = "ja"

# Download and install Argos Translate package
#argostranslate.package.update_package_index()

available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())


Translate = argostranslate.translate.translate("Hello World", from_code, to_code)
print(Translate)

'''


class Detection (QThread):                                  #Thread used for streaming 
    
    frameupdate = Signal (QImage)                           #Initialize variables
    listsend = Signal (str) 
    temp = 0
    source_folder = ''
    
    model = YOLO('runs/pose/train/weights/best.pt')         #Load the trained model

    def __init__(self, parent=None):                        #Intialize default variables to start stram
        QThread.__init__(self, parent)
        self.status=True
        self.source = "0"
        self.cap = cv2.VideoCapture(self.source)
        
        
    def end (self):
        self.status = False                                 #End stream
        self.cap.release()
        

    def stream_to_url(self, url, quality='best'):           #Define url and quality for livestreaming
        streams = streamlink.streams(url)
        if streams:
            return streams[quality].to_url()
        else:
            raise ValueError("No steams were available")

     
    def Webcam (self):                                     #Use webcam as streaming source
        self.status = True
        self.cap = cv2.VideoCapture(0)
        
   
    def Livestream (self):                                 #Use online livestreame as streaming source
        self.status = True
        stream_url = self.stream_to_url(self.source_folder, 'best')
        self.cap = cv2.VideoCapture(stream_url)
        

    #Reference:https://doc.qt.io/qtforpython-6/examples/example_external_opencv.html#opencv-face-detection-example

    def StreamPredict(self):                              #Prediciton function for webcam or livestream
            
        while self.status:                                #Run streaming indefinetly                         

            ret, frame = self.cap.read()                  #Read frames in stream

            if ret is False:                              #Stop streaming if status is false
               break
    
            results = self.model.predict(frame, conf = 0.6, show=False)        #Run inference on webcam or livestream at 0.6 IoU
            names = self.model.names
            
            annotated_frame = results[0].plot()             
            color_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)      #Read the image in RGB 
      
            h, w, ch = color_frame.shape            
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)  #Convert image in QImage format for UI display
            img = img.scaled(640, 480, Qt.KeepAspectRatio)              #Scale frame to Screen Size
            
            
            for r in results:  
                for box in r.boxes.cls:                   #Load prediciton results
                    
                    c = (names[int(box)]) 
                    if (c == "space"):                    #Changes'space' classname to ' ' 
                        c = " "     
                    self.listsend.emit(str (c))           #Send class prediction to gesture capture for processing
                    
            self.frameupdate.emit(img)                    #Send frame image for processing
        #self.cap.release()
         
           
    def Video(self):                                      #Use video as stream source
        
            self.status = True
            
            video_folder= r''.join(self.source_folder)    
            
            for video_name in os.listdir(video_folder):    #Loads videos from folder
                
                if not video_name.endswith((".mpg",".mpeg4"))  :
                    continue
                video_path = os.path.join(video_folder, video_name)    
                
                video = cv2.VideoCapture(video_path)      #Run videos 
                
                while self.status:                        #Run videos indefinetly
                    
                    ret, frame = video.read()             #Stop current video is status is false
                    if not ret:
                         break   
                    
                    cv2.waitKey(1)                        #Speed to read video frames
                    
                    w = int(frame.shape[1] * 1)            
                    h = int(frame.shape[0] * 1)
                    resized = cv2.resize(frame, (w,h))   #Resize video frame to preference
                    
                    results = self.model.predict(resized, conf = 0.6, show=False)       #Run inference on video at 0.6 IoU
                    names = self.model.names
                    
                    annotated_frame = results[0].plot()
                    color_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)      #Read the image in RGB 
                    
                    h, w, ch = color_frame.shape
                    img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)  #Convert image in QImage format for UI display
                    img = img.scaled(640, 480, Qt.KeepAspectRatio)                      #Scale video frame to screen size
                    
                    self.frameupdate.emit(img)            #Send frame image for processing 
                video.release()
                
                
    def Image(self):                                     #Use image as stream source
        
            self.status = True
            
            image_folder= r''.join(self.source_folder)   
            
            for image_name in os.listdir(image_folder):   #Load Images from folder

                if not image_name.endswith((".png",".jpg",".JPG"))  :
                    continue
                image_path = os.path.join(image_folder, image_name)  
                
                if self.status == False:                  #Stop loading images from folder if status is false
                    break

                frame =cv2.imread(image_path)             #Read an image

                w = int(frame.shape[1] * 1)
                h = int(frame.shape[0] * 1)
                resized = cv2.resize(frame, (w,h))        #Resize Image to preference
                
                results = self.model.predict(resized, conf = 0.6, show=False)        #Run inference on image at 0.6 IoU
                names = self.model.names
                
                annotated_frame = results[0].plot()
                color_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
                h, w, ch = color_frame.shape
                img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
                #img = img.scaled(640, 480, Qt.KeepAspectRatio)                      #Scale image to screen size

                for r in results:
                    for box in r.boxes.cls:
               
                        c = (names[int(box)]) 
                        if (c == "space"):
                            c = " "  
                            
                        with open ('Pred.csv', 'a', newline="") as f:  #Predicted classes are save in a file. 
                            writer= csv.writer (f)                     #Used to evaluate image datasets
                            writer.writerows (c)
                        #self.listsend.emit(str (c))
        
                self.frameupdate.emit(img)              #Send frame image for processing 
                
                cv2.waitKey(1)                          #Speed to read images              
                

    def run(self):                                      #Run streaming sources based on UI selection
        
        if self.temp == 0:
           self.Webcam()   
           self.StreamPredict()

        elif self.temp ==1:
            self.Video()

        elif self.temp ==2:
            self.Image()
            
        elif self.temp ==3:     
           self.Livestream()
           self.StreamPredict()



class Window(QMainWindow):                             #Main Thread used for all UI functions 
    
    textappendmain = Signal (str)                      #Initialsze all strings and List
    ValueM = ''
    ValueM2 = ''
    ValueM3 = ''
    ValueJ = ''
    RecordZ = ''
    FrameRecord = []
    FrameCount = []
    LastCount = []
    RECORD = []
    gest = []
    Current = ''
    
 
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()                       #Load Configurations from UI Python file
        self.ui.setupUi(self)
                                                       
        #UI Functions__________________________________ #Define variables for UI functions
        self.det = Detection (self)
        
        self.speech = QTextToSpeech (self)
        
        self.speechTrans = QTextToSpeech (self)
        
        self.input_voices = []
        
        self.output_voices = []
        
        self.InitialiseLanguages ()
 
        self.InitialiseLanguagesTrans ()
        
        self.IntialiaseGesture()
        
        self.IntialiaseStream()
        
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End)

        self.ui.Translate.setCheckable(True)
        
        self.ui.concurrentbut.setCheckable (True)
        
        #___________________________________________________________________________________
        
        #Connections____________________________________ Define signal connection for slot functions
        self.det.frameupdate.connect(self.setImage)
        
        self.textappendmain.connect (self.appendText)
 
        self.ui.start.clicked.connect (self.start)
        self.ui.stop.clicked.connect (self.end)
        
        self.ui.pitch.valueChanged.connect(self.set_Pitch)
        self.ui.rate.valueChanged.connect(self.set_Rate)
        self.ui.volume.valueChanged.connect(self.set_Volume)
        
        self.ui.input_voice.currentIndexChanged.connect(self.select_Voice)
        self.ui.input_language.currentIndexChanged.connect(self.select_Language)
        
        self.ui.output_voice.currentIndexChanged.connect(self.select_VoiceTrans)
        self.ui.output_language.currentIndexChanged.connect(self.select_LanguageTrans)
        
        self.speech.localeChanged.connect(self.locale_changed)
        self.speechTrans.localeChanged.connect(self.locale_changedTrans)
        
        self.ui.speak_start.clicked.connect(self.startSpeak)
        self.ui.speak_stop.clicked.connect(self.stopSpeak)
        self.ui.pause.clicked.connect(self.pauseSpeak)
        self.ui.resume.clicked.connect(self.resumeSpeak)
                   
        self.ui.clear.clicked.connect(self.clearText)
        
        self.ui.Translate.clicked.connect(self.Toggle)
        
        self.ui.concurrentbut.clicked.connect (self.TogCon)
        
        self.det.listsend.connect (self.processlist)
        
        self.ui.Gesture.currentIndexChanged.connect (self.mapNames)
        
        self.ui.Mapping.textEdited.connect (self.changeMapping)
        
        self.ui.Stream_Type.currentIndexChanged.connect (self.running)
        
        self.ui.Synchronize.clicked.connect(self.Sync)
        
        #_________________________________________________________________________________

  

    def IntialiaseStream (self):                         # Initailze stream source        
        Stm = []
        Stm = ('Webcam', 'Video', 'Image','Livestream')
        for s in Stm:
            self.ui.Stream_Type.addItem (s)


    @Slot (int)                                          #Select current stream source
    def running (self):   
        if self.ui.Stream_Type.currentIndex() == 0:
           self.det.temp = 0
           #print ('say webcam')
    
        elif self.ui.Stream_Type.currentIndex() == 1:     
            self.det.temp = 1
            #print (self.ui.Stream_Type.currentIndex())
            
        elif self.ui.Stream_Type.currentIndex() == 2:  
            self.det.temp = 2
        
        elif self.ui.Stream_Type.currentIndex() == 3:
            self.det.temp = 3


    @Slot (str)                                        #MIGHT BE DEAD          
    def TestValue (self, testing):
        self.ui.translated_text.appendPlainText(testing)

   
    def Toggle(self):                                  #Toggle on/off translate button
        if self.ui.Translate.isChecked():
            self.ui.Translate.setText ("On")
        else:
            self.ui.Translate.setText ("Off")
            
        self.ui.inputted_text.setFocus()               #Automatically sets the cursor postion to visible at the end of input text after executing a function 
        self.ui.inputted_text.moveCursor(QTextCursor.End)     
        
    
    def TogCon (self):                                #Toggle on/off concurrent button
        if self.ui.concurrentbut.isChecked():
            self.ui.concurrentbut.setText ("On")
        else:
            self.ui.concurrentbut.setText ("Off")
            
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End)        
     

    def IntialiaseGesture (self):                    #Initialisze gesture class names from loaded model 
        #print (self.det.model.names)    
        #self.gest.append(self.det.model.names)
        for m in self.det.model.names.values():
                self.gest.append (m[0]) 
                  
        self.gest [13] = 'delete'                     #Some gestures are manually set as class name contains only the first letter
        self.gest [15] = 'enter'
        self.gest [20] = 'j4'
        self.gest [36] = 'z1'
        self.gest [37] = 'z2'
                
        for g in self.gest: 
            self.ui.Gesture.addItem (g)               #Add class names to combo box
            

    @Slot (int)                                       #Initialze gesture mapping
    def mapNames (self, map):
        self.ui.Mapping.setText (self.gest [map])
        
    def ActualMap (self, txt ):                       #Set gesture names to default map or user-defined maps
       if txt == '1':
           self.Current = self.gest[0]
       elif txt == '2':
           self.Current = self.gest[1]
       elif txt == '3':
           self.Current = self.gest[2]
       elif txt == '4':
           self.Current = self.gest[3]    
       elif txt == '5':
           self.Current = self.gest[4]
       elif txt == '6':
           self.Current = self.gest[5]
       elif txt == '7':
           self.Current = self.gest[6]
       elif txt == '8':
           self.Current = self.gest[7]
       elif txt == '9':
           self.Current = self.gest[8]
       elif txt == 'a':
           self.Current = self.gest[9]    
       elif txt == 'b':
           self.Current = self.gest[10]
       elif txt == 'c':
           self.Current = self.gest[11]
       elif txt == 'd':
           self.Current = self.gest[12]       
       elif txt == 'delete': 
           self.Current = self.gest [13]            
       elif txt == 'e':
           self.Current = self.gest[14]      
       elif txt == 'enter':
           self.Current = self.gest [15]     
       elif txt == 'f':
           self.Current = self.gest[16]
       elif txt == 'g':
           self.Current = self.gest[17]
       elif txt == 'h':
           self.Current = self.gest[18]
       elif txt == 'i':
           self.Current = self.gest[19]
                                                       #Comment and go txt=='j' to test motion for dynamic gesture
       elif txt == 'j4':                               #Change dynamic gesture to be read as j only
           #self.Current = self.gest[20]
            self.Current = 'j'
           
       elif txt == 'k':
           self.Current = self.gest[21]  
       elif txt == 'l':
           self.Current = self.gest[22]
       elif txt == 'm':
           self.Current = self.gest[23]
       elif txt == 'n':
           self.Current = self.gest[24]    
       elif txt == 'o':
           self.Current = self.gest[25]
       elif txt == 'p':
           self.Current = self.gest[26]
       elif txt == 'q':
           self.Current = self.gest[27]
       elif txt == 'r':
           self.Current = self.gest[28]    
       elif txt == 's':
           self.Current = self.gest[29]
       elif txt == ' ':
           self.gest[30] = " "
           self.Current = self.gest[30]
       elif txt == 't':
           self.Current = self.gest[31]
       elif txt == 'u':
           self.Current = self.gest[32]    
       #elif txt == 'v':
        #   self.Current = self.gest[33]
       elif txt == 'w':
           self.Current = self.gest[33]
       elif txt == 'x':
           self.Current = self.gest[34]
       elif txt == 'y':
           self.Current = self.gest[35]
                                                      #Comment and go txt=='z' to test motion for dynamic gesture
       elif txt == 'z1':                              #Change dynamic gesture to be read as z only   
           #self.Current = self.gest[36]
            self.Current ='z'
           
       elif txt == 'z2':                              #Change dynamic gesture to be read as z only  
           #self.Current = self.gest[37]
           self.Current = 'z'
           
       #elif txt == 'j':                              #Uncomment to test motion for dynamic gestures 'j' and 'z'
           #self.Current = 'j'
       
       #elif txt == 'z':
           #self.Current = 'z'

    @Slot (str)                                     #Change gesture mapping to text
    def changeMapping (self, text):
        self.gest [self.ui.Gesture.currentIndex()] = text
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End) 
        
 
    #Reference: https://doc.qt.io/qtforpython-6/examples/example_speech_hello_speak.html
    def InitialiseLanguages (self):                  #Initialise locale languages for input combobox
        current = self.speech.locale()
        with QSignalBlocker(self.ui.input_language):
            self.ui.input_language.clear()  
            locales = self.speech.availableLocales()         #Populate the languages combobox before connecting its signal.
            for locale in locales:
                lang = QLocale.languageToString(locale.language())
                territory = QLocale.territoryToString(locale.territory())
                self.ui.input_language.addItem(f"{lang} ({territory})", locale)
                if locale.name() == current.name():
                    current = locale     
        self.locale_changed(current)  
        

    def InitialiseLanguagesTrans (self):              #Function to initialise locale languages for translated combobox
        current = self.speechTrans.locale()
        with QSignalBlocker(self.ui.output_language):
            self.ui.output_language.clear()
            locales = self.speechTrans.availableLocales()     
            for locale in locales:
                lang = QLocale.languageToString(locale.language())
                territory = QLocale.territoryToString(locale.territory())
                self.ui.output_language.addItem(f"{lang} ({territory})", locale)
                if locale.name() == current.name():
                    current = locale
        self.locale_changedTrans(current)            #For more languages, download from Windows language settings and reload application 

    @Slot(int)                                       #Set pitch parameters
    def set_Pitch (self, pitch):
        self.speech.setPitch (pitch / 10)
        self.speechTrans.setPitch (pitch / 10)
        

    @Slot(int)                                       #Set rate parameters
    def set_Rate (self, rate):
        self.speech.setRate (rate / 10)
        self.speechTrans.setRate (rate / 10)
        

    @Slot(int)                                       #Set volume parameters  
    def set_Volume(self, volume):
        self.speech.setVolume (volume / 20)  
        self.speechTrans.setVolume (volume / 20) 
        

    @Slot (int)                                      #Select input language locale
    def select_Language (self, lng):
        self.speech.setLocale(self.ui.input_language.itemData(lng))
    

    @Slot (int)                                      #Select translated language locale
    def select_LanguageTrans (self, lng):
        self.speechTrans.setLocale(self.ui.output_language.itemData(lng))    
     

    @Slot (int)                                      #Select input language voice
    def select_Voice (self, vc):
        self.speech.setVoice(self.input_voices[vc]) 
    

    @Slot (int)                                      #Select translated language voice
    def select_VoiceTrans (self, vc):
        self.speechTrans.setVoice(self.output_voices[vc]) 
        
        
    #Reference: https://doc.qt.io/qtforpython-6/examples/example_speech_hello_speak.html 
    @Slot(QLocale)                                    #Initialize voices for input language combobox
    def locale_changed(self, locale):
        self.ui.input_language.setCurrentIndex(self.ui.input_language.findData(locale))
        with QSignalBlocker(self.ui.input_voice):
            self.ui.input_voice.clear()
            self.input_voices = self.speech.availableVoices()
            current_voice = self.speech.voice()
            for v in self.input_voices:
                name = v.name()
                gender = QVoice.genderName(v.gender())
                #age = QVoice.ageName(v.age())
                self.ui.input_voice.addItem(f"{name} - {gender} ")
                if v.name() == current_voice.name():
                    self.ui.input_voice.setCurrentIndex(self.ui.input_voice.count() - 1)
                    

    @Slot(QLocale)                                    #Initialize voices for translated language combobox
    def locale_changedTrans(self, locale):
        self.ui.output_language.setCurrentIndex(self.ui.output_language.findData(locale))
        with QSignalBlocker(self.ui.output_voice):
            self.ui.output_voice.clear()
            self.output_voices = self.speechTrans.availableVoices()
            current_voice = self.speechTrans.voice()
            for v in self.output_voices:
                name = v.name()
                gender = QVoice.genderName(v.gender())
                #age = QVoice.ageName(v.age())
                self.ui.output_voice.addItem(f"{name} - {gender} ")
                if v.name() == current_voice.name():
                    self.ui.output_voice.setCurrentIndex(self.ui.output_voice.count() - 1)  #For more voices, download from Windows language settings and reload application
                    

    @Slot ()                                           #Start speaking
    def startSpeak (self):
        if self.ui.Translate.isChecked():              #Checks if translate button is on
                                                                   
            current = self.speech.locale()             #Supported languages for input language. 
            lang = QLocale.languageToString(current.language())
            if lang == 'English':
                lang = 'en'
            elif lang == 'French':
                lang = 'fr'
            elif lang == 'Spanish':
                lang = 'es'
            elif lang == 'German':
                lang = 'de' 
            #elif lang == 'Japanese':                  #Tried Japanese but characters have to be Roman
              #  lang = 'ja'
                print (lang)  

            currentTrans = self.speechTrans.locale()   #Supported languages for translated language.    
            langTrans = QLocale.languageToString(currentTrans.language())
            if langTrans == 'English':
                langTrans = 'en'
            elif langTrans == 'French':
                langTrans = 'fr'
            elif langTrans == 'Spanish':
                langTrans = 'es'     
            elif langTrans == 'German':
                langTrans = 'de'
            #elif lang == 'Japanese':
               # lang = 'ja'
                print (langTrans)                      #For more langauges, download lanugages from Argos translated package and language code  
    
            Translate = argostranslate.translate.translate(self.ui.inputted_text.toPlainText(), lang, langTrans)
            self.ui.translated_text.setPlainText(Translate)
            self.speechTrans.say (self.ui.translated_text.toPlainText())   #Speak function pronounces translated text
            
        else:  
            self.speech.say (self.ui.inputted_text.toPlainText())          #Speak function pronounces input text
    
        self.ui.inputted_text.setFocus()                                   
        self.ui.inputted_text.moveCursor(QTextCursor.End)             

            
    @Slot()                                            #Stop speaking
    def stopSpeak (self):
        if self.ui.Translate.isChecked():
            self.speechTrans.stop()
            self.ValueM=''
        else:
            self.speech.stop()
            self.ValueM = ''
            
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End) 
        

    @Slot()                                            #Pause speak
    def pauseSpeak (self):
        if self.ui.Translate.isChecked():
            self.speechTrans.pause()
        else:
            self.speech.pause()
            

    @Slot()                                           #Resume speak
    def resumeSpeak (self):
        if self.ui.Translate.isChecked():
            self.speechTrans.resume()
        else:
            self.speech.resume()

    
    @Slot()                                           #Clear text in input and translated textbox
    def clearText (self):
        self.ui.inputted_text.clear()
        self.ui.translated_text.clear()
        self.RECORD.clear()
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End) 
        
        
    @Slot ()                                          #Synchronize Record if textbox is manually edited
    def Sync(self):
        self.ui.inputted_text.selectAll()
        self.ui.inputted_text.copy()
        self.RECORD.clear()
        self.RECORD =  (list(pyperclip.paste()))
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End)

    
    @Slot (str)                                       #Appends text from RECORD to textbox
    def appendText(self,text):
         
           self.ActualMap (text)                             
           
           if self.Current == 'o' and self.RECORD [-1] in ['0','1','2','3','4','5','6','7','8','9']:
              self.Current = '0'                      #Changes context for current gesture 'o' or '0' if the previous gessture was a number 

           if self.Current == '2' and self.RECORD [-1] in ['a','b','c','d','e','f','g','h','i','f','k','l','m','n','o','p','q','r','t','v','w','x','y','z']:
              self.Current = 'v'                      #Changes context for current gesture '2' or 'v' if the previous gessture was a letter 
       
           if self.Current == self.gest[15]:          #Start speak if current gesture is enter   
               self.startSpeak()
               self.RECORD.clear()
               self.ui.inputted_text.clear()
               self.ui.translated_text.clear()
               self.ui.inputted_text.setFocus()
               self.ui.inputted_text.moveCursor(QTextCursor.End)
               self.FrameRecord.clear()
               self.FrameCount.clear()
               
           elif self.Current == self.gest[13]:        #Delete text from input textbox if current gesture is delete
              self.RECORD.pop()
              self.ui.inputted_text.setPlainText(''.join(self.RECORD))
              self.ui.inputted_text.moveCursor(QTextCursor.End)
              self.FrameRecord.clear()
              self.FrameCount.clear()
               
           else:                                      #Appened text to textbox for all static gestures 
               self.RECORD.append (self.Current) 
               self.ui.inputted_text.insertPlainText (self.RECORD[-1])  
               self.FrameRecord.clear()
               self.FrameCount.clear()
               
           
           #self.RECORD.append (text)                                    #Commented code that test append function without gesture map function
           #self.ui.inputted_text.insertPlainText (self.RECORD[-1])  
           #self.FrameRecord.clear()
           #self.FrameCount.clear()
           
  
           if self.ui.concurrentbut.isChecked():        #If concurrent is on, speak function prounces each word in real-time
               self.ui.translated_text.insertPlainText (self.RECORD[-1])
               if self.Current.endswith(' '):  
                    self.speech.say (self.ui.translated_text.toPlainText())   
                    self.ui.translated_text.clear()
                            
          
    @Slot(str)                                           #Insert text to input textbox
    def setText(self, text):
        self.ui.inputted_text.insertPlainText (text)
        
 
    @Slot(QImage)                                       #Display image using emitted img from stream source
    def setImage(self, image):
        self.ui.Display.setPixmap(QPixmap.fromImage(image)) 

    
    @Slot (str)   
    def processlist(self, valuesent):                          #function to prcosses gestures detected from the stream
        self.FrameRecord.append(valuesent)                     #string class name of detected gesture    
        
        for nme, cnt in groupby(self.FrameRecord):             # counts reoccuring class names
                self.FrameCount.append((nme, len(list(cnt))))  # creates a dictionary of class name and count
        self.LastCount = self.FrameCount [-1]                  # takes the most recent frame count
    
        
        
        if self.LastCount[0] == 'delete':
            if  10 < self.LastCount[1] <=15: 
                self.ValueM = ''.join(str(self.LastCount[0]))      #ValueM(1,2,3) are temporary placeholders
                self.textappendmain.emit (self.ValueM)                
              
        else:
            #Static Gestures
            if 10 <=  self.LastCount[1] <= 15 and not self.ValueM.endswith(str(self.LastCount[0])):  #Single Lettere Gloss 
            
                self.ValueM = ''.join(str(self.LastCount[0]))      #ValueM(1,2,3) are temporary placeholders
                self.textappendmain.emit (self.ValueM)             #Placeholder is sent to Record to be appended  
                             
            elif (25 <=  self.LastCount[1] <= 30 and self.ValueM.endswith(str(self.LastCount[0])) and  #Doubled Letter Gloss
                    not self.ValueM2.endswith(str(self.LastCount[0]))):
                
                    self.ValueM2 = ''.join(str(self.LastCount[0]))   
                    self.ValueM =''.join (self.ValueM2)
                    self.textappendmain.emit (self.ValueM)

            elif (45 <= self.LastCount[1] <= 50 and self.ValueM.endswith (str(self.LastCount[0])) and   #Triple letter Gloss
                    self.ValueM2.endswith(str(self.LastCount[0])) and not self.ValueM3.endswith(str(self.LastCount[0]))):
                
                    self.ValueM3 = ''.join(str(self.LastCount[0]))  
                    self.ValueM =''.join (self.ValueM3)
                    self.textappendmain.emit (self.ValueM)

                                                               #Uncomment dynamic gestures in gesture map to test z 
        #Lettering for z                        
        if self.LastCount[0] == 'z1' and 5 < self.LastCount[1] <=15 and not self.RecordZ:  
                self.RecordZ = ''.join('z1')                   #Add first sequnce gesture z1 to RecordZ
                #self.textappendmain.emit ('1st worked')       #test for errors                
                    
        elif self.LastCount[0] == 'z2' and 5 < self.LastCount[1] <=15  and self.RecordZ.endswith('z1'):
              self.RecordZ = ''.join ('z1z2')                  #Add second sequence of gesture z2 to RecordZ
              #self.textappendmain.emit ('2nd worked')
              self.ValueM =''.join ('z')                       #z is added to placeholder 
              #self.textappendmain.emit (self.ValueM)           #Placeholder is sent to Record to be appended
              self.RecordZ = ''                                #RecordZ is reset to be ready to accept the first sequence letter
        
        elif self.LastCount[0] != 'z2' and 1<= self.LastCount[1] <=5  and self.RecordZ.endswith('z1'):  
              #self.textappendmain.emit ('error1')
              pass                                             #skips additon of gesture if it is detected for less than 5 frames
             
        elif (self.LastCount[0] != 'z2' and 5 <  self.LastCount[1]) and self.RecordZ.endswith('z1'):    
            if self.LastCount[0] == 'z1':
                pass                                          #skips addition of gesture if the second sequence gesture is z1
            else:
              #self.textappendmain.emit ('error2')              
              self.RecordZ = ''.join                          #Reset RecordZ if the second sequenced gesture is not z2
              
        #Unimplemented Code for a third sequenced gesture z3                    
        #elif self.LastCount[0] == 'z3' and 5 < self.LastCount[1] <10 and self.RecordZ.endswith('z1z2'):       
              #self.RecordZ = ''.join ('z1z2z3')             #Add z3 to RecordZ if RecordZ contains member z1 and z2 
              #self.ValueM =''.join ('z')
              #self.textappendmain.emit (self.ValueM)
             ##self.textappendmain.emit ('3rd worked')
              #self.RecordZ = '' 

        #elif self.LastCount[0] != 'z3' and 1<= self.LastCount[1] <=5 and self.RecordZ.endswith('z1z2'): 
            ##self.textappendmain.emit ('error3')            
             #pass                                           #skips addition of gesture if it detected for less than 5 frames
           
        #elif (self.LastCount[0] != 'z3' and 5 < self.LastCount[1]) and self.RecordZ.endswith('z1z2'): 
            #if self.LastCount[0] == 'z2':                   
                #pass                                        #skips addition of gesture if the third sequence gesture is z2
            #else: 
              ##self.textappendmain.emit ('error4')          
              #self.RecordZ = ''                             #Reset RecordZ if the third sequence gesture is not z3  


                                                              #Uncomment dynamic gestures in gesture map to test j 
        #Lettering for j                                      #j is the same as z
        if self.LastCount[0] == 'i' and 5 < self.LastCount[1] <=10 and not self.ValueJ:
                self.ValueJ = ''.join('i')  
                #self.textappendmain.emit ('1st worked')
                
        #elif self.LastCount[0] != '4' and self.ValueI.endswith('5'):
            #    self.ValueI = ''
                    
        elif self.LastCount[0] == 'j4' and 5 < self.LastCount[1] <=10  and self.ValueJ.endswith('i'):
              self.ValueJ = ''.join ('ij4') 
              #self.textappendmain.emit ('2nd worked')
              self.ValueM =''.join ('j')
              #self.textappendmain.emit (self.ValueM)
              self.ValueJ = ''
                         
        elif self.LastCount[0] != 'j4' and 1<= self.LastCount[1] <=5  and self.ValueJ.endswith('i'):  
              #self.textappendmain.emit ('error1')
              pass
             
        elif (self.LastCount[0] != 'j4' and 5 <  self.LastCount[1]) and self.ValueJ.endswith('i'):    
            if self.LastCount[0] == 'i':
                pass
            else:
              #self.textappendmain.emit ('error2')
              self.ValueJ = ''.join
              
  
        if self.FrameRecord [-2] != self.FrameRecord [-1]: 
              self.FrameRecord.clear()                  #Reset FrameRecord when a differnt gesture is detected before required frame count
              self.FrameCount.clear()

 
    @Slot ()                                            #Start Streaming
    def start (self):
        self.ui.stop.setEnabled(True)
        self.ui.start.setEnabled(False)    
        self.ui.Stream_Source.selectAll()
        self.ui.Stream_Source.copy()
        self.det.source_folder = ''
        self.det.source_folder = ''.join(pyperclip.paste())
        self.det.start()
        self.ui.inputted_text.clear()
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End)
        self.ValueI = ''
        self.RECORD.clear()
        
        
    @Slot ()                                        #End Streaming
    def end (self):                                 #Print to prompt to test any functions when stream ends
        self.ui.stop.setEnabled(False)
        self.ui.start.setEnabled(True)
        self.det.end()
        self.det.quit()
        self.det.wait()  
        self.ValueM = ''
        self.ValueJ = ''
        self.RecordZ = ''
       
        #print ('ValueM:  ',self.ValueM)
        #print ('ValueJ:  ',self.ValueJ)
        #print ('RecordZ:  ',self.RecordZ)
        
        print ('FrameRecord:', self.FrameRecord)
        print ('FrameCount: ', self.FrameCount)
        print ('LastCount: ', self.LastCount) 
        print ('RECORD,',  self.RECORD)

        self.FrameRecord.clear()
        self.FrameCount.clear()
        #self.LastCount.clear()
  
       
            

if __name__ == "__main__":                         #Start User-Interface Application
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

