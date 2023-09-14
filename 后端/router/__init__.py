from router.song.songinfo import song_bp
from router.user.userinfo import user_bp
from router.album.albuminfo import album_bp
from router.artist.artistinfo import artist_bp
from router.playlist.playlistinfo import playlist_bp
def init_app(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(song_bp)
    app.register_blueprint(album_bp)
    app.register_blueprint(artist_bp)
    app.register_blueprint(playlist_bp)
