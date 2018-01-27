from database.Plant import Plant as PlantDB
from models.Plant import Plant
from repository.base import Base
from sqlalchemy import or_

class PlantRepository(Base):
    """
    Plant repository, dedicated to realize all functions related to plants
    """
    def __init__(self,
                dbuser="",
                dbpass="",
                dbhost="",
                port="",
                dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, plant=Plant()):
        """
        (Plant) -> (Plant)
        """
        plantDB = PlantDB(plant=plant)
        session = self.session_factory()
        session.add(plantDB)
        session.flush()
        session.refresh(plantDB)
        session.commit()
        return Plant(plantDB.id,
                    plantDB.scientificName,
                    plantDB.commonName)

    def update(self, plant=Plant()):
        """
        (Plant) -> (Plant)
        """
        session = self.session_factory()
        plantDB = session.query(PlantDB).filter_by(id=plant.id).first()
        dic = {}
        if (plantDB.scientificName != plant.scientificName):
            dic['scientificName'] = plant.scientificName
        if (plantDB.commonName != plant.commonName):
            dic['commonName'] = plant.commonName
        if (dic != {}):
            session.query(PlantDB).filter_by(id=plant.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(plantDB)
            
        return Plant(plantDB.id,
                    plantDB.scientificName,
                    plantDB.commonName)

    def delete(self, plant=Plant()):
        """
        (Plant) -> (Boolean)
        """
        status = False
        session = self.session_factory()
        plantDB = session.query(PlantDB).filter_by(id=plant.id).first()
        session.delete(plantDB)
        session.commit()
        session.flush()
        if (not session.query(PlantDB).filter_by(id=plantDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, plant=Plant(), pageSize=10, offset=0):
        """
        (Plant, pageSize, offset) -> {'total': int, 'content':[Plant]}
        """
        session = self.session_factory()
        query = session.query(PlantDB).filter(or_(
                        PlantDB.scientificName.like('%'+plant.scientificName+'%'),
                        PlantDB.commonName == plant.commonName))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        dic = {'total': total, 'content': content}
        return dic

    def searchByID(self, plantId):
        """
        (Int) -> (Plant)
        """
        session = self.session_factory()
        plantDB = session.query(PlantDB).get(plantId)
        return Plant(plantDB.id,
                    plantDB.scientificName,
                    plantDB.commonName)
