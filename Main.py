import emotions
import Speech_recognition
import django

print(django.get_version())
emotion = emotions.Emotions()
speech = Speech_recognition.SpeechRecognition(emotion)
emotion.daemon = True
speech.daemon = True
emotion.start()
speech.start()
emotion.join()
speech.join()



