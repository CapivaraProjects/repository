from ClassifierRepository import ClassifierRepository
import models.Classifier
<<<<<<< HEAD

classifierRep = ClassifierRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')

	def test_search():
		def test_search():
                classifiers = classifierRep.search(classifier=models.Classifier.Classifier(tag="some"))
                print('return {0} lines'.format(len(classifiers)))
                assert 'some' in classifiers['content'].[0].tag

	def test_insert():
		classifier = models.Classifier.Classifier(0,
							  1,
							  'testing something',
							  'a.to.b')
		assert classifierRep.create(classifier).tag == 'testing something'
	
	def test_update():
		 classifier = models.Classifier.Classifier(0,
                                                          1,
                                                          'testing something update',
                                                          'a.to.b')
		classifier = classifierRep.update(classifier)
                assert classifierRep.create(classifier).tag == 'testing something update'

	def second_test_search():
                classifiers = classifierRep.search(classifier=models.Classifier.Classifier(tag="some"))
                print('return {0} lines'.format(len(classifiers)))
                assert 'some' in classifiers['content'].[0].tag

	def test_delete():
		classifier = models.Classifier.Classifier(0,
							  1,
							  'testing something update',
							  'a.to.b')
		result = classifierRep.delete(classifier)
		assert result is True
=======
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
>>>>>>> upstream/master
