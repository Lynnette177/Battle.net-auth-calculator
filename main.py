import requests
import base64

def new_auth(SSO):
    url = 'https://oauth.battle.net/oauth/sso'
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    data = {
        'client_id': 'baedda12fe054e4abdfc3ad7bdea970a',
        'grant_type': 'client_sso',
        'scope': 'auth.authenticator',
        'token': SSO
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    jsondata = response.json()
    beartoken = jsondata["access_token"]
    print(beartoken)
    url = 'https://authenticator-rest-api.bnet-identity.blizzard.net/v1/authenticator'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + beartoken
    }

    response = requests.post(url, headers=headers)
    print(response.json())

def get_device_secret(SSO):
    url = 'https://oauth.battle.net/oauth/sso'
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    data = {
        'client_id': 'baedda12fe054e4abdfc3ad7bdea970a',
        'grant_type': 'client_sso',
        'scope': 'auth.authenticator',
        'token': SSO
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    jsondata = response.json()
    beartoken = jsondata["access_token"]
    print(beartoken)
    url = 'https://authenticator-rest-api.bnet-identity.blizzard.net/v1/authenticator'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer '+beartoken
    }

    response = requests.get(url, headers=headers)
    jsondata = response.json()
    print(jsondata)
    Rcode = jsondata["restoreCode"]
    Scode = jsondata["serial"]

    url = 'https://authenticator-rest-api.bnet-identity.blizzard.net/v1/authenticator/device'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ beartoken
    }
    data = {
        "restoreCode": Rcode,
        "serial": Scode
    }
    response = requests.post(url, headers=headers, json=data)
    jsondata = response.json()
    Dsecret = jsondata["deviceSecret"]
    print(f'Your Device Secret:{Dsecret}')
    original_bytes = bytes.fromhex(Dsecret)
    # 使用 base32 进行编码
    encoded_bytes = base64.b32encode(original_bytes)
    encoded_string = encoded_bytes.decode('utf-8')
    print("After Base32:", encoded_string)
    print("Use totp with following URL:\notpauth://totp/Battle.net?secret=deviceSecret&digits=8")

if  __name__ == "__main__":
    print("Goto this website and login to get SSO\nhttps://account.battle.net/login/en/?ref=localhost\n\n")
    SSO = input("Input SSO:\n")
    mode = input("Mode,1 for new ,2 for device secret:\n")
    if mode == '2' :
        get_device_secret(SSO)
    else:
        new_auth(SSO)
