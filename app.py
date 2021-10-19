from logging import DEBUG
from flask import Flask,render_template,stream_with_context
import requests
from jiolib import JioTV
from firetv import FireTV
from urllib.parse import unquote

app = Flask(__name__)
jio = JioTV("+918921433239", "treegrp123")
# firetv = FireTV()

@app.route("/")
def home():
    return render_template('player.html', pathToSource="Animal_Planet_HD.m3u8")
    
@app.route("/remote")
def remote():
    return render_template('remote.html')

@app.route("/remote/key/<path>")
def remoteKey(path):
    result = firetv.keyPress(path.upper())
    if(result!=""):
        return str(path)
    return path + "<Failed>"
    
@app.route("/remote/tv/<path>")
def remoteTV(path):
    return "tvmode"

@app.route("/video-stream/<path:path>")
def remoteVideoStream(path):
    result = firetv.playStream(unquote(path))
    if(result):
        return path
    else:
        return "<Failed>"


@app.route("/url-site/<path:path>")
def remoteURL(path): 
    result = firetv.openURI(unquote(path))
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




