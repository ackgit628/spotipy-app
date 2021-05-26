import os
import sys
import json
import spotipy
import webbrowser
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth

# Create the spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="MY CLIENT ID",
                                               client_secret="MY SECRET ID",
                                               redirect_uri="YOUR REDIRECT URI",
                                               scope="user-library-read user-top-read"))

# get the current user
user = sp.current_user()
# print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']

while True:
    print()
    print(">>> Welcome to Spotipy "+ displayName +"!")
    print()
    print("1 Search for a track")
    print("2 Search for an artist")
    print("3 View your top tracks")
    print("4 View your top artists")
    print("9 Exit")

    print()
    choice = input("Your choice: ")

    # search for a track
    if choice == "1":
        print()
        searchQuery = input("Ok, what's the name of the track?: ")
        print()

        # get search results
        searchResult = sp.search(searchQuery, 10, 0, 'track')
        # print(json.dumps(searchResult, sort_keys=True, indent=4))

        # Track Details
        trackIDs = []
        trackArt = []
        z = 0

        tracks = searchResult['tracks']['items']

        for item in tracks:
            print(str(z) + ". " + item['name'] + " - " + item['artists'][0]['name'])
            trackIDs.append(item['id'])
            trackArt.append(item['album']['images'][0]['url'])
            z+=1
        print()

        trackChoice = input("Enter the track number you searched for (x to exit): ")
        if trackChoice == "x":
            continue

        # Select Track and Display info
        trackInfo = sp.track(trackIDs[int(trackChoice)])
        trackLengthMin = int((trackInfo['duration_ms']/1000)/60)
        trackLengthSec = int((trackInfo['duration_ms']/1000)%60)
        print()
        print("Track name: " + trackInfo['name'])
        print("Artist: " + trackInfo['artists'][0]['name'])
        print("Album: " + trackInfo['album']['name'])
        print("Track length: " + str(trackLengthMin) + "m" + str(trackLengthSec) + "s")
        print()
        webbrowser.open(trackArt[int(trackChoice)])

    # search for an artist
    if choice == "2":
        print()
        searchQuery = input("Ok, what's the name of the artist?: ")
        print()

        # get search results
        searchResult = sp.search(searchQuery, 1, 0, 'artist')
        # print(json.dumps(searchResult, sort_keys=True, indent=4))

        # Artist Details
        artist = searchResult['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        # Album and Track Details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract Album Data
        albumResults = sp.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("Album " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            trackResults = sp.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ". " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        # See album art
        while True:
            songSelection = input("Enter a song number to see its album art (x to exit): ")
            if songSelection == "x":
                break
            webbrowser.open(trackArt[int(songSelection)])

    # get current user's top tracks
    if choice == "3":
        results = sp.current_user_top_tracks(10,0,'long_term')
        
        # Album Art
        trackArt = []

        print()
        for idx, item in enumerate(results['items']):
            print(idx, item['artists'][0]['name'], " – ", item['name'])
            albumArt = item['album']['images'][0]['url']
            trackArt.append(albumArt)
        print()

        # See album art
        while True:
            songSelection = input("Enter a song number to see its album art (x to exit): ")
            if songSelection == "x":
                break
            webbrowser.open(trackArt[int(songSelection)])

    # get current user's top artists
    if choice == "4":
        results = sp.current_user_top_artists(10,0,'long_term')
        
        # Artist image
        artistImage = []

        print()
        for idx, item in enumerate(results['items']):
            print(idx, item['name'], "\t\t", item['followers']['total'], "followers")
            image = item['images'][0]['url']
            artistImage.append(image)
        print()

        # See album art
        while True:
            artistSelection = input("Enter a number to view the artist's image (x to exit): ")
            if artistSelection == "x":
                break
            webbrowser.open(artistImage[int(artistSelection)])

    # exit spotipy
    if choice == "9":
        break


# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])