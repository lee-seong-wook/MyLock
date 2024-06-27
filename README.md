# MyLock

<img width="500" alt="image" src="https://github.com/lee-seong-wook/MyLock/assets/130055880/8f207969-70e9-4d09-b557-f384f075e55d"> <img width="280" alt="image" src="https://github.com/lee-seong-wook/MyLock/assets/130055880/af318836-e278-4316-bd99-1b6cac954729"> 

## 팀 소개

|      이성욱       |          이용진         |       장성영         |         예진희        |
| :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
|   <img width="160px" src="https://github.com/lee-seong-wook/MyLock/assets/130055880/813d2c89-0c3b-49c6-89ed-43969d02ce1f" />    |                      <img width="160px" src="https://github.com/lee-seong-wook/object-detection-robot-/assets/130055880/b032aa51-f0d0-4354-b310-d57b3549b58a" />    |                  <img width="160px" src="https://github.com/lee-seong-wook/MyLock/assets/130055880/cf67e022-41c2-45d4-94ab-dff07c089034"/>   |       <img width="160px" src="https://github.com/lee-seong-wook/MyLock/assets/130055880/0bf50633-c987-4620-b488-602a8f4f91c6"/>         |
| 대림대학 메카트로닉스과 3학년 | 대림대학 메카트로닉스과 3학년 | 대림대학 메카트로닉스과 3학년 | 대림대학 메카트로닉스과 3학년 |
|  하드웨어 및 소프트웨어 구현    |  하드웨어 및 소프트웨어 구현   | 웹 개발  |  웹 개발    |


## 사용 환경 
#### Rasberry Pi 4

## 초기 설정
```bash
$ sudo apt-get update  #업데이트할 패키지들의 목록을 최신으로 갱신합니다.
$ sudo apt-get upgrade # update로 갱신된 최신 패키지들을 실제로 업그레이드합니다.
```
## Python 설치
```bash
$ sudo apt-get install python3-pip #버전은 3.11을 사용했습니다.
```
## Numpy 및 OpenCV 설치
```bash
$ sudo pip install numpy
$ sudo pip install opencv-python
```
## MySQL 설치
```bash
$ pip install mysql-connector-python #MySQL 8.0 이상 유저 사용
$ pip install mysql.connector # 하위 버전 사용
```

## Dlib 설치
```bash
$ sudo pip install cmake
$ sudo apt-get install libatlas-base-dev
$ sudo pip install dlib
# 참고: dlib 설치 시 시간이 많이 소요될 수 있습니다. 설치가 실패할 경우,
 직접 라이브러리를 다운로드하여 설치하는 방법도 고려해 보시기 바랍니다.
```
## LCD 라이브러리 설치
```bash
$ sudo apt-get install python-smbus
$ i2cdetect -y 1 # 이 명령어를 사용하면 행열로 연결된 숫자가 나오는데 저희 LCD 제품의 경우 0x27이 나왔습니다. (lcd 제품별로 나오는 숫자가 다릅니다.)
$ git clone https://github.com/eleparts/RPi_I2C_LCD_driver # 패키지 다운로드 합니다
$ cd RPi_I2C_LCD_driver # 패키지 설치 후 해당 디렉토리로 이동합니다. 
$ python3 example.py # 이 명령어를 통해 LCD 동작 테스트를 진행합니다. 
```




