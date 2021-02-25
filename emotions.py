import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
import os
from threading import Thread
import statistics
from statistics import mode


class Emotions(Thread):

    def __init__(self):
        super().__init__()
        self.vectEmotion = []
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        # Create the model
        self.model = Sequential()

        self.model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
        self.model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(7, activation='softmax'))

        # emotions will be displayed on your face from the webcam feed

        self.model.load_weights('model.h5')

        # prevents openCL usage and unnecessary logging messages
        cv2.ocl.setUseOpenCL(False)
        # dictionary which assigns each label an emotion (alphabetical order)
        self.emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad",
                             6: "Surprised"}

        # start the webcam feed
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:

            # Find haar cascade to draw bounding box around face
            ret, frame = self.cap.read()
            if not ret:
                break
            facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                self.cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = self.model.predict(self.cropped_img)
                maxindex = int(np.argmax(prediction))
                self.vectEmotion.append(maxindex)
                cv2.putText(frame, self.emotion_dict[maxindex], (x + 20, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 255, 255),
                            2, cv2.LINE_AA)

            cv2.imshow('Video', cv2.resize(frame, (1600, 960), interpolation=cv2.INTER_CUBIC))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def getEmotion(self):
        return self.emotion_dict[self.most_common(self.vectEmotion)]

    def getCropeImage(self):
        return self.cropped_img

    def setReady(self):
        self.vectEmotion.clear()

    def most_common(self, List):
        return mode(List)
