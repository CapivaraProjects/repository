import os
import cv2
import six
import uuid
import base64
import datetime
import numpy as np
from sqlalchemy import and_
from google.cloud import storage
from werkzeug import secure_filename

from database.Image import Image as ImageDB
from models.Image import Image
from models.Disease import Disease
from models.Plant import Plant
from repository.base import Base


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

    def _get_storage_client(self, json_file):
        """
        Get storage client

        Args:
            json_file: JSON authorization file

        Returns:
            A storage client
        """
        return storage.Client.from_service_account_json(json_file)

    def _safe_filename(self, filename):
        """
        Generates a safe filename

        Args:
            filename: Image filename

        Returns:
            A filename
        """
        filename = secure_filename(filename)
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
        basename, extension = filename.rsplit('.', 1)
        return "{0}-{1}.{2}".format(basename, date, extension)

    def upload_file(
            self,
            file_stream,
            filename,
            json_file,
            storage_bucket):
        """
        Upload file to storage cloud

        Args:
            file_stream: file stram binary
            filename: filename
            content_type: content type
            json_file: JSON authorization file
            storage_bucket: Storage bucket

        Returns:
            A url
        """
        filename = self._safe_filename(filename)
        client = self._get_storage_client(json_file)
        bucket = client.bucket(storage_bucket)
        blob = bucket.blob(filename)

        blob.upload_from_string(
            file_stream,
            content_type='image/jpeg')

        url = blob.public_url

        if isinstance(url, six.binary_type):
            url = url.encode('utf-8')

        return url

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
        if (not session.query(ImageDB).filter_by(id=imageDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, image=Image(), pageSize=10, offset=0):
        """
        (Image, pageSize, offset) -> [Image]
        """
        session = self.session_factory()
        query = session.query(ImageDB).filter(
                and_(
                    ImageDB.url.like('%'+image.url+'%'),
                    ImageDB.description.like('%'+image.description+'%'),
                    ImageDB.source.like('%'+image.source+'%')))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        images = []
        for imageDB in content:
            images.append(Image(
                     imageDB.id,
                     Disease(imageDB.disease.id,
                             Plant(imageDB.disease.plant.id,
                                   imageDB.disease.plant.scientificName,
                                   imageDB.disease.plant.commonName),
                             imageDB.disease.scientificName,
                             imageDB.disease.commonName),
                     imageDB.url,
                     imageDB.description,
                     imageDB.source,
                     imageDB.size))
        return {'total': total, 'content': images}

    def searchByID(self, id):
        """
        (Int) -> (Image)
        Method used to get image object by ID
        """
        session = self.session_factory()
        imageDB = session.query(ImageDB).get(id)
        if (imageDB is None):
            raise Exception("Image not found!")
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

    def getImageBase64(self, image=Image(), imagesDir=""):
        """
        (Image, String) -> (Image)
        Method used to get image considering plant common name,
        disease scientific name, size image and url and
        convert it to base64 in url field
        """
        size = "large"
        if image.size == 1:
            size = "thumb"
        elif image.size == 2:
            size = "medium"
        elif image.size == 3:
            size = "large"
        filepath = "{}/{}/{}/{}/{}".format(
             imagesDir,
             size,
             image.disease.plant.commonName.replace(
                 ' ',
                 '_').replace(
                     '(',
                     '_').replace(
                         ')',
                         '_'),
             image.disease.scientificName.replace(
                 " ",
                 "_").replace(
                     ";",
                     "").replace(
                         "(",
                         "_").replace(
                             ")",
                             "_").replace(
                                 "<i>",
                                 "").replace(
                                     "</i>",
                                     ""),
             image.url)
        fh = open(filepath, 'rb')
        content = fh.read()
        fh.close()

        image.url = base64.encodestring(content).decode('utf-8')
        return image

    def saveImage(self, image=Image(), imagesDir="", extension=".JPG"):
        """
        (Image, str, str) -> (Image)
            Method used to save images considering image url field
        """
        size = "large"
        if image.size == 1:
            size = "thumb"
        elif image.size == 2:
            size = "medium"
        elif image.size == 3:
            size = "large"
        filename = str(uuid.uuid4())
        filepath = "{}/{}/{}/{}/{}".format(
             imagesDir,
             size,
             image.disease.plant.commonName.replace(
                 ' ',
                 '_').replace(
                     '(',
                     '_').replace(
                         ')',
                         '_'),
             image.disease.scientificName.replace(
                 " ",
                 "_").replace(
                     ";",
                     "").replace(
                         "(",
                         "_").replace(
                             ")",
                             "_").replace(
                                 "<i>",
                                 "").replace(
                                     "</i>",
                                     ""),
             filename + extension)

        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except Exception as exc:
                raise exc

        nparr = np.fromstring(base64.b64decode(image.url), np.uint8)
        cv2.imwrite(filepath, cv2.imdecode(nparr, cv2.IMREAD_COLOR))

        image.url = filepath

        return image
