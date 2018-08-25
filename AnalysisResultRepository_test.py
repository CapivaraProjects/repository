from repository.AnalysisResultRepository import AnalysisResultRepository
import models.AnalysisResult
import models.Analysis
import models.Plant
import models.Disease
import models.Image
import models.Classifier


analysisResultRep = AnalysisResultRepository(
                'capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')

plantModelTest = models.Plant.Plant(
                        24,
                        'Lycopersicum esculentum',
                        'Tomato')
                        
diseaseModelTest = models.Disease.Disease(
                        53,
                        plantModelTest,
                        '<i>Alternaria solani</i>',
                        'Early blight')

imageModelTest = models.Image.Image(
                        1,
                        diseaseModelTest,        
                        'test',
                        '',
                        '',
                        1)

# already exists a classifier with id 1 in the database
classifierModelTest = models.Classifier.Classifier(
                        1,
                        plantModelTest,
                        '1',
                        'gykernel/saved_models')
                        
# already exists an analysis with id 1 in the database
analysisModelTest = models.Analysis.Analysis(
                        1,
                        imageModelTest,
                        classifierModelTest)

analysisResultModelTest = models.AnalysisResult.AnalysisResult(
                        1, 
                        analysisModelTest,
                        diseaseModelTest,
                        0.98,
                        '100,100,128,128')


def test_insert():
    assert analysisResultRep.create(analysisResultModelTest).score == 0.98

def test_search_by_id():
    analysisResult = analysisResultRep.searchByID(1)
    assert analysisResult.score == 0.98
    
def test_search():
    analysisResults = analysisResultRep.search(analysisResultModelTest)
    print('return {0} lines'.format(analysisResults['total']))
    assert analysisResults['content'][0].score == 0.98


def test_update():
    analysisResultModelTest.score = 0.87
    analysisResult = analysisResultRep.update(analysisResultModelTest)
    assert analysisResult.score == 0.87


def test_delete():
    result = analysisResultRep.delete(analysisResultModelTest)
    assert result is True
