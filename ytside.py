import requests

class Main:
    """Youtube side"""

    def __init__(self, key, playlist_id):
        self.key = key
        self.pageToken = ""
        self.playlist_id = playlist_id
        self.videos_id = []
        self.titles = []
        self.durations = []

    def getPlaylistItems(self):
        # print("pgtkn =",self.pageToken)
        videos_id = []
        r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", {
            "part": "contentDetails",
            "maxResults":"50",
            "pageToken":self.pageToken,
            "playlistId": self.playlist_id,
            "key": self.key
        }).json()

        for el in r["items"]:
            videos_id.append(el["contentDetails"]["videoId"])
            self.videos_id.append(el["contentDetails"]["videoId"])

        try:
            self.pageToken = r["nextPageToken"]
        except:
            self.pageToken = ""

        self.getVideosData(videos_id)
        self.getTDI()


    def getVideosData(self,videos_id):
        # print(videos_id)
        r = requests.get("https://www.googleapis.com/youtube/v3/videos", {
            "part": "snippet,contentDetails",
            "maxResults":"50",
            "id": videos_id,
            "key": self.key
        })
        if r.status_code != 200:
            return

        self.videosData = r.json()["items"]


    def getTDI(self):
        for el in self.videosData:
            self.titles.append(el["snippet"]["title"])
            self.durations.append(el["contentDetails"]["duration"])

    def time_fmt(self):
        durations = []
        for el in self.durations:
            a = "0"
            b = el[2:-1].split("H")[-1].split("M")[0]
            c = el[2:-1].split("M")[1].split("S")[0]
            d = "{0}:{1}".format(b, c)
            if el.find("H") != -1:
                a = el[2:-1].split("H")[0]
            d = "{0}:{1}".format(a, d)
            durations.append(d)
        self.durations = durations

    def mainFlow(self):
        self.getPlaylistItems()
        while self.pageToken != "":
            self.getPlaylistItems()
        self.time_fmt()

