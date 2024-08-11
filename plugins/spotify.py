from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import aiohttp
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CLIENT_ID = "adb3797e3a6a431f9544c6c51f088d9e"
CLIENT_SECRET = "fdfad8cce09c472f97bde3e2ca7e23bd"

# print("Welcome to the musical time machine playlister")


# date = input("Which date do you prefer? ")
# month = input("Enter yr favourite month? ")
# year = input("Enter your year of choice ... ")
# pl_name = input("Enter a playlist name ... ")

# full_date = f"{int(year)}-{int(month)}-{int(date)}"
# url = f"https://www.billboard.com/charts/hot-100/{full_date}/"
# url = "https://www.billboard.com/charts/hot-100/1979-08-12/"

# webb = requests.get(url)
# web = webb.text


@Client.on_message(filters.command(['top_100', 'tops', 'top']))
async def send_toptier(client, message):
    playlist_names = ['walter','yellow',                    
    "Happy Vibes Mix",
    "Chill Beats Collection",
    "Sunset Serenade",
    "Summer Breeze Jams",
    "Starry Night Melodies",
    "Weekend Chillout Mix",
    "Feel Good Anthems",
    "Smooth Sailing Sounds",
    "Cozy Fireplace Tunes",
    "Morning Dew Playlist"
]
    pl_name = random.choice(playlist_names)
    date_string = message.text.split(' ', 1)[1]
    day, month, year = date_string.split('/')
    full_date = f"{int(year)}-{int(month):02d}-{int(day):02d}"
    try:
        # Fetch the webpage content asynchronously
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.billboard.com/charts/hot-100/{full_date}/") as response:
                web_page = await response.text()

        soup = BeautifulSoup(web_page, "html.parser")
        song_names_spans = soup.select("li ul li h3")
        song_names = [song.getText().strip() for song in song_names_spans]
        print(song_names)
        tracks_to_add = []

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="https://example.com",
    scope="user-library-read playlist-modify-public",
    #cache_path=".spotify_cache"  # Cache the token for future runs
))

        pl1 = sp.user_playlist_create(user="31gwwiu2onm2fgqrju62vlsi4a5i", 
                                name=f"{pl_name} - {full_date}", 
                                public=True, 
                                collaborative=False, 
                                description='This is python-made ... #$%!')

        playlist_id = pl1['id']
        playlist_location = pl1['external_urls']['spotify']

        # Send an initial message
        progress_message = await client.send_message(
            chat_id=message.chat.id,
            text="Creating playlist... Please wait."
        )

        for idx, song_name in enumerate(song_names, start=1):
            results = sp.search(q=f"track:{song_name}", type='track', limit=1)
            try:
                song_id = results['tracks']['items'][0]['id']
                tracks_to_add.append(song_id)
                # Update the progress message with the current song
                await progress_message.edit_text(
                    f"Processing song {idx}/{len(song_names)}: {song_name} (ID: {song_id})"
                )
            except IndexError:
                await progress_message.edit_text(
                    f"Processing song {idx}/{len(song_names)}: {song_name} is not available on Spotify"
                )
        if tracks_to_add:        
            sp.user_playlist_add_tracks(user="31gwwiu2onm2fgqrju62vlsi4a5i",playlist_id=f"{playlist_id}",tracks=tracks_to_add)

        print(f"PLAYLIST - {pl_name} created successfully.\nYou can find it at URL : {playlist_location}")

        await client.send_message(
            chat_id=message.chat.id,
            text=f"PLAYLIST - {pl_name} created successfully.\nYou can find it at URL : {playlist_location}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='GO', url=playlist_location)],
                [InlineKeyboardButton(text='Back', url='https://mr-righteousdev.github.io')]
            ])
        )

    except Exception as e:
        print(e)



