class FireKeys:
    keys = {
        "HOME":3,
        "RETURN":4,
        "BACK":4,
        "VOL+":"",
        "VOL-":"",
        "OK":23,
        "DPAD-CENTER":23,
        "DPAD-UP":19,
        "DPAD-DOWN":20,
        "DPAD-LEFT":21,
        "DPAD-RIGHT":22,
        "MEDIA-STOP":86,
        "MEDIA-PLAY-PAUSE":127,
        "MEDIA-CLOSE":128,
        "SEARCH":84,
        "SETTINGS":176,
        "SLEEP":223,
        "REFRESH":285,
        "MUSIC":209
    }
    
    def key(self,key):
        try:
            keycode = self.keys[key]
        except KeyError:
            keycode = "",
        return keycode