from UserRepository import UserRepository
import models.User
#import models.Type

userRep = UserRepository(
                'capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')

def test_insert():
    user = models.User.User(0,
							0,
							#models.Type.Type(1,'thumb','image-size'),
                            'tester@test.com',
                            'tester',
                            'password',
                            'ashdiuhsduiahu',
                            '12/12/12',
                            '')
    assert userRep.create(user).username == 'tester'

def test_search():
    users = userRep.search(user=models.User.User(username="tester"))
    print('return {0} lines'.format(len(users)))
    assert 'tester' in users['content'][0].username

def test_update():
    user = models.User.User(0,
							0,
                            #models.Type.Type(1,'thumb','image-size'),
                            'tester@test.com',
                            'tester update',
                            'password',
                            'ashdiuhsduiahu',
                            '12/01/18',
                            '13/12/18')
    user = userRep.update(user)
    assert user.username == 'tester update'

def test_delete():
    user = models.User.User(0,
							0,
                            #models.Type.Type(1,'thumb','image-size'),
                            'tester@test.com',
                            'tester update',
                            'password',
                            'ashdiuhsduiahu',
                            '12/01/18',
                            '13/12/18')
    result = userRep.delete(user)
    assert result is True
