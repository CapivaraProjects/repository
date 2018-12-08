from database.Classifier import Classifier as ClassifierDB
from models.Classifier import Classifier
from models.Plant import Plant
from repository.base import Base
from sqlalchemy import and_


class ClassifierRepository(Base):
    """
    Classifier repository, dedicated to realize all functions related to classifiers.
    """

    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, classifier=Classifier()):
        """
        (Classifier) -> (Classifier)
        """
        classifierDB = ClassifierDB(classifier=classifier)
        session = self.session_factory()
        session.add(classifierDB)
        session.flush()
        session.refresh(classifierDB)
        session.commit()
        return Classifier(classifierDB.id,
                       Plant(classifierDB.plant.id,
                             classifierDB.plant.scientificName,
                             classifierDB.plant.commonName),
                       classifierDB.tag,
                       classifierDB.path)

    def update(self, classifier=Classifier()):
        """
        (Classifier) -> (Classifier)
        """
        session = self.session_factory()
        classifierDB = session.query(ClassifierDB).filter_by(id=classifier.id).first()
        dic = {}
        if (classifierDB.plant.id != classifier.plant.id):
            dic['idPlant'] = classifier.plant.id
        if (classifierDB.tag != classifier.tag):
            dic['tag'] = classifier.tag
        if (classifierDB.path != classifier.path):
            dic['path'] = classifier.path
        if (dic != {}):
            session.query(ClassifierDB).filter_by(id=classifier.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(classifierDB)
        return Classifier(classifierDB.id,
                       Plant(classifierDB.plant.id,
                             classifierDB.plant.scientificName,
                             classifierDB.plant.commonName),
                       classifierDB.tag,
                       classifierDB.path)

    def delete(self, classifier=Classifier()):
        """
        (Plant) -> (Boolean)
        """
        status = False
        session = self.session_factory()
        classifierDB = session.query(ClassifierDB).filter_by(id=classifier.id).first()
        session.delete(classifierDB)
        session.commit()
        session.flush()
        if (not session.query(ClassifierDB).filter_by(id=classifierDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, classifier=Classifier(), pageSize=10, offset=0):
        """
        (Classifier, pageSize, offset) -> {'total': int, 'content':[Classifier]}
        """
        session = self.session_factory()
        query = session.query(ClassifierDB).filter(and_(
                        ClassifierDB.tag.like(
                            '%'+classifier.tag+'%'),
                        ClassifierDB.path.like('%'+classifier.path+'%')))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        classifiers = []
        for classifierDB in content:
            classifiers.append(Classifier(
                       classifierDB.id,
                       Plant(classifierDB.plant.id,
                             classifierDB.plant.scientificName,
                             classifierDB.plant.commonName),
                       classifierDB.tag,
                       classifierDB.path))
        dic = {'total': total, 'content': classifiers}
        return dic

    def searchByID(self, id):
        """
        (Int) -> (Classifier)
        """
        session = self.session_factory()
        classifierDB = session.query(ClassifierDB).get(id)
        return Classifier(classifierDB.id,
                       Plant(classifierDB.plant.id,
                             classifierDB.plant.scientificName,
                             classifierDB.plant.commonName),
                       classifierDB.tag,
                       classifierDB.path)
