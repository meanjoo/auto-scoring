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
    
    def __hash__(self) -> int: # 같은지 비교를 위함 -> ==과 set에서 씀
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

cv.namedWindow('image', cv.WINDOW_NORMAL)
cv.imshow('image', img)

rects = getContoursRect(img)
rects.sort(key=lambda rect : (-(rect.w*rect.h), rect.x, rect.y)) # 가장 큰 사각형을 찾기 위함
tableRect = rects[0] # tableRect: 가장 큰 사각형
offset = 0
tableRect.x = max(0, tableRect.x - offset)
tableRect.y = max(0, tableRect.y - offset)
tableArea = img[tableRect.y:tableRect.y+tableRect.h+offset*2, tableRect.x:tableRect.x+tableRect.w+offset*2] # 표 영역만 추출(BGR)
grayTable = cv.cvtColor(tableArea, cv.COLOR_BGR2GRAY)

img1 = tableArea.copy()
img2 = tableArea.copy()


row, col = 7, 2 # table의 행과 열 개수
h = int(tableRect.h / row) # 문항 박스 하나의 높이
w = int(tableRect.w / col) # 문항 박스 하나의 너비
offset = -10
imgidx, imgidx28 = 1, 1

savepath = './save_test'
whiteBg = cv.imread(path + '/white_bg.jpg', cv.IMREAD_GRAYSCALE)

for c in range(col):
    for r in range(row):
        sx = max(0, c*w - offset)
        ex = min(tableRect.w, sx + w + offset*2)
        sy = max(0, r*h - offset)
        ey = min(tableRect.h, sy + h + offset*2)
        box = tableArea[sy:ey, sx:ex]
        box2 = box.copy()
        grayBox = cv.cvtColor(box, cv.COLOR_BGR2GRAY)
        border, boxBinary = cv.threshold(grayBox, 125, 255, cv.THRESH_BINARY)

        cv.imwrite('binarytest' + str(imgidx) + '.jpg', boxBinary)

        rects = getContoursRect(box)
        for rect in rects: # 처리 전 그려보기
            color = (0,255,0)
            cv.rectangle(box, (rect.x, rect.y),
                 (rect.x+rect.w, rect.y+rect.h), color, 2)
        
        # 포함되는 사각형이 있으면 하나로 합치는 과정 -> 겹치는 사각형이 있으면 하나로 합치기
        rects.sort(key=lambda rect : (rect.x, rect.y, rect.w, rect.h))
        idx = 0
        # print(f'before: {r}, {c}: {rects}')

        while idx < len(rects)-1:
            # # 두 사각형이 만약 포함 관계라면 포함되는 사각형의 minPt x,y 좌표는 두 사각형 중 더 큰 값이고, maxPt x,y 좌표는 두 사각형 중 더 작은 값이다.
            # # ix1: 포함되는 사각형의 minPt의 x 좌표, iy1: 포함되는 사각형의 minPt의 y 좌표
            # # ix2: 포함되는 사각형의 maxPt의 x 좌표, iy2: 포함되는 사각형의 masPt의 y 좌표
            # # ir: 포함되는 사각형
            # ix1 = max(rects[idx].x, rects[idx+1].x)
            # iy1 = max(rects[idx].y, rects[idx+1].y)
            # ix2 = min(rects[idx].x+rects[idx].w, rects[idx+1].x+rects[idx+1].w)
            # iy2 = min(rects[idx].y+rects[idx].h, rects[idx+1].y+rects[idx+1].h)
            # ir = Rect((ix1, iy1, ix2-ix1, iy2-iy1))

            # if rects[idx] == ir:
            #     # 포함되는 사각형 중 큰 사각형만 idx번째에 남기기
            #     rects[idx] = rects[idx+1]
            #     rects.pop(idx+1)
            # elif rects[idx+1] == ir:
            #     rects.pop(idx+1)
            # else:
            #     idx += 1

            if (rects[idx].x <= rects[idx+1].x+rects[idx+1].w and
                rects[idx].x+rects[idx].w >= rects[idx+1].x and
                rects[idx].y <= rects[idx+1].y+rects[idx+1].h and
                rects[idx].y+rects[idx].h >= rects[idx+1].y):
                nx = min(rects[idx].x, rects[idx+1].x)
                ny = min(rects[idx].y, rects[idx+1].y)
                nw = max(rects[idx].x+rects[idx].w, rects[idx+1].x+rects[idx+1].w) - min(rects[idx].x, rects[idx+1].x)
                nh = max(rects[idx].y+rects[idx].h, rects[idx+1].y+rects[idx+1].h) - min(rects[idx].y, rects[idx+1].y)
                rects[idx].x = nx
                rects[idx].y = ny
                rects[idx].w = nw
                rects[idx].h = nh
                rects.pop(idx+1)
            else:
                idx += 1

        # 겹치는 사각형을 다 합치고도 불필요한 사각형이 존재하면 버리기
        idx = 0
        while idx < len(rects):
            if (rects[idx].w*rects[idx].h) <= 10:
                rects.pop(idx)
            else:
                idx += 1

        for rect in rects:
            color = (0,255,0)
            cv.rectangle(box2, (rect.x, rect.y),
                 (rect.x+rect.w, rect.y+rect.h), color, 2)
            
        for rect in rects:
            target = boxBinary[rect.y:rect.y+rect.h, rect.x:rect.x+rect.w]
            mask = 255-target
            sz = (int)(max(rect.w, rect.h)*1.5)
            squareWhite = cv.resize(whiteBg.copy(), dsize=(sz,sz))

            # squareimg 중심: (sz/2, sz/2)
            # img의 시작점: (sz/2 - w/2, sz/2 - h/2)
            sx = (int)(sz/2 - rect.w/2)
            sy = (int)(sz/2 - rect.h/2)
            crop = squareWhite[sy:sy+rect.h, sx:sx+rect.w]
            cv.copyTo(target, mask, crop)

            cv.imwrite(savepath + '/squareimg' + str(imgidx) + '.jpg', squareWhite) # 28*28 아님
            imgidx += 1

            # 28*28로 변환
            if squareWhite.shape[0] > 28: # 이미지 축소 - INTER_AREA
                squareWhite = cv.resize(squareWhite, (28,28), interpolation=cv.INTER_AREA)
            elif squareWhite.shape[0] < 28: # 이미지 확대 - INTER_LINEAR(default, slow) / INTER_CUBIC(linear보다 느리지만 품질 굿)
                squareWhite = cv.resize(squareWhite, (28,28), interpolation=cv.INTER_LINEAR)
            cv.imwrite(savepath + '/square28img' + str(imgidx28) + '.jpg', squareWhite)
            imgidx28 += 1
        
        cv.imwrite(savepath + '/square28img' + str(imgidx28) + '.jpg', cv.resize(whiteBg, (28,28), interpolation=cv.INTER_AREA)) # 문항 마지막에 흰색 배경 추가
        imgidx28 += 1
        # print(f'after: {r}, {c}: {rects}')

        cv.imwrite(str(r) + str(c) + 'a.jpg', box)
        cv.imwrite(str(r) + str(c) + 'b.jpg', box2)

k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    # cv.imwrite('testgray.jpg', gray)
    # cv.imwrite('testblur.jpg', blur)
    # cv.imwrite('testcanny.jpg', canny)

    cv.imwrite('testimg1.jpg', img1)
    cv.imwrite('testimg2.jpg', img2)

    cv.imwrite('extractTable.jpg', tableArea)

    cv.destroyAllWindows()