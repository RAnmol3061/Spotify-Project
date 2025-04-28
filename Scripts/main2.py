import mysql.connector as c
import spotipy, time, sys, os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
#------------------------------------------#






load_dotenv()

try:
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth ( client_id = os.getenv("client_id"),
                                                   client_secret = os.getenv("client_secret"),
                                                   redirect_uri="http://127.0.0.1:5000/callback",
                                                   scope= "user-library-read"))
except:
    print("Helo")
    sys.exit("Error")

def getting_all_tracks():
    track_all = []
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        track_all.extend(results['items'])

        if len(results['items']) < limit:
            break

        offset += limit

        #Given just incase 
        time.sleep(1)
    return track_all


def mysql():

    try:
        with c.connect(host='localhost', user='root', password= os.getenv("password"), database= os.getenv("database")) as con:
            with con.cursor() as cursor:

                record = []

                for item in getting_all_tracks():
                    track = item['track']

                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    album_name = track['album']['name']                
                
                    record.append((track_name, artist_name, album_name))
                
                querys = """ INSERT INTO Details (track_name, artist_name, album_name) VALUES (%s, %s, %s) """
                #cursor.executemany(querys,record)
                #con.commit()
    except:
        print("hello")
        sys.exit("Exiting due to some issue in Mysql stage")

mysql()
print("Program Completed")