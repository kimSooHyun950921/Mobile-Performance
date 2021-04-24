# Robot based Application Performance Test
## 1. Introduce
### This Code is Composed of Three Part
1. Robot Manage Module(clone from Tapster.io)
    - Robot Manage Module Operates Robots 
    - Robot Manage Module requests to Image Analysis Module 
3. Image Analysis and Object Detetction Module(clone from keras-retinanet)
    - Analaysis Mobile App's Clickable Element
    - Send Click Axis to Robot
5. Peformance Analysis Module
    - Uses Correlate2d and SSIM
    - Calcuates Speed Index(https://web.dev/speed-index/)
    - Analyzes Packet
## 2. TODO List
1. 각 모듈별 Docker Composing
2. 웹으로 접근할 수 있는 페이지 만들기
    - vue.js로 웹 프론트엔드 만들기
    - Django로 웹 백엔드 만들기
 3. Object Detection 개선
    - 모바일 앱의 위젯별로 인식하는 Object Detection 모델 생성
 4. 웹으로부터 .apk 파일 받는 프로그램 만들기
    - 아이폰앱파일은 어떻게 설치하는지? (고민해야할부분)
 5. 이미지로 앱 아이콘 찾기(SIFT, SURF)
## 4. Reference 
1. clone and modify from https://github.com/tapsterbot/tapsterbot
2. clone and modify from https://github.com/fizyr/keras-retinanet
3. clone and modify from https://github.com/munhyunsu/ApplicationPerformance
