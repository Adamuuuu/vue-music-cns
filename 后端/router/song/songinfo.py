from flask import Blueprint, request
from model.song.song import SongInfo,AlbumInfo,ArtistInfo,ArtistSong,PlaylistSong,PlaylistInfo
from model import db
from sqlalchemy import or_

song_bp = Blueprint("song", __name__, url_prefix="/v1")

# 查询所有歌曲
# 查询所有歌曲并分页
@song_bp.route('/all/song', methods=['GET'])
def queryAllSongsInfo():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    song_all = SongInfo.query.paginate(page=page, per_page=per_page)
    total_pages = song_all.pages
    current_page = song_all.page
    songs = song_all.items

    # data = [song.to_json() for song in songs]
    data=[]
    for song in songs:
        song_dict = song.to_json()  # 将 SongInfo 对象转换为字典
        album = AlbumInfo.query.filter_by(AlbumID=song_dict['AlbumID']).first()
        if album:
            song_dict['Album'] = album.AlbumName
        artist_id = ArtistSong.query.filter_by(SongID=song_dict['SongID']).first()
        if artist_id:
            artist = ArtistInfo.query.filter_by(ArtistID=artist_id.ArtistID).first()
            if artist:
                song_dict['Artist'] = artist.ArtistName
        data.append(song_dict)

    response = {
        "code": 0,
        "message": "查询成功",
        "data": data,
        "total_pages": total_pages,
        "current_page": current_page
    }

    return response

# 查询特定信息的歌曲
@song_bp.route("/some/song", methods=["POST"])
def query_songs():
    data = request.get_json()
    query = SongInfo.query
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if "SongID" in data:
        query = query.filter(SongInfo.SongID == data["SongID"])
    if "SongName" in data and data["SongName"] != "":
        query = query.filter(SongInfo.SongName == data["SongName"])
    if "Artist" in data and data["Artist"] != '':
        query_artist = ArtistInfo.query.filter(ArtistInfo.ArtistName == data["Artist"]).first()
        if query_artist is None:
            response = {
                "code": -1002,
                "message": "请输入有效的歌手名"
            }
            return response
        artist_song_query = ArtistSong.query.filter(ArtistSong.ArtistID == query_artist.ArtistID)
        song_ids = [artist_song.SongID for artist_song in artist_song_query]
        query = query.filter(SongInfo.SongID.in_(song_ids))
    if "Album" in data and data["Album"] != '':
        query_album = AlbumInfo.query.filter(AlbumInfo.AlbumName == data["Album"]).first()
        if query_album is None:
            response = {
                "code": -1002,
                "message": "请输入有效的专辑名"
            }
            return response
        query = query.filter(SongInfo.AlbumID == query_album.AlbumID)

    pagination = query.paginate(page=page, per_page=per_page)
    songs = pagination.items  # 获取当前页面的数据


    data = []
    for song in songs:
        song_dict = song.to_json()  # 将 SongInfo 对象转换为字典
        album = AlbumInfo.query.filter_by(AlbumID=song_dict['AlbumID']).first()
        if album:
            song_dict['Album'] = album.AlbumName
        artist_id = ArtistSong.query.filter_by(SongID=song_dict['SongID']).first()
        if artist_id:
            artist = ArtistInfo.query.filter_by(ArtistID=artist_id.ArtistID).first()
            if artist:
                song_dict['Artist'] = artist.ArtistName
        data.append(song_dict)

    response = {
        "code": 0,
        "message": "查询成功",
        "data": data,

    }

    return response


# 搜索功能（输出的关键字可能是歌名，也可能是歌手名）
@song_bp.route('/search/song', methods=['POST'])
def searchSongInfo():
    data = request.get_json()

    query_song = SongInfo.query
    query_artist = ArtistInfo.query
    query_album = AlbumInfo.query

    if "SongName" in data:
        # 搜索歌曲
        search_song = query_song.filter(or_(SongInfo.SongName.like(f"%{data['Keyword']}%")))
    if "Artist" in data:
        # 搜索歌曲
        artist_song = ArtistSong.query.filter(or_(SongInfo.SongName.like(f"%{data['Keyword']}%")))
        # 搜索歌手名
        search_artist = query_artist.filter(or_(ArtistInfo.ArtistName.like(f"%{data['Keyword']}%")))
        # 搜索专辑名
        search_album=query_album.filter(or_(AlbumInfo.AlbumName.like(f"%{data['Keyword']}%")))


    songs = search_song.all()
    data_song = [song.to_json() for song in songs]
    artists = search_artist.all()
    data_artist = [artist.to_json() for artist in artists]
    albums = search_album.all()
    data_album = [album.to_json() for album in albums]
    response = {
        "code": 0,
        "message": "搜索成功",
        "data": [{"songs": data_song},
                 {"artists": data_artist},
                 {"albums": data_album}

                 ]
    }
    return response


# @song_bp.route('/search/song', methods=['POST'])
# def searchSongInfo():
#     data = request.get_json()
#
#     query_song = SongInfo.query
#     query_artist = ArtistInfo.query
#     query_album = AlbumInfo.query
#
#     if "Keyword" in data:
#         # 搜索歌曲
#         search_song = query_song.filter(or_(SongInfo.SongName.like(f"%{data['Keyword']}%")))
#         # 搜索歌手名
#         search_artist = query_artist.filter(or_(ArtistInfo.ArtistName.like(f"%{data['Keyword']}%")))
#         # 搜索专辑名
#         search_album = query_album.filter(or_(AlbumInfo.AlbumName.like(f"%{data['Keyword']}%")))
#
#     songs = search_song.all()
#     data_song = [song.to_json() for song in songs]
#     artists = search_artist.all()
#     data_artist = [artist.to_json() for artist in artists]
#     albums = search_album.all()
#     data_album = [album.to_json() for album in albums]
#     response = {
#         "code": 0,
#         "message": "搜索成功",
#         "data": [{"songs": data_song},
#                  {"artists": data_artist},
#                  {"albums": data_album}
#
#                  ]
#     }
#     return response
# 新增歌曲
@song_bp.route('/song', methods=['POST'])
def createSongInfo():
    data = request.json
    print(data['SongName'])

    # 判断歌手是否存在
    artist_id = 0  # 默认歌手ID为0
    album_id = 0  # 默认专辑ID为0

    if "Singer" in data:
        artist_query = ArtistInfo.query.filter(ArtistInfo.ArtistName == data["Singer"]).first()
        if artist_query is None:
            print("请输入有效的歌手名")
            response = {
                "code": -1002,
                "message": "请输入有效的歌手名"
            }
            return response
        artist_id = artist_query.ArtistID

    if "Album" in data:
        album_query = AlbumInfo.query.filter(AlbumInfo.AlbumName == data["Album"]).first()
        if album_query is None:
            print("请输入有效的专辑名")
            response = {
                "code": -1002,
                "message": "请输入有效的专辑名"
            }
            return response
        album_id = album_query.AlbumID

    print("这是歌手id",artist_id)
    print("这是专辑id",album_id)

    song = SongInfo(
        SongID=data['SongID'],
        SongName=data['SongName'],
        CoverURL=data['CoverURL'],
        SongURL=data['SongURL'],
        Duration=data['Duration'],
        # ArtistID=artist_id,
        AlbumID=album_id
    )
    db.session.add(song)
    db.session.commit()

    if artist_id != 0:
        artist_song = ArtistSong(
            SongID=data['SongID'],
            ArtistID=artist_id
        )
        db.session.add(artist_song)

    # if album_id != 0:
    #     album_song = AlbumSong(
    #         SongID=data['SongID'],
    #         AlbumID=album_id
    #     )
    #     db.session.add(album_song)

    db.session.commit()
    response = {
        "code": 0,
        "message": "插入成功"
    }
    return response


# 修改歌曲信息
@song_bp.route('/song', methods=['PATCH'])
def updateSongInfo():
    data = request.json
    artist_id = 0  # 默认歌手ID为0
    album_id = 0  # 默认专辑ID为0

    if "Artist" in data:
        artist_query = ArtistInfo.query.filter(ArtistInfo.ArtistName == data["Artist"]).first()
        if artist_query is None:
            print("请输入有效的歌手名")
            response = {
                "code": -1002,
                "message": "请输入有效的歌手名"
            }
            return response
        artist_id = artist_query.ArtistID

    if "Album" in data:
        album_query = AlbumInfo.query.filter(AlbumInfo.AlbumName == data["Album"]).first()
        if album_query is None:
            print("请输入有效的专辑名")
            response = {
                "code": -1002,
                "message": "请输入有效的专辑名"
            }
            return response
        album_id = album_query.AlbumID

    print("这是歌手id", artist_id)
    print("这是专辑id", album_id)

    try:
        song = SongInfo.query.get(data['SongID'])


        if song:
            # 更新歌曲信息
            song.SongName = data.get('SongName', song.SongName)
            song.SongID = data.get('SongID', song.SongID)
            song.AlbumID = album_id
            # song.Album = data.get('Album', song.Album)
            song.SongURL = data.get('SongURL', song.SongURL)
            song.Duration = data.get('Duration', song.Duration)
            song.CoverURL = data.get('CoverURL', song.CoverURL)



            db.session.commit()

            if artist_id != 0:
                artist_song = ArtistSong.query.filter(ArtistSong.SongID == data['SongID']).first()
                if artist_song:
                    artist_song.ArtistID = artist_id
                    print("歌手", artist_id)
                    print("中间表id",artist_song.ID)
                    db.session.commit()
                else:

                    artist_song = ArtistSong(SongID=data['SongID'], ArtistID=artist_id)

                    db.session.add(artist_song)
                    db.session.commit()
            response={
                "code":0,
                "message":"更新数据成功",
                "data":data
            }
        else:
            response = {
                "code": -1005,
                "message": "未查询到数据"
            }

    except Exception as e:
        print("这是错误信息")
        response = {
            "code": -1006,
            "message": f"数据库操作出错{e}"
        }
    return response

# 删除歌曲信息
@song_bp.route('/song', methods=['DELETE'])
def deleteSongInfo():
    data = request.json

    try:
        song = SongInfo.query.filter_by(SongID=data['SongID']).first()
        if song is not None:
            song.SongURL = None  # 将SongURL字段置为空
            db.session.commit()
            response={
                "code":0,
                "message":"删除成功",
                "data":data
            }
        else:
            response = {
                "code": -1005,
                "message": "未查询到数据"
            }

    except Exception as e:
        print("这是错误信息")
        response = {
            "code": -1006,
            "message": f"数据库操作出错{e}"
        }
    return response
