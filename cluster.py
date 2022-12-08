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
top_tracks = sp_user.current_user_top_tracks(limit=50, time_range='short_term')
# * print top tracks and artists
artists=[]
for track in top_tracks['items']:
    artists.append(track['artists'][0]['id'])
#     print(track['name'])
artists=[sp_user.artist(artist) for artist in artists]
print(artists)

# %%
top_artists = sp_user.current_user_top_artists(limit=50, time_range='short_term')
top_artists


# %%
def extract_genres(artists):
    genres=[]
    # * print top tracks and artists
    for artist in artists['items']:
        genres.append(artist['genres'])
        # print(track['name'])
    genres_list=[]
    for genre_l in genres:
        for genre in genre_l:
            genres_list.append(genre)
    genres_dict={}
    for genre in genres_list:
        genres_dict[genre]=0
    # print(genres_dict)
    for artist in top_artists['items']:
        if artist['genres']!=[]:
            for genre in artist['genres']:
                genres_dict[genre]+=1
    return genres_dict


# %%

# %%
def plot_features(genres):
    from matplotlib.pyplot import figure
    import numpy as np
    y_pos = np.arange(len(genres))
    figure(figsize=(12, 10), dpi=200)
    plt.barh( y_pos, list(genres.values()), align='center', alpha=0.5)
    plt.yticks(y_pos, list(genres.keys()))


# %%
genres_dict=extract_genres(artists)
plot_features(genres_dict)

# %%
