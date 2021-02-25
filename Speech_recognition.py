import speech_recognition as sr
from threading import Thread
from PIL import Image
import base64
import io

class SpeechRecognition(Thread):
    def __init__(self, emotion):
        super().__init__()
        self.emotion = emotion

    def run(self):
        # obtain audio from the microphone
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                self.emotion.setReady()
                audio = r.listen(source)


            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                print("Google Speech Recognition thinks you said: " + r.recognize_google(audio, language="it-IT"))
                print(self.emotion.getEmotion())
                IMIR = self.emotion.getCropeImage().reshape(48, 48)
                img = Image.fromarray(IMIR)
                print(type(img))
                img.save('prova.png')
                with open("prova.png", "rb") as file:
                    img = base64.b64encode(file.read())
                img = Image.open(io.BytesIO(base64.b64decode(img)))
                #img.show()
                print(type(img))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
