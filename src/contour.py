import cv2 as cv
import sys
import copy

'''
* python 반복자
python에서 어떤 타입/클래스가 iterable하다는 것은 for ... in문을 통해 반복될 수 있다는 것이다.
iterable한 타입은 __iter__ 메소드와 __next__ 메소드를 가지고 있다.
__iter__는 iterator를 반환한다. 
iterator는 __next__ 메소드로 어떤 컨테이너의 개별 요소를 반복하게 해준다.
__next__는 다음 반복 요소를 반환하고 더 이상 반환할 요소가 없으면 StopIteration 예외를 발생시킨다.
'''

class Point:
    def __init__(self, x ,y):
        self.x = x
        self.y = y

class Rect:
    def __init__(self, rect):
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]

    def __iter__(self):
        self.i = -1
        return self
    
    def __next__(self):
        r = (self.x, self.y, self.w, self.h)
        self.i += 1
        if self.i >= 4:
            raise StopIteration
        return r[self.i]

    def __repr__(self):
        return repr((self.x, self.y, self.w, self.h))

# def is_rect_intersect(rect1, rect2):
#     minx = min(rect1.x, rect2.x)
#     miny = min(rect1.y, rect2.y)
#     maxx = max(rect1.x + rect1.w, rect2.x + rect2.w)
#     maxy = max(rect1.y + rect1.h, rect2.y + rect2.h)

#     if maxx - minx <= rect1.w + rect2.w and maxy - miny <= rect1.h + rect2.h:
#         return True
#     return False

# def is_rect_near_included(rect1, rect2):
#     pass

# def minimum_area_contain_two_rects(rect1, rect2):
#     leftTop = Point(min(rect1.x, rect2.x), min(rect1.y, rect2.y))
#     rightBottom = Point(max(rect1.x + rect1.w, rect2.x + rect2.w), max(rect1.y + rect1.h, rect2.y + rect2.h))

#     return Rect((leftTop.x, leftTop.y, rect1.w + rect2.w - (rightBottom.x - leftTop.x), rect1.h + rect2.h - (rightBottom.y - leftTop.y)))

path = './test_image'
img = cv.imread(path+'/newsample.jpeg')
img2 = img.copy()

if img is None:
    sys.exit('Could not read the image.')

cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (3,3),0)
canny = cv.Canny(blur, 100, 200)

row, col = 6,2
contours, hier = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# rects = [cv.boundingRect(each) for each in contours] # 사각형 정보 튜플(x,y,w,h)을 원소로 하는 리스트
rects = [Rect(cv.boundingRect(each)) for each in contours] # cv.boundingRect(each)는 사각형 정보 튜플(x,y,w,h)을 반환
rects.sort(key=lambda rect : (rect.x, rect.y, rect.w, rect.w))

crop, cropAll = [], []
# 세로로 자르기
for rect in rects:
    tmp = (int)(rect.w / col)
    for c in range(col):
        crop.append(Rect((rect.x + tmp*c, rect.y, tmp, rect.h)))

# 가로로 자르기
for rect in crop:
    tmp = (int)(rect.h / row)
    for r in range(row):
        cropAll.append(Rect((rect.x, rect.y + tmp*r, rect.w, tmp)))

result = []
for rect in cropAll:
    croprect = canny[rect.y+rect.h:rect.x+rect.w]
    contours, heir = cv.findContours(croprect, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) # contours는 numpy.ndarray
    result.extend(Rect(cv.boundingRect(each)) for each in contours)

print('==crop==')
print(crop)
print('==cropAll==')
print(cropAll)

area = [rect.w*rect.h for rect in rects]
area.sort()
print('==area==')
print(area)

for rect in rects:
    color = (0,255,0)
    cv.rectangle(img, (rect.x, rect.y),
            (rect.x + rect.w, rect.y + rect.h), color, 5)

print('==result==')
print(result)
for rect in cropAll:
    color = (0,255,0)
    cv.rectangle(img2, (rect.x, rect.y),
            (rect.x + rect.w, rect.y + rect.h), color, 5)
    


k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    cv.imwrite('contourTest.jpg', img)
    cv.imwrite('contourTest2.jpg', img2)
    
    cv.destroyAllWindows()