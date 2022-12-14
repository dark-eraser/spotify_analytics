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
import random
import json 
import matplotlib.pyplot as plt

# %%
data= json.load(open('metadata/ids.json'))
username = data["username"]
client_id = data["client-id"]
client_secret = data["client-secret"]
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-top-read'

# %%
token = spotipy.util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
# print(token)
sp_user= spotipy.Spotify(auth=token)
# token = spotipy.util.prompt_for_user_token(username=username,
#                                    scope=scope,
#                                    client_id=client_id,
#                                    client_secret=client_secret,
#                                    redirect_uri=redirect_uri)
# # print(token)
# sp_= spotipy.Spotify(auth=token)

# %%
top_artists = sp_user.current_user_top_artists(limit=50, time_range='short_term')
# * print top tracks and artists
# for track in top_tracks['items']:
#     print(track['artists'][0]['name'])
#     print(track['name'])

# * related artists
related_artists_list = []
for artist in top_artists['items']:
    related_artists = sp_user.artist_related_artists(artist['id'])
    # print(related_artists)
    related_artists_list.append(related_artists)
rel_artists_short = []
for rel_artist in related_artists_list:
    for artists in rel_artist['artists']:
        rel_artists_short.append((artists['name'],artists['id']))

# %%
top_tracks = sp_user.current_user_top_tracks(limit=50, time_range='short_term')
# * print top tracks and artists
# for track in top_tracks['items']:
#     print(track['artists'][0]['name'])
#     print(track['name'])

# * related artists
related_artists_list_bis= []
for track in top_tracks['items']:
    related_artists =sp_user.artist_related_artists(track['artists'][0]['id'])
    # print(related_artists)
    related_artists_list_bis.append(related_artists)
rel_artists_short_bis = []
for rel_artist in related_artists_list_bis:
    for artists in rel_artist['artists']:
        rel_artists_short_bis.append((artists['name'],artists['id']))
rel_artists_short=rel_artists_short+rel_artists_short_bis


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

# %% [markdown]
# Creates new playlist with 30 similar songs
#

# %%
new_disc_weekly = []
for i in range(0,30):
    rand=random.randint(0,len(top_tracks_per_artist))
    track_id =top_tracks_per_artist[rand][1]
    track= sp_user.track(track_id)
    new_disc_weekly.append(track)

scope='playlist-modify-public'
token = spotipy.util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
sp_user= spotipy.Spotify(auth=token)
id=sp_user.user_playlist_create(user=username, name='New Discovery Weekly', public=True)
print(id)
sp_user.playlist_add_items(playlist_id=id['id'], items=[track['uri'] for track in new_disc_weekly])

# %%
