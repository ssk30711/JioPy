import requests
import urlquick
import time
import base64
import hashlib
import re
from flask import Response


class JioTV:
    
    retries = 0
    username=""
    password=""
    
    # Support Objects
    HEADERS= False
    CREDS  = False
    token  = False
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.login()

    def login(self):
        body = {
            "identifier": self.username,
            "password": self.password,
            "rememberUser": "T",
            "upgradeAuth": "Y",
            "returnSessionDetails": "T",
            "deviceInfo": {
                "consumptionDeviceName": "unknown sdk_google_atv_x86",
                "info": {
                    "type": "android",
                    "platform": {
                        "name": "generic_x86",
                        "version": "8.1.0"
                    },
                    "androidId": ""
                }
            }
        }
        headers = {"User-Agent": "JioTV Kodi", "x-api-key": "l7xx75e822925f184370b2e25170c5d5820a"}
        response = urlquick.post("https://api.jio.com/v3/dip/user/unpw/verify", json=body, headers=headers, max_age=-1, verify=False).json()
        if response.get("ssoToken", "") != "":
            self.CREDS = {
                "ssotoken": response.get("ssoToken"),
                "userId": response.get("sessionAttributes", {}).get("user", {}).get("uid"),
                "uniqueId": response.get("sessionAttributes", {}).get("user", {}).get("unique"),
                "crmid": response.get("sessionAttributes", {}).get("user", {}).get("subscriberId"),
            }
            # self.CREDS['ssotoken'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1bmlxdWUiOiI1YWNiYjk5Yi05ZjhiLTQ1ZTctYmVlYy02Zjg4MWE2NWI3YjQiLCJ1c2VyVHlwZSI6IlJJTHBlcnNvbiIsImF1dGhMZXZlbCI6IjIwIiwiZGV2aWNlSWQiOiJjNDMyMTNhOGMzYjljNTAxYzI4MDY1NjRiYzNkNjlhNDkwY2IwZDdiOTM0MzI4MDQ5Mzk1MTU0Mzk3NmViOTM2ZDcxNmZmZTMwYmNjM2UxOWU1MTMzZjNiNTg1MjNiNGY3OGU0YWMxYjFhYzc4MTVjNTNjMTE5MDBkYTM0ZTEwZCIsImp0aSI6ImE5NDY1ZmZhLTk5NzMtNDRhMi05Zjk1LTI2ZTFiZjI5ZDNiOCIsImlhdCI6MTY0NzMyMTA5NH0.B3GYQpugRqj2_AGgMbUzBOk-qzZj5-v3g0vxBazT79c"
            self.HEADERS = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                "os": "Android",
                "deviceId": "6e1a0e1c-5935-48e5-a8d7-c86534afa4d8",
                "versionCode": "226",
                "devicetype": "Android",
                "srno": "200206173037",
                "appkey": "NzNiMDhlYzQyNjJm",
                "channelid": "100",
                "usergroup": "tvYR7NSNn7rymo3F",
            }
            #str(uuid4()) for device ID
            print(" * Login Successful")
            self.HEADERS.update(self.CREDS)
            return "success"
        else:
            msg = response.get("message", "Error @ login()")
            print("Error @ Login",msg)
            return msg

    def reLogin(self):
        print("Attempting Relogin...")
        if(self.retries<=3):
            self.login()
            self.retries+=1
    
    def getToken(self):
        def magic(x): return base64.b64encode(hashlib.md5(x.encode()).digest()).decode().replace(
            '=', '').replace('+', '-').replace('/', '_').replace('\r', '').replace('\n', '')
        t= time.time()
        pxe = str(int(t+(3600*9.2)))
        jct = magic("cutibeau2ic9p-O_v1qIyd6E-rf8_gEOQ"+pxe)
        return {"jct": jct, "pxe": pxe, "st": "9p-O_v1qIyd6E-rf8_gEOQ"}

    
    def getChannelStreams(self,channel_id):
        GET_CHANNEL_URL = "https://tv.media.jio.com/apis/v1.4/getchannelurl/getchannelurl?langId=6&userLanguages=All"
        body = {"channel_id": int(channel_id),"stream_type": "Seek"}
        response = requests.post(GET_CHANNEL_URL, json=body).json()
        return response["result"]
    
    def getChannelPlaylist(self,channel):
        #url = "http://mumsite.cdnsrv.jio.com/jiotv.live.cdn.jio.com/"+channel+"/"+channel+"_1200.m3u8"
        url = "http://jiotv.live.cdn.jio.com/"+channel+"/"+channel+"_1200.m3u8"
        self.token = self.getToken()
        response = requests.get(url,params=self.token,headers=self.HEADERS)
        if("406 Not Acceptable" in response.text):
            self.reLogin()
        if("404 Not Found" in response.text):
            print("Channel not Found")
            return ""
        return self.proxify(response.text,channel)
    
    def proxify(self,content,channel):
        content = re.sub("https://tv.media.jio.com/streams_live/","",content)
        def matches(match): return channel+"/"+match.group(0)       
        return re.sub("[-A-Za-z_0-9]*.ts",matches,content)
    
    def client(self,url):
        self.token = self.getToken()
        url = "https://tv.media.jio.com/streams_live/"+url
        # url = "http://mumsite.cdnsrv.jio.com/jiotv.live.cdn.jio.com/"+url
        print(url)
        #response  = urlquick.get(url,headers=self.HEADERS,params=self.token)
        response = requests.get(url,params=self.token,headers=self.HEADERS,verify=False,stream=True)
        if("406 Not Acceptable" in response.text):
            self.reLogin()
        else:
            self.retries=0
        try:
            # return Response(response.iter_content(chunk_size=10*1024),
            # content_type=response.headers['Content-Type'])
            return response.content
        except:
            return Response(response.iter_content(chunk_size=10*1024))
