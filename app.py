from logging import DEBUG
from flask import Flask,render_template,stream_with_context
import requests
from jiolib import JioTV
from urllib.parse import unquote

app = Flask(__name__)
jio = JioTV("+918921433239", "password")


@app.route("/")
def home():
    return render_template('player.html', pathToSource="Animal_Planet_HD.m3u8")


@app.route("/video-stream/<path:path>")
def remoteVideoStream(path):
    result = firetv.playStream(unquote(path))
    if(result):
        return path
    else:
        return "<Failed>"


@app.route("/<path:path>")
def common_page(path):
    if(path[-3:]=="key"):
        return jio.client(path)
    elif(path[-4:]=="m3u8"):
        return jio.getChannelPlaylist(path[:-5])
    elif(path[-2:]=="ts"):
        return jio.client(path)
    else:
        return render_template('player.html', pathToSource= path+".m3u8")

@app.route("/login")
def login():
    return "<p>Hello, Loginer!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)




