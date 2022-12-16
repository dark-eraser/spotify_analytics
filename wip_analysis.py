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
from requests import ReadTimeout
import json 
import matplotlib.pyplot as plt
import numpy as np

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
    recently_played = sp.current_user_recently_played(limit=50)
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
def get_features(track_ids):
    try:
        features = sp.audio_features(track_ids)
    except ReadTimeout as e:
        print("sleeping..")
        time.sleep(5)
        features = sp.audio_features(track_ids)
    features_data=json.loads(json.dumps(features))
    with open('metadata/features.json', 'w') as outfile:
        json.dump(features_data, outfile)
    # print(features_data)
    return features_data

def unix_time():
    # print(int(str(time.time()).split('.')[0]))
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
def audio_analysis():
    with open("metadata/recently_played.json", "r") as f:
        data=json.load(f)
        ids=ret_ids(data)
        # print(ids)
        analysis_list=[]
        for id in ids:
            aa=sp.audio_analysis(id)
            analysis_list.append(aa)
        # print(analysis_list)


# %%
def average_features(features):
    categories=["danceability", "energy", "loudness", "key","mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
    # features=json.load(features)
    averages={}
    for category in categories:
        y=[feature[category] for feature in features]
        averages[category]=sum(y)/len(y)
    return averages


# %%
def create_batch(features):
    batches=[]
    for i in range(0,len(features),50):
        batches.append(features[i:i+50])
    return batches


# %%
def filter_with_features(avgs):
    with open("metadata/top_tracks_per_similar_artist.json", "r") as f:
        tracks=json.load(f)
    batches=create_batch(tracks)
    tracks_with_features=[]
    for batch in batches:
        tracks_with_features+=get_features([track[1]for track in batch])
    categories=["danceability", "energy", "loudness", "key","mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
    filtered_tracks=[]
    # count=[]
    for track in tracks_with_features:
        # count[track.index()]=0
        count=0
        # print(track.keys())
        if track is not None:
            for category in categories:
                # print(str(track[category])+"                 cc         " +str(np.arange(0.9*avgs[category],1.1*avgs[category],0.001)))
                if track[category]  >0.9*avgs[category]and track[category]<1.1*avgs[category]:
                    count+=1
        # break
        if count>3:
            try:
                filtered_tracks.append(track)
            except Exception as e:
                print(e )
                pass
    return filtered_tracks


# %%
# def main():
#     ids=get_ids()
#     features=get_features(ids)
#     with open("metadata/top_tracks_per_similar_artist.json", "r") as f:
#         tracks=json.load(f)
#         print(tracks.__len__())
#     filtered_tracks=filter_with_features(average_features(features))
#     print(filtered_tracks.__len__())
#     print(filtered_tracks)
#     # audio_analysis()
# main()
# test()

# %%
ids=get_ids()
features=get_features(ids)
with open("metadata/top_tracks_per_similar_artist.json", "r") as f:
    tracks=json.load(f)
    print(tracks.__len__())
filtered_tracks=filter_with_features(average_features(features))
print(filtered_tracks.__len__())
print(filtered_tracks)

# %%
# print(sp.recommendation_genre_seeds())
