from flask import Flask,render_template,send_from_directory
from jiolib import JioTV
import json
import requests
from datetime import datetime
import time

app = Flask(__name__, static_folder='static')
jio = JioTV("+91********", "password")

retries = 0

@app.route("/")
def home():
    return render_template('index.html', channel="Animal_Planet_HD")

@app.route("/EPG/<int:channel_id>")
def getEPG(channel_id):
    epgData = requests.get("http://snoidcdnems04.cdnsrv.jio.com/jiotv.data.cdn.jio.com/apis/v1.3/getepg/get?offset=0&channel_id={}".format(str(channel_id)))
    return epgData.text

@app.route("/EPG/NOW/<string:channel_name>")
def getEPGNow(channel_name):
    f = open("assets/channels.json")
    channelList = json.load(f)
    channel_id = channelList[channel_name]["channel_id"]
    epgData = requests.get("http://snoidcdnems04.cdnsrv.jio.com/jiotv.data.cdn.jio.com/apis/v1.3/getepg/get?offset=0&channel_id={}".format(str(channel_id)))
    shows =  json.loads(epgData.text)
    shows =  shows["epg"]
    nowTime = datetime.now()
    for show in shows:
        endTime = datetime.strptime(nowTime.strftime("%d-%m-%y ")+show["endtime"],"%d-%m-%y %H:%M:%S")
        startTime = datetime.strptime(nowTime.strftime("%d-%m-%y ")+show["showtime"],"%d-%m-%y %H:%M:%S")
        if(startTime<nowTime and endTime>nowTime):
            return json.dumps(show)
    return "IDK"

@app.route('/channelList')
def channelList():
    f = open("assets/channel-list.json")
    channels = json.load(f)
    return render_template('channelList.html',channels=channels)

@app.route("/<path:path>")
def common_page(path):
    if(path[-3:]=="key"):
        return jio.client(path)
    elif(path[-4:]=="m3u8"):
        data = jio.getChannelPlaylist(path[:-5])
        return data if "406 Not Acceptable" not in data else ""
    elif(path[-2:]=="ts"): 
        return jio.client(path)
    else:
        print(path)
        return render_template('index.html', channel= path)

@app.route("/login")
def login():
    return "<p>Hello, Loginer! This page is not ready :(</p>"

@app.route("/all_channels.m3u8")
def allChannels():
    return send_from_directory('assets','channels.m3u8', as_attachment=False)

@app.route("/nostreamavailable.mp4")
def nostream():
    return send_from_directory('assets','NoStreamVideo.mp4', as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=80)


