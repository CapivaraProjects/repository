from database.Disease import Disease as DiseaseDB
from models.Disease import Disease
from models.Plant import Plant
from repository.base import Base
from sqlalchemy import or_


class DiseaseRepository(Base):
    """
    Disease repository, dedicated to realize all functions related to diseases.
    """

    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, disease=Disease()):
        """
        (Disease) -> (Disease)
        """
        diseaseDB = DiseaseDB(disease=disease)
        session = self.session_factory()
        session.add(diseaseDB)
        session.flush()
        session.refresh(diseaseDB)
        session.commit()
        return Disease(diseaseDB.id,
                       Plant(diseaseDB.plant.id,
                             diseaseDB.plant.scientificName,
                             diseaseDB.plant.commonName),
                       diseaseDB.scientificName,
                       diseaseDB.commonName)

    def update(self, disease=Disease()):
        """
        (Disease) -> (Disease)
        """
        session = self.session_factory()
        diseaseDB = session.query(DiseaseDB).filter_by(id=disease.id).first()
        dic = {}
        if (diseaseDB.plant.id != disease.plant.id):
            dic['idPlant'] = disease.plant.id
        if (diseaseDB.scientificName != disease.scientificName):
            dic['scientificName'] = disease.scientificName
        if (diseaseDB.commonName != disease.commonName):
            dic['commonName'] = disease.commonName
        if (dic != {}):
            session.query(DiseaseDB).filter_by(id=disease.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(diseaseDB)
        return Disease(diseaseDB.id,
                       Plant(diseaseDB.plant.id,
                             diseaseDB.plant.scientificName,
                             diseaseDB.plant.commonName),
                       diseaseDB.scientificName,
                       diseaseDB.commonName)

    def delete(self, disease=Disease()):
        """
        (Plant) -> (Boolean)
        """
        status = False
        session = self.session_factory()
        diseaseDB = session.query(DiseaseDB).filter_by(id=disease.id).first()
        session.delete(diseaseDB)
        session.commit()
        session.flush()
        if (not session.query(DiseaseDB).filter_by(id=diseaseDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, disease=Disease(), pageSize=10, offset=0):
        """
        (Disease, pageSize, offset) -> {'total': int, 'content':[Disease]}
        """
        session = self.session_factory()
        query = session.query(DiseaseDB).filter(or_(
                        DiseaseDB.scientificName.like(
                            '%'+disease.scientificName+'%'),
                        DiseaseDB.commonName == disease.commonName))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        diseases = []
        for diseaseDB in content:
            diseases.append(Disease(
                       diseaseDB.id,
                       Plant(diseaseDB.plant.id,
                             diseaseDB.plant.scientificName,
                             diseaseDB.plant.commonName),
                       diseaseDB.scientificName,
                       diseaseDB.commonName))
        dic = {'total': total, 'content': diseases}
        return dic

    def searchByID(self, id):
        """
        (Int) -> (Disease)
        """
        session = self.session_factory()
        diseaseDB = session.query(DiseaseDB).get(id)
        return Disease(diseaseDB.id,
                       Plant(diseaseDB.plant.id,
                             diseaseDB.plant.scientificName,
                             diseaseDB.plant.commonName),
                       diseaseDB.scientificName,
                       diseaseDB.commonName)
