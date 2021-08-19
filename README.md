# TotalTime2WatchThisPlaylist
This program should display the time it takes to view an open YouTube playlist.
____

### Why:
I sometimes calculate how much time it takes to watch all videos at playlist "watch later" and others. _Yeah, I have enough much free time to do this_

### How does it work:
Script runs flask server, displaying form with playlist id and id to google sheet.
User enters playlist id, then the programm gets the duration, title and link of all videos at the playlist and display total time of playlist,\
the biggest video and the smallest video via duration.

The field "spreadsheet id" is not required, but you need to fill it to save each videos data, like title, duration and one's link at your Google spreadsheet.
Unfortunately, I had not realized feature to show this data primary in the webpage.

### How to use:
#### If you are a developer.
1. Get this repo 
2. Put your YouTube data v3 key to _yttoken.txt_ \
 It looks like _abc123-456xyz_
If you want use google spreadsheet to extend info about video:
1. Put your service account data to _creds.json_ \
 You should have downloaded it, when created a service account. Just rename it to _creds.json_ and put near about _main.py_. 
2. Create a new spreadsheet and share it to email address from _creds.json_. 
3. Run main.py as you like to. 

#### If you want to try it:
1. https://ttw2tp.herokuapp.com/
