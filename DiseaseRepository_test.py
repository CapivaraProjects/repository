from DiseaseRepository import DiseaseRepository
import models.Disease
import models.Plant

diseaseRep = DiseaseRepository(
                'capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')

def test_search():
    diseases = diseaseRep.search(disease=models.Disease.Disease(scientificName="ria"))
    print('return {0} lines'.format(len(diseases)))
    assert 'ria' in diseases['content'][0].scientificName

def test_insert():
    disease = models.Disease.Disease(0,
                                    models.Plant.Plant(1,'Malus domestica','Apple'),
                                    '<i>Venturia inaequalis </i>',
                                    'Apple scab test')
    assert diseaseRep.create(disease).commonName == 'Apple scab test'

def test_update():
    disease = models.Disease.Disease(0,
                                    models.Plant.Plant(1,'Malus domestica','Apple'),
                                    '<i>Venturia inaequalis </i>',
                                    'Apple scab test update')
    disease = diseaseRep.update(disease)
    assert disease.commonName == 'Apple scab test update'

def test_delete():
    disease = models.Disease.Disease(0,
                                    models.Plant.Plant(1,'Malus domestica','Apple'),
                                    '<i>Venturia inaequalis </i>',
                                    'Apple scab test update')
    result = diseaseRep.delete(disease)
    assert result is True

