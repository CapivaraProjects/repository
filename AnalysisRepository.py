from database.Analysis import Analysis as AnalysisDB
from models.Analysis import Analysis
from repository.base import Base
from sqlalchemy import and_

class AnalysisRepository(Base):
    
    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, analysis=Analysis()):
        """
        (Analysis) -> (Analysis)
        Add analysis to database
        """
        analysisDB = AnalysisDB(analysis=analysis)
        session = self.session_factory()
        session.add(analysisDB)
        session.flush()
        session.commit()
        session.refresh(analysisDB)
        return Analysis(analysisDB.id,
                    Image(analysisDB.image.id,
                        Disease(analysisDB.image.disease.id,
                            Plant(analysisDB.image.disease.plant.id,
                                analysisDB.image.disease.plant.scientificName,
                                analysisDB.image.disease.plant.commonName),
                            analysisDB.image.disease.scientificName,
                            analysisDB.image.disease.commonName),
                        analysisDB.image.url,
                        analysisDB.image.description,
                        analysisDB.image.source,
                        analysisDB.image.size),
                    Classifier(analysisDB.classifier.id,
                        Plant(analysisDB.classifier.plant.id,
                            analysisDB.classifier.plant.scientificName,
                            analysisDB.classifier.plant.commonName),
                        analysisDB.classifier.tag,
                        analysisDB.classifier.path))

    def update(self, analysis=Analysis()):
        """
        (Analysis) -> (Analysis)
        update analysis table
        """
        session = self.session_factory()
        analysisDB = session.query(AnalysisDB).filter_by(id=analysis.id).first()
        dic = {}
        if (analysisDB.image.id != analysis.image.id):
            dic['idImage'] = analysis.image.id
        if (analysisDB.classifier.id != analysis.classifier.id):
            dic['idClassifier'] = analysis.classifier.id
        if (dic != {}):
            session.query(AnalysisDB).filter_by(id=analysis.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(analysisDB)
        
        return Analysis(analysisDB.id,
                    Image(analysisDB.image.id,
                        Disease(analysisDB.image.disease.id,
                            Plant(analysisDB.image.disease.plant.id,
                                analysisDB.image.disease.plant.scientificName,
                                analysisDB.image.disease.plant.commonName),
                            analysisDB.image.disease.scientificName,
                            analysisDB.image.disease.commonName),
                        analysisDB.image.url,
                        analysisDB.image.description,
                        analysisDB.image.source,
                        analysisDB.image.size),
                    Classifier(analysisDB.classifier.id,
                        Plant(analysisDB.classifier.plant.id,
                            analysisDB.classifier.plant.scientificName,
                            analysisDB.classifier.plant.commonName),
                        analysisDB.classifier.tag,
                        analysisDB.classifier.path))

    def delete(self, analysis=Analysis()):
        """
        (Analysis) -> (bool)
        Delete analysis from database
        """
        status = False
        session = self.session_factory()
        analysisDB = session.query(AnalysisDB).filter_by(id=analysis.id).first()
        session.delete(analysisDB)
        session.flush()
        session.commit()
        if (not session.query(AnalysisDB).filter_by(id=analysisDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, analysis=Analysis(), pageSize=10, offset=0):
        """
        (Analysis, pageSize, offset) -> [Analysis]
        search by analysis
        """
        session = self.session_factory()
        query = session.query(AnalysisDB).filter(
                            and_(AnalysisDB.image.id == analysis.image.id,
                                AnalysisDB.classifier.id == analysis.classifier.id))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        analyzes = []
        for analysisDB in content:
            analyzes.append(Analysis(analysisDB.id,
                    Image(analysisDB.image.id,
                        Disease(analysisDB.image.disease.id,
                            Plant(analysisDB.image.disease.plant.id,
                                analysisDB.image.disease.plant.scientificName,
                                analysisDB.image.disease.plant.commonName),
                            analysisDB.image.disease.scientificName,
                            analysisDB.image.disease.commonName),
                        analysisDB.image.url,
                        analysisDB.image.description,
                        analysisDB.image.source,
                        analysisDB.image.size),
                    Classifier(analysisDB.classifier.id,
                        Plant(analysisDB.classifier.plant.id,
                            analysisDB.classifier.plant.scientificName,
                            analysisDB.classifier.plant.commonName),
                        analysisDB.classifier.tag,
                        analysisDB.classifier.path)))
    
        return {'total': total, 'content': analyzes}

    def searchByID(self, id):
        """
        (int) -> (Analysis)
        Search analysis by ID
        """
        session = self.session_factory()
        analysisDB = session.query(AnalysisDB).get(id)
        if (analysisDB is None):
            raise Exception("Analysis not found!")

        return Analysis(analysisDB.id,
                    Image(analysisDB.image.id,
                        Disease(analysisDB.image.disease.id,
                            Plant(analysisDB.image.disease.plant.id,
                                analysisDB.image.disease.plant.scientificName,
                                analysisDB.image.disease.plant.commonName),
                            analysisDB.image.disease.scientificName,
                            analysisDB.image.disease.commonName),
                        analysisDB.image.url,
                        analysisDB.image.description,
                        analysisDB.image.source,
                        analysisDB.image.size),
                    Classifier(analysisDB.classifier.id,
                        Plant(analysisDB.classifier.plant.id,
                            analysisDB.classifier.plant.scientificName,
                            analysisDB.classifier.plant.commonName),
                        analysisDB.classifier.tag,
                        analysisDB.classifier.path))