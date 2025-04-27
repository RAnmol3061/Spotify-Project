import mysql.connector as c
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import time

client_id = "34d66b37608a4552b92856fc9ed0a9c9"
client_secret = "eef96295684f400cab722e26f7f06d75"

sp = spotipy.Spotify(auth_manager = SpotifyOAuth ( client_id = client_id,
                                                   client_secret = client_secret,
                                                   redirect_uri="http://127.0.0.1:5000/callback",
                                                   scope= "user-library-read"))

con = c.connect(host = 'localhost',
                user = 'root',
                password = 'hello@123helloA',
                database = 'Spotify_Project_27042025')
cursor = con.cursor()



def all_tracks():
    track_all = []
    offset = 0
    limit = 50

    while True:

        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        track_all.extend(results['items'])

        if len(results['items']) < limit:
            break

        offset += limit

        time.sleep(2)
    return track_all


for idx, item in enumerate(all_tracks()):
    track = item['track']

    track_name = track['name']
    artist_name = track['artists'][0]['name']
    album_name = track['album']['name']
    track_uri = track['uri']
    
    print(type(track_name))
    #cursor.execute("INSERT INTO Details VALUES (%s, %s, %s, %s)", (track_name, artist_name, album_name, track_uri))

con.commit()
con.close()


