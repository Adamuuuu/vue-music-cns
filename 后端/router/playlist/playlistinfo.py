from flask import Blueprint, request
from model.song.song import SongInfo,AlbumInfo,ArtistInfo,ArtistSong,PlaylistSong,PlaylistInfo
from model import db
from sqlalchemy import or_

playlist_bp = Blueprint("playlist", __name__, url_prefix="/v1")

# 查询所有播放列表
# 查询所有播放列表并分页
@playlist_bp.route('/all/playlist', methods=['GET'])
def queryAllPlaylistsInfo():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    playlist_all = PlaylistInfo.query.paginate(page=page, per_page=per_page)
    total_pages = playlist_all.pages
    current_page = playlist_all.page
    playlists = playlist_all.items

    data = [playlist.to_json() for playlist in playlists]

    response = {
        "code": 0,
        "message": "查询成功",
        "data": data,
        "total_pages": total_pages,
        "current_page": current_page
    }

    return response
# 搜索歌单
@playlist_bp.route("/some/playlist",methods=['POST'])
def searchPlaylist():
    data=request.json
    query = PlaylistInfo.query
    if "Keyword" in data:
        query = query.filter(
            or_(PlaylistInfo.PlaylistName.like(f"%{data['Keyword']}%"), PlaylistInfo.CreatorName.like(f"%{data['Keyword']}%")))

    playlists = query.all()
    data = [playlist.to_json() for playlist in playlists]
    response = {
        "code": 0,
        "message": "搜索成功",
        "data": data
    }
    return response
# 获取歌单中的所有歌曲
@playlist_bp.route('/playlist/all/songs',methods=['GET'])
def queryAllPlaylistSongs():
    playlist_id=request.args.get('playlist_id')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    try:
        playlist_song_query=PlaylistSong.query.filter(PlaylistSong.PlaylistID==playlist_id).paginate(page=page, per_page=per_page)
        song_ids=[playlist_song.SongID for playlist_song in playlist_song_query]
        query=SongInfo.query.filter(SongInfo.SongID.in_(song_ids))

        songs = query.all()
        data = [song.to_json() for song in songs]
        response = {
            "code": 0,
            "message": "查询成功",
            "data": data
        }

    except Exception as e:
        print("出现错误",e)
        response = {
            "code": -1006,
            "message": f"数据库操作出错：{e}"
        }
    return response

# 新增歌单
@playlist_bp.route('/playlist', methods=['POST'])
def createPlaylistInfo():
    data = request.json

    playlist = PlaylistInfo(
        PlaylistID=data['PlaylistID'],
        PlaylistName=data['PlaylistName'],
        CreatorID=data['CreatorID'],
        CoverURL=data['CoverURL'],
        Introduction=data['Introduction'],
        PlayCount=data.get('PlayCount', 0),
        FavoriteCount=data.get('FavoriteCount', 0),
        CreatorName=data['CreatorName'],
        Avatar=data['Avatar']
    )
    db.session.add(playlist)
    db.session.commit()

    response = {
        "code": 0,
        "message": "新增歌单成功"
    }
    return response


# 修改歌单信息
@playlist_bp.route('/playlist', methods=['PATCH'])
def updatePlaylistInfo():
    data = request.json

    try:
        playlist = PlaylistInfo.query.get(data['PlaylistID'])

        if playlist:
            playlist.PlaylistName = data.get('PlaylistName', playlist.PlaylistName)
            playlist.CoverURL = data.get('CoverURL', playlist.CoverURL)
            playlist.Introduction = data.get('Introduction', playlist.Introduction)
            playlist.PlayCount = data.get('PlayCount', playlist.PlayCount)
            playlist.FavoriteCount = data.get('FavoriteCount', playlist.FavoriteCount)
            playlist.CreatorName = data.get('CreatorName', playlist.CreatorName)
            playlist.Avatar = data.get('Avatar', playlist.Avatar)

            db.session.commit()

            response = {
                "code": 0,
                "message": "修改歌单信息成功",
                "data": data
            }
        else:
            response = {
                "code": -1005,
                "message": "未查询到数据"
            }

    except Exception as e:
        response = {
            "code": -1006,
            "message": f"数据库操作出错：{e}"
        }

    return response


# 删除歌单
@playlist_bp.route('/playlist', methods=['DELETE'])
def deletePlaylistInfo():
    data = request.json

    try:
        playlist = PlaylistInfo.query.filter(PlaylistInfo.PlaylistID == data['PlaylistID']).first()

        if playlist is not None:
            db.session.delete(playlist)
            db.session.commit()
            response = {
                "code": 0,
                "message": "删除成功"
            }
        else:
            response = {
                "code": -1005,
                "message": "未找到数据"
            }

    except Exception as e:
        response = {
            "code": -1006,
            "message": f"查询出错：{e}"
        }

    return response

# 在歌单中新增歌曲
@playlist_bp.route('/playlist/songs',methods=['POST'])
def insertSongs():
    data=request.json
    try:
        song=SongInfo.query.filter(SongInfo.SongID==data['SongID']).first()
        playlist=PlaylistInfo.query.filter(PlaylistInfo.PlaylistID==data['PlaylistID']).first()
        if song and playlist is not None:
            playlist_song=PlaylistSong(
                SongID=data['SongID'],
                PlaylistID=data['PlaylistID']
            )
            # print(playlist_song)
            db.session.add(playlist_song)
            db.session.commit()
            db.session.close()
            response = {
                "code": 0,
                "message": "添加成功"
            }
        else:
            response = {
                "code": -1005,
                "message": "未找到数据"
            }

    except Exception as e:
        response = {
            "code": -1006,
            "message": f"查询出错：{e}"
        }

    return response
