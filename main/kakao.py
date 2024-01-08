import requests
import json

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '개인 rest api key'
redirect_uri = 'https://example.com/oauth'
authorize_code = '주소에서 받은 code= 이후부분'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# Token저장
with open(r"/home/masgt/Desktop/main/kakao.json","w") as fp:
    json.dump(tokens, fp)

#https://kauth.kakao.com/oauth/authorize?client_id=478f42744e62a0277a6dc1c4da3ef228&redirect_uri=https://example.com/oauth&response_type=code&scope=talk_message,friends
