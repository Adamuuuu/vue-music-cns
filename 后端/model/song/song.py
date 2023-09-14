from model import db

# 歌曲实体类
class SongInfo(db.Model):
    __tablename__ = "song"

    SongID = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    SongName = db.Column(db.String(300))
    AlbumID = db.Column(db.BigInteger, db.ForeignKey('album.AlbumID'))
    Duration = db.Column(db.Time)
    SongURL = db.Column(db.String(200))
    CoverURL = db.Column(db.String(200))

    def to_json(self):
        return {
            "SongID": self.SongID,
            "SongName": self.SongName,
            "AlbumID": self.AlbumID,
            "Duration": str(self.Duration),
            "SongURL": self.SongURL,
            "CoverURL": self.CoverURL
        }

# 歌手和歌曲中间表
class ArtistSong(db.Model):
    __tablename__ = 'artist_song'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='关联ID，主键')
    ArtistID = db.Column(db.BigInteger, nullable=True, comment='关联的歌手ID')
    SongID = db.Column(db.BigInteger, nullable=True, comment='关联的歌曲ID')

    def to_json(self):
        return {
            'ID': self.ID,
            'ArtistID': self.ArtistID,
            'SongID': self.SongID
        }

# 歌单和歌曲中间表
class PlaylistSong(db.Model):
    __tablename__ = 'playlist_song'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='关联ID，主键')
    PlaylistID = db.Column(db.BigInteger,db.ForeignKey('playlist.PlaylistID'), nullable=True, comment='关联的歌单ID')
    SongID = db.Column(db.BigInteger, db.ForeignKey('song.SongID'),nullable=True, comment='关联的歌曲ID')

    def to_json(self):
        return {
            'ID': self.ID,
            'PlaylistID': self.PlaylistID,
            'SongID': self.SongID
        }

# 专辑实体类
class AlbumInfo(db.Model):
    __tablename__ = "album"
    AlbumID = db.Column(db.BigInteger, primary_key=True)
    AlbumName = db.Column(db.String(300))
    CoverURL = db.Column(db.String(200))
    Artist = db.Column(db.String(100))
    ReleaseTime = db.Column(db.String(100))
    Introduction = db.Column(db.Text)

    def to_json(self):
        return {
            "AlbumID": self.AlbumID,
            "AlbumName": self.AlbumName,
            "CoverURL": self.CoverURL,
            "Artist": self.Artist,
            "ReleaseTime": self.ReleaseTime,
            "Introduction": self.Introduction
        }

# 歌手实体类
class ArtistInfo(db.Model):
    __tablename__ = "artist"

    ArtistID = db.Column(db.BigInteger, primary_key=True)
    ArtistName = db.Column(db.String(100))
    Avatar = db.Column(db.String(100))
    FansCount = db.Column(db.Integer, default=0)
    Wiki = db.Column(db.Text)

    def to_json(self):
        return {
            "ArtistID": self.ArtistID,
            "ArtistName": self.ArtistName,
            "Avatar": self.Avatar,
            "FansCount": self.FansCount,
            "Wiki": self.Wiki
        }

# 歌单实体类
class PlaylistInfo(db.Model):
    __tablename__ = "playlist"

    PlaylistID = db.Column(db.BigInteger, primary_key=True, comment='歌单ID，主键')
    PlaylistName = db.Column(db.String(50), comment='歌单名称')
    CreatorID = db.Column(db.BigInteger, comment='创建该歌单的用户ID')
    CoverURL = db.Column(db.String(800), comment='歌单封面图URL')
    Introduction = db.Column(db.Text, comment='歌单简介')
    PlayCount = db.Column(db.BigInteger, default=0, comment='歌单播放次数，默认为0')
    FavoriteCount = db.Column(db.BigInteger, default=0, comment='歌单收藏次数，默认为0')
    CreatorName = db.Column(db.String(50), comment='创建者昵称')
    Avatar = db.Column(db.String(200), comment='创建者头像')

    def to_json(self):
        return {
            "PlaylistID": self.PlaylistID,
            "PlaylistName": self.PlaylistName,
            "CreatorID": self.CreatorID,
            "CoverURL": self.CoverURL,
            "Introduction": self.Introduction,
            "PlayCount": self.PlayCount,
            "FavoriteCount": self.FavoriteCount,
            "CreatorName": self.CreatorName,
            "Avatar": self.Avatar
        }
