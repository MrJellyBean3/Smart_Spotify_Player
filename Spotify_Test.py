
import os
os.sys.path.append(r"C:\VS_Projects\Spotify_Test\env\Lib\site-packages")
import json 
import time
import spotipy
import spotipy.util as util
import random
import pickle
import datetime as dt
import keyboard
day_float=((365*(dt.datetime.now().year-2022))+dt.datetime.now().timetuple().tm_yday)




client_info_file=open("client_secrets.txt","r")#parameters for authentication
SPOTIPY_CLIENT_ID=client_info_file.readline().split("\n")[0]
SPOTIPY_CLIENT_SECRET=client_info_file.readline().split("\n")[0]


SPOTIPY_REDIRECT_URI="http://google.com"
scope=["streaming","user-read-recently-played","playlist-read-private","user-read-currently-playing"]#access codes

oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,#authentication
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                    scope=scope)
token_dict=oauth_object.get_access_token()
token=(token_dict['access_token'])
spotify_object=spotipy.Spotify(auth=token)#spotify object



currently_playing=spotify_object.currently_playing#song playing
print(currently_playing)





playlists=spotify_object.user_playlists("ehlowe31")#gets my playlists
NAME_SELECT="Forbidden"
playlist_id=""
while playlists:
    for i, playlist in enumerate(playlists["items"]):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlist['name']==NAME_SELECT:
            playlist_id=playlist['uri']
    if playlists['next']:
        playlists = spotify_object.next(playlists)
    else:
        playlists = None



history_range=50
song_history=spotify_object.current_user_recently_played(limit=history_range)#song history stuff
song_list=[]
i=0
for i in range(0,history_range):
    song_list.append(song_history["items"][i]["track"]["name"])
#print(song_list)




if os.path.exists("ForbiddenPickel.wb"):#opens up pickle file
    infile = open("ForbiddenPickel.wb",'rb')
    song_dict = pickle.load(infile)
    infile.close()
else:
    song_dict={}




manual_dating=True#manual data entry
if manual_dating:
    day_temp=0
    for item in song_dict:
        if song_dict[item]["data"]==["n"]:#get rid of accidental n
                song_dict[item]["data"]=[]
        for ind in range(len(song_dict[item]["data"])):#convert all to int
            song_dict[item]["data"][ind]=int(song_dict[item]["data"][ind])  
            

        if not (day_temp=="n" or day_temp=="N"):#ask input until n
            if song_dict[item]["data"]==[]:
                print(day_float)
                day_temp=int(input(str("day for song name "+str(item)+" ")))
                if not (day_temp=="n" or day_temp=="N"):
                    song_dict[item]["data"].append(day_temp)
                print(song_dict[item]["data"])
            else:
                print(item," ", song_dict[item]["data"])



        if (day_temp=="n" or day_temp=="N"):#prints the info for songs not mentioned
            print(item," ",song_dict[item]["data"])
    outfile=open("ForbiddenPickel.wb",'wb')#save the pickel
    pickle.dump(song_dict, outfile)
    outfile.close()











#R=random.randrange(0, songs_in_playlist-1,1)
#uri_ex=[(spotify_object.playlist_tracks(playlist_id)["items"][int(R)]["track"]['uri'])]#picks out random song
#spotify_object.start_playback(uris=uri_ex)
#current_song=spotify_object.currently_playing()['item']['name']
#song_dict[str(current_song)]["data"].append(day_float)
#print(song_dict[str(current_song)])
#time.sleep(3)
#spotify_object.pause_playback()



song_dates=[]#playlist history
for song in song_dict:
    if song_dict[song]["data"]!=[]:
        song_dates.append([day_float-song_dict[song]["data"][-1], song, song_dict[song]["uri"]])
song_dates.sort(reverse=True)
#print(song_dates)


play_song=True#song selector
if play_song:
    song_uri=song_dates[0][2]
    song_name=song_dates[0][1]
    print(song_name, song_dates[0][0])
    txt=input("would you like to play " +str(song_name)+ ", "+str(song_dates[0][0])+" days ")
    if txt=="y":
        print("playing: ",song_name)
        spotify_object.start_playback(uris=[song_uri])
        song_start_time=time.time()
        song_dict[str(song_name)]["data"].append(day_float)
        time.sleep(1)
        cp=spotify_object.currently_playing()
        song_duration=cp["item"]["duration_ms"]/1000
        
        #spotify_object.pause_playback()
        #spotify_object.devices()
        index_prev=-1
        index=0
        while not(keyboard.is_pressed("Esc")):
            if index_prev!=index:
                outfile=open("ForbiddenPickel.wb",'wb')#save the pickel
                pickle.dump(song_dict, outfile)
                outfile.close()
                index_prev=index
                print("playing next: ", song_dates[index+1][1], ", ",song_dates[index+1][0]," days")
            if((time.time()-song_start_time)>song_duration-1):
                index+=1
                song_uri=song_dates[index][2]
                song_name=song_dates[index][1]
                print("playing:", song_name, ", ",song_dates[0][0]," days")
                spotify_object.start_playback(uris=[song_uri])
                song_start_time=time.time()
                song_dict[str(song_name)]["data"].append(day_float)
                time.sleep(1)
                cp=spotify_object.currently_playing()
                song_duration=cp["item"]["duration_ms"]/1000
            else:
                time.sleep(0.1)
print("updating playlist songs")





playlist_song_names=[]
playlist_song_uris=[]
songs_in_playlist=(len(spotify_object.playlist_tracks(playlist_id)["items"]))#gets songs from playlist
for index in range(songs_in_playlist):
    temp_dict=(spotify_object.playlist_tracks(playlist_id)["items"][index]["track"])
    playlist_song_names.append(temp_dict["name"])
    playlist_song_uris.append(temp_dict['uri'])
print(playlist_song_names)



for name_index in range(len(playlist_song_names)):#add new songs
    if (str(playlist_song_names[name_index]) not in song_dict.keys()):
        song_dict[str(playlist_song_names[name_index])]={"uri":str(playlist_song_uris[name_index]),"data":[]}




outfile=open("ForbiddenPickel.wb",'wb')#save the pickel
pickle.dump(song_dict, outfile)
outfile.close()

#artist=current_dict['item']['album']['artists'][0]['name']
#song=current_dict['item']['name']

#print(artist,song)