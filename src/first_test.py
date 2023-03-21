import cv2 as cv
import sys

path = './test_image' # 'C:/Users/user/Desktop/workspace/test_image'
img = cv.imread(path+'/sample2.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

if img is None:
    sys.exit('Could not read the image.')

# cv.namedWindow('grayImage', cv.WINDOW_NORMAL)
# cv.imshow('grayImage', gray)

blur = cv.GaussianBlur(gray, (3,3),0)
# cv.namedWindow('blurImage', cv.WINDOW_NORMAL)
# cv.imshow('blurImage', blur)

canny = cv.Canny(blur, 100, 200)
cv.namedWindow('cannyImage', cv.WINDOW_NORMAL)
cv.imshow('cannyImage', canny)

k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    cv.imwrite('canny_sample2.jpg', canny)
    cv.destroyAllWindows()