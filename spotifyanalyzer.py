# NAME: Lillian Murtonen
# ID: 2140930924
# DATE: 2023-05-04
# DESCRIPTION: This program receives an artist from the user and recommends similar artists. It
# also recommends songs from these artists according to how similar the song is to songs the
# user already likes.

import spotipy
from typing import Dict, List
# to make dictionaries more readable during development
import json
from spotipy.oauth2 import SpotifyClientCredentials

# my Spotify developer account API keys
client_id = 'INSERT YOUR OWN KEYS'
client_secret = 'INSERT YOUR OWN KEYS'

# get authorization token, create instance of class (SpotifyClientCredentials)
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# access Spotify API via python via spotipy
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# checked out
def get_liked_artist_id(liked_artist: str) -> str:
    # search spotify using input, get first artist
    results = spotify.search(q='artist:' + liked_artist, type='artist')
    # get id from first result in search
    liked_artist_id = results["artists"]["items"][0]["id"]
    # if you get search results from input
    if results:
        return liked_artist_id
    else:
        print("Sorry, we didn't find any results for your artist. Run the program again.")


# checked out
def recommend_related_artists(liked_artist_id: str, how_many_related_artists: int) -> List:
    related_artist_ids = spotify.artist_related_artists(liked_artist_id)
    related_artist_list = []

    # get top six related artists
    for x in range(how_many_related_artists):
        # retrieve related artist id from nested dictionary, append to list
        related_artist_list.append(related_artist_ids["artists"][x]["id"])
    return related_artist_list


# checked out
def get_liked_song_ids(liked_songs_by_artist: str, liked_artist_id: str) -> List:
    song_list = liked_songs_by_artist.split(',')
    # strip items in song list
    stripped_song_list = [x.strip() for x in song_list]

    liked_song_ids = []
    # get ids for each song in list
    for i in range(len(stripped_song_list)):
        # search spotify for song
        searchQuery = stripped_song_list[i] + ' ' + get_artist_name(liked_artist_id)
        results = spotify.search(q=searchQuery, type='track', limit=50)
        # print(json.dumps(results, indent=4))
        # search results for matching artist id to get the correct song
        # loops according to total amount of search results, which varies
        for x in range(len(results["tracks"]["items"])):
            # if the result's artist_id matches liked_artist_id, it's the correct song
            if results["tracks"]["items"][x]["artists"][0]["id"] == liked_artist_id:
                liked_song_ids.append(results["tracks"]["items"][x]["id"])
                break
        if not liked_song_ids:
            # go to next page
            results = spotify.search(q=searchQuery, type='track', limit=50, offset=50)
            # try the loop again
            i -= 1

    print(liked_song_ids)
    if liked_song_ids == []:
        print("Check your spelling of the song and run the program again. We couldn't find it.")
    return liked_song_ids


def analyze_liked_songs(liked_song_ids: List) -> Dict:
    similarities_dict = {}
    # because the similarity is emergent, created by comparing the first two songs
    # there will be variable results due to the order
    # sorting the list creates consistency
    liked_song_ids.sort()
    # if just one song, return all the audio_features
    if len(liked_song_ids) < 2:
        # audio_features returns a list of one item, a dict (spotify's API does this, idk why they do).

        song = spotify.audio_features(liked_song_ids[0])[0]
        return song
    else:
        # for multiple songs
        for i in range(len(liked_song_ids) - 1):
            # print(json.dumps(spotify.audio_features(liked_song_ids[i]), indent=4))
            current_song = spotify.audio_features(liked_song_ids[i])[0]
            next_song = spotify.audio_features(liked_song_ids[i + 1])[0]
            # print(json.dumps(next_song, indent=4))
            # print(json.dumps(current_song, indent=4))
            # print(current_song.keys())
            # loop through keys
            for x in next_song.keys():
                # print(x)
                # print(current_song[x], type(current_song[x]), next_song[x], type(next_song[x]))
                # some values are strings, so this condition filters them out
                if type(next_song[x]) is float:
                    # float values are on a scale of 0.0 to 1.0, so I chose .1 as the range of similarity

                    # first comparison between 2 songs
                    # makes sure we don't reenter first loop after first iteration
                    if i == 0:
                        if x != "loudness" or x != "tempo":
                            if abs(next_song[x] - current_song[x]) < .1:
                                # print("first two songs comparison")
                                # add values to list
                                similarities_dict[x] = (current_song[x] + next_song[x]) / 2
                                # print(similarities_dict)
                        # tempo range is different, from 50-200
                        elif x == "tempo":
                            if abs(next_song["tempo"] - current_song["tempo"]) < 10:
                                similarities_dict["tempo"] = (current_song["tempo"] + next_song["tempo"]) / 2
                        # loudness range is different and all negative, from -60 - 0
                        elif x == "loudness":
                            if abs(abs(next_song["loudness"]) - abs(current_song["loudness"])) < 5:
                                similarities_dict = (current_song["loudness"] + next_song["loudness"]) / 2
                    # if similarities_dict key is not empty (3+ songs entered)
                    elif x in similarities_dict:
                        # compare average of last songs [x] with current song's [x]
                        # this way, we find a similarity across ALL the input songs
                        if x != "tempo" or x != "loudness":
                            if abs(similarities_dict[x] - current_song[x]) < .1:
                                # print("3+ songs loop, updating value for", x)
                                # replace with new average of prev key value and new value
                                similarities_dict[x] = (similarities_dict[x] + next_song[x]) / 2
                        elif x == "tempo":
                            if abs(similarities_dict["tempo"] - current_song["tempo"]) < 10:
                                similarities_dict = (similarities_dict["tempo"] + next_song["tempo"]) / 2
                        elif x == "loudness":
                            if abs(abs(similarities_dict["loudness"]) - abs(current_song["loudness"])) < 5:
                                similarities_dict = (similarities_dict["loudness"] + next_song["loudness"]) / 2
                        # ex. if similar value found in song1 and song2, but not song3, delete category
                        else:
                            del similarities_dict[x]
    return similarities_dict


def analyze_multiple_song_similarity(song_analysis: Dict, song_id: str, similarity_amount: float) -> bool:
    check_new_song = spotify.audio_features(song_id)[0]
    flag = True
    print(get_track_name(song_id))
    # comparing two dictionaries, only runs once
    for x in song_analysis.keys():
        # only need to check if flag is still up
        if flag:
            if type(song_analysis[x]) is float:
                if x != "loudness" or x != "tempo":
                    if abs(song_analysis[x] - check_new_song[x]) > similarity_amount:
                        flag = False
                        # print(x)
                        # print(song_analysis[x], check_new_song[x])
                        # print(abs(song_analysis[x] - check_new_song[x]), flag)
                # tempo range is judged differently
                if x == "tempo":
                    if abs(song_analysis["tempo"] - check_new_song["tempo"]) > 10:
                        flag = False
                        # print(abs(song_analysis["tempo"] - check_new_song["tempo"], flag))
                # loudness range is judged differently
                elif x == "loudness":
                    if abs(abs(song_analysis["loudness"]) - abs(check_new_song["loudness"])) > 5:
                        flag = False
                        # print(abs(abs(song_analysis["loudness"]) - abs(check_new_song["loudness"])), flag)
    # print(flag)
    return flag


# more lax criteria, hard to find a similar song with just one song bc all categories intact
def analyze_single_song_similarity(song_analysis: Dict, song_id: str, similarity_amount: float) -> bool:
    check_new_song = spotify.audio_features(song_id)[0]
    flag = True
    # if default value
    if similarity_amount == .1:
        # change to looser default for single song criteria
        similarity_amount = .2
    print(get_track_name(song_id))
    # comparing two dictionaries, only runs once
    for x in song_analysis.keys():
        # only need to check if flag is still up
        if flag:
            if type(song_analysis[x]) is float:
                if x != "loudness":
                    if x != "tempo":
                        if abs(song_analysis[x] - check_new_song[x]) > similarity_amount:
                            flag = False
                            # print(x)
                            # print(song_analysis[x], check_new_song[x])
                            # print(abs(song_analysis[x] - check_new_song[x]), flag)
                # tempo range is judged differently
                elif x == "tempo":
                    if abs(song_analysis["tempo"] - check_new_song["tempo"]) > 20:
                        flag = False
                        # print(abs(song_analysis["tempo"] - check_new_song["tempo"], flag))
                # loudness range is judged differently
                elif x == "loudness":
                    if abs(abs(song_analysis["loudness"]) - abs(check_new_song["loudness"])) > 10:
                        flag = False
                        # print(abs(abs(song_analysis["loudness"]) - abs(check_new_song["loudness"])), flag)
    # print(flag)
    return flag


def narrow_down_related_songs(related_artist_list: List, song_analysis: Dict,
                              liked_song_ids: List, similarity_amount: float) -> List:
    recommend_songs = []

    for x in range(len(related_artist_list)):
        # run through each artist in list
        potential_related_artist = spotify.artist_top_tracks(related_artist_list[x])
        # run through each artist's top ten songs (default) or however many the artist has
        for y in range(len(potential_related_artist["tracks"])):
            # get id from each song
            potential_related_song_from_artist = potential_related_artist["tracks"][y]["id"]
            # if song fits criteria of song analysis
            if len(liked_song_ids) == 1:
                if analyze_single_song_similarity(song_analysis, potential_related_song_from_artist, similarity_amount):
                    recommend_songs.append(potential_related_song_from_artist)
            else:
                if analyze_multiple_song_similarity(song_analysis, potential_related_song_from_artist,
                                                    similarity_amount):
                    # store track id if it's a match
                    recommend_songs.append(potential_related_song_from_artist)
    return recommend_songs


def get_artist_name(artist_id: str) -> str:
    artist_info = spotify.artist(artist_id)
    return artist_info["name"]


def get_artist_name_from_list(artist_id_list: List) -> List:
    artist_name_list = []
    for y in range(len(artist_id_list)):
        name = get_artist_name(artist_id_list[y])
        print(name)
        artist_name_list.append(name)
    return artist_name_list


def get_track_name(track_id: str) -> str:
    track_info = spotify.track(track_id)
    # print(json.dumps(track_info, indent=4))
    return track_info["name"] + " by " + track_info["artists"][0]["name"]


def get_track_link(track_id: str) -> str:
    track_info = spotify.track(track_id)
    return track_info["external_urls"]["spotify"]


def main():
    print("Welcome to Lillian's Spotify Music Analyzer Service.\n"
          "（✿ ͡◕ ᴗ◕)つ━━✫・*。・*。・*。・*。\n"
          "This program will try to help you find new tunes that you'll like.\n")
    liked_artist = input("Who's an artist you already like? ")
    liked_artist_id = get_liked_artist_id(liked_artist)
    liked_songs_by_artist = input("Enter one or more of your favorite songs by this artist, separated by commas. "
                                  "Make sure it is spelled correctly: ")

    # get ids for liked songs
    liked_song_ids = get_liked_song_ids(liked_songs_by_artist, liked_artist_id)
    # analyze liked songs, what they all have in common, create average
    song_analysis = analyze_liked_songs(liked_song_ids)

    if len(liked_song_ids) > 1:
        print("After analyzing your songs, listed below are the qualities they have in common "
              "and their averages: ")
    else:
        print("Here are the qualities of your song: ")
    print(json.dumps(song_analysis, indent=4))

    how_many_related_artists = int(input("How many related artists do you want? "
                                         "This will also increase/decrease how many related songs you get.\n"))
    while how_many_related_artists > 20:
        print("Must be 20 or less:")
        how_many_related_artists = int(input("Enter a new number: "))
    # get list of related artists
    related_artists = recommend_related_artists(liked_artist_id, how_many_related_artists)

    print("After combing through related artists similar to " + liked_artist +
          ", here are some we think you'll like:")
    get_artist_name_from_list(related_artists)

    print("\nYou can customize how similar you want your recommended songs to be.\n")
    customize_answer = input("Would you like to?\n"
                             "yes/no\n")
    if customize_answer == "yes":
        similarity_amount = abs(float(input("How similar do you want your recommendations, "
                                            "on a scale of 0.00 to 1.00?\n")) - 1)
    else:
        # default value
        similarity_amount = .1

    print("Checking these songs...\n")
    # print new recommended songs using previous song_analysis
    related_songs = narrow_down_related_songs(related_artists, song_analysis, liked_song_ids, similarity_amount)
    if not related_songs:
        print("\nSorry, we couldn't find related tracks to your song. Please try again with a new song or "
              "adjust your similarity criteria.")
    else:
        print("\nOut of the songs above, these are the songs that fit the criteria."
              "\nIf you want to listen to some new artists, these are the songs you should start with!")

        for x in range(len(related_songs)):
            # just give five songs at first
            if len(related_songs) > 5 and x < 5:
                print(get_track_name(related_songs[x]))
                print(get_track_link(related_songs[x]))
            elif len(related_songs) <= 5:
                print(get_track_name(related_songs[x]))
                print(get_track_link(related_songs[x]))
        if len(related_songs) > 5:
            print("We found more than five related songs that fit the criteria. Would you like the rest?")
            more_songs = input("yes/no\n")
            for y in range(len(related_songs) - 5):
                print(y)
                if more_songs == "yes":
                    # give more songs
                    print(get_track_name(related_songs[y + 5]))
                    print(get_track_link(related_songs[y + 5]))
                else:
                    print("All good. This is the end of the program.")

    print("\nTip for how to better use this program: On the next round, if you are looking "
          "specifically for a type of sound, only input songs that have the sound you are looking for."
          "\nOr, just input one song. Inputting multiple songs will "
          "yield broader recommendations and you may have to increase the similarity index accordingly.")
    # print(json.dumps(spotify.recommendations(seed_tracks=liked_song_ids), indent=4))


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()
