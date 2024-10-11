import cv2
import os
import numpy as np
from PIL import Image
from fotopost.settings import BASE_DIR

detector = cv2.CascadeClassifier(
    BASE_DIR + "/app/face_recognition/haarcascade_frontalface_default.xml"
)
recognizer = cv2.face.LBPHFaceRecognizer_create()


class FaceRecognition:

    def faceDetect(
        self,
        Entry1,
    ):
        face_id = Entry1
        cam = cv2.VideoCapture(0)

        count = 0

        while True:

            ret, img = cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for x, y, w, h in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

                cv2.imwrite(
                    BASE_DIR
                    + "/app/face_recognition/dataset/User."
                    + str(face_id)
                    + "."
                    + str(count)
                    + ".jpg",
                    gray[y : y + h, x : x + w],
                )

                cv2.imshow("Register Face", img)

            k = cv2.waitKey(100) & 0xFF
            if k == 27:
                break
            elif count >= 30:
                break

        cam.release()
        cv2.destroyAllWindows()

    def trainFace(self):

        path = BASE_DIR + "/app/face_recognition/dataset"

        def getImagesAndLabels(path):

            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert("L")
                img_numpy = np.array(PIL_img, "uint8")

                face_id = int(os.path.split(imagePath)[-1].split(".")[1])

                faces = detector.detectMultiScale(img_numpy)

                for x, y, w, h in faces:
                    faceSamples.append(img_numpy[y : y + h, x : x + w])
                    ids.append(face_id)

            return faceSamples, ids

        print("\n Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        recognizer.save(BASE_DIR + "/app/face_recognition/trainer/trainer.yml")

        print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))

    def recognizeFace(self):
        recognizer.read(BASE_DIR + "/app/face_recognition/trainer/trainer.yml")
        cascadePath = (
            BASE_DIR + "/app/face_recognition/haarcascade_frontalface_default.xml"
        )
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        confidence = 0
        cam = cv2.VideoCapture(0)
        cam.release

        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        face_id = None

        while True:

            ret, img = cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for x, y, w, h in faces:

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                face_id, confidence = recognizer.predict(gray[y : y + h, x : x + w])

                if confidence < 100:
                    name = "Detected"
                else:
                    name = "Unknown"

                cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(
                    img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1
                )

            cv2.imshow("Detect Face", img)

            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                face_id = None
                break
            if confidence < 60:
                break

        print("\n Exiting Program")
        cam.release()
        cv2.destroyAllWindows()

        return face_id
