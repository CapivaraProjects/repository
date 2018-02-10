from database.Type import Type as TypeDB
from models.Type import Type
from repository.base import Base
from sqlalchemy import or_


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

	"""
        (Type) -> (Type)
         Add type to database
        """
	def create(self, type=Type()):
		typeDB = TypeDB(type=type)
		session = self.session_factory()
		session.add(typeDB)
		session.flush()
		session.refresh(typeDB)
		session.commit()
		return Type(typeDB.id, typeDB.value, typeDB.description)


	"""
                (Type) -> (Type)
                 Update database type
        """

	def update(self, type=Type()):
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


	"""
                (Type) -> (bool)
                 Delete database type
	"""

	def delete(self, type=Type()):
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


	"""
		(Type, pageSize, offset) -> [Type]
	"""

	def search(self, type=Type(), pageSize=10, offset=0):
		session = self.session_factory()
		return session.query(TypeDB).filter(or_(
		TypeDB.value == type.value,
		TypeDB.description == type.description)).slice(offset, pageSize).all()
