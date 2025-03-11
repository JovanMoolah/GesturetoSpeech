# GesturetoSpeech
# Gesture Information
This application automatically convert gestures in ASL fingerspelling to text and then voice. It includes all numbers and letters. Gestures for 'j' and 'z' only include one position which is 'j4' for j and 'z1' or 'z2' for z.

Gestures for '0' and 'o', and 'v' and '2' are the same. If the previous gesture is a number, the gesture is '0' and '2'. If the previous gesture is a letter, the gesture is 'o' and 'v'. Default states for those gestures are 'o' and '2'.

Additional gestures: 'delete', 'enter' and 'space' are used to delete text, start speech and separte words. 

Gestures glosses can also be cutomized to user-defined text

All gestures are seen in diagram below

![image](https://github.com/user-attachments/assets/f3baf81a-9e55-4e1f-953c-19933cb3072f)

# Dataset
The original dataset for the model can be found here: https://universe.roboflow.com/asl-pose/american-sign-language-pose-dataset/dataset/27

The dataset used to train the model can be found here: https://www.kaggle.com/datasets/jovanmoolah1/asl-pose-various-backgrounds


