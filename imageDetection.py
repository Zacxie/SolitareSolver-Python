import cv2

#for image
img = cv2.imread('IMG_20210427_184443_1.jpg')

#for webcam
#cap = cv2.VideoCapture(0)
#cap.set(3,640)
#cap.set(4,480)

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'custom-yolov4-tiny-detector.cfg'
weightsPath = 'custom-yolov4-tiny-detector_best.weights'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5,127.5,127.5))
net.setInputSwapRB(True)

classIds, confs, bbox = net.detect(img, confThreshold=0.5)
print(classIds, bbox)

for classIds, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
    cv2.rectangle(img, box, color=(255,0,0), thickness=3)
    cv2.putText(img, classNames[classIds], (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)





cv2.imshow("output", img)
cv2.waitKey(0)

