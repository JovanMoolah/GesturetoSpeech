# Compiled Version
Compiled Version for application:
```
https://drive.google.com/file/d/1LpFbGddI9TXjDm9ZP2hl9KdEWzR-r1bO/view?usp=drive_link
```
Download, unzip and run exe. 
Program works with only NVIDIA GPUs.

# Python Installtion
Clone repository and create virtual environment:
```
git clone https://github.com/JovanMoolah/GesturetoSpeech.git
cd GesturetoSpeech
python -m venv GtS
source GtS/bin/activate
```
Install libraries:
```
pip install -r Requirements.txt
```
If CPU is used, change requirements for torch to:
```
torch torchvision torchaudio
```

# Gestures
This application automatically convert gestures in ASL fingerspelling to text and then voice. It includes all numbers and letters. Gestures for 'j' and 'z' only include one position which is 'j4' for j and 'z1' or 'z2' for z.

Gestures for '0' and 'o', and 'v' and '2' are the same. If the previous gesture is a number, the gesture is '0' and '2'. If the previous gesture is a letter, the gesture is 'o' and 'v'. Default states for those gestures are 'o' and '2'.

Additional gestures: 'delete', 'enter' and 'space' are used to delete text, start speech and separte words. 

Gestures glosses can also be cutomized to user-defined text

All gestures are seen in diagram below.

![image](https://github.com/user-attachments/assets/f3baf81a-9e55-4e1f-953c-19933cb3072f)

# Speech
For speech to work, please download languages and voices in Windows Languages settings. 
Tutorial: 
```
https://support.microsoft.com/en-us/windows/language-packs-for-windows-a5094319-a92d-18de-5b53-1cfc697cfca8
```
For Translation to work, please uncomment Argos translate package and download desired model.
Models can be found here:
```
https://github.com/argosopentech/argos-translate/blob/master/argostranslate/languages.csv
```
For example, English to Spanish would be: from_code="en", to_code="es" 

# User-Interface
![image](https://github.com/user-attachments/assets/2508ddc6-059e-4678-bf4c-a2b78a654e41)

Stream can be started and stopped at anything time. After changing stream source, stop and restart stream. 

Rate, pitch and volume controls the rate of speech, the pitch of the voice and volume of the voice.

Gesture glosses that are captured to text box can be renamed by editing the textbox next to combobox mapping.

Languages and voices for native (top) and translated (bottom) combo boxes can be changed. Languages must be installed in Windows Languages settings for it to be shown in the combobox.  

When translate button is on, text is voiced in selected translate voice. When off text is voiced in native language. 

Concurrent voices text in real-time after every whitespace. Only works for native language.

Buttons for start, stop, pause and resume control the speech duration. It voices words currently in the text box. Use when you retain information after speaking, otherwise, use 'enter' gesture.

Clear deletes all text in both native and translated text boxes.

Synchronize button synchronizes text box data with Gloss Record. It prevents an error in which old text is pasted back into box when manually inserting/deleting. 

# Dataset
The original dataset for the model can be found here: 
```
https://universe.roboflow.com/asl-pose/american-sign-language-pose-dataset/dataset/27
```
The dataset used to train the model can be found here: 
```
https://www.kaggle.com/datasets/jovanmoolah1/asl-pose-various-backgrounds
```
The model obtained validation accuries: 99% Recall, 99% Precision, 99% mAP50, 91% mAP50-95 Box and 95% mAP50-95 Pose 

# Testing
The application was run on an RTX 4060 GPU and a 30 FPS webcam. Capture speed averaged 30 to 45 gestures a minute. 

The model works well with white backgrounds up to 1.5m and cluttered background up to 0.5m with confidence greater than 0.6. Model has significantly greater accuracy with light, plain colored backgrounds.

Online datasets can be evaluated with the model by changing stream source to image and video, and typing directory location in text box next to stream source. 

A livestream source was added. Just type livestreaming url such as youtube or twitch. Note, there is too much latency for livestreaming to work effectively. 

# Demo
[![Demo Application for Gesture to Speech ](https://img.youtube.com/vi/mnxsYEXihq8/0.jpg)](https://youtu.be/mnxsYEXihq8)
The Demonstration for the application can be found on YouTube with the link:
```
https://youtu.be/mnxsYEXihq8
```
