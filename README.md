# Spotify Music Analyzer and Recommender

<h3>
⚠️ Note: This project is no longer functional due to changes in the Spotify Web API as of November 2024. 
   The API endpoint used by the <code>audio_features()</code> function in Spotipy—essential to the analyzer—is no longer supported. RIP!   
</h3>

## Features:
- Find Related Artists: Input an artist's name to get a list of up to 10 (or a custom-specified number) of related artists.
- Analyze a Song: Enter a song to get an analysis of its mood, tempo, key, energy, and other characteristics.
- Discover Similar Songs: Generate a list of songs with similar audio profiles by related artists.

## Requirements

- Python 3.8 or later
- Installing spotipy
  
<h1>
Example Interaction: 
</h1>

Welcome to Lillian's Spotify Music Analyzer Service.
（✿ ͡◕ ᴗ◕)つ━━✫・*。・*。・*。・*。

Who's an artist you already like? Fontaines D.C.
Enter one or more of your favorite songs by this artist, separated by commas. Make sure it is spelled correctly: 
> Boys in the Better Land

Here are the qualities of your song:
<pre>
<code>
{
    "danceability": 0.742,
    "energy": 0.945,
    "key": 5,
    "loudness": -6.445,
    "mode": 1,
    "speechiness": 0.0428,
    "acousticness": 0.0639,
    "instrumentalness": 0.165,
    "liveness": 0.131,
    "valence": 0.742,
    "tempo": 112.977,
    "type": "audio_features",
    "id": "0Cn4UhpHhgf88eWaS9nn5u",
    "uri": "spotify:track:0Cn4UhpHhgf88eWaS9nn5u",
    "track_href": "https://api.spotify.com/v1/tracks/0Cn4UhpHhgf88eWaS9nn5u",
    "analysis_url": "https://api.spotify.com/v1/audio-analysis/0Cn4UhpHhgf88eWaS9nn5u",
    "duration_ms": 256693,
    "time_signature": 4
}
</code>
</pre>


Do you want to pick the artist to find a similar song from?
yes/no
> no

How many related artists do you want? This will also increase/decrease how many related songs you get:
> 3

After combing through related artists similar to Fontaines D.C., here are some we think you'll like:
1. IDLES
2. Shame
3. The Murder Capital

You can customize how similar you want your recommended songs to be.
Would you like to?
yes/no
> yes

How similar do you want your recommendations, on a scale of 0.00 to 1.00? The higher the number, the more similar:
> 0.8

Checking these songs...

Out of the songs above, these are the songs that fit the criteria.
If you want to listen to some new artists, these are the songs you should start with!

1. War by IDLES
   https://open.spotify.com/track/2kYn0VPQY1iTY3XpCvUaPt
2. Dust on Trial by Shame
   https://open.spotify.com/track/3y0rgC8Enu01ZeeL7jzFnI
3. Green & Blue by The Murder Capital
   https://open.spotify.com/track/41h3NPLQyDIOpER0690Yh9

Tip for how to better use this program: Inputting more songs will yield broader recommendations and you may have to increase the similarity index accordingly. 
If you're after a specific feel or song, limit your input to one song.
