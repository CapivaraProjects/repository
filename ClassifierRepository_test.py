from ClassifierRepository import ClassifierRepository
import models.Classifier
import models.Plant

classifierRep = ClassifierRepository(
                'capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')

def test_insert():
    classifier = models.Classifier.Classifier(0,
                                    models.Plant.Plant(1,'Malus domestica','Apple'),
                                    '1',
                                    'gykernel/saved_models')
    assert classifierRep.create(classifier).path == 'gykernel/saved_models'

def test_search():
    classifiers = classifierRep.search(classifier=models.Classifier.Classifier(path="gykernel/saved_models"))
    print('return {0} lines'.format(len(classifiers)))
    assert 'gykernel/saved_models' in classifiers['content'][0].path

def test_update():
    classifier = models.Classifier.Classifier(0,
                                    models.Plant.Plant(1,'Malus domestica','Apple'),
                                    '2',
                                    'gykernel/saved_models')
    classifier = classifierRep.update(classifier)
    assert classifier.tag == '2'

def test_delete():
    classifier = models.Classifier.Classifier(0,
                                    models.Plant.Plant(1,'Malus domestica','Apple'),
                                    '2',
                                    'gykernel/saved_models')
    result = classifierRep.delete(classifier)
    assert result is True
