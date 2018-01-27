from DiseaseRepository import DiseaseRepository
import models.Disease
import models.Plant

def test_search():
	diseaseRep = DiseaseRepository(
				 'capivara',
				 'test',
				 '127.0.0.1',
				 '5432',
				 'green_eyes')
	diseases = diseaseRep.search(disease=models.Disease.Disease(scientificName="ria"))
	print('return {0} lines'.format(len(diseases)))
	assert 'ria' in diseases[0].scientificName

def test_insert():
	diseaseRep = DiseaseRepository(
				 'capivara',
				 'test',
				 '127.0.0.1',
				 '5432',
				 'green_eyes')
	assert diseaseRep.create(models.Disease.Disease(
						0,
						models.Plant.Plant(
								1,
								'Malus domestica',
								'Apple'),
						'<i>Venturia inaequalis </i>',
						'Apple scab test')).commonName == 'Apple scab test'

def test_update():
	diseaseRep = DiseaseRepository(
				 'capivara',
				 'test',
				 '127.0.0.1',
				 '5432',
				 'green_eyes')
	disease = models.Disease.Disease(
					  0,
					  models.Plant.Plant(
		                      1,
		                      'Malus domestica',
		                      'Apple'),
                      '<i>Venturia inaequalis </i>',
                      'Apple scab test update')
	disease = diseaseRep.update(disease)
	assert disease.commonName == 'Apple scab test update'

def test_delete():
	diseaseRep = DiseaseRepository(
				 'capivara',
				 'test',
				 '127.0.0.1',
				 '5432',
				 'green_eyes')
	disease = models.Disease.Disease(
					  0,
					  models.Plant.Plant(
		                      1,
		                      'Malus domestica',
		                      'Apple'),
                      '<i>Venturia inaequalis </i>',
                      'Apple scab test update')
	result = diseaseRep.delete(disease)
	assert result is True


