from ClassifierRepository import ClassifierRepository
import models.Classifier

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
