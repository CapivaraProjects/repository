from AnalysisRepository import AnalysisRepository
import models.Analysis
import models.Image


analysisRep = AnalysisRepository(
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
                                        
analysisModelTest = models.Analysis.Analysis(
                    0,
                    imageModelTest,
                    classifierModelTest)

def test_insert():
    assert analysisRep.create(analysis=analysisModelTest).id == 0

def test_search_by_id():
    analysis = analysisRep.searchByID(0)
    assert analysis.classifier.tag == '1'
    
def test_search():

    analyses = analysisRep.search(analysis=analysisModelTest)
    print('return {0} lines'.format(len(analyses)))
    assert analyses['content'][0].classifier.tag == '1'
    
def test_update():
    analysisModelTest.image.id = 2
    analysis = analysisRep.update(analysis=analysisModelTest)
    assert analysis.image.id == 2

def test_delete():
    result = analysisRep.delete(analysis=analysisModelTest)
    assert result is True
