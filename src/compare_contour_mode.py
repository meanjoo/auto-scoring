import cv2 as cv
import sys

path = '../test_image'
img = cv.imread(path+'/sample.jpeg')


if img is None:
    sys.exit('Could not read the image.')

cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.namedWindow('grayImage', cv.WINDOW_NORMAL)
# cv.imshow('grayImage', gray)
blur = cv.GaussianBlur(gray, (3,3),0)
# cv.namedWindow('blurImage', cv.WINDOW_NORMAL)
# cv.imshow('blurImage', blur)
canny = cv.Canny(blur, 100, 200)
# cv.namedWindow('cannyImage', cv.WINDOW_NORMAL)
# cv.imshow('cannyImage', blur)

img1 = img.copy()
img2 = img.copy()
img3 = img.copy()
img4 = img.copy()

# EXTERNAL
contours1, hier1 = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
rects1 = [cv.boundingRect(each) for each in contours1]

for rect in rects1:
    cv.rectangle(img1, (rect[0], rect[1]),
                 (rect[0] + rect[2], rect[1] + rect[3]), (0,255,0), 5)

# LIST
contours2, hier2 = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
rects2 = [cv.boundingRect(each) for each in contours2]

for rect in rects2:
    cv.rectangle(img2, (rect[0], rect[1]),
                 (rect[0] + rect[2], rect[1] + rect[3]), (0,255,0), 5)

# CCOMP
contours3, hier3 = cv.findContours(canny, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
rects3 = [cv.boundingRect(each) for each in contours3]

for rect in rects3:
    cv.rectangle(img3, (rect[0], rect[1]),
                 (rect[0] + rect[2], rect[1] + rect[3]), (0,255,0), 5)
    
# TREE
contours4, hier4 = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
rects4 = [cv.boundingRect(each) for each in contours4]

for rect in rects4:
    cv.rectangle(img4, (rect[0], rect[1]),
                 (rect[0] + rect[2], rect[1] + rect[3]), (0,255,0), 5)
    
print("external: ", len(rects1))
print("list: ", len(rects2))
print("ccomp: ", len(rects3))
print("tree: ", len(rects4))

k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    cv.imwrite('sample.jpg', img)
    cv.imwrite('sample_gray.jpg', gray)
    cv.imwrite('sample_blur.jpg', blur)
    cv.imwrite('sample_canny.jpg', canny)
    cv.imwrite('sample_rect_external.jpg', img1)
    cv.imwrite('sample_rect_list.jpg', img2)
    cv.imwrite('sample_rect_ccomp.jpg', img3)
    cv.imwrite('sample_rect_tree.jpg', img4)

    cv.destroyAllWindows()