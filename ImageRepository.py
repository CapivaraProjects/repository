from database.Image import Image as ImageDB
from models.Image import Image
from models.Disease import Disease
from models.Plant import Plant
from repository.base import Base
from sqlalchemy import or_


class ImageRepository(Base):
    """
    Image repository, dedicated to realize all functions related to images,
        including CRUD, and other things.
    """

    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, image=Image()):
        """
        (Image) -> (Image)
        Add image to database
        """
        imageDB = ImageDB(image=image)
        session = self.session_factory()
        session.add(imageDB)
        session.flush()
        session.refresh(imageDB)
        session.commit()
        return Image(imageDB.id,
                     Disease(imageDB.disease.id,
                             Plant(imageDB.disease.plant.id,
                                   imageDB.disease.plant.scientificName,
                                   imageDB.disease.plant.commonName),
                             imageDB.disease.scientificName,
                             imageDB.disease.commonName),
                     imageDB.url,
                     imageDB.description,
                     imageDB.source,
                     imageDB.size)

    def update(self, image=Image()):
        """
        (Image) -> (Image)
        Update database image
        """
        session = self.session_factory()
        imageDB = session.query(ImageDB).filter_by(id=image.id).first()
        dic = {}
        if (imageDB.disease.id != image.disease.id):
            dic['idDisease'] = image.disease.id
        if (imageDB.url != image.url):
            dic['url'] = image.url
        if (imageDB.description != image.description):
            dic['description'] = image.description
        if (imageDB.source != image.source):
            dic['source'] = image.source
        if (imageDB.size != image.size):
            dic['size'] = image.size
        if (dic != {}):
            session.query(ImageDB).filter_by(id=image.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(imageDB)

        return Image(imageDB.id,
                     Disease(imageDB.disease.id,
                             Plant(imageDB.disease.plant.id,
                                   imageDB.disease.plant.scientificName,
                                   imageDB.disease.plant.commonName),
                             imageDB.disease.scientificName,
                             imageDB.disease.commonName),
                     imageDB.url,
                     imageDB.description,
                     imageDB.source,
                     imageDB.size)

    def delete(self, image=Image()):
        """
        (Image) -> (bool)
        Delete database image
        """
        status = False
        session = self.session_factory()
        imageDB = session.query(ImageDB).filter_by(id=image.id).first()
        session.delete(imageDB)
        session.commit()
        session.flush()
        if (not session.query(ImageDB).filter_by(url=imageDB.url).count()):
            status = True
        session.close()
        return status

    def search(self, image=Image(), pageSize=10, offset=0):
        """
        (Image, pageSize, offset) -> [Image]
        """
        session = self.session_factory()
        return session.query(ImageDB).filter(or_(
                ImageDB.url.like('%'+image.url+'%'),
                ImageDB.description == image.description,
                ImageDB.source == image.source)).slice(offset, pageSize).all()
