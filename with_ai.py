#!/usr/bin/env python3
import logging
import time
import serial
from knikkersorteermachine import KnikkerSorteerMachine
from keras.models import load_model
import numpy as np
import cv2

# Load the model
model = load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cap = cv2.VideoCapture(4)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)

with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0) as serial:
    machine = KnikkerSorteerMachine(serial, logging.DEBUG)

    while True:
        # Replace this with the path to your image
        # image = Image.open('<IMAGE_PATH>')
        ret, image = cap.read()

        # image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image = cv2.resize(image, size)

        cv2.imshow('img', image)

        #turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)

        chute_id = np.argmax(prediction)

        print(f"Chute: {chute_id}")
        print(f"Red: {prediction[0][0]}")
        print(f"Blue: {prediction[0][1]}")
        print(f"Green: {prediction[0][2]}")
        print(f"Cyan: {prediction[0][3]}")
        print(f"Yellow: {prediction[0][4]}")
        print(f"Nothing: {prediction[0][5]}")

        machine.move_chute(chute_id)
        machine.feed_one()

        cv2.waitKey(1000)
