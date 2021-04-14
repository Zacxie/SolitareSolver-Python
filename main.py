import cv2

cam = cv2.VideoCapture(0)
image = cv2.imread('cards.jpg')

while True:
    check, frame = cam.read()

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('video', grayFrame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()



# # make it grayscale
# Gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#
# # Make canny Function
# canny=cv2.Canny(Gray,40,140)
#
# # the threshold is varies bw 0 and 255
# cv2.imshow("Canny",canny)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#



