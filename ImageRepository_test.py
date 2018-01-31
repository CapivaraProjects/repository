from ImageRepository import ImageRepository
import os
import models.Image
import models.Disease
import models.Plant
import models.Type


def test_search():
    imgRep = ImageRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
    images = imgRep.search(
        image=models.Image.Image(
            url="FREC_Scab_"))['content']
    for image in images:
        print(image.disease.plant.commonName)
    assert 'FREC_Scab_' in images[0].url


def test_insert():
    imgRep = ImageRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
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
    imgRep = ImageRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
    image = models.Image.Image(
                       171052,
                       models.Disease.Disease(
                               1,
                               models.Plant.Plant(
                                     1,
                                     'Malus domestica',
                                     'Apple'),
                               '<i>Venturia inaequalis </i>',
                               'Apple scab'),
                       'test2004',
                       'photographed in field/outside, FREC, Biglerville, PA',
                       'PlantVillage',
                       3)
    image = imgRep.update(image)
    print(type(image))
    assert image.url == 'test2004'


def test_delete():
    imgRep = ImageRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
    image = models.Image.Image(
                       171047,
                       models.Disease.Disease(
                               1,
                               models.Plant.Plant(
                                     1,
                                     'Malus domestica',
                                     'Apple'),
                               '<i>Venturia inaequalis </i>',
                               'Apple scab'),
                       'FREC_Scab_3108_resized.JPG',
                       'photographed in field/outside, FREC, Biglerville, PA',
                       'PlantVillage',
                       3)

    result = imgRep.delete(image)
    print(type(image))
    assert result is True


def test_convert_to_base64():
    imgRep = ImageRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')

    image = imgRep.searchByID(3264)
    image = imgRep.getImageBase64(
            imagesDir=os.getcwd(),
            image=image)
    assert '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\n3Uobn1EYmDgbSvwJ/9k=\n' in image.url


def test_save_image():
    imgRep = ImageRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')

    image = imgRep.searchByID(3264)
    image.url = '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\n3Uobn1EYmDgbSvwJ/9k=\n'
    image = imgRep.saveImage(
            imagesDir=os.getcwd(),
            image=image,
            extension='.JPG')
    size = "large"
    if image.size == 1:
        size = "thumb"
    elif image.size == 2:
        size = "medium"
    elif image.size == 3:
        size = "large"
    filepath = "{}/{}/{}/{}/{}".format(
        os.getcwd(),
        size,
        image.disease.plant.commonName.replace(
            ' ',
            '_').replace(
                '(',
                '_').replace(
                    ')',
                    '_'),
        image.disease.scientificName.replace(
            " ",
            "_").replace(
                ";",
                "").replace(
                    "(",
                    "_").replace(
                        ")",
                        "_").replace(
                            "<i>",
                            "").replace(
                                "</i>",
                                ""),
        image.url)
    assert os.path.isfile(filepath)
