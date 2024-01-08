import cv2
import time
import ftplib
import dlib
import os
import sys
import threading
import mysql.connector
import requests
import json
from RPi_I2C_LCD_driver import RPi_I2C_driver
import RPi.GPIO as GPIO
import numpy as np

#파일 위치 및 사진저장 기본경로지정
PATH = r'파일을 놔둔 경로/main/sub'
os.chdir(PATH)

#lcd
lcd = RPi_I2C_driver.lcd(0x27)

#키패드 행, 열 정의
L1 = 5
L2 = 6
L3 = 13
C1 = 12
C2 = 16
C3 = 20
C4 = 21

#사용할 기본변수
pinRELAY = 18
keypadPressed = -1
count = 0
rcount = 0
lcdkey = 0
input = ""
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

#얼굴인식 설정
detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor(os.path.join(PATH, 'shape_predictor_68_face_landmarks.dat'))
face_rec_model = dlib.face_recognition_model_v1(os.path.join(PATH, 'dlib_face_recognition_resnet_model_v1.dat'))

def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

def shape_to_np(dlib_shape):
    return np.array([(dlib_shape.part(i).x, dlib_shape.part(i).y) for i in range(68)])

def detect_face_embedding(img, landmark_detector, face_recognizer):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    if len(rects) < 1:
        return None, None

    # 첫 번째 인식된 얼굴 사용
    rect = rects[0]
    shape = landmark_detector(gray, rect)
    landmarks = shape_to_np(shape)
    face_descriptor = face_recognizer.compute_face_descriptor(img, shape)

    return landmarks, face_descriptor

#작동내역(열림 등) 전송 세팅
def datasend(table1, colom1, colom2, data1, data2):
    connection = mysql.connector.connect(
        host = "zxz0608.cafe24.com",
        user = "유저 아이디",
        password = "비밀번호",
        database = "데이터 베이스"
    )
    cursor = connection.cursor()
    sql = "INSERT INTO "+table1+" (" + colom1+", " + colom2+") VALUES (%s, %s)"
    data = (data1, data2)
    cursor.execute(sql, data)
    connection.commit()
    cursor.close()
    connection.close()

#실행문 관련 업데이트 설정
def dataUpdate(table1, colom1, data1, colom2, data2):
    connection = mysql.connector.connect(
        host = "zxz0608.cafe24.com",
        user = "유저 아이디",
        password = "비밀번호",
        database = "데이터 베이스"
    )
    cursor = connection.cursor()
    sql = "UPDATE {} SET {} = %s WHERE {} = %s".format(table1, colom1, colom2)
    cursor.execute(sql, (data1, data2))
    connection.commit()
    cursor.close()
    connection.close()

#사진data 전송부 세팅
def sendphoto(osphoto, path, file):
    ftp = ftplib.FTP()
    ftp.connect("아이피주소",포트번호)
    ftp.login("아이디","비밀번호")
    ftp.cwd(osphoto)
    os.chdir(path)
    myfile = open(file,'rb')
    ftp.storbinary('STOR '+file, myfile)
    myfile.close()
    ftp.close()

#data 수신부 세팅
def datarecv(colom1, table1, colom2, data1):
    connection = mysql.connector.connect(
        host = "zxz0608.cafe24.com",
        user = "유저 아이디",
        password = "비밀번호",
        database = "데이터 베이스"
    )
    cursor = connection.cursor()
    sql = "SELECT {} FROM {} WHERE {} = %s".format(colom1, table1, colom2)
    cursor.execute(sql, data1)
    results = cursor.fetchall()
    for row in results:
        second_value = row[0]
    cursor.close()
    connection.close()
    return second_value

#웹페이지 초기세팅(이 부분은 저희 sql내 테이블 명으로 작업한거라 사용하시려면 수정 하셔야 합니다.)
sendphoto(osphoto = "서버내 얼굴인증 사진올리는 경로", path='메인화면에 표시할 기본이미지가 있는경로', file="face8.jpg")
dataUpdate(table1= 'userManagement', colom1='pw', data1='0000', colom2 = 'user_name', data2='1001')
dataUpdate(table1= 'userManagement', colom1='tp', data1='0', colom2 = 'user_name', data2='1001')
dataUpdate(table1= 'userManagement', colom1='errorcode', data1='0', colom2 = 'user_name', data2='1001')
dataUpdate(table1= 'userManagement', colom1='SL', data1='1', colom2 = 'user_name', data2='1001')
dataUpdate(table1= 'userManagement', colom1='reset', data1='0', colom2 = 'user_name', data2='1001')
os.chdir(PATH)

#kakaotalk 세팅
def kakao(txt):
    with open(r"/home/masgt/Desktop/main/output.json","r") as fp:
        tokens = json.load(fp)
    friend_url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers={"Authorization" : "Bearer " + tokens["access_token"]}
    result = json.loads(requests.get(friend_url, headers=headers).text)
    friends_list = result.get("elements")
    friend_id = friends_list[2].get("uuid")
    send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    kakao_send1={
        'receiver_uuids': '["{}"]'.format(friend_id),
        "template_object": json.dumps({
            "object_type":"text",
            "text":"전송할 메시지 입력",
            "link":{
                "web_url":"사용할 주소 입력",
            },
            "button_title": "바로 확인하기"
        })
    }
    response = requests.post(send_url, headers=headers, data=kakao_send1)
    response.status_code
kakao("사용자 등록 및\n비밀번호를 설정해 주세요")

#병렬 쓰레드
def periodic_task():
    global lcdkey
    global PATH
    while True:
        #도어락 리셋
        if datarecv(colom1='reset', table1='userManagement', colom2='user_name', data1=("1001",)) == str(1):
            restart()

        #사용자 추가 등록
        if datarecv(colom1='tp', table1='userManagement', colom2='user_name', data1=("1001",)) == str(1):
            exec(open("/home/masgt/Desktop/main/sub/face.py").read())
            
            sendphoto(osphoto = "./doorLockManagement/1001/facePicture", path=PATH, file="face8.jpg")
            dataUpdate(table1= 'userManagement', colom1='tp', data1='0', colom2 = 'user_name', data2='1001')
            lcdkey = 1
        time.sleep(1)

#스레드 시작
task_thread = threading.Thread(target=periodic_task)
task_thread.daemon = True
task_thread.start()

#GPIO 세팅
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(pinRELAY, GPIO.OUT)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)

# 비밀번호 대조비교
def checkSpecialKeys():
    global current_time, input, count
    pressed = False

    GPIO.output(L3, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        lcd.lcd_clear()
        pressed = True

    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)
    if (not pressed and GPIO.input(C4) == 1):

        if input == datarecv(colom1='pw', table1='userManagement', colom2='user_name', data1=("1001",)) and datarecv(colom1='errorcode', table1='userManagement', colom2='user_name', data1=("1001",)) != str('1'):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            lcd.lcd_display_string("Password Correct", 1)
            time.sleep(1)
            lcd.lcd_clear()
            datasend(table1='actionRecoding', colom1='user_name', colom2='word', data1="1001", data2='인증되었습니다.')

            #if안쪽이 2단계 즉 얼굴인식까지 사용 else부분이 1단계 즉 얼굴인식을 사용하지 않을 때
            if datarecv(colom1='SL', table1='userManagement', colom2='user_name', data1=("1001",)) == str(2):
                count = -1
            else:
                lcd.lcd_clear()
                lcd.lcd_display_string("Welcome",1)
                time.sleep(1)
                GPIO.output(pinRELAY, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(pinRELAY, GPIO.LOW)

        elif input != datarecv(colom1='pw', table1='userManagement', colom2='user_name', data1=("1001",)) and datarecv(colom1='errorcode', table1='userManagement', colom2='user_name', data1=("1001",)) != str('1'):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            count += 1
            lcd.lcd_display_string("Wrong Password",1)
            time.sleep(3)
            lcd.lcd_clear()
            datasend(table1='actionRecoding', colom1='user_name', colom2='word', data1="1001", data2='비밀번호가 틀렸습니다.')
        
        #5회이상 틀렸을 시 대조 잠금
        if datarecv(colom1='errorcode', table1='userManagement', colom2='user_name', data1=("1001",)) == str('1'):
            lcd.lcd_clear()
            lcd.lcd_display_string("Password Locked",1)
            time.sleep(3)
            lcd.lcd_clear()

        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        input = ""
    return pressed

#키패드 값 읽어오기
def readLine(line, characters):
    global input
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
    GPIO.output(line, GPIO.LOW) 

while True:
    #키패드 배열 세팅밑 인식
    if keypadPressed != -1:
        setAllLines(GPIO.HIGH)
        if GPIO.input(keypadPressed) == 0:
            keypadPressed = -1
        else:
            time.sleep(0.1)
            
    else:
        if not checkSpecialKeys():
            readLine(L1, ["1","4","7","*"])
            readLine(L2, ["2","5","8","0"])
            readLine(L3, ["3","6","9","#"])
            time.sleep(0.1)
        else:
            time.sleep(0.1)

    if lcdkey == 1:
        lcd.lcd_clear()
        lcd.lcd_display_string("Finish", 1)
        time.sleep(2)
        lcd.lcd_clear()
        lcdkey = 0

    if count == -1:
        lcd.lcd_clear()
        lcd.lcd_display_string("Start Recognize",1)

        reference_image_file1 = "등록한 사용자 얼굴 사진경로/face8.jpg"
        reference_image_file2 = "테스트용 고정얼굴 경로/manager.jpg"
        reference_image1 = cv2.imread(reference_image_file1, 1)
        reference_image2 = cv2.imread(reference_image_file2, 1)
        ref_landmarks1, reference_face_descriptor1 = detect_face_embedding(reference_image1, landmark_predictor, face_rec_model)
        ref_landmarks2, reference_face_descriptor2 = detect_face_embedding(reference_image2, landmark_predictor, face_rec_model)
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        ret, frame = cap.read()
        rcount+=1
        time.sleep(1)
        face_landmarks, face_descriptor = detect_face_embedding(frame, landmark_predictor, face_rec_model)

        if face_landmarks is not None:
            try:
                distance1 = np.linalg.norm(np.array(face_descriptor) - np.array(reference_face_descriptor1))
                distance2 = np.linalg.norm(np.array(face_descriptor) - np.array(reference_face_descriptor2))
                rcount+=1
                time.sleep(1)

                #얼굴인증 맞을시 도어락 오픈
                if distance1 < 0.35 or distance2<0.4:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Welcome",1)
                    time.sleep(1)
                    GPIO.output(pinRELAY, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(pinRELAY, GPIO.LOW)
                    count = 0
                    rcount = 0

                    #5초안에 얼굴인증 실패시 실행
                elif rcount > 5 and (distance1 >= 0.33 or distance2 >= 0.33):
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Fail", 1)
                    time.sleep(1)
                    count = 7
                    rcount = 0

            except:
                lcd.lcd_clear
                lcd.lcd_display_string("Update Your", 1)
                lcd.lcd_display_string("Face Again", 2)
                time.sleep(5)
                count = 0
                rcount = 0
                lcd.lcd_clear()

        lcd.lcd_clear()
        cap.release()
        cv2.destroyAllWindows()

    #비밀번호 인증 3회 실패시 사진 촬영밑 전송
    if count == 3:
        timestr = time.strftime('%Y%m%d_%H%M%S')

        cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        filename = f'thief_{str(timestr)}.jpg'
        res, frame = cap.read()
        frame = cv2.flip(frame,1)
        cv2.imwrite(filename, frame) 
        cap.release()
        cv2.destroyAllWindows()

        datasend(table1='actionRecoding', colom1='user_name', colom2='word', data1="1001", data2='사진을 촬영했습니다.')
        sendphoto(osphoto = "서버 내 사진 저장 경로", path=PATH, file=filename)
        kakao("비밀번호 3회 오류")
        count = 4

    #비밀번호 인증 5회 실패시 반영구적 잠금
    if count == 6:
        lcd.lcd_display_string("Password Locked",1)

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        datasend(table1='actionRecoding', colom1='user_name', colom2='word', data1="1001", data2='비밀번호가 비활성화 되었습니다.')
        dataUpdate(table1= 'userManagement', colom1='errorcode', data1='1', colom2 = 'user_name', data2='1001')
        kakao("비밀번호 5회오류\n도어락 인증을 차단합니다")
        count = 0
        rcount = 0
        lcd.lcd_clear()

    #얼굴인식 실패시 도어락 반영구 잠금
    if count == 7:
        lcd.lcd_display_string("Password Locked",1)

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        datasend(table1='actionRecoding', colom1='user_name', colom2='word', data1="1001", data2='비밀번호가 비활성화 되었습니다.')
        dataUpdate(table1= 'userManagement', colom1='errorcode', data1='1', colom2 = 'user_name', data2='1001')
        kakao("얼굴인식 실패 \n도어락 인증을 차단합니다")
        count = 0
        rcount = 0
        lcd.lcd_clear()

    print(input)
    if rcount == 0:
        lcd.lcd_display_string("Enter Password", 1)
        lcd.lcd_display_string(input, 2)