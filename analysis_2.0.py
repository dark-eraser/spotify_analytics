# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3.8.8 ('base')
#     language: python
#     name: python3
# ---

# %%
import spotipy
import pandas as pd
import time
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials
import json

# %%
data= json.load(open('metadata/ids.json'))
username = data["username"]
client_id = data["client-id"]
client_secret = data["client-secret"]
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-top-read'

# %%
# client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
token = spotipy.util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
# print(token)
sp= spotipy.Spotify(auth=token)


# %%
def get_track_id(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

# ids = get_track_id('allen1249', '37i9dQZEVXcNMEcpECCTVh')



# %%
top_tracks={}
track_ids=[]

offset=0
from requests import HTTPError
# while top_tracks_tmp == {}:
# for i in range(100):
    # try:
top_tracks= sp.current_user_top_tracks(limit=50, time_range='short_term', offset=0)

# except Exception as e:
    # print(e)
    # break
for track in top_tracks['items']:
    track_ids.append(track['id'])
    
# # * print top tracks and artists


# %%
# top_tracks = [item for sublist in top_tracks for item in sublist]
# print(top_tracks)
track_ids=[]
for track in top_tracks['items']:
    track_ids.append(track['id'])


# %%

def get_track_info(ids):
    meta = [sp.track(x) for x in ids]
    features = sp.audio_features(ids)
    # track name
    name = meta[0]['name']
    # artist name
    artist = meta[0]['artists'][0]['name']
    # album name
    album = meta[0]['album']['name']
    # release date
    release_date = meta[0]['album']['release_date']
    # duration
    duration = meta[0]['duration_ms']
    # popularity
    popularity = meta[0]['popularity']
    # Explicit
    explicit = meta[0]['explicit']

    # Song features
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    key = features[0]['key']
    loudness = features[0]['loudness']
    mode = features[0]['mode']
    speechiness = features[0]['speechiness']
    acousticness = features[0]['acousticness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, artist, album, release_date, duration, popularity, explicit,
            danceability, energy, key, loudness, mode, speechiness, acousticness,
            valence, temp, time_signature]
    return track
tracks = []

general = [sp.track(x) for x in track_ids]
features = sp.audio_features(track_ids)

for i in range(len(track_ids)-1):
    # track name
    name = general[i]['name']
    # artist name
    artist = general[i]['artists'][0]['name']
    # album name
    album = general[i]['album']['name']
    # release date
    release_date = general[0]['album']['release_date']
    # duration
    duration = general[i]['duration_ms']
    # popularity
    popularity = general[i]['popularity']
    # Explicit
    explicit = general[i]['explicit']

    # Song features
    danceability = features[i]['danceability']
    energy = features[i]['energy']
    instrumentalness = features[i]['instrumentalness']
    loudness = features[i]['loudness']
    speechiness = features[i]['speechiness']
    acousticness = features[i]['acousticness']
    liveness = features[i]['liveness']
    valence = features[i]['valence']
    tempo = features[i]['tempo']
    key = features[i]['key']
    mode = features[i]['mode']
    time_signature = features[i]['time_signature']

    track = [name, artist, album, release_date, duration, popularity, explicit,
            danceability, energy, instrumentalness, speechiness, acousticness,
            liveness, valence, tempo, loudness, key, mode, time_signature]
    tracks.append(track)

# %%
tracks = pd.DataFrame(tracks)
tracks.columns = ['name', 'artist', 'album', 'release_date', 'duration', 'popularity', 'explicit', 'danceability', 'energy', 'instrumentalness', 'speechiness', 'acousticness', 'liveness', 'valence', 'tempo', 'loudness','key', 'mode', 'time_signature']



# %%
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dance = tracks.sort_values('danceability', ascending = True)
energy = tracks.sort_values('energy', ascending = True)
loudness = tracks.sort_values('loudness', ascending = True)
speechiness = tracks.sort_values('speechiness', ascending = True)
acousticness = tracks.sort_values('acousticness', ascending = True)
liveness = tracks.sort_values('liveness', ascending = True)
valence = tracks.sort_values('valence', ascending = True)
tempo = tracks.sort_values('tempo', ascending = True)

# %%
fig = make_subplots(rows=2, cols=4, start_cell="top-left", subplot_titles=("Danceability", "Energy", "Loudness", "Speechiness", "Acousticness", "Livenss", "Valence", "Tempo"))
fig.add_trace(go.Bar(y = dance['danceability'], name = 'danceability'),
              row=1, col=1)
fig.add_trace(go.Bar(y = energy['energy'], name = 'energy'),
              row=1, col=2)
fig.add_trace(go.Bar(y = loudness['loudness'], name = 'loudness'),
              row=1, col=3)
fig.add_trace(go.Bar(y = speechiness['speechiness'], name = 'speechiness'),
              row=1, col=4)
fig.add_trace(go.Bar(y = acousticness['acousticness'], name = 'acousticness'),
              row=2, col=1)
fig.add_trace(go.Bar(y = liveness['liveness'], name = 'liveness'),
              row=2, col=2)
fig.add_trace(go.Bar(y = valence['valence'], name = 'valence'),
              row=2, col=3)
fig.add_trace(go.Bar(y = tempo['tempo'], name = 'tempo'),
              row=2, col=4)

fig.show()

# %%
import seaborn as sns
f, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(tracks['danceability'], ax = axes[0], color = 'g', bins = 6)
sns.histplot(tracks['energy'], ax = axes[1], color = 'g', bins = 6)
sns.histplot(tracks['instrumentalness'], ax = axes[2], color = 'g', bins = 6)



f, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(tracks['loudness'], ax = axes[0], color = 'g', bins = 6)
sns.histplot(tracks['speechiness'], ax = axes[1], color = 'g', bins = 6)
sns.histplot(tracks['acousticness'], ax = axes[2], color = 'g', bins = 6)

f, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(tracks['liveness'], ax = axes[0], color = 'g', bins = 6)
sns.histplot(tracks['valence'], ax = axes[1], color = 'g', bins = 6)
sns.histplot(tracks['tempo'], ax = axes[2], color = 'g', bins = 6)

plt.show()

# %%
import plotly.express as px
features = list(tracks.columns[7:14])
values = list(tracks[tracks.columns[7:14]].mean())
df = pd.DataFrame(dict(
    r=values,
    theta=features))
fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r = [0,1])
fig.show()

# %%
