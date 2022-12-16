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
from requests.exceptions import ReadTimeout


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
def top_artists_user():
    top_artists = sp_user.current_user_top_artists(limit=50, time_range='short_term')
    # * print top tracks and artists
    # for track in top_artists['items']:
    #     print(track['name'])

    # * related artists
    related_artists_list = []
    for artist in top_artists['items']:
        print("coucou")
        try:
            related_artists = sp_user.artist_related_artists(artist['id'])
        except ReadTimeout:
            print("ReadTimeout")
            time.sleep(5)
            related_artists = sp_user.artist_related_artists(artist['id'])
        # print(related_artists)
        related_artists_list.append(related_artists)
    rel_artists_short = []
    print("coucou")
    for rel_artist in related_artists_list:
        for artists in rel_artist['artists']:
            rel_artists_short.append((artists['name'],artists['id']))
    return list(set(rel_artists_short))
# %%
def top_artists_rel(top_artists):
    # top_artists = sp_user.current_user_top_artists(limit=50, time_range='short_term')
    # * print top tracks and artists
    # for track in top_tracks['items']:
    #     print(track['artists'][0]['name'])
    #     print(track['name'])

    # * related artists
    related_artists_list = []
    for artist in top_artists:
        related_artists = sp_user.artist_related_artists(artist[1])
        # print(related_artists)
        related_artists_list.append(related_artists)
    rel_artists_short = []
    for rel_artist in related_artists_list:
        for artists in rel_artist['artists']:
            rel_artists_short.append((artists['name'],artists['id']))
    return list(set(rel_artists_short))


# %%
def top_tracks_user():
    top_tracks = sp_user.current_user_top_tracks(limit=50, time_range='short_term')
    # * print top tracks and artists
    for track in top_tracks['items']:
        print(track['artists'][0]['name'])
        print(track['name'])

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
    rel_artists_short=rel_artists_short_bis
    return list(set(rel_artists_short))

# %%
# print(rel_artists_short)



# %%
def top_tracks_per_artist(rel_artists_short):
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
    return top_tracks_per_artist

# %%
# * tracks in discovery weekly playlist
def disc_weekly():
    disc_weekly=sp_user.search(q='Discovery Weekly', type='playlist', limit=1)
    # print(disc_weekly['playlists']['items'][0]['id'])
    disc_weekly_tracks=sp_user.playlist_tracks(disc_weekly['playlists']['items'][0]['id'])
    disc_weekly_tracks_ids=[]
    for track in disc_weekly_tracks['items']:
        disc_weekly_tracks_ids.append((track['track']['id'],track['track']['name']))
    with open('metadata/disc_weekly_tracks.json', 'w') as f:
        json.dump(disc_weekly_tracks_ids, f)
    return disc_weekly_tracks_ids
# %%
def rep(top_artists):
    artists=[]
    for i in range(2):
        artists[i]=top_artists_rel(top_artists)
    return artists
    
 


# %%

# %%


def main():
    rel_artists_from_artists=top_artists_user()
    print("==================== Step 1 done ====================")
    rel_artists_from_tracks=top_tracks_user()
    print("==================== Step 2 done ====================")
    all_rel_artists=[]
    try:
        all_rel_artists=rep(rel_artists_from_artists+rel_artists_from_tracks)
    except ReadTimeout:
        print("ReadTimeout")
        time.sleep(5)
        all_rel_artists=rep(rel_artists_from_artists+rel_artists_from_tracks )
    all_rel_artists=list(set(all_rel_artists))
    print("==================== Step 3 done ====================")

    top_tracks_per_artist_list=top_tracks_per_artist(all_rel_artists)
    print("==================== Step 4 done ====================")

    disc_weekly_tracks_ids= disc_weekly()
    print("==================== Step 5 done ====================")
    print(set(top_tracks_per_artist_list).intersection(disc_weekly_tracks_ids))
    print(top_tracks_per_artist_list.__len__())



# %%
main()
