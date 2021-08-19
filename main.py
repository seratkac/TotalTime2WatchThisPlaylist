import ytside
import GoogleSheetRW
import os

from datetime import timedelta


class SMT:
    obj = None


def main(playlist_id, spreadsheet_id):
    try:
        playlist_id = playlist_id.split("list=")[-1] or None
    except Exception as e:
        raise e

    try:
        spreadsheet_id = spreadsheet_id.split("/d/")[1].split("/e")[0]
    except:
        spreadsheet_id = ""

    with open("yttoken.txt", "r") as f:
        yttoken = f.read()

    yts = ytside.Main(yttoken, playlist_id)

    yts.main_flow()

    max_duration = max(yts.durations)
    min_duration = min(yts.durations)

    total_d = timedelta(seconds=0)
    for i in yts.durations:
        total_d += i
    yts.total_d = total_d
    SMT.obj = yts

    def tvi(d):
        return yts.titles[
                   yts.durations.index(d)
               ], vid_id2lnk(yts.videos_id, playlist_id)[
                   yts.durations.index(d)
               ]

    # print(
    #     " Total video duration: ",
    #     total_d,
    #     "\n",
    #     "Minimum video duration: ",
    #     min_duration,
    #     tvi(min_duration),
    #     "\n",
    #     "Maximum video duration: ",
    #     max_duration,
    #     tvi(max_duration)
    # )
    if spreadsheet_id != "":
        GS = GoogleSheetRW.RW(playlist_id, spreadsheet_id)
        GS.write(column_a=yts.videos_id, column_b=yts.durations, column_c=yts.titles)

    SMT.max_duration, SMT.min_duration, SMT.total_d = (max_duration, min_duration, total_d)
    return SMT


def vid_id2lnk(vidid, playlist_id):
    vid_lnk = []
    for el in vidid:
        vid_lnk.append("https://www.youtube.com/watch?v={0}&list={1}".format(el, playlist_id))
    return vid_lnk


if __name__ == "__main__":
    from app import server
    server.run()
