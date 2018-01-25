from ImageRepository import ImageRepository
import models.Image
import models.Disease
import models.Plant
import models.Type


def test_search():
    imgRep = ImageRepository('capivara', 'test', '127.0.0.1', '5432', 'green_eyes')
    images = imgRep.search(
        image=models.Image.Image(
            url="FREC_Scab_"))
    for image in images:
        print(image.disease.plant.commonName)
    assert 'FREC_Scab_' in images[0].url


def test_insert():
    imgRep = ImageRepository('capivara', 'test', '127.0.0.1', '5432', 'green_eyes')
    assert imgRep.create(models.Image.Image(
                     0,
                     models.Disease.Disease(
                             1,
                             models.Plant.Plant(
                                   1,
                                   'Malus domestica',
                                   'Apple'),
                             '<i>Venturia inaequalis </i>',
                             'Apple scab'),
                     'test',
                     '',
                     '',
                     1)).url == 'test'


def test_update():
    imgRep = ImageRepository('capivara', 'test', '127.0.0.1', '5432', 'green_eyes')
    image = models.Image.Image(
                       0,
                       models.Disease.Disease(
                               1,
                               models.Plant.Plant(
                                     1,
                                     'Malus domestica',
                                     'Apple'),
                               '<i>Venturia inaequalis </i>',
                               'Apple scab'),
                       'test2000',
                       '',
                       '',
                       1)
    image = imgRep.update(image)
    print(type(image))
    assert image.url == 'test2000'


def test_delete():
    imgRep = ImageRepository('capivara', 'test', '127.0.0.1', '5432', 'green_eyes')
    image = models.Image.Image(
                       0,
                       models.Disease.Disease(
                               1,
                               models.Plant.Plant(
                                     1,
                                     'Malus domestica',
                                     'Apple'),
                               '<i>Venturia inaequalis </i>',
                               'Apple scab'),
                       'test2000',
                       '',
                       '',
                       1)

    result = imgRep.delete(image)
    print(type(image))
    assert result is True
