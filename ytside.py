import requests

from datetime import timedelta


class Main:
    """Youtube side"""

    def __init__(self, key, playlist_id):
        self.key = key

        self.pageToken = ""

        self.playlist_id = playlist_id

        self.videos_id = []
        self.titles = []
        self.durations = []

        self.videosData = tuple()

    def get_playlist_items(self):
        videos_id = []
        r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", {
            "part": "contentDetails",
            "maxResults": "50",
            "pageToken": self.pageToken,
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

        self.get_videos_data(videos_id)
        self.get_title_duration()

    def get_videos_data(self, videos_id):
        r = requests.get("https://www.googleapis.com/youtube/v3/videos", {
            "part": "snippet,contentDetails",
            "maxResults": "50",
            "id": videos_id,
            "key": self.key
        })
        if r.status_code != 200:
            return

        self.videosData = tuple(r.json()["items"])

    def get_title_duration(self):
        for el in self.videosData:
            self.titles.append(el["snippet"]["title"])
            self.durations.append(el["contentDetails"]["duration"])

    def time_fmt(self):
        durations = []
        for el in self.durations:
            a = "0"
            b = el[2:-1].split("H")[-1].split("M")[0]
            c = el[2:-1].split("M")[1].split("S")[0]
            a, b, c = map(int, (a, b, c))
            durations.append(timedelta(seconds=c, minutes=b, hours=a))

        self.durations = durations

    def main_flow(self):
        self.get_playlist_items()
        while self.pageToken != "":
            self.get_playlist_items()
        self.time_fmt()
