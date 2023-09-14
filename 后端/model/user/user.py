from model import db
import datetime
# 用户实体
class UserInfo(db.Model):
    __tablename__ = "user"

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nickname = db.Column(db.String(50), nullable=False)
    Account = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    RegistrationTime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    Avatar = db.Column(db.String(100))
    Gender = db.Column(db.Enum('Male', 'Female'))
    Province = db.Column(db.String(50))
    City = db.Column(db.String(50))
    Introduction = db.Column(db.Text)
    Level = db.Column(db.Integer, default=1)

    def to_json(self):
        return {
            "UserID": self.UserID,
            "Nickname": self.Nickname,
            "Account": self.Account,
            "Password": self.Password,
            "RegistrationTime": str(self.RegistrationTime),
            "Avatar": self.Avatar,
            "Gender": self.Gender,
            "Province": self.Province,
            "City": self.City,
            "Introduction": self.Introduction,
            "Level": self.Level
        }
