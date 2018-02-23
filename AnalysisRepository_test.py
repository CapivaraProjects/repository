from AnalysisRepository import AnalysisRepository
import models.Analysis

analysisRep = AnalysisRepository(
                'capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')

def test_insert():
    analysis = models.Analysis.Analysis()
    assert analysisRep.create(analysis).id == 0

def test_search():
    analyzes = analysisRep.search(analysis=models.Analysis.Analysis(idImage=0))
    print('return {0} lines'.format(len(analyzes)))
    assert analyzes['content'][0].idImage == 0

def test_update():
    analysis = models.Analysis.Analysis(0, 1)
    analysis = analysisRep.update(analysis)
    assert analysis.idImage == 1

def test_delete():
    analysis = models.Analysis.Analysis(0, 1)
    result = analysisRep.delete(analysis)
    assert result is True

