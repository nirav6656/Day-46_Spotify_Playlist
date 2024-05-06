import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
BILLBOARD_LINK = "https://www.billboard.com/charts/hot-100/"
USER_DATE = input("Enter the date in the format of YYY-MM-DD : ")
link_with_date = f"{BILLBOARD_LINK}{USER_DATE}/"
response = requests.get(url=link_with_date)
print(response)
song_name_list = []
soup = BeautifulSoup(response.content,"html.parser")
song_names = soup.find_all("h3",class_="a-truncate-ellipsis")
for song in song_names:
    song_text = song.getText()
    song_name_list.append(song_text.strip())
print(song_name_list)

image_b64 = "IMG_0581.JPG"
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scope=scope,redirect_uri="https://chatgpt.com/"))

current_user = sp.current_user()
current_user_id = current_user["id"]
print(current_user_id)
year = USER_DATE.split("-")[0]
song_uris = []
for song in song_name_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

my_playlist = sp.user_playlist_create(user=current_user_id,name=f"{USER_DATE} Billboard 100",public=False)
playlist_id = my_playlist["id"]
sp.playlist_add_items(playlist_id, song_uris, position=None)
