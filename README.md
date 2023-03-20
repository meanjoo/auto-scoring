# auto-scoring

## Environment
* Editor: vscode  
* Python 3.10.7  
* OpenCV 4.7.0  

## OpenCV
`pip list`를 통해 설치된 패키지를 확인할 수 있다.

### opencv 설치  
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
  * filename
  
    이미지 파일의 경로
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

  * winname
  
    윈도우 창의 제목
  
  * mat
  
    표시할 이미지
  
* 저장: `cv2.imwrite()` 함수를 이용한다.

example] 
