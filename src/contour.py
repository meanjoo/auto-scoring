import cv2 as cv
import sys

class Rect:
    pass

def line_box_intersection(lineP0, lineP1, boxMinPt, boxMaxPt):
    pass

path = '../test_image'
img = cv.imread(path+'/sample.jpeg')

if img is None:
    sys.exit('Could not read the image.')

cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (3,3),0)
canny = cv.Canny(blur, 100, 200)

contours, hier = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
rects = [cv.boundingRect(each) for each in contours] # 사각형 정보 튜플(x,y,w,h)을 원소로 하는 리스트
area = [w*h for (x,y,w,h) in rects]
area.sort()
sort_rects = sorted(rects)

print('==rects==')
print(rects)
print('==sorted_rects==')
print(sort_rects)
print('==area==')
print(area)

width = set()

for x,y,w,h in rects:
    width.add(w)

print('==width set==')
print(width)
sort_width = list(width)
sort_width.sort()
print(sort_width)
print(len(sort_width))

for x,y,w,h in rects:
    color = (0,255,0) if w > sort_width[int(len(sort_width)*3/5)] else (0,0,255)
    # color = (0,255,0)
    cv.rectangle(img, (x, y),
                 (x + w, y + h), color, 5)

k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    cv.imwrite('contourTest.jpg', img)

    cv.destroyAllWindows()