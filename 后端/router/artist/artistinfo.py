from flask import Blueprint, request
from model.song.song import SongInfo,AlbumInfo,ArtistInfo,ArtistSong,PlaylistSong,PlaylistInfo
from model import db
from sqlalchemy import or_

artist_bp = Blueprint("artist", __name__, url_prefix="/v1")

# 查询所有歌手
# 查询所有歌手并分页
@artist_bp.route('/all/artist', methods=['GET'])
def queryAllArtistsInfo():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    artist_all = ArtistInfo.query.paginate(page=page, per_page=per_page)
    total_pages = artist_all.pages
    current_page = artist_all.page
    artists = artist_all.items

    # adata = ArtistInfo.query.filter(ArtistInfo.ArtistName == '陈奕迅').first()
    # print(adata.ArtistID)



    data = [artist.to_json() for artist in artists]

    response = {
        "code": 0,
        "message": "查询成功",
        "data": data,
        "total_pages": total_pages,
        "current_page": current_page
    }

    return response
# 搜索歌手信息
@artist_bp.route("/some/artist",methods=['POST'])
def searchArtistInfo():
    data=request.json
    if "ArtistName" in  data:
        artist_data=ArtistInfo.query.filter(ArtistInfo.ArtistName==data['ArtistName'])
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        artist_all = artist_data.paginate(page=page, per_page=per_page)
        total_pages = artist_all.pages
        current_page = artist_all.page
        artists = artist_all.items

        # adata = ArtistInfo.query.filter(ArtistInfo.ArtistName == '陈奕迅').first()
        # print(adata.ArtistID)

        data = [artist.to_json() for artist in artists]

        response = {
            "code": 0,
            "message": "查询成功",
            "data": data,
            "total_pages": total_pages,
            "current_page": current_page
        }

        return response


# 新增歌手
@artist_bp.route('/artist', methods=['POST'])
def createArtistInfo():
    data = request.json

    artist = ArtistInfo(
        ArtistID=data['ArtistID'],
        ArtistName=data['ArtistName'],
        Avatar=data['Avatar'],
        # FansCount=data['FansCount'],
        Wiki=data['Wiki'],
        # ArtistID=artist_id,
        # AlbumID=album_id
    )
    db.session.add(artist)
    db.session.commit()



    db.session.commit()
    response = {
        "code": 0,
        "message": "新增歌手成功"
    }
    return response

# 修改歌手信息

@artist_bp.route('artist',methods=['PATCH'])
def updateArtist():
    data=request.json
    try:
        artist=ArtistInfo.query.get(data['ArtistID'])
        if artist:
            artist.ArtistName=data.get('ArtistName',artist.ArtistName)
            artist.Avatar=data.get('Avatar',artist.Avatar)
            artist.FansCount=data.get('FansCount',artist.FansCount)
            artist.Wiki=data.get('Wiki',artist.Wiki)

            db.session.commit()
            db.session.close()
            response={
                "code":0,
                "message":"修改歌手信息成功",
                "data":data
            }

        else:
            response={
                "code":-1005,
                "message":"未查询到数据"
            }

    except Exception as e:
        print("这是错误信息")
        response={
            "code":-1006,
            "message":f"数据库操作出错{e}"
        }
    return response

# 删除歌手
@artist_bp.route('/artist', methods=['DELETE'])
def deleteArtist():
    data = request.json

    try:
        artist = ArtistInfo.query.filter(ArtistInfo.ArtistID == data['ArtistID']).first()

        if artist is not None:
            db.session.delete(artist)
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

