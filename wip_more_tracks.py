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
#     display_name: Python 3.10.4 64-bit
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
sp= spotipy.Spotify(auth=token)

# %%
def get_ids():
    lastPass=False
    ids=[]
    date_now=unix_time()
    date_7_day_ago=date_now-(7*86400)
    date=date_now
    while not lastPass:
        track_ids,before_dates=get_ids_batch(50,before=date)
        for d in before_dates:
            if (d <= date_7_day_ago):
                lastPass=True
    ids.append(track_id for track_id in track_ids)
    date=min(before_dates)

def get_ids_batch(limit=50,before=0):
    recently_played = sp.current_user_recently_played(limit=limit,before=before)
    recently_played_data=json.loads(json.dumps(recently_played))
    with open('metadata/recently_played.json', 'a') as outfile:
        json.dump(recently_played_data, outfile)
    track_ids=[]
    before_dates=[]
    for track in recently_played_data['items']:
        # print(track["track"]["id"])
        track_ids.append(track["track"]["id"])
        before_dates.append(track["track"]["cursors"]["before"])
    return track_ids,before_dates

# %%
def get_features(track_ids):
    features = sp.audio_features(track_ids)
    features_data=json.loads(json.dumps(features))
    with open('metadata/features.json', 'w') as outfile:
        json.dump(features_data, outfile)
    print(features_data)
    return features_data

def unix_time():
    print(int(str(time.time()).split('.')[0]))
    return int(str(time.time()).split('.')[0])
# %%
def plot_features(features):
    categories=["danceability", "energy", "loudness", "key","mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
    features=json.load(features)
    for category in categories:
        plt.figure(figsize=(8, 8))
        y=[feature[category] for feature in features]
        # y=
        x=[feature["id"] for feature in features]
        plt.plot(x,y)
        plt.savefig("plots/"+str(category)+".png")

# %%
def test():
    recently_played = sp.current_user_recently_played(limit=1,after=1668876450)
    print(recently_played)


# %%
def main():
    ids=get_ids()
    get_features(ids)
    plot_features(open('metadata/features.json'))
main()
# test()