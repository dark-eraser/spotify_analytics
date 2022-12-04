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
data= json.load(open('ids.json'))
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
    recently_played = sp.current_user_recently_played(limit=50)
    
    with open('recently_played.json', 'w') as outfile:
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
def get_features(track_ids):
    features = sp.audio_features(track_ids)
    features_data=json.loads(json.dumps(features))
    with open('features.json', 'w') as outfile:
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
def audio_analysis():
    with open("recently_played.json", "r") as f:
        data=json.load(f)
        ids=ret_ids(data)
        print(ids)
        analysis_list=[]
        for id in ids:
            aa=sp.audio_analysis(id)
            analysis_list.append(aa)
        print(analysis_list)


# %%
def main():
    ids=get_ids()
    # get_features(ids)
    # plot_features(open('features.json'))
    audio_analysis()
main()
# test()

# %%
