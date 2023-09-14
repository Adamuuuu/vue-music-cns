from flask import Blueprint, request
from model.song.song import SongInfo,AlbumInfo,ArtistInfo,ArtistSong,PlaylistSong,PlaylistInfo
from model import db
from sqlalchemy import or_

album_bp = Blueprint("album", __name__, url_prefix="/v1")

# 查询所有歌曲
# 查询所有专辑并分页
@album_bp.route('/all/album', methods=['GET'])
def queryAllAlbumInfo():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    album_all = AlbumInfo.query.paginate(page=page, per_page=per_page)
    total_pages = album_all.pages
    current_page = album_all.page
    albums = album_all.items



    data = [album.to_json() for album in albums]

    response = {
        "code": 0,
        "message": "查询成功",
        "data": data,
        "total_pages": total_pages,
        "current_page": current_page
    }

    return response


# 新增专辑信息
@album_bp.route('/album', methods=['POST'])
def createAlbumInfo():
    data = request.json

    album = AlbumInfo(
        AlbumID=data['AlbumID'],
        AlbumName=data['AlbumName'],
        CoverURL=data['CoverURL'],
        Artist=data['Artist'],
        ReleaseTime=data['ReleaseTime'],
        Introduction=data['Introduction']
    )
    db.session.add(album)
    db.session.commit()

    response = {
        "code": 0,
        "message": "新增专辑成功"
    }
    return response

# 搜索转接
@album_bp.route('/some/album',methods=['POST'])
def searchAlbumInfo():
    data=request.json
    if 'AlbumName' in data:
        album_data=AlbumInfo.query.filter(AlbumInfo.AlbumName==data['AlbumName'])
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        album_all = album_data.paginate(page=page, per_page=per_page)
        total_pages = album_all.pages
        current_page = album_all.page
        albums = album_all.items

        data = [album.to_json() for album in albums]

        response = {
            "code": 0,
            "message": "查询成功",
            "data": data,
            "total_pages": total_pages,
            "current_page": current_page
        }

        return response


# 修改专辑信息
@album_bp.route('/album', methods=['PATCH'])
def updateAlbumInfo():
    data = request.json

    try:
        album = AlbumInfo.query.get(data['AlbumID'])

        if album:
            album.AlbumName = data.get('AlbumName', album.AlbumName)
            album.CoverURL = data.get('CoverURL', album.CoverURL)
            album.Artist = data.get('Artist', album.Artist)
            album.ReleaseTime = data.get('ReleaseTime', album.ReleaseTime)
            album.Introduction = data.get('Introduction', album.Introduction)

            db.session.commit()

            response = {
                "code": 0,
                "message": "修改专辑信息成功",
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


# 删除专辑
@album_bp.route('/album', methods=['DELETE'])
def deleteAlbumInfo():
    data = request.json

    try:
        album = AlbumInfo.query.filter(AlbumInfo.AlbumID == data['AlbumID']).first()

        if album is not None:
            db.session.delete(album)
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
