import cv2 as cv
import sys

# 점 클래스
class Point:
    def __init__(self, x ,y):
        self.x = x
        self.y = y

# 사각형 클래스
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
    
    def __add__(self, other):
        return (self.x + other.x, self.y + other.y, self.w + other.w, self.h + other.h)
    
    def __eq__(self, other):
        return (self.x==other.x and self.y==other.y and self.w==other.w and self.h==other.h)
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.w, self.h))
    
# img에 대해 윤곽선을 사각형 형태의 리스트로 반환하는 함수
def getContoursRect(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # img를 grayscale(회색조)로 변환
    blur = cv.GaussianBlur(gray, (3,3), 0) # 가우시안 블러 처리
    canny = cv.Canny(blur, 150, 100)
    contours, hier = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    rects = [Rect(cv.boundingRect(each)) for each in contours] # cv.boundingRect(each)는 사각형 정보 튜플(x,y,w,h)을 반환
    rectsNoDup = set(rects) # rectsNoDup: rects의 중복 제거(출력해서 확인해보면 rects에는 중복되는 사각형이 있다)
    return list(rectsNoDup)

    
path = './test_image'
img = cv.imread(path + '/realimg.jpeg')

if img is None:
    sys.exit('Could not read the image.')

img1 = img.copy()
img2 = img.copy()
img3 = img.copy()

cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)

rects = getContoursRect(img)
rects.sort(key=lambda rect : (-(rect.w*rect.h), rect.x, rect.y)) # 가장 큰 사각형을 찾기 위함
tableRect = rects[0] # tableRect: 가장 큰 사각형
offset = 0
tableRect.x = max(0, tableRect.x - offset)
tableRect.y = max(0, tableRect.y - offset)
tableArea = img[tableRect.y:tableRect.y+tableRect.h+offset*2, tableRect.x:tableRect.x+tableRect.w+offset*2] # 표 영역만 추출

img1 = tableArea.copy()
img2 = tableArea.copy()


row, col = 7, 2 # table의 행과 열 개수
h = tableRect.h / row # 문항 박스 하나의 높이
w = tableRect.w / col # 문항 박스 하나의 너비

for r in range(row):
    for c in range(col):
        pass


gray = cv.cvtColor(tableArea, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (3,3), 0)
canny = cv.Canny(blur, 150, 100)
contours, hier = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
rects = [Rect(cv.boundingRect(each)) for each in contours]
rects2 = set(rects)
rects2 = list(rects2)

print(f'rects: {len(rects)}, rects2: {len(rects2)}')

print('--rects')
print(rects)
print('--rects2')
print(rects2)

# 처음부터 사진을 자르고 다시 찾기 (14등분 <- r*c등분)
rects2.sort(key=lambda rect : (-(rect.w*rect.h), rect.x, rect.y))
for rect in rects2:
    color = (0,255,0)
    cv.rectangle(img1, (rect.x, rect.y),
                 (rect.x+rect.w, rect.y+rect.h), color, 2)
rects2.pop(0)

for rect in rects2:
    color = (0,255,0)
    cv.rectangle(img2, (rect.x, rect.y),
                 (rect.x+rect.w, rect.y+rect.h), color, 2)
    
rects3 = rects2[14:]
rects3.sort(key=lambda rect : (rect.x, rect.y, rect.w, rect.h))

for i in range(14):
    color = (0,255,0)
    cv.rectangle(img3, (rects2[i].x, rects2[i].y),
                 (rects2[i].x+rects2[i].w, rects2[i].y+rects2[i].h), color, 2)

for i in range(len(rects3)-1):
    color = (0,255,0)
    rect = rects3[i]
    nextrect = rects3[i+1]

    if (rect.x <= nextrect.x+nextrect.w and nextrect.x <= rect.x+rect.w and rect.y <= nextrect.y+nextrect.h and nextrect.y <= rect.y+rect.h):
        pass


print('rects3')
print(rects3)


k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    cv.imwrite('testgray.jpg', gray)
    cv.imwrite('testblur.jpg', blur)
    cv.imwrite('testcanny.jpg', canny)

    cv.imwrite('testimg1.jpg', img1)
    cv.imwrite('testimg2.jpg', img2)
    cv.imwrite('testimg3.jpg', img3)

    cv.imwrite('extractTable.jpg', tableArea)

    cv.destroyAllWindows()