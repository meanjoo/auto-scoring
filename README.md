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
* 읽기: `cv2.imread()` 함수를 이용한다.
  
* 저장: `cv2.imwrite()` 함수를 이용한다.

