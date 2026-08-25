"""Initialize Flask app."""

from flask import Flask, render_template

from music.adapters import memory_repository, repository_populate
import music.adapters.repository as repo



def create_app():
    app = Flask(__name__)
    repo.repo_instance = memory_repository.MemoryRepo()
    repository_populate.populate_repo(repo.repo_instance)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .tracks import tracks
        app.register_blueprint(tracks.tracks_blueprint)


    return app
