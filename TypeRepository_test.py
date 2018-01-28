from TypeRepository import TypeRepository
import models.Type


def test_search():
	typeRep = TypeRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')
	types = typeRep.search(
			type = models.Type.Type(value="value test"))
	for type in types:
		print(type.id)
		assert 'value test' in types[0].value

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

def test_update():
	typeRep = TypeRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')
	type = models.Type.Type(
			4,
			"administrator",
			"user type")
	type = typeRep.update(type)
	print(type(type))
	assert type.description == 'user type'

def test_delete():
	typeRep = TypeRepository(
			'capivara',
			'test',
			'127.0.0.1',
			'5432',
			'green_eyes')
	type = models.Type.Type(
			 4,
			 "administrator",
			 "user typer")
	result = typeRep.delete(type)
	print(type(type))
	assert result is True
