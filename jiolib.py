import requests
import urlquick
from uuid import uuid4
import time
import base64
import hashlib
import re
import m3u8
from flask import Response


class JioTV:
    
    username=""
    password=""
    
    # Support Objects
    session= False
    HEADERS= False
    CREDS  = False
    token  = False
    
    def __init__(self,username,password):
        self.session = requests.Session()
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
            self.HEADERS = {
                "User-Agent": "JioTV",
                "os": "Kodi",
                "deviceId": str(uuid4()),
                "versionCode": "226",
                "devicetype": "Kodi",
                "srno": "200206173037",
                "appkey": "NzNiMDhlYzQyNjJm",
                "channelid": "100",
                "usergroup": "tvYR7NSNn7rymo3F",
                "lbcookie": "1"
            }
            print(" * Login Successful")
            self.HEADERS.update(self.CREDS)
            return "success"
        else:
            msg = response.get("message", "Error @ login()")
            print("Error @ Login")
            return msg
    
    
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
        url = "http://jiotv.live.cdn.jio.com/"+channel+"/"+channel+"_1200.m3u8"
        self.token = self.getToken()
        response = requests.get(url,params=self.token,headers=self.HEADERS)
        return self.proxify(response.text,channel)
    
    def proxify(self,content,channel):
        # return content
        content = re.sub("https://tv.media.jio.com/streams_live/","",content)
        def matches(match): return channel+"/"+match.group(0)       
        return re.sub("[-A-Za-z_0-9]*.ts",matches,content)
    
    def clientOld(self,url):
        #url= "Animal_Planet_HD_800-1620914368000.ts"
        url = "http://jiotv.live.cdn.jio.com/"
        channelName="DD_National"
        self.token = self.getToken()
        req = urlquick.get(url+"/"+channelName+"/"+channelName+"_1200.m3u8", headers=self.HEADERS, params=token)
        player = m3u8.loads(req.text)
        url = player.data["segments"][1]["key"]["uri"]
        response  = urlquick.get(url,headers=self.HEADERS,params=token)
        return response.content
    
    def client(self,url):
        #url= "Animal_Planet_HD_800-1620914368000.ts"
        # token = self.getToken()
        self.token = self.getToken()
        url = "https://tv.media.jio.com/streams_live/"+url
        print(url)
        response  = urlquick.get(url,headers=self.HEADERS,params=self.token)
        # return response.content
        return Response(response.iter_content(chunk_size=10*1024),
                    content_type=response.headers['Content-Type'])


# jio = JioTV("+918921433239", "treegrp123")
# print(jio.getChannelPlaylist("DD_National"))