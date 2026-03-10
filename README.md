# MyLock

> A Raspberry Pi smart lock that combines keypad authentication, face recognition, access logging, and alert delivery.

<img width="520" alt="MyLock overview" src="https://github.com/lee-seong-wook/MyLock/assets/130055880/8f207969-70e9-4d09-b557-f384f075e55d">

## Overview
MyLock은 Raspberry Pi 기반으로 구현한 얼굴 인식 도어락 프로젝트입니다. 키패드 비밀번호 입력, LCD 안내, 릴레이 기반 도어락 제어, dlib 기반 얼굴 인식, MySQL 기록 저장, FTP 사진 전송, 카카오톡 알림까지 하나의 흐름으로 통합했습니다. 단순 인증 장치를 넘어서 출입 기록과 이상 상황 대응까지 고려한 스마트 잠금 시스템으로 구성했습니다.

## Project Context
| Item | Details |
| --- | --- |
| Context | Daelim University project |
| Period | 2023.08 ~ 2023.11 |
| Goal | 얼굴 인식과 비밀번호 인증을 결합한 스마트 도어락 구현 |
| Scope | 하드웨어 연동, 얼굴 인식 파이프라인, 출입 기록 저장, 알림 전송 |

## My Role
- 하드웨어와 소프트웨어 전체 구성을 통합해 프로젝트를 구현했습니다.
- 키패드, LCD, 릴레이 제어와 얼굴 인식 인증 흐름을 하나의 제어 로직으로 연결했습니다.
- 사용자 등록, 침입 사진 저장, DB 기록, 카카오톡 알림까지 보안 시나리오를 포함해 정리했습니다.

## Tech Stack
`Python`, `Raspberry Pi 4`, `OpenCV`, `dlib`, `MySQL`, `GPIO`, `I2C LCD`, `FTP`, `KakaoTalk API`

## Key Contributions
- 키패드 입력과 LCD 안내를 포함한 도어락 제어 로직 구현
- dlib 기반 얼굴 인식과 등록 사용자 비교 파이프라인 구성
- 비밀번호 오류 누적 시 사진 촬영, FTP 업로드, 카카오톡 알림 처리
- MySQL 기반 출입 기록과 상태 업데이트 흐름 구현

## Implementation Notes
- `main.py`: 키패드 입력, 얼굴 인식, 릴레이 제어, DB 기록, 알림 전송을 묶는 메인 제어 스크립트
- `main/sub/face.py`: 사용자 얼굴 등록 보조 스크립트
- `main/sub/`: 얼굴 인식 모델 파일과 참조 이미지 보관
- `main/RPi_I2C_LCD_driver`: LCD 제어 드라이버
- `main/` 하위에는 카카오톡 연동 관련 보조 스크립트가 포함되어 있습니다.

## Images / Demo
<img width="520" alt="MyLock detail" src="https://github.com/lee-seong-wook/MyLock/assets/130055880/af318836-e278-4316-bd99-1b6cac954729">

<details>
<summary>Legacy Notes</summary>

### Team
| Name | Role |
| --- | --- |
| 이성욱 | 하드웨어 및 소프트웨어 구현 |
| 이용진 | 하드웨어 및 소프트웨어 구현 |
| 장성영 | 웹 개발 |
| 예진희 | 웹 개발 |

### Setup Notes
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo pip install numpy
sudo pip install opencv-python
pip install mysql-connector-python
pip install mysql.connector
sudo pip install cmake
sudo apt-get install libatlas-base-dev
sudo pip install dlib
sudo apt-get install python-smbus
i2cdetect -y 1
git clone https://github.com/eleparts/RPi_I2C_LCD_driver
cd RPi_I2C_LCD_driver
python3 example.py
```

기존 README의 상세 설치 기록은 유지하되, 상단에는 프로젝트 설명 중심으로 재구성했습니다.

</details>
