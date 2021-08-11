import ytside
import GoogleSheetRW

from datetime import timedelta


def main():
    with open("yttoken.txt", "r") as f:
        yttoken = f.read()

    playlist_id = input("->Open playlist id or link<-\n->").split("list=")[-1]
    try:
        spreadsheet_id = \
            input("->Spreadsheet id or link or or nothing to print result to console<-\n->").split("/d/")[1].split(
                "/e")[0]
    except:
        spreadsheet_id = ""

    yts = ytside.Main(yttoken, playlist_id)

    yts.main_flow()

    max_duration = max(yts.durations)
    min_duration = min(yts.durations)

    total_d = timedelta(seconds=0)
    for i in yts.durations:
        total_d += i

    def tvi(d):
        return yts.titles[
                   yts.durations.index(d)
               ], vid_id2lnk(yts.videos_id, playlist_id)[
                   yts.durations.index(d)
               ]

    print(
        " Total video duration: ",
        total_d,
        "\n",
        "Minimum video duration: ",
        min_duration,
        tvi(min_duration),
        "\n",
        "Maximum video duration: ",
        max_duration,
        tvi(max_duration)
    )

    if spreadsheet_id != "":
        GS = GoogleSheetRW.RW(playlist_id, spreadsheet_id)
        GS.write(column_a=yts.videos_id, column_b=yts.durations, column_c=yts.titles)


def vid_id2lnk(vidid, playlist_id):
    vid_lnk = []
    for el in vidid:
        vid_lnk.append("https://www.youtube.com/watch?v={0}&list={1}".format(el, playlist_id))
    return vid_lnk


if __name__ == "__main__":
    main()
