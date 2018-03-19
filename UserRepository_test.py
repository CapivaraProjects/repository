from UserRepository import UserRepository
import models.User
from tools.Cryptography import Crypto


userRep = UserRepository(
                'capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')
crypto = Crypto()
salt = crypto.generateRandomSalt()
ciphredPassword = crypto.encrypt(salt, 'test')


def test_insert():
    user = models.User.User(0,
                            0,
                            'tester@test.com',
                            'tester',
                            ciphredPassword,
                            salt,
                            '12/12/12',
                            '')
    assert userRep.create(user).username == 'tester'


def test_search():
    users = userRep.search(user=models.User.User(username='tester'))
    print('return {0} lines'.format(len(users)))
    assert 'tester' in users['content'][0].username


def test_authentication():
    crypto = Crypto()
    salt = crypto.generateRandomSalt()
    ciphredPassword = crypto.encrypt(salt, 'test')
    user = models.User.User(username='tester',
                            salt=salt, password=ciphredPassword)
    authUser = userRep.authentication(user)
    assert authUser.username == user.username


def test_authentication_fail():
    crypto = Crypto()
    salt = crypto.generateRandomSalt()
    wrongPassword = crypto.encrypt(salt, 'wrong')
    user = models.User.User(username='tester', salt=salt,
                            password=wrongPassword)
    authUser = userRep.authentication(user)
    assert authUser.username == ""


def test_update():
    user = models.User.User(0,
                            0,
                            'tester@test.com',
                            'tester update',
                            ciphredPassword,
                            salt,
                            '12/01/18',
                            '13/12/18')
    user = userRep.update(user)
    assert user.username == 'tester update'


def test_delete():
    user = models.User.User(0,
                            0,
                            'tester@test.com',
                            'tester update',
                            ciphredPassword,
                            salt,
                            '12/01/18',
                            '13/12/18')
    result = userRep.delete(user)
    assert result is True
