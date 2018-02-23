from AnalysisResultRepository import AnalysisResultRepository
import models.AnalysisResult

analysisResultRep = AnalysisResultRepository(
                'capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')

def test_insert():
    analysisResult = models.AnalysisResult.AnalysisResult(0, 0, 0, 0.99)
    assert analysisResultRep.create(analysisResult).id == 0

def test_search():
    analysisResults = analysisResultRep.search(analysisResult=models.AnalysisResult.AnalysisResult(score=0.99))
    print('return {0} lines'.format(analysisResults['total']))
    assert analysisResults['content'][0].idDisease == 0

def test_update():
    analysisResult = models.AnalysisResult.AnalysisResult(0, 0, 0, 0.87)
    analysisResult = analysisResultRep.update(analysisResult)
    assert analysisResult.score == 0.87

def test_delete():
    analysisResult = models.AnalysisResult.AnalysisResult(0, 0, 0, 0.87)
    result = analysisResultRep.delete(analysisResult)
    assert result is True

