from database.AnalysisResult import AnalysisResult as AnalysisResultDB
from models.AnalysisResult import AnalysisResult
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
        return AnalysisResult(
                        analysisResultDB.id,
                        analysisResultDB.idAnalysis,
                        analysisResultDB.idDisease,
                        analysisResultDB.score)

    def update(self, analysisResult=AnalysisResult()):
        """
        (AnalysisResult) -> (AnalysisResult)
        update analysis_result table
        """
        session = self.session_factory()
        analysisResultDB = session.query(AnalysisResultDB).filter_by(id=analysisResult.id).first()
        dic = {}
        if (analysisResultDB.idAnalysis != analysisResult.idAnalysis):
            dic['idAnalysis'] = analysisResult.idAnalysis
        if (analysisResultDB.idDisease != analysisResult.idDisease):
            dic['idDisease'] = analysisResult.idDisease
        if (analysisResultDB.score != analysisResult.score):
            dic['score'] = analysisResult.score
        if (dic != {}):
            session.query(AnalysisResultDB).filter_by(id=analysisResult.id).update(dic)
            session.commit()
            session.flush()
            session.refresh(analysisResultDB)
        
        return AnalysisResult(
                        analysisResultDB.id,
                        analysisResultDB.idAnalysis,
                        analysisResultDB.idDisease,
                        analysisResultDB.score)

    def delete(self, analysisResult=AnalysisResult()):
        """
        (AnalysisResult) -> (bool)
        Delete analysisResult from database
        """
        status = False
        session = self.session_factory()
        analysisResultDB = session.query(AnalysisResultDB).filter_by(id=analysisResult.id).first()
        session.delete(analysisResultDB)
        session.flush()
        session.commit()
        if (not session.query(AnalysisResultDB).filter_by(id=analysisResultDB.id).count()):
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
                        AnalysisResultDB.idAnalysis == analysisResult.idAnalysis,
                        AnalysisResultDB.idDisease == analysisResult.idDisease,
                        AnalysisResultDB.score == analysisResult.score))
        content = query.slice(offset, pageSize).all()
        total = query.count()
        analysisResults = []
        for analysisResultDB in content:
            analysisResults.append(AnalysisResult(
                                        analysisResultDB.id,
                                        analysisResultDB.idAnalysis,
                                        analysisResultDB.idDisease,
                                        analysisResultDB.score))
    
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

        return AnalysisResult(
                        analysisResultDB.id,
                        analysisResultDB.idAnalysis,
                        analysisResultDB.idDisease,
                        analysisResultDB.score)
