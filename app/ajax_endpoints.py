from app import app, logging as logger
from flask import request, json
from flask_login import current_user, login_required

from .spotify_client import SpotifyClient
from .user_repository import UserRepository
from .post_repository import PostRepository

@app.route('/follow', methods=['POST'])
@login_required
def follow():
    repo = UserRepository()
    if repo.setFollow(current_user.user_id, request.json['username'], request.json['state']):
        return json.dumps({'status': 'OK'})
    return json.dumps({'status': 'ERROR'})

@app.route('/search', methods=['POST'])
@login_required
def search():
    search_query = request.json['query']

    if search_query == None or search_query == '' or search_query.isspace():
        return "{}"
    
    logger.debug(f"Searching Spotify with query: '{search_query}'")

    sp = SpotifyClient()
    tracks = sp.search(search_query)

    for i in range(len(tracks)):
        tracks[i] = tracks[i].to_dict()

    return json.dumps(tracks)

@app.route('/like', methods=['POST'])
@login_required
def like():
    repo = PostRepository()
    repo.setLike(current_user.user_id, request.json['post_id'], request.json['state'])
    return json.dumps({'status': 'OK'})