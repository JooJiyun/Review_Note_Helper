# 오답노트 도우미
 ##### 문제파일(pdf파일)과 틀린번호 입력 -> 오답파일 생성
 
* 사용 라이브러리
```swift
pandas==1.3.4,
Pillow==8.4.0,
pdf2image==1.16.0,
```
	 - poppler-utils 필요
	 - NotoSansKR-Regular.otf 폰트 파일 사용
	코드파일과 같은 폴더에 있어야함
	다른 폰트 사용시 코드 변경 필요
	https://fonts.google.com/noto/specimen/Noto+Sans+KR

* 스크린샷

|   |   |
| ------------ | ------------ |
| <img src = "https://github.com/JooJiyun/Review_Note_Helper/blob/main/screenshot/capture1.PNG" width ="400" height="265">  |  <img src = "https://github.com/JooJiyun/Review_Note_Helper/blob/main/screenshot/capture2.PNG" width ="400" height="265">  |

<br>
* 사용법
	1. 문제지관리 탭에서 학년별 문제집 등록
	2. 오답노트 탭에서 학생 등록 후 문제집과 틀린번호 선택
	3. 오답노트에 들어갈 문제지들을 선택후 오답노트생성 버튼 클릭

<br>
* 사용가능한 문제지 형식 예시(pdf파일)

|   |   |
| ------------ | ------------ |
| <img src = "https://github.com/JooJiyun/Review_Note_Helper/blob/main/screenshot/format.png" width ="400" height="580">  |  <img src = "https://github.com/JooJiyun/Review_Note_Helper/blob/main/screenshot/format_area.png" width ="400" height="580">  |

	-노란색 영역 : header와 footer 영역
	-분홍색 영역 : 문제영역
	-파란색 영역 : 문제번호영역
