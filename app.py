#  Backend code with Flask


import json
from flask_cors import CORS
from crypt import methods
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import insert
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

db = SQLAlchemy(app)

class playlist(db.Model):
  __tablename__ = 'playlist'
  id = db.Column("id", db.Integer, primary_key=True)
  playlistUrl = db.Column(db.String(100))
  genreName = db.Column(db.String(100))
#   genre_id =  db.Column(db.Integer, db.ForeignKey('genre.id'))
  # genre


# class genre(db.Model):
#   __tablename__ = 'genre'
#   id = db.Column("id",db.Integer, primary_key=True)
#   genreName = db.Column(db.String(100))



@app.route('/', methods=["GET"])
def dummyFunc():
    print("request received")

    # return "<h1>hello world</h1>"
    r = requests.post('http://localhost:8081/api/addplaylist', json={"playlistURL": "http:spotify.com/12345", "genreID": "5"})
    return "<h1>hell/o world</h1>"


@app.route("/api/onload", methods=["GET"])
def onLoad():
    print('On Load')
    playLists = [
        {
            "playListUrl": "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd",
            "genre": "Pop"
        },
        {
            "playListUrl": "https://open.spotify.com/playlist/37i9dQZF1DX0kbJZpiYdZl",
            "genre": "EDM"
        },
        {
            'playListUrl': 'https://open.spotify.com/playlist/37i9dQZF1DX1lVhptIYRda',
            'genre': 'Country'
        }



    ]


    # response = json.dumps(response)
    print("Sending...")

    return json.dumps({'playListURL': playLists[0]['playListUrl']}), 202, {'ContentType':'application/json'}





@app.route("/api/addplaylist", methods=['POST'])
def addplayList():
    if request.method == 'POST':
        print("API called received")
        content = request.json
        playListURL = content['playlistURL']
        genre = content['genre']
        print(genre)
        # response = {""}
        try:
            # statement = insert(songs).values(playlistUrl=playlistURL)
            # pl = playlist(playlistUrl=playListURL, genreName=genre)
            # db.session.add(pl)
            # db.session.commit()
            # # return Response(status_code = 200)
            # found_pl = playlist.query.filter_by(playlistUrl=playListURL).first()
            # print(found_pl)
            return str(playListURL) + " added!"

        except:
            return Response(status_code=401)



if __name__ == "__main__":
    db.create_all()
    app.run(port=8081, debug=True)