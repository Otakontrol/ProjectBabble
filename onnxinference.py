import os
import time
import torch
import onnx 
import onnxruntime as ort
import numpy as np
import cv2
from pythonosc import udp_client
from threading import Thread
import cv2
from imutils.video import WebcamVideoStream

OSCip = "127.0.0.1" 
OSCport = 9000 #VR Chat OSC port
client = udp_client.SimpleUDPClient(OSCip, OSCport)

classes = ["cheekPuff", "cheekSquint_L", "cheekSquint_R", "noseSneer_L", "noseSneer_R", "jawOpen", "jawForward", "jawLeft", "jawRight", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", "mouthRollUpper", "mouthRollLower", "mouthShrugUpper", "mouthShrugLower", "mouthClose", "mouthSmile_L", "mouthSmile_R", "mouthFrown_L", "mouthFrown_R", "mouthDimple_L", "mouthDimple_R", "mouthUpperUp_L", "mouthUpperUp_R", "mouthLowerDown_L", "mouthLowerDown_R", "mouthPress_L", "mouthPress_R", "mouthStretch_L", "mouthStretch_R", "tongueOut"]

cap = WebcamVideoStream(src=0).start()
sessionOptions = ort.SessionOptions()
ort_sess = ort.InferenceSession("NeckModel.onnx", providers = ['CPUExecutionProvider'])
while True:
    frame = cap.read()
    frame = cv2.resize(frame, (100,100))
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100,100))
    gray = cv2.GaussianBlur(img, (3, 3), 0)
    image = gray.reshape(1,1, 100, 100)
    image = torch.from_numpy(image).float()
    image = image.numpy()
    outputs = ort_sess.run(None, {'input': image})
    output = outputs[0][0]
    output = output.tolist()
    end = time.time()
    output = [x * 100 for x in output] 

    for i in range(len(output)):
        client.send_message(f"/{classes[i]}", output[i])
        #print(f"{classes[i]} : {output[i]}")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()