from database.Text import Text as TextDB
from models.Text import Text
from repository.base import Base
from sqlalchemy import or_
import base64
import uuid

class TextRepository(Base):
    """
    Text repository, dedicated to realize all functions related to text,
        including CRUD, and other things.
    """

    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, text=Text()):
        """
        (Image) -> (Image)
        Add image to database
        """
        textDB = TextDB(text=text)
        session = self.session_factory()
        session.add(textDB)
        session.flush()
        session.refresh(textDB)
        session.commit()
        return Text(textDB.id,
                    textDB.language,
                    textDB.tag,
                    textDB.value,
                    textDB.description)

    def update(self, text=Text()):
        """
        (Text) -> (Text)
        Update database text
        """
        session = self.session_factory()
        textDB = session.query(TextDB).filter_by(id=text.id).first()
        dic = {}
        if (textDB.language != text.language):
            dic['language'] = text.language
        if (textDB.tag != text.tag):
            dic['tag'] = text.tag
        if (textDB.value != text.value):
            dic['value'] = text.value
        if (textDB.description != text.description):
            dic['description'] = text.description
        if (dic != {}):
            session.query(TextDB).filter_by(id=text.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(textDB)

        return Text(textDB.id,
                    textDB.language,
                    textDB.tag,
                    textDB.value,
                    textDB.description)

    def delete(self, text=Text()):
        """
        (Text) -> (bool)
        Delete database text
        """
        status = False
        session = self.session_factory()
        textDB = session.query(TextDB).filter_by(id=text.id).first()
        session.delete(textDB)
        session.commit()
        session.flush()
        if (not session.query(TextDB).filter_by(value=textDB.value).count()):
            status = True
        session.close()
        return status

    def search(self, text=Text(), pageSize=10, offset=0):
        """
        (Text, pageSize, offset) -> [Text]
        """
        session = self.session_factory()
        return session.query(TextDB).filter(or_(
                TextDB.language.like('%'+text.language+'%'),
                TextDB.tag.like('%'+text.tag+'%'),
                TextDB.value.like('%'+text.value+'%'),
                TextDB.description.like('%'+text.description+'%'))).slice(offset, pageSize).all()
