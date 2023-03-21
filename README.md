# auto-scoring

## Environment
* Editor: vscode  
* Python 3.10.7  
* OpenCV 4.7.0  

## OpenCV
`pip list`를 통해 설치된 패키지를 확인할 수 있다.

### opencv 설치
둘 중 하나를 설치해주면 된다.
```
pip install opencv-python # 메인 모듈만 포함된 기본 Python OpenCV 패키지 
pip install opencv-contrib-python # 메인 모듈과 확장 모듈이 포함된 패키지
```

```
import cv2 as cv
print(cv.__version__)
```
설치 후에 위 코드를 통해 설치된 opencv의 버전이 출력되면 정상적으로 설치된 것이다.

### 이미지
* 읽기: `cv2.imread(filename[, flags])` 함수를 이용한다. [reference](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#ga288b8b3da0892bd651fce07b3bbd3a56)
  
  색상을 표현하는 방법 중 빨강, 초록, 파랑 세 종류의 빛을 이용하여 색을 표현하는 RGB 방식이 있다.  
  **OpenCV는 이 반대 순서인 BGR로 색상을 표현한다.**
  
  `imread()`에 옵션을 주지 않으면 default인 `cv2.IMREAD_COLOR`가 적용되어 BGR 색상 이미지로 불러온다.
  * filename : 이미지 파일의 경로
  * flags 옵션  
  
    `cv2.IMREAD_COLOR` : default; BGR 이미지로 읽기  
    `cv2.IMREAD_GRAYSCALE` : Grayscale(회색조) 이미지로 읽기  
    `cv2.IMREAD_UNCHANGED` : Alpha channel까지 포함하여 이미지 읽기
  
  `cv2.cvtColor()` 함수를 이용하여 처음부터 Grayscale로 불러오지 않고 BGR 이미지로 불러온 후 Grayscale 이미지로 변환할 수도 있다.
  ```
  bgr_img = cv2.imread(filename)
  gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
  ```

* 보기: `cv2.imshow(winname, mat)` 함수를 이용한다. [reference](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga453d42fe4cb60e5723281a89973ee563)

  * winname : 창의 이름
  * mat : 표시할 이미지
    
  ※ Note  
  표시할 이미지 창을 마우스 및 키보드 이벤트에 응답하게 만드려면 `cv2.waitKey()` 또는 `cv2.pollKey()`를 사용해야 한다.  
  이 함수를 사용하지 않으면 이미지 창이 표시되지 않는다.
  
* 저장: `cv2.imwrite(filename, img[, params])` 함수를 이용한다. [reference](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce)

  * filename : 파일명  
  * img : 저장될 이미지
  
* 창 관리
  * `cv2.namedWindow(winname[, flags])` : 새 창을 만드는 함수 [reference](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga5afdf8410934fd099df85c75b2e0888b)
    * winname: 창의 이름  
    * flags 옵션  
      ※ `cv2.namedWindow()`가 `cv2.imshow()`보다 선행하고, `cv2.namedWindow()`의 winname과 `cv2.imshow()`의 winname이 일치해야 flags 옵션이 해당 winname의 윈도우에 적용된다. 두 이름이 다르면 이름이 다른 창이 2개 생성된다.
      
      `cv2.WINDOW_NORMAL` : 사용자가 창 크기를 조절할 수 있다.  
      `cv2.WINDOW_AUTOSIZE` : default; 이미지와 동일한 크기로 창이 생성되며 창 크기를 조절할 수 없다.
  * `cv2.moveWindow(winname, x, y)` : 윈도우 위치 이동 [reference](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga8d86b207f7211250dbe6e28f76307ffb)
    * winname : 창 이름
    * x : 창을 이동시킬 위치의 x 좌표
    * y : 창을 이동시킬 위치의 y 좌표
  * `cv2.resizeWindow(winname, width, height)` : 창 크기 조절 [reference](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga9e80e080f7ef33f897e415358aee7f7e)
    * winname : 창 이름
    * width : 창의 너비
    * height : 창의 높이
  * `cv2.destroyWindow(winname)` : 창 이름이 winname인 특정 창 닫기 [reference](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga851ccdd6961022d1d5b4c4f255dbab34)
    * winname : 창 이름
  * `cv2.destroyAllWindows()` : 열린 모든 창 닫기 [reference](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga6b7fc1c1a8960438156912027b38f481)

* 키보드 이벤트
  * `cv2.waitKey([, delay])` : 키보드 입력 대기 [reference](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html#ga5628525ad33f52eab17feebcfba38bd7)
    * delay  
      0 : default; key 입력이 있을 때까지 무한 대기
      
    ※ Esc를 누르면 27을 return

**[example]** RGB 이미지를 Grayscale로 읽어서 윈도우 창에 띄운 후 Esc를 누르면 창을 닫고, s를 누르면 이미지를 저장한 후 창을 닫는 코드
```
import cv2 as cv
import sys

path = 'C:/Users/user/Desktop/workspace/test_image'
img = cv.imread(path+'/sample1.jpg', cv.IMREAD_GRAYSCALE)

if img is None:
    sys.exit('Could not read the image.')

cv.imshow('Display window', img)
k = cv.waitKey(0)

if k == 27:
    cv.destroyAllWindows()
elif k == ord('s'):
    cv.imwrite('gray_sample1.jpg', img)
    cv.destroyAllWindows()
```
※ 주의  
path 변수에 경로를 저장할 때 탐색기에서 경로를 그대로 복사해서 붙여넣으면 오류가 발생한다.  
그대로 복사붙여넣기 하면 `path = C:\Users\user\Desktop\workspace\test_image`와 같은 형태가 된다.  
오류를 없애기 위해서는 `path = C:/Users/user/Desktop/workspace/test_image` 또는 `path = C:\\Users\\user\\Desktop\\workspace\\test_image`로 변경해야 한다.  
또는 path 변수 없이 `img = cv.imread(r'C:\Users\user\Desktop\workspace\test_image\sample1.jpg', cv.IMREAD_GRAYSCALE)`로도 해결할 수 있다.

