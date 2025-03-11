# Gestures
This application automatically convert gestures in ASL fingerspelling to text and then voice. It includes all numbers and letters. Gestures for 'j' and 'z' only include one position which is 'j4' for j and 'z1' or 'z2' for z.

Gestures for '0' and 'o', and 'v' and '2' are the same. If the previous gesture is a number, the gesture is '0' and '2'. If the previous gesture is a letter, the gesture is 'o' and 'v'. Default states for those gestures are 'o' and '2'.

Additional gestures: 'delete', 'enter' and 'space' are used to delete text, start speech and separte words. 

Gestures glosses can also be cutomized to user-defined text

All gestures are seen in diagram below.

![image](https://github.com/user-attachments/assets/f3baf81a-9e55-4e1f-953c-19933cb3072f)

# Speech
For speech to work, please download languages and voices in Windows Languages settings. 
Tutorial: https://support.microsoft.com/en-us/windows/language-packs-for-windows-a5094319-a92d-18de-5b53-1cfc697cfca8

For Translation to work, please uncomment Argos translate package and download desired model.
Models can be found here: https://github.com/argosopentech/argos-translate/blob/master/argostranslate/languages.csv
For example, English to Spanish would be: from_code="en", to_code="es" 

# Dataset
The original dataset for the model can be found here: https://universe.roboflow.com/asl-pose/american-sign-language-pose-dataset/dataset/27

The dataset used to train the model can be found here: https://www.kaggle.com/datasets/jovanmoolah1/asl-pose-various-backgrounds


# Testing
The application was run on RTX 4060 GPU and a 30 FPS webcam. Capture speed averaged 30 to 45 gestures a minute. 

The model works well with white backgrounds up to 1.5m and cluttered background up to 0.5m. Model has significantly greater accuracy with light, plain colored backgrounds.

Online datasets can be evaluated with the model by changing stream source to image and video, and typing directory location in text box next to stream source. 

A livestream source was added. Just type livestreaming url such as youtube or twitch. Note, there is too much latency for livestreaming to work effectively.  

