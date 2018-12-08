from TextRepository import TextRepository
import os
import models.Text

def test_insert():
    textRep = TextRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
    assert textRep.create(models.Text.Text(
                     0,
                     'test',
		      'test plant',
		      'test status',
                     'test attribute',
                     'test value',
                     'test reference')).value == 'test value'

def test_search():
    textRep = TextRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
    texts = textRep.search(text=models.Text.Text(value="test value"))['content']
    for text in texts:
        print(text.id)
    assert 'test value' in texts[0].value

def test_update():
    textRep = TextRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
    text = models.Text.Text(
                       0,
                       'test',
		        'test plant',
		        'test status',
                       'test attribute',
                       'test value',
                       'test reference 2000')
    text = textRep.update(text)
    print(type(text))
    assert text.description == 'test reference 2000'

def test_delete():
    textRep = TextRepository(
            'capivara',
            'test',
            '127.0.0.1',
            '5432',
            'green_eyes')
    text = models.Text.Text(
                       0,
                       'test language',
		        'test plant',
		        'test status',
                       'test attribute',
                       'test value',
                       'test reference')

    result = textRep.delete(text)
    print(type(text))
    assert result is True
