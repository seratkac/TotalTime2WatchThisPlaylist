import sys

import ytside, GoogleSheetRW
def main():
    with open("yttoken.txt", "r") as f:
        yttoken = f.read()

    playlist_id = input("->Open playlist id or link<-\n->").split("list=")[-1]
    try:
        spreadsheet_id = input("->Spreadsheet id or link or or nothing to print result to console<-\n->").split("/d/")[1].split("/e")[0]
    except:
        spreadsheet_id = ""
    yts = ytside.Main(yttoken, playlist_id)

    yts.mainFlow()

    max_d = max(yts.durations)
    min_d = min(yts.durations)
    # total_d = sum(yts.durations)




    def tvi(d):
        return yts.titles[
            yts.durations.index(d)
        ], vidId2Lnk(yts.videos_id, playlist_id)[
            yts.durations.index(d)
        ]

    print(
        # "Total video duration: ",
        # total_d,
        # tvi(total_d),
        # "\n",
        "Minimum video duration: ",
        min_d,
        tvi(min_d),
        "\n",
        "Maximum video duration: ",
        max_d,
        tvi(max_d)
    )

    if spreadsheet_id != "":
        GS = GoogleSheetRW.RW(playlist_id,spreadsheet_id)
        GS.write(A = yts.videos_id, B = yts.durations, C = yts.titles)

def vidId2Lnk(vidId, playlist_id):
    vidLnk = []
    for el in vidId:
        vidLnk.append("https://www.youtube.com/watch?v={0}&list={1}".format(el, playlist_id))
    return vidLnk


if __name__ == "__main__":
    # main()
    print(sys.platform)