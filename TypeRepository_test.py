from TypeRepository import TypeRepository
import models.Type

<<<<<<< HEAD

def test_insert():
        typeRep = TypeRepository(
                        'capivara',
                        'test',
                        '127.0.0.1',
                        '5432',
                        'green_eyes')
        assert typeRep.create(models.Type.Type(
                                0,
                                "admin",
                                "user")).value == 'admin'
=======
def test_insert():
	typeRep = TypeRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')
	assert typeRep.create(models.Type.Type(
				0,
				'admin',
				'user')).value == 'admin'
>>>>>>> upstream/master

def test_search():
	typeRep = TypeRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')
<<<<<<< HEAD
	types = typeRep.search(
<<<<<<< HEAD
			type = models.Type.Type(value="admin"))
	for type in types:
		print(type.id)
		assert 'admin' in types[0].value
=======
			type = models.Type.Type(value="value test"))['content']
	for type in types:
		print(type.id)
		assert 'value test' in types[0].value
>>>>>>> upstream/master
=======
	assert typeRep.create(models.Type.Type(
				0,
				"admin",
				"user")).value == 'admin'
>>>>>>> 628e9d9deaa051d500fdff57d59797bad94d918f

def test_update():
	typeRep = TypeRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')
	type = models.Type.Type(
<<<<<<< HEAD
			4,
			"administrator",
			"user type")
	type = typeRep.update(type)
	print(type(type))
=======
			0,
			"administrator",
			"user type")
	type = typeRep.update(type)
	#print(type(type))
>>>>>>> upstream/master
	assert type.description == 'user type'

def test_delete():
	typeRep = TypeRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')
	type = models.Type.Type(
<<<<<<< HEAD
			 4,
			 "administrator",
			 "user typer")
	result = typeRep.delete(type)
	print(type(type))
=======
			 0,
			 "administrator",
			 "user typer")
	result = typeRep.delete(type)
	#print(type(type))
>>>>>>> upstream/master
	assert result is True
