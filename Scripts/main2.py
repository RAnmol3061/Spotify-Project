import mysql.connector as c
import spotipy, time, sys, os, itertools, traceback
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd
#------------------------------------------#
load_dotenv()

try:
    #Connecting to Spotify
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth ( client_id = os.getenv("CLIENT_ID"),
                                                   client_secret = os.getenv("CLIENT_SECRET"),
                                                   redirect_uri="http://127.0.0.1:5000/callback",
                                                   scope= "user-library-read"))
except Exception as e:
    print(e, end="\n")
    traceback.print_exc()
    sys.exit()

def getting_all_tracks():
    #Getting all tracks in Liked Playlist
    track_all = []
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        track_all.extend(results['items'])

        if len(results['items']) < limit:
            break

        offset += limit

        #Given to aviod rate limit in Spotify
        time.sleep(1)
    return track_all


def mysql():

    try:
        #Connecting with mysql
        with c.connect(host='localhost', user='root', password= os.getenv("PASSWORD"), database= os.getenv("DATABASE")) as con:
            with con.cursor() as cursor:

                record = []

                #Extracting values from "track_all"
                for item in getting_all_tracks():
                    track = item['track']

                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    album_name = track['album']['name']
                    track_id = track['id']
                
                    record.append((track_name, artist_name, album_name, track_id))
                
                query = """ INSERT INTO Details (track_name, artist_name, album_name, track_id) VALUES (%s, %s, %s, %s) """
                query2 = """Select * from details"""
                
                try:
                    def sorting():
                        
                        #Putting Values of Spotify and Mysql in Pandas DataFrame
                        df = pd.DataFrame(record, columns=['track_name', 'artist_name', 'album_name', 'track_id']) # Spotify Liked List
                        df2 = pd.read_sql(query2, con) # Mysql Database
                                            
                        unique_id = list(set(df['track_id']) ^ set(df2['track_id']))

                        a = df[df['track_id'].isin(unique_id)]
                        b = df2[df2['track_id'].isin(unique_id)]

                        return a
                    
                except Exception as e:
                    print(e, end="\n")
                    traceback.print_exc()
                    sys.exit()
                    
                record_apply = sorting().values.tolist()
                
                cursor.executemany(query,record_apply)
                con.commit()

    except Exception as e:
        print(e, end="\n")
        traceback.print_exc()
        sys.exit()

mysql()