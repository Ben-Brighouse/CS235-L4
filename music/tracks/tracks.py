from flask import render_template, Blueprint
from music.tracks import services
import music.adapters.repository as repo

tracks_blueprint = Blueprint('tracks_bp', __name__)


@tracks_blueprint.route('/browse')
def browse():
    list_of_tunes = services.get_tracks(repo.repo_instance)
    return render_template('browse.html', page_title='Browse', tracks=list_of_tunes)

@tracks_blueprint.route('/song/<int:track_id>')
def simple_track(track_id):
    track = services.get_track_by_id(track_id, repo.repo_instance)
    return render_template('simple_track.html', track=track)
