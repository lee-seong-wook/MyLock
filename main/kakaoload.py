import requests
import json

with open(r"json파일이 있는 경로/kakao.json","r") as fp:
    tokens = json.load(fp)

friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

headers={"Authorization" : "Bearer " + tokens["access_token"]}

result = json.loads(requests.get(friend_url, headers=headers).text)
print(result)

friends_list = result.get("elements")
if friends_list:
    friend_id = friends_list[0].get("uuid")
    print(friend_id)
else:
    print("친구 목록이 비어 있습니다.")