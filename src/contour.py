import cv2 as cv
import sys

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

def is_rect_intersect(rect1, rect2):
    minx = min(rect1.x, rect2.x)
    miny = min(rect1.y, rect2.y)
    maxx = max(rect1.x + rect1.w, rect2.x + rect2.w)
    maxy = max(rect1.y + rect1.h, rect2.y + rect2.h)

    if maxx - minx <= rect1.w + rect2.w and maxy - miny <= rect1.h + rect2.h:
        return True
    return False

def is_rect_near_included(rect1, rect2):
    pass

def minimum_area_contain_two_rects(rect1, rect2):
    leftTop = Point(min(rect1.x, rect2.x), min(rect1.y, rect2.y))
    rightBottom = Point(max(rect1.x + rect1.w, rect2.x + rect2.w), max(rect1.y + rect1.h, rect2.y + rect2.h))

    return Rect((leftTop.x, leftTop.y, rect1.w + rect2.w - (rightBottom.x - leftTop.x), rect1.h + rect2.h - (rightBottom.y - leftTop.y)))

path = './test_image'
img = cv.imread(path+'/sample.jpeg')
img2 = img.copy()

if img is None:
    sys.exit('Could not read the image.')

cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (3,3),0)
canny = cv.Canny(blur, 100, 200)


contours, hier = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
# rects = [cv.boundingRect(each) for each in contours] # 사각형 정보 튜플(x,y,w,h)을 원소로 하는 리스트
rects = [Rect(cv.boundingRect(each)) for each in contours] # cv.boundingRect(each)는 사각형 정보 튜플(x,y,w,h)을 반환
rects.sort(key=lambda rect : (rect.x, rect.y, rect.w, rect.w))

# area = [rect.w*rect.h for rect in rects]
# print(area)

# area.sort()

print('==rects==')
print(rects)
# print('==area==')
# print(area)

# width = set()
# for x,y,w,h in rects:
#     width.add(w)

# print('==width set==')
# print(width)
# sort_width = list(width)
# sort_width.sort()
# print(sort_width)
# print(len(sort_width))

for rect in rects:
    # color = (0,255,0) if w > sort_width[int(len(sort_width)*3/5)] else (0,0,255)
    color = (0,255,0)
    cv.rectangle(img, (rect.x, rect.y),
                (rect.x + rect.w, rect.y + rect.h), color, 5)

result = []
for rect in rects:
    # if not result:
    #     result.append(rect)
    #     continue
    result.append(rect).sort(key=lambda rect : (rect.x, rect.y, rect.w, rect.w))

    tmp = []

    # if abs(result[-1].x - rect.x) >= 10 or abs(result[-1].y - rect.y) >= 10:
    #     result.append(rect)
    #     continue

    if is_rect_intersect(result[-1], rect):
        t = result.pop()
        result.append(minimum_area_contain_two_rects(t, rect))
    else:
        result.append(rect)

print('==result==')
print(result)

print(len(rects))
print(len(result))

for rect in result:
    # color = (0,255,0) if w > sort_width[int(len(sort_width)*3/5)] else (0,0,255)
    color = (0,255,0)
    cv.rectangle(img2, (rect.x, rect.y),
                (rect.x + rect.w, rect.y + rect.h), color, 5)

k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    cv.imwrite('contourTest.jpg', img)
    cv.imwrite('contourProcess.jpg', img2)
    
    cv.destroyAllWindows()