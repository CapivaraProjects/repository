from database.AnalysisResult import AnalysisResult as AnalysisResultDB
from models.AnalysisResult import AnalysisResult 
from models.Analysis import Analysis 
from models.Plant import Plant 
from models.Disease import Disease 
from models.Image import Image 
from models.Classifier import Classifier


from repository.base import Base
from sqlalchemy import or_

class AnalysisResultRepository(Base):
    
    def __init__(self,
                 dbuser="",
                 dbpass="",
                 dbhost="",
                 port="",
                 dbname=""):
        super().__init__(dbuser, dbpass, dbhost, port, dbname)

    def create(self, analysisResult=AnalysisResult()):
        """
        (AnalysisResult) -> (AnalysisResult)
        Add analysis result to database
        """
        analysisResultDB = AnalysisResultDB(analysisResult=analysisResult)
        session = self.session_factory()
        session.add(analysisResultDB)
        session.flush()
        session.commit()
        session.refresh(analysisResultDB)
        return AnalysisResult(analysisResultDB.id,
                        Analysis(analysisResultDB.analysis.id,
                            Image(analysisResultDB.analysis.image.id,
                                Disease(analysisResultDB.analysis.image.disease.id,
                                    Plant(analysisResultDB.analysis.image.disease.plant.id,
                                        analysisResultDB.analysis.image.disease.plant.scientificName,
                                        analysisResultDB.analysis.image.disease.plant.commonName),
                                    analysisResultDB.analysis.image.disease.scientificName,
                                    analysisResultDB.analysis.image.disease.commonName),
                                analysisResultDB.analysis.image.url,
                                analysisResultDB.analysis.image.description,
                                analysisResultDB.analysis.image.source,
                                analysisResultDB.analysis.image.size),
                            Classifier(analysisResultDB.analysis.classifier.id,
                                Plant(analysisResultDB.analysis.classifier.plant.id,
                                    analysisResultDB.analysis.classifier.plant.scientificName,
                                    analysisResultDB.analysis.classifier.plant.commonName),
                                analysisResultDB.analysis.classifier.tag,
                                analysisResultDB.analysis.classifier.path)),
                        Disease(analysisResultDB.disease.id,
                            Plant(analysisResultDB.disease.plant.id,
                                analysisResultDB.disease.plant.scientificName,
                                analysisResultDB.disease.plant.commonName),
                            analysisResultDB.disease.scientificName,
                            analysisResultDB.disease.commonName),
                        analysisResultDB.score,
                        analysisResultDB.frame)

    def create_using_list(self, analysis_results):
        """Create AnalysisResults on db using a list
        Args:
            analysis_results: A list of analysis results to be inserted
        Returns:
            A list of filled  AnalysisResults
        """
        analysis_results_db = [AnalysisResultDB(
            analysisResult=analysis_result) for analysis_result in analysis_results]
        session = self.session_factory()
        session.add_all(analysis_results_db)
        session.flush()
        session.commit()
        return True

    def update(self, analysisResult=AnalysisResult()):
        """
        (AnalysisResult) -> (AnalysisResult)
        update analysis_result table
        """
        session = self.session_factory()
        analysisResultDB = session.query(AnalysisResultDB).filter_by(
            id=analysisResult.id).first()
        dic = {}
        if (analysisResultDB.idAnalysis != analysisResult.analysis.id):
            dic['idAnalysis'] = analysisResult.analysis.id
        if (analysisResultDB.idDisease != analysisResult.disease.id):
            dic['idDisease'] = analysisResult.disease.id
        if (analysisResultDB.score != analysisResult.score):
            dic['score'] = analysisResult.score
        if (analysisResultDB.frame != analysisResult.frame):
            dic['frame'] = analysisResult.frame
        if (dic != {}):
            session.query(AnalysisResultDB).filter_by(
                id=analysisResult.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(analysisResultDB)

        return AnalysisResult(analysisResultDB.id,
                        Analysis(analysisResultDB.analysis.id,
                            Image(analysisResultDB.analysis.image.id,
                                Disease(analysisResultDB.analysis.image.disease.id,
                                    Plant(analysisResultDB.analysis.image.disease.plant.id,
                                        analysisResultDB.analysis.image.disease.plant.scientificName,
                                        analysisResultDB.analysis.image.disease.plant.commonName),
                                    analysisResultDB.analysis.image.disease.scientificName,
                                    analysisResultDB.analysis.image.disease.commonName),
                                analysisResultDB.analysis.image.url,
                                analysisResultDB.analysis.image.description,
                                analysisResultDB.analysis.image.source,
                                analysisResultDB.analysis.image.size),
                            Classifier(analysisResultDB.analysis.classifier.id,
                                Plant(analysisResultDB.analysis.classifier.plant.id,
                                    analysisResultDB.analysis.classifier.plant.scientificName,
                                    analysisResultDB.analysis.classifier.plant.commonName),
                                analysisResultDB.analysis.classifier.tag,
                                analysisResultDB.analysis.classifier.path)),
                        Disease(analysisResultDB.disease.id,
                            Plant(analysisResultDB.disease.plant.id,
                                analysisResultDB.disease.plant.scientificName,
                                analysisResultDB.disease.plant.commonName),
                            analysisResultDB.disease.scientificName,
                            analysisResultDB.disease.commonName),
                        analysisResultDB.score,
                        analysisResultDB.frame)

    def delete(self, analysisResult=AnalysisResult()):
        """
        (AnalysisResult) -> (bool)
        Delete analysisResult from database
        """
        status = False
        session = self.session_factory()
        analysisResultDB = session.query(AnalysisResultDB).filter_by(
            id=analysisResult.id).first()
        session.delete(analysisResultDB)
        session.flush()
        session.commit()
        if (not session.query(AnalysisResultDB).filter_by(
                id=analysisResultDB.id).count()):
            status = True
        session.close()
        return status

    def search(self, analysisResult=AnalysisResult(), pageSize=10, offset=0):
        """
        (AnalysisResult, pageSize, offset) -> [AnalysisResult]
        search by analysisResult
        """
        session = self.session_factory()
        query = session.query(AnalysisResultDB).filter(or_(
                        AnalysisResultDB.idAnalysis == analysisResult.analysis.id,
                        AnalysisResultDB.idDisease == analysisResult.disease.id,
                        AnalysisResultDB.score == analysisResult.score,
                        AnalysisResultDB.frame == analysisResult.frame))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        analysisResults = []
        for analysisResultDB in content:
            analysisResults.append(AnalysisResult(analysisResultDB.id,
                        Analysis(analysisResultDB.analysis.id,
                            Image(analysisResultDB.analysis.image.id,
                                Disease(analysisResultDB.analysis.image.disease.id,
                                    Plant(analysisResultDB.analysis.image.disease.plant.id,
                                        analysisResultDB.analysis.image.disease.plant.scientificName,
                                        analysisResultDB.analysis.image.disease.plant.commonName),
                                    analysisResultDB.analysis.image.disease.scientificName,
                                    analysisResultDB.analysis.image.disease.commonName),
                                analysisResultDB.analysis.image.url,
                                analysisResultDB.analysis.image.description,
                                analysisResultDB.analysis.image.source,
                                analysisResultDB.analysis.image.size),
                            Classifier(analysisResultDB.analysis.classifier.id,
                                Plant(analysisResultDB.analysis.classifier.plant.id,
                                    analysisResultDB.analysis.classifier.plant.scientificName,
                                    analysisResultDB.analysis.classifier.plant.commonName),
                                analysisResultDB.analysis.classifier.tag,
                                analysisResultDB.analysis.classifier.path)),
                        Disease(analysisResultDB.disease.id,
                            Plant(analysisResultDB.disease.plant.id,
                                analysisResultDB.disease.plant.scientificName,
                                analysisResultDB.disease.plant.commonName),
                            analysisResultDB.disease.scientificName,
                            analysisResultDB.disease.commonName),
                        analysisResultDB.score,
                        analysisResultDB.frame))

        return {'total': total, 'content': analysisResults}

    def searchByID(self, id):
        """
        (int) -> (AnalysisResult)
        Search analysis result by ID
        """
        session = self.session_factory()
        analysisResultDB = session.query(AnalysisResultDB).get(id)
        if (analysisResultDB is None):
            raise Exception("AnalysisResults not found!")

        return AnalysisResult(analysisResultDB.id,
                        Analysis(analysisResultDB.analysis.id,
                            Image(analysisResultDB.analysis.image.id,
                                Disease(analysisResultDB.analysis.image.disease.id,
                                    Plant(analysisResultDB.analysis.image.disease.plant.id,
                                        analysisResultDB.analysis.image.disease.plant.scientificName,
                                        analysisResultDB.analysis.image.disease.plant.commonName),
                                    analysisResultDB.analysis.image.disease.scientificName,
                                    analysisResultDB.analysis.image.disease.commonName),
                                analysisResultDB.analysis.image.url,
                                analysisResultDB.analysis.image.description,
                                analysisResultDB.analysis.image.source,
                                analysisResultDB.analysis.image.size),
                            Classifier(analysisResultDB.analysis.classifier.id,
                                Plant(analysisResultDB.analysis.classifier.plant.id,
                                    analysisResultDB.analysis.classifier.plant.scientificName,
                                    analysisResultDB.analysis.classifier.plant.commonName),
                                analysisResultDB.analysis.classifier.tag,
                                analysisResultDB.analysis.classifier.path)),
                        Disease(analysisResultDB.disease.id,
                            Plant(analysisResultDB.disease.plant.id,
                                analysisResultDB.disease.plant.scientificName,
                                analysisResultDB.disease.plant.commonName),
                            analysisResultDB.disease.scientificName,
                            analysisResultDB.disease.commonName),
                        analysisResultDB.score,
                        analysisResultDB.frame)
