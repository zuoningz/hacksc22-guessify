import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request
#from h11 import Response

# set up flask 
app = Flask(__name__)

# set up spotify object
cid = '1dd228296e1e457696270ce494ba73ac'
csecret = '80e8ea445f874703bc28a1fca532f54f'
auth_manager = SpotifyClientCredentials(client_id = cid, client_secret = csecret)
sp = spotipy.Spotify(auth_manager=auth_manager)

track_uris = []
track_names = []
artist_uris = []
artist_names = []

# for old parser
trackNames = []
trackNum = 0  # to keep track of which song playlist is at 
artistNames = []
artistNum = 0

@app.route('/api/addplaylist')
def parsePlaylist(playlistURL):
    #content = request.json
    #playlistURL = content
    playlist_uri = playlistURL.split("/")[-1].split("?")[0]
    #track_uri = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_id)["items"]]
    for track in sp.playlist_tracks(playlist_uri)["items"]:
        # Track URI
        track_uri = track["track"]["uri"]
        track_uris.append(track_uri)
        # Track name
        track_name = track["track"]["name"]
        track_names.append(track_name)
        # Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_name = sp.artist(artist_uri)["name"]
        artist_uris.append(artist_uri)
        artist_names.append(artist_name)
    return None

@app.route('/getRecs')
def getRecommendations():
    recs = sp.recommendations(artist_uris, sp.recommendation_genre_seeds(), track_uris)
    #print(recs)
    return recs


def parsePlaylist2(playlistURL):
  #content = request.json
  #URL = content
  URL = playlistURL
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  # print(soup.title.text)
  # soup = soupTemp
  # get all the songs in the playlist 
  mainPage = soup.find("div", id="main")
  topContainer = mainPage.div.div
  print("Testing: " + topContainer.prettify())
  playlistContent = topContainer.find("div", class_="contentSpacing")
  songRows = playlistContent.find_all("div", role="row")

  for song in songRows:
    track = songRows.find("div", class_="t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line w_Xs9cRXMwmQHw8BpiID")
    # why tf this class name so long
    trackName = track.text.strip() # gets name of song in plain text 
    print(trackName)
    trackNames.append(trackName)

  for artist in songRows:
    artistTemp = songRows.find("span", class_="rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line Hi9FqPX1LNRRPf31tfA8")
    artist = artistTemp.find("a")
    artistName = artist.text.strip() # gets name of artist
    print(artistName)
    artistNames.append(artistName)
  print("Track Names filled: ")
  print(trackNames.size > 0)
  print("Artist Names filled: ")
  print(artistNames.size > 0)
  return None

@app.route('/getSong')
def getSongID():
  global trackNum
  global artistNum
  trackName = trackNames[trackNum]
  artistName = artistNames[artistNum]
  trackNum += 1
  artistNum += 1
  print("Track: "+trackName+"\tArtist: "+artistName) # for testing/debugging purposes
  track_search = sp.search(q='artist:' + artistName + ' track:' + trackName, type='track')
  track_id = track_search['tracks']['items'][0]['id']
  # ideally, get song ID and return it
  return track_id


# for searching for genres??
# on the search page of spotify
# mainPage = soup.find("div", class_="contentSpacing")
# browseGenres = mainPage.find("div", data_testid="browse-all")
# containers = browseGenres.find("div", data_testid="grid-container")
# genreLabels = containers.find_all("a", class_="Em2LrSSfvrgXQoajs6cm")
# for loop through genreLabels :
#   genreName = genreLabels.find("h3", class_="i2yp6pOoZpYZLd5QWguN")
#   genreNameText = genreName.text

#app.run(host='0.0.0.0', port=8080, debug = True)
