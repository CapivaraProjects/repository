from database.User import User as UserDB
from models.User import User
from models.Type import Type
from repository.base import Base
from sqlalchemy import or_

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
                    userDB.email,
                    userDB.username,
                    userDB.password,
                    userDB.salt,
                    Type(userDB.type.id,
                        userDB.type.value,
                        userDB.type.description),
                    userDB.date_insertion,
                    userDB.update)

    def update(self, user=User()):
        """
        (User) -> (User)
        """
        session = self.session_factory()
        userDB = session.query(UserDB).filter_by(id=user.id).first()
        dic = {}
        if (userDB.type.id != user.type.id):
            dic['idType'] = user.type.id
        if (userDB.email != user.email):
            dic['email'] = user.email
        if (userDB.username != user.username):
            dic['username'] = user.username
        if (userDB.password != user.password):
            dic['password'] = user.password
        if (userDB.salt != user.salt):
            dic['salt'] = user.salt
        if (userDB.date_insertion != user.date_insertion):
            dic['date_insertion'] = user.date_insertion
        if (userDB.date_update != user.date_update):
            dic['date_update'] = user.date_update
        if (dic != {}):
            session.query(UserDB).filter_by(id=user.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(userDB)
        return User(userDB.id,
                    userDB.email,
                    userDB.username,
                    userDB.password,
                    userDB.salt,
                    Type(userDB.type.id,
                        userDB.type.value,
                        userDB.type.description),
                    userDB.date_insertion,
                    userDB.update)

    def delete(self, user=User()):
        """
        (Type) -> (Boolean)
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
        query = session.query(UserDB).filter(or_(
                        userDB.email.like('%'+user.email+'%'),
                        userDB.username.like('%'+user.username+'%'),
                        userDB.date_insertion == user.date_insertion,
                        userDB.date_update == user.date_update))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        dic = {'total': total, 'content': content}
        return dic

    def searchByID(self, id):
        """
        (Int) -> (User)
        """
        session = self.session_factory()
        userDB = session.query(UserDB).get(id)
        return User(userDB.id,
                    Type(userDB.type.id,
                        userDB.type.value,
                        userDB.type.description),
                    userDB.scientificName,
                    userDB.commonName)
