from PlantRepository import PlantRepository
import models.Plant

plantRep = PlantRepository(
                        'capivara',
                        'test',
                        '127.0.0.1',
                        '5432',
                        'green_eyes')

def test_search():
    plants = plantRep.search(plant=models.Plant.Plant(scientificName="ria"))
    print('return {0} lines'.format(len(plants)))
    assert 'ria' in plants['content'][0].scientificName

def test_insert():
    plant = plantRep.create(models.Plant.Plant(0,'Malus domestica','Apple test'))
    assert plant.commonName == 'Apple test'

def test_update():
    plant = plantRep.update(models.Plant.Plant(0, 'Malus domestica','Apple test update'))
    assert plant.commonName == 'Apple test update'

def test_delete():
    result = plantRep.delete(models.Plant.Plant(0, 'Malus domestica','Apple test'))
    assert result is True
