from database.Type import Type as TypeDB
from models.Type import Type
from repository.base import Base
from sqlalchemy import and_


class TypeRepository(Base):
    """
    Type repository, dedicated to realize all functions related to types,
    including CRUD, and other things.
    """
    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, type=Type()):
        """
        (Type) -> (Type)
        Add type to database
        """
        typeDB = TypeDB(type=type)
        session = self.session_factory()
        session.add(typeDB)
        session.flush()
        session.refresh(typeDB)
        session.commit()
        return Type(typeDB.id, typeDB.value, typeDB.description)

    def update(self, type=Type()):
        """
        (Type) -> (Type)
        Update database type
        """
        session = self.session_factory()
        typeDB = session.query(TypeDB).filter_by(id=type.id).first()
        dic = {}
        if (typeDB.value != type.value):
            dic['value'] = type.value
        if (typeDB.description != type.description):
            dic['description'] = type.description
        if (dic != {}):
            session.query(TypeDB).filter_by(id=type.id).update(dic)
        session.commit()
        session.flush()
        session.refresh(typeDB)

        return Type(typeDB.id, typeDB.value, typeDB.description)

    def delete(self, type=Type()):
        """
                (Type) -> (bool)
                 Delete database type
        """
        status = False
        session = self.session_factory()
        typeDB = session.query(TypeDB).filter_by(id=type.id).first()
        session.delete(typeDB)
        session.commit()
        session.flush()
        if (not session.query(TypeDB).filter_by(id=typeDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, type=Type(), pageSize=10, offset=0):
        """
        (Type, pageSize, offset) -> [Type]
        """
        session = self.session_factory()
        query = session.query(TypeDB).filter(and_(
            TypeDB.value.like('%'+type.value+'%'),
            TypeDB.description.like('%'+type.description+'%')))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        types = []
        for typeDB in content:
            types.append(Type(
                typeDB.id,
                typeDB.value,
                typeDB.description))
        return {'total': total, 'content': types}

    def searchByID(self, typeId):
        """
        (Int) -> (Type)
        """
        session = self.session_factory()
        typeDB = session.query(TypeDB).get(typeId)
        return Type(typeDB.id,
                    typeDB.value,
                    typeDB.description)
