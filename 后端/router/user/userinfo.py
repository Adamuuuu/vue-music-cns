from flask import  Blueprint,request
from model.user.user import UserInfo
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import hashlib
from model import db
from sqlalchemy import or_
user_bp=Blueprint("user",__name__,url_prefix="/v1")
# 查询所有用户
@user_bp.route('/all/user',methods=['GET'])
def queryAllUsersInfo():
    user_all=UserInfo.query.all()
    data = []

    for user in user_all:
        data.append(user.to_json())

    print(data)

    response = {
        "code": 0,
        "message": "查询成功",
        "data": data
    }

    return response

# 查询特定信息的用户
@user_bp.route("/query", methods=["POST"])
def query_users():
    data = request.get_json()
    query = UserInfo.query

    if "UserID" in data:
        query = query.filter(UserInfo.UserID == data["UserID"])
    if "Nickname" in data:
        query = query.filter(UserInfo.Nickname == data["Nickname"])
    if "Account" in data:
        query = query.filter(UserInfo.Account == data["Account"])
    if "Gender" in data:
        query = query.filter(UserInfo.Gender == data["Gender"])
    if "Province" in data:
        query = query.filter(UserInfo.Province == data["Province"])
    if "City" in data:
        query = query.filter(UserInfo.City == data["City"])

    users = query.all()
    data = [user.to_json() for user in users]
    response = {
        "code": 0,
        "message": "查询成功",
        "data": data
    }
    return response

# 搜索功能（输出的关键字可能是用户名，也可能是账号）
@user_bp.route('/some/user',methods=['POST'])
def searchUserInfo():
    data = request.get_json()

    query=UserInfo.query
    if "Keyword" in data:
        query = query.filter(or_(UserInfo.Nickname.like(f"%{data['Keyword']}%"), UserInfo.Account.like(f"%{data['Keyword']}%")))

    users = query.all()
    data = [user.to_json() for user in users]
    response = {
        "code": 0,
        "message": "搜索成功",
        "data": data
    }
    return response


# 新增用户
@user_bp.route('/user', methods=['POST'])
def createUserInfo():
    data = request.json
    print(data['Nickname'])

    try:
        user = UserInfo(
            Nickname=data['Nickname'],
            Account=data['Account'],
            Password=data['Password'],
            # RegistrationTime=str(data['RegistrationTime']),
            Avatar=data['Avatar'],
            Gender=data['Gender'],
            Province=data['Province'],
            City=data['City'],
            Introduction=data['Introduction'],
            Level=data['Level']
        )
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        print("发生了如下错误: %s", e)

    return '获取新增用户信息成功'

# 修改用户信息
@user_bp.route('/user', methods=['PATCH'])
def updateUserInfo():
    data = request.json

    try:
        user = UserInfo.query.get(data['UserID'])

        if user:
            # 更新用户信息
            user.Nickname = data.get('Nickname', user.Nickname)
            user.Password = data.get('Password', user.Password)
            user.Gender = data.get('Gender', user.Gender)
            user.Province = data.get('Province', user.Province)
            user.City = data.get('City', user.City)
            user.Introduction = data.get('Introduction', user.Introduction)
            user.Level = data.get('Level', user.Level)

            db.session.commit()
            return '更新用户信息成功'
        else:
            return '找不到指定的用户'

    except Exception as e:
        print("发生了如下错误: %s", e)
        return '更新用户信息失败'

# 删除用户信息
@user_bp.route('/user', methods=['DELETE'])
def deleteUserInfo():
    data = request.json

    try:
        user = UserInfo.query.get(data['user_id'])

        if user:
            db.session.delete(user)
            db.session.commit()
            return '删除用户信息成功'
        else:
            return '找不到指定的用户'

    except Exception as e:
        print("发生了如下错误: %s", e)
        return '删除用户信息失败'


def existing_user(username):
    existing_name=UserInfo.query.filter_by(Account=username).first()
    if existing_name:
        return True
    else:
        return False

# 使用md5对密码进行加密
def encrypt_password(password):
    # 创建MD5对象
    md5 = hashlib.md5()

    # 将密码转换为字节流并进行哈希计算
    md5.update(password.encode('utf-8'))

    # 获取加密后的密码摘要
    encrypted_password = md5.hexdigest()

    return encrypted_password


# 生成公钥私钥并将其序列化
private_key=rsa.generate_private_key(
    public_exponent=65537,
    key_size=1024
)
public_key = private_key.public_key()

# 注册
@user_bp.route('/register',methods=['POST'])
def register():
    username=request.json.get('username')
    password=request.json.get('password')


    # 加密密码


    #保存用户名和密码到数据库
    encrypted_password = encrypt_password(password)
    is_name = existing_user(username)


    if is_name:  # 如果已存在相同用户名的用户

        response = {
            "code":-1001,
            "message":'注册失败，用户名重复',
            "data":[]
        }
        return response


    try:
        user = UserInfo(
            Account=username,
            Password=encrypted_password
        )
        print(user)
        db.session.add(user)
        db.session.commit()

        response = {
            "code": 0,
            "message": '注册成功',
            "data": []
        }
        return response

    except Exception as e:
        print("有报错",e)
        response = {
            "code": -1002,
            "message": '注册失败',
            "data": []
        }
        return response


@user_bp.route('/login',methods=['POST'])
def login():
    username=request.json.get('username')
    password=request.json.get('password')
    is_name=existing_user(username)

    if is_name == False:
        response={
            "code":-1003,
            "message":"用户名不存在",
            "data":[]
        }
        return response
    else:
        decrypted_user=UserInfo.query.filter_by(Account=username).first()

        decrypted_password=encrypt_password(password)
        id=decrypted_user.UserID

        if decrypted_password==decrypted_user.Password:
            print(id)
            token = jwt.encode({'username': username},private_key, algorithm='RS256')
            print(token)
            response = {
                "code":0,
                "message":"登陆成功",
                "data":[
                    {
                        "id":id,
                        "name":username,
                        "token":token
                    }
                ]
            }

        return response

# 用户菜单
@user_bp.route('menu',methods=['GET'])
def getMune():
    data=[{"name": "管理总览",
                "type": 1,
                "url": "/main/home",
                "icon": "el-icon-monitor",

                "children": [
                    {
                        "id":1,

                        "url": "/main/home/user",
                        "icon": "",
                        "name": "用户管理",
                        "type": 2,
                        "children": {},

                    },
                    {
                        "id":2,

                        "url": "/main/home/song",
                        "icon": "",
                        "name": "歌曲管理",
                        "type": 2,
                        "children": {},

                    },
                    {
                        "id": 3,

                        "url": "/main/home/playlist",
                        "icon": "",
                        "name": "歌单管理",
                        "type": 2,
                        "children": {},

                    },
                    {
                        "id": 4,

                        "url": "/main/home/album",
                        "icon": "",
                        "name": "专辑管理",
                        "type": 2,
                        "children": {},

                    },
                    {
                        "id": 5,
                        "url": "/main/home/artist",
                        "icon": "",
                        "name": "歌手管理",
                        "type": 2,
                        "children": {},
                    },

                ]
            },]
    response={
        "code":0,
        "message":"获取成功",
        "data":data
    }
    return response






@user_bp.route("/verify", methods=['GET'])
# 验证token
def verify_token():
    authorization_header = request.headers.get('Authorization')  # 获取请求头中的Authorization标头
    if authorization_header:
        token = authorization_header.split('Bearer ')[1]  # 剥离Bearer前缀获取令牌
    print("这是token",token)


    try:
        decoded_token = jwt.decode(token, public_key, algorithms='RS256')  # 解码和验证JWT令牌
        print("这是解密后的token",decoded_token)
        return decoded_token  # 返回解码后的令牌数据
    except Exception as  e:
        print(e)
        return "Invalid token"  # 令牌无效
