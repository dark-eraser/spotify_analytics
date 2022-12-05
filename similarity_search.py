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
import time
import requests
import json 
import matplotlib.pyplot as plt

# %%
data= json.load(open('metadata/ids.json'))
username = data["username"]
client_id = data["client-id"]
client_secret = data["client-secret"]
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played'

# %%
token = spotipy.util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
# print(token)
sp_user= spotipy.Spotify(auth=token)


# %%
# scope = 'user-follow-read'
# token = spotipy.util.prompt_for_user_token(username=username,
#                                    scope=scope,
#                                    client_id=client_id,
#                                    client_secret=client_secret,
#                                    redirect_uri=redirect_uri)
# # print(token)
# sp_= spotipy.Spotify(auth=token)

# %%
# * tracks in discovery weekly playlist

# disc_weekly=sp_.search(q='Discovery Weekly', type='playlist', limit=1)
# # print(disc_weekly['playlists']['items'][0]['id'])
# disc_weekly_tracks=sp_.playlist_tracks(disc_weekly['playlists']['items'][0]['id'])
# disc_weekly_tracks_ids=[]
# for track in disc_weekly_tracks['items']:
#     disc_weekly_tracks_ids.append(track['track']['id'])
# with open('metadata/disc_weekly_tracks.json', 'w') as f:
#     json.dump(disc_weekly_tracks_ids, f)

# %%
def get_ids():
    recently_played = sp_.current_user_recently_played(limit=50)
    with open('metadata/recently_played.json', 'w') as outfile:
        json.dump(recently_played, outfile)

    before_dates=[]
    return ret_ids(recently_played)

def ret_ids(recently_played):
    track_ids=[]
    for track in recently_played['items']:
        # print(track["track"]["id"])
        track_ids.append(track["track"]["id"])
        # before_dates.append(track["track"]["cursors"]["before"])
    return track_ids


# %%
# * related artists
related_artists_list_bis= []
for track in get_ids()['items']:
    related_artists =sp_user.artist_related_artists(track['artists'][0]['id'])
    # print(related_artists)
    related_artists_list_bis.append(related_artists)
rel_artists_short = []
for rel_artist in related_artists_list_bis:
    for artists in rel_artist['artists']:
        rel_artists_short.append((artists['name'],artists['id']))



# %%
rel_artists_short= list(set(rel_artists_short))
# print(rel_artists_short)



# %%
top_tracks_per_artist = []
# * top tracks per related artist
for artist in rel_artists_short:
    top_ts=sp_user.artist_top_tracks(artist[1])
    # print(top_ts['tracks'][0])
    for track in top_ts['tracks']:
        top_tracks_per_artist.append((track['name'],track['id']))
        # top_tracks_per_artist.append(track['id'])
with open('metadata/top_tracks_per_similar_artist.json', 'w') as f:
    json.dump(top_tracks_per_artist, f)

# %%
