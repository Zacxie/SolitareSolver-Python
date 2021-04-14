import cv2

image = cv2.imread('cards.jpg')

# make it grayscale
Gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# Make canny Function
canny=cv2.Canny(Gray,40,140)

# the threshold is varies bw 0 and 255
cv2.imshow("Canny",canny)
cv2.waitKey(0)
cv2.destroyAllWindows()




