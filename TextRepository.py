from database.Text import Text as TextDB
from models.Text import Text
from repository.base import Base
from sqlalchemy import and_


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
                    textDB.plant,
                    textDB.status,
                    textDB.attribute,
                    textDB.value,
                    textDB.reference)

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
        if (textDB.plant != text.plant):
            dic['plant'] = text.plant
        if (textDB.status != text.status):
            dic['status'] = text.status
        if (textDB.attribute != text.attribute):
            dic['attribute'] = text.attribute
        if (textDB.value != text.value):
            dic['value'] = text.value
        if (textDB.reference != text.reference):
            dic['reference'] = text.reference
        if (dic != {}):
            session.query(TextDB).filter_by(id=text.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(textDB)

        return Text(textDB.id,
                    textDB.language,
                    textDB.plant,
                    textDB.status,
                    textDB.attribute,
                    textDB.value,
                    textDB.reference)

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
        if (not session.query(TextDB).filter_by(id=textDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, text=Text(), pageSize=10, offset=0):
        """
        (Text, pageSize, offset) -> [Text]
        """
        session = self.session_factory()
        query = session.query(TextDB).filter(and_(
                TextDB.language.like('%'+text.language+'%'),
                TextDB.plant.like('%'+text.plant+'%'),
                TextDB.status.like('%'+text.status+'%'),
                TextDB.attribute.like('%'+text.attribute+'%'),
                TextDB.value.like('%'+text.value+'%'),
                TextDB.reference.like('%'+text.reference+'%')))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        texts = []
        for textDB in content:
            texts.append(Text(
                    textDB.id,
                    textDB.language,
                    textDB.plant,
                    textDB.status,
                    textDB.attribute,
                    textDB.value,
                    textDB.reference))
        return {'total': total, 'content': texts}


    def searchByID(self, textId):
        """
        (Int) -> (Text)
        """
        session = self.session_factory()
        textDB = session.query(TextDB).get(textId)
        return Text(textDB.id,
                    textDB.language,
                    textDB.plant,
                    textDB.status,
                    textDB.attribute,
                    textDB.value,
                    textDB.reference)
