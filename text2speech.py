from gtts import gTTS
import os
import warnings

warnings.filterwarnings("default")
text = "Hello"
language = 'en'
obj = gTTS(text=text, lang=language, slow=False)
save_path = "sample.mp3"
try:
    obj.save(save_path)
    print(f"File saved successfully at {os.path.abspath(save_path)}")
except Exception as e:
    print(f"An error occurred: {e}")
if os.path.exists(save_path):
    print("File exists in the directory")
    
else:
    print("File does not exist in the directory")
