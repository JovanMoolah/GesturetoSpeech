
from re import S

from PyQt5.QtCore import qAbs

import ultralytics

import supervision as sv

import cv2

import random

from ultralytics import YOLO

from roboflow import Roboflow

from matplotlib import pyplot as plt

import albumentations as A

import numpy as np

import torch

import os

from sklearn.model_selection import train_test_split

from tqdm import tqdm

import pyttsx3

from itertools import groupby

import argostranslate.package

import argostranslate.translate

import sys

import time

import gc

from PySide6.QtCore import Qt, QThread, Signal, Slot, QLocale, QSignalBlocker

from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap, QTextCursor

from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)

from PySide6.QtTextToSpeech import QTextToSpeech, QVoice


from UIForHand import Ui_MainWindow

'''
from_code = "en"
to_code = "de"

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


class Detection (QThread):
    frameupdate = Signal (QImage)
    
    listsend = Signal (str)
    
  
    model = YOLO('runs/pose/train15/weights/best.pt') # load the trained model


    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status=True
        self.source = "0"
        self.cap = cv2.VideoCapture(self.source)
       
    def end (self):
        self.status = False
        self.cap.release()
    
    def begin (self):
        self.status = True
        self.cap = cv2.VideoCapture (0)
    
    def Prediction (self):
      
             
        while self.status:
           # if (self.status == False):
              #  break
            
            ret, frame = self.cap.read()

            # Make predictions
            results = self.model.predict(frame, conf = 0.6, show=False)
            names = self.model.names
            
            annotated_frame = results[0].plot()

            # Reading the image in RGB to display it
            color_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

            # Creating and scaling QImage
            h, w, ch = color_frame.shape
            
            #print (h,w, ch)
            
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            #scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
            
            
            for r in results:
             
                # r.save_txt("output.txt")
                for box in r.boxes.cls:
               
                    c = (names[int(box)]) 
                    if (c == "space"):
                        c = " "  
                    if (c == 'q'):
                          global CLO 
                          CLO = 'CLOSEWIN'
   
                    self.listsend.emit(str (c))
                 
            self.frameupdate.emit(img)
            

    def run(self):

       self.Prediction()
       
 

class Window(QMainWindow):
    textappendmain = Signal (str)
    
    ValueM = ''
    ValueM2 = ''
    ValueM3 = ''
    ValueI = ''
    ACTLIST = []
    ACTLIST2 = []
    ACTLIST3 = []
    RECORD = []
    gest = []
    Current = ''

    
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.det = Detection (self)
        
        #self.det.finished.connect (self.close)

        self.speech = QTextToSpeech (self)
        
        self.speechTrans = QTextToSpeech (self)
        
     

        self.input_voices = []
        
        self.output_voices = []
        
        #self.ui.inputted_text.cursorRect()
        
        #self.ui.inputted_text.setTextCursor()

        #self.cursor = QTextCursor (self)
        
        self.InitialiseLanguages ()
        self.InitialiseLanguagesTrans ()
        
        self.IntialiaseGesture()
        
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End)
        
        #self.select_Engine(0)

        self.ui.Translate.setCheckable(True)
        
        self.ui.concurrentbut.setCheckable (True)
        
        #Connections_____________________________________
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
            
        
        self.speech.stateChanged.connect(self.state_changed)
        self.ui.clear.clicked.connect(self.clearText)
        
        self.ui.Translate.clicked.connect(self.Toggle)
        
        self.ui.concurrentbut.clicked.connect (self.TogCon)
        

        self.det.listsend.connect (self.processlist)
        
        self.ui.Gesture.currentIndexChanged.connect (self.mapNames)
        
        self.ui.Mapping.textEdited.connect (self.changeMapping)
        
        self.ui.Stream.textEdited.connect (self.select_Stream)

        

        #_________________________________________________________________________________



    @Slot (str)
    def select_Stream (self, text):
         self.det.source = text


    
  
    @Slot (str)
    def TestValue (self, testing):
        self.ui.translated_text.appendPlainText(testing)

   
    def Toggle(self):
        if self.ui.Translate.isChecked():
            self.ui.Translate.setText ("On")
        else:
            self.ui.Translate.setText ("Off")
    
    def TogCon (self):
        if self.ui.concurrentbut.isChecked():
            self.ui.concurrentbut.setText ("On")
        else:
            self.ui.concurrentbut.setText ("Off")
     
    def IntialiaseGesture (self):
        print (self.det.model.names)    
        #self.gest.append(self.det.model.names)
        for m in self.det.model.names.values():
                self.gest.append (m[0])     
        for g in self.gest:
            self.ui.Gesture.addItem (g)

    @Slot (int)
    def mapNames (self, map):
        self.ui.Mapping.setText (self.gest [map])
        
    def ActualMap (self, txt ):
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
       elif txt == 'e':
           self.Current = self.gest[13]    
       elif txt == 'f':
           self.Current = self.gest[14]
       elif txt == 'g':
           self.Current = self.gest[15]
       elif txt == 'h':
           self.Current = self.gest[16]
       elif txt == 'i':
           self.Current = self.gest[17]    
       elif txt == 'k':
           self.Current = self.gest[18]  
       elif txt == 'l':
           self.Current = self.gest[19]
       elif txt == 'm':
           self.Current = self.gest[20]
       elif txt == 'n':
           self.Current = self.gest[21]    
       elif txt == 'o':
           self.Current = self.gest[22]
       elif txt == 'p':
           self.Current = self.gest[23]
       elif txt == 'q':
           self.Current = self.gest[24]
       elif txt == 'r':
           self.Current = self.gest[25]    
       elif txt == 's':
           self.Current = self.gest[26]
       elif txt == ' ':
           self.gest[27] = " "
           self.Current = self.gest[27]
       elif txt == 't':
           self.Current = self.gest[28]
       elif txt == 'u':
           self.Current = self.gest[29]    
       elif txt == 'v':
           self.Current = self.gest[30]
       elif txt == 'w':
           self.Current = self.gest[31]
       elif txt == 'x':
           self.Current = self.gest[32]
       elif txt == 'y':
           self.Current = self.gest[33]


    @Slot (str)
    def changeMapping (self, text):
        self.gest [self.ui.Gesture.currentIndex()] = text
        
  
    def InitialiseLanguages (self):
        current = self.speech.locale()
        with QSignalBlocker(self.ui.input_language):
            self.ui.input_language.clear()
            # Populate the languages combobox before connecting its signal.
            locales = self.speech.availableLocales()
            for locale in locales:
                lang = QLocale.languageToString(locale.language())
                territory = QLocale.territoryToString(locale.territory())
                self.ui.input_language.addItem(f"{lang} ({territory})", locale)
                if locale.name() == current.name():
                    current = locale     
        self.locale_changed(current)
   
    
    def InitialiseLanguagesTrans (self):
        current = self.speechTrans.locale()
        with QSignalBlocker(self.ui.output_language):
            self.ui.output_language.clear()
            # Populate the languages combobox before connecting its signal.
            locales = self.speechTrans.availableLocales()
            for locale in locales:
                lang = QLocale.languageToString(locale.language())
                territory = QLocale.territoryToString(locale.territory())
                self.ui.output_language.addItem(f"{lang} ({territory})", locale)
                if locale.name() == current.name():
                    current = locale
        self.locale_changedTrans(current)

    @Slot(int)
    def set_Pitch (self, pitch):
        self.speech.setPitch (pitch / 10)
        self.speechTrans.setPitch (pitch / 10)
        
    @Slot(int)
    def set_Rate (self, rate):
        self.speech.setRate (rate / 10)
        self.speechTrans.setRate (rate / 10)
        
    @Slot(int)
    def set_Volume(self, volume):
        self.speech.setVolume (volume / 20)  
        self.speechTrans.setVolume (volume / 20) 
        
    @Slot (int)    
    def select_Language (self, lng):
        self.speech.setLocale(self.ui.input_language.itemData(lng))
    
    @Slot (int)    
    def select_LanguageTrans (self, lng):
        self.speechTrans.setLocale(self.ui.output_language.itemData(lng))    
     
    @Slot (int)  
    def select_Voice (self, vc):
        self.speech.setVoice(self.input_voices[vc]) 
    
    @Slot (int)  
    def select_VoiceTrans (self, vc):
        self.speechTrans.setVoice(self.output_voices[vc]) 

    @Slot(QLocale)
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

    @Slot(QLocale)
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
                    self.ui.output_voice.setCurrentIndex(self.ui.output_voice.count() - 1)

    @Slot ()
    def startSpeak (self):
        if self.ui.Translate.isChecked(): 
            
            current = self.speech.locale()
            lang = QLocale.languageToString(current.language())
            if lang == 'English':
                lang = 'en'
            elif lang == 'French':
                lang = 'fr'
            elif lang == 'Spanish':
                lang = 'es'
            elif lang == 'German':
                lang = 'de'
            #print (lang)   

            currentTrans = self.speechTrans.locale()
            langTrans = QLocale.languageToString(currentTrans.language())
            if langTrans == 'English':
                langTrans = 'en'
            elif langTrans == 'French':
                langTrans = 'fr'
            elif langTrans == 'Spanish':
                langTrans = 'es'     
            elif langTrans == 'German':
                langTrans = 'de'
            #print (langTrans)


            Translate = argostranslate.translate.translate(self.ui.inputted_text.toPlainText(), lang, langTrans)
            self.ui.translated_text.setPlainText(Translate)
            self.speechTrans.say (self.ui.translated_text.toPlainText())  
            
        else:  
            self.speech.say (self.ui.inputted_text.toPlainText())
     
            
    @Slot()
    def stopSpeak (self):
        if self.ui.Translate.isChecked():
            self.speechTrans.stop()
            self.ValueM=''
        else:
            self.speech.stop()
            self.ValueM = ''

    @Slot()
    def pauseSpeak (self):
        if self.ui.Translate.isChecked():
            self.speechTrans.pause()
        else:
            self.speech.pause()
            

    @Slot()
    def resumeSpeak (self):
        if self.ui.Translate.isChecked():
            self.speechTrans.resume()
        else:
            self.speech.resume()


    @Slot(QTextToSpeech.State)
    def state_changed(self, state):
   
        if state == QTextToSpeech.Ready:
            #self.ui.inputted_text.clear()
            self.ui.inputted_text.setFocus()
            
  
    @Slot()
    def clearText (self):
        self.ui.inputted_text.clear()
        self.ui.translated_text.clear()
        
    
    @Slot (str)
    def appendText(self,text):
       
      
           self.ActualMap (text)
           if self.Current == 'o' and self.RECORD [-1] in ['0','1','2','3','4','5','6','7','8','9']:
              self.Current = '0'
       
           self.RECORD.append (self.Current)
       
       
           #self.RECORD.append (text)

           #if text == 'o':
              # text = '0'
           
           self.ui.inputted_text.insertPlainText (self.RECORD[-1]) 
       

           if self.ui.concurrentbut.isChecked(): 
               self.ui.translated_text.insertPlainText (self.RECORD[-1])
               if self.Current == ' ':
                    self.speech.say (self.ui.translated_text.toPlainText())   
                    self.ui.translated_text.clear()
                    
    
    @Slot(str)
    def setText(self, text):
        self.ui.inputted_text.insertPlainText (text)
        
 
    @Slot(QImage)
    def setImage(self, image):
        self.ui.Display.setPixmap(QPixmap.fromImage(image)) 

    
    @Slot (str)   
    def processlist(self, valuesent):
        self.ACTLIST.append(valuesent)
        
        for nme, cnt in groupby(self.ACTLIST):
                self.ACTLIST2.append((nme, len(list(cnt))))
        self.ACTLIST3 = self.ACTLIST2 [-1]
    

        #Normal lettering except for j,z
        if 20 <=  self.ACTLIST3[1] <= 25 and not self.ValueM.endswith(str(self.ACTLIST3[0])):
            self.ValueM = ''.join(str(self.ACTLIST3[0]))
            self.textappendmain.emit (self.ValueM)
            
                        
        elif 40 <=  self.ACTLIST3[1] <= 45 and self.ValueM.endswith(str(self.ACTLIST3[0])) and not self.ValueM2.endswith(str(self.ACTLIST3[0])):
         
                self.ValueM2 = ''.join(str(self.ACTLIST3[0]))   
                self.ValueM =''.join (self.ValueM2)
                self.textappendmain.emit (self.ValueM)

        elif 70 <= self.ACTLIST3[1] <= 75 and self.ValueM.endswith (str(self.ACTLIST3[0])) and self.ValueM2.endswith(str(self.ACTLIST3[0]))and not self.ValueM3.endswith(str(self.ACTLIST3[0])):

                self.ValueM3 = ''.join(str(self.ACTLIST3[0]))  
                self.ValueM =''.join (self.ValueM3)
                self.textappendmain.emit (self.ValueM)


        #Lettering for j,z
        if self.ACTLIST3[0] == '5' and 5 < self.ACTLIST3[1] <=20 and not self.ValueI:
                self.ValueI = ''.join('5')  
                #self.textappendmain.emit ('1st worked')
                
                    
        elif self.ACTLIST3[0] == '4' and 5 < self.ACTLIST3[1] <=20  and self.ValueI.endswith('5'):
              self.ValueI = ''.join ('54') 
              #self.textappendmain.emit ('2nd worked')
              #elf.ValueM =''.join ('j')
              #self.textappendmain.emit (self.ValueM)
              #self.ValueI = ''
              
                
        elif self.ACTLIST3[0] != '4' and 1<= self.ACTLIST3[1] <=5  and self.ValueI.endswith('5'):  
              #self.textappendmain.emit ('error1')
              pass
             
        elif (self.ACTLIST3[0] != '4' and 5 <  self.ACTLIST3[1]) and self.ValueI.endswith('5'):    
            if self.ACTLIST3[0] == '5':
                pass
            else:
              #self.textappendmain.emit ('error2')
              self.ValueI = ''.join

        elif self.ACTLIST3[0] == '3' and 5 < self.ACTLIST3[1] <20 and self.ValueI.endswith('54'):       
              self.ValueI = ''.join ('543') 
              self.ValueM =''.join ('j')
              self.textappendmain.emit (self.ValueM)
              #self.textappendmain.emit ('3rd worked')
              self.ValueI = '' 

        elif self.ACTLIST3[0] != '3' and 1<= self.ACTLIST3[1] <=5 and self.ValueI.endswith('54'): 
            #self.textappendmain.emit ('error3')
             pass
           
        elif (self.ACTLIST3[0] != '3' and 5 < self.ACTLIST3[1]) and self.ValueI.endswith('54'): 
            if self.ACTLIST3[0] == '4':
                pass
            else: 
              #self.textappendmain.emit ('error4')
              self.ValueI = '' 
              
        if self.ACTLIST [-2] != self.ACTLIST [-1]:
              self.ACTLIST.clear()
              self.ACTLIST2.clear()      


    @Slot ()
    def start (self):
        self.ui.stop.setEnabled(True)
        self.ui.start.setEnabled(False)
        
        self.det.begin ()
        self.det.start()
        self.ui.inputted_text.clear()
        self.ui.inputted_text.setFocus()
        self.ui.inputted_text.moveCursor(QTextCursor.End)
        self.ValueI = ''
        

        
    @Slot ()
    def end (self):
        self.ui.stop.setEnabled(False)
        self.ui.start.setEnabled(True)
        self.det.end()
        self.det.quit()
        self.det.wait()
        self.ValueI = ''

        print ('ValueM:  ',self.ValueM)
        print ('ValueI:  ',self.ValueI)
        print ('ACTLIST:', self.ACTLIST)
        print ('ACTLIST2: ', self.ACTLIST2)
        print ('ACTLIST3: ', self.ACTLIST3)   
        print ('RECORD,',  self.RECORD)
    
        self.ACTLIST.clear()
        self.ACTLIST2.clear()
        #self.ACTLIST3.clear()

        #time.sleep(1)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())



