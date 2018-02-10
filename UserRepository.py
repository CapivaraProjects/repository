from database.User import User as UserDB
from models.User import User
from repository.base import Base
from sqlalchemy import and_
from tools.Cryptography import Crypto


class UserRepository(Base):
    """
    User repository, dedicated to realize all functions related to users.
    """

    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, user=User()):
        """
        (User) -> (User)
        """
        userDB = UserDB(user=user)
        session = self.session_factory()
        session.add(userDB)
        session.flush()
        session.refresh(userDB)
        session.commit()
        return User(userDB.id,
                    userDB.idType,
                    userDB.email,
                    userDB.username,
                    userDB.password,
                    userDB.salt,
                    userDB.dateInsertion,
                    userDB.dateUpdate)

    def update(self, user=User()):
        """
        (User) -> (User)
        """
        session = self.session_factory()
        userDB = session.query(UserDB).filter_by(id=user.id).first()
        dic = {}
        if (userDB.idType != user.idType):
            dic['idType'] = user.idType
        if (userDB.email != user.email):
            dic['email'] = user.email
        if (userDB.username != user.username):
            dic['username'] = user.username
        if (userDB.password != user.password):
            dic['password'] = user.password
        if (userDB.salt != user.salt):
            dic['salt'] = user.salt
        if (userDB.dateInsertion != user.dateInsertion):
            dic['dateInsertion'] = user.dateInsertion
        if (userDB.dateUpdate != user.dateUpdate):
            dic['dateUpdate'] = user.dateUpdate
        if (dic != {}):
            session.query(UserDB).filter_by(id=user.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(userDB)
        return User(userDB.id,
                    userDB.idType,
                    userDB.email,
                    userDB.username,
                    userDB.password,
                    userDB.salt,
                    userDB.dateInsertion,
                    userDB.dateUpdate)

    def delete(self, user=User()):
        """
        (User) -> (Boolean)
        """
        status = False
        session = self.session_factory()
        userDB = session.query(UserDB).filter_by(id=user.id).first()
        session.delete(userDB)
        session.commit()
        session.flush()
        if (not session.query(UserDB).filter_by(id=userDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, user=User(), pageSize=10, offset=0):
        """
        (User, pageSize, offset) -> {'total': int, 'content':[User]}
        """
        session = self.session_factory()
        query = session.query(UserDB).filter(and_(
                        UserDB.email.like('%'+user.email+'%'),
                        UserDB.username.like('%'+user.username+'%'),
                        UserDB.dateInsertion.like('%'+user.dateInsertion+'%'),
                        UserDB.dateUpdate.like('%'+user.dateUpdate+'%')))
        content = query.slice(offset, pageSize).all()
        users = []
        for userDB in content:
            users.append(User(
                    userDB.id,
                    userDB.idType,
                    userDB.email,
                    userDB.username,
                    userDB.password,
                    userDB.salt,
                    userDB.dateInsertion,
                    userDB.dateUpdate))
        total = query.count()
        dic = {'total': total, 'content': users}
        return dic

    def searchByID(self, id):
        """
        (Int) -> (User)
        """
        session = self.session_factory()
        userDB = session.query(UserDB).get(id)
        return User(userDB.id,
                    userDB.idType,
                    userDB.email,
                    userDB.username,
                    userDB.password,
                    userDB.salt,
                    userDB.dateInsertion,
                    userDB.dateUpdate)

    def authentication(self, user=User()):
        """
        (User) -> (User)
        """
        session = self.session_factory()
        userDB = session.query(UserDB).filter_by(
                username=user.username).first()
        crypto = Crypto()
        decriptedTest = crypto.decrypt(userDB.salt, userDB.password)
        decriptedUser = crypto.decrypt(userDB.salt, user.password)

        if (decriptedTest == decriptedUser):
            return User(userDB.id,
                        userDB.idType,
                        userDB.email,
                        userDB.username,
                        userDB.password,
                        userDB.salt,
                        userDB.dateInsertion,
                        userDB.dateUpdate)
        else:
            return User()
