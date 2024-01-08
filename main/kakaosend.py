import requests
import json

with open(r"/json파일이 있는 경로/kakao.json","r") as fp:
    tokens = json.load(fp)

friend_url = "https://kapi.kakao.com/v1/api/talk/friends"


headers={"Authorization" : "Bearer " + tokens["access_token"]}

result = json.loads(requests.get(friend_url, headers=headers).text)
friends_list = result.get("elements")
print(friends_list)
print("\n")
friend_id = friends_list[0].get("uuid") #리스트에 사람이 많다면 이부분 수정해서 사용
print(friend_id)

send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

data={
    'receiver_uuids': '["{}"]'.format(friend_id),
    "template_object": json.dumps({
        "object_type":"text",
        "text":"전송 테스트입니다.",
        "link":{
            "web_url":"google.com",
        },
        "button_title": "바로가기"
    })
}

response = requests.post(send_url, headers=headers, data=data)
response.status_code