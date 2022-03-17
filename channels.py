import json
f = open('assets/channels.json','r')
channelList = {}

data = json.load(f)

langs = {
    1:"Hindi",
    6:"English",
    7:"Malayalam",
    8:"Tamil"
}

channel_list = {
    "English":[],
    "Malayalam":[],
    "Hindi":[],
    "Tamil":[],
}

for channel in data:
    # print(channel)
    if(data[channel]["lang_id"] in langs):
        data[channel]["lang_id"] = langs[data[channel]["lang_id"]]
        if(data[channel]["lang_id"] in channel_list):
            channel_list[data[channel]["lang_id"]].append(data[channel])
        else:
            channel_list[data[channel]["lang_id"]] = [data[channel]]
    
print(str(channel_list)[:30])
store = open('assets/channel-list.json','w')
json.dump(channel_list,store)