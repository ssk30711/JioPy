from firekeys import FireKeys
import subprocess

class FireTV:
    ip=""
    adb_connected=False
    keys = FireKeys()
    
    def osCommand(self,command):
        output=""
        try:
            output = subprocess.check_output(command, shell=True)
        except:
            return "Error in ADB"
        return output
    
    def __init__(self,ip="192.168.0.10"):
        op = self.osCommand("adb connect "+ip)
    
    def openURI(self,uri):
        result = self.osCommand("adb shell am start -a android.intent.action.VIEW -d "+uri)
        return result
    
    def playStream(self,pathToVideo):
        result = self.osCommand("adb shell am start -n org.videolan.vlc/org.videolan.vlc.gui.video.VideoPlayerActivity -a android.intent.action.VIEW -d "+pathToVideo)
        return result
    
    def powerState(self,state):
        pass
    
    def keyCodePress(self,key):
        self.osCommand("adb shell input keyevent "+str(key))

    
    def keyPress(self,keyName):
        keyCode = self.keys.key(keyName)
        self.osCommand("adb shell input keyevent "+str(keyCode))



# fire_tv = firetv()
# #fire_tv.openURI("https://www.youtube.com/watch?v=3OakodfKjrU")
# fire_tv.keyCodePress(84) 