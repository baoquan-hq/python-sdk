import unittest
import os
import datetime
import uuid
from src.main.util import utils


class TestPython(unittest.TestCase):
    def test_sign(self):
        en = utils.sign(os.path.dirname(__file__) + '/resources/private_key.pem', '123')
        print(type(en))
        print(en)
        print(en.decode())

    def test_checksum(self):
        with open(os.path.dirname(__file__) + '/resources/contract.pdf', 'rb') as file:
            bytes = file.read()
        print(utils.checksum(bytes))

    def test_time(self):
        print(datetime.datetime.now().timestamp())

    def test_uuid(self):
        print(uuid.uuid4())

    def test_assert1(self):
        a = {}
        if 'b' in a:
            print(True)
        else:
            print(False)

    def test_assert2(self):
        a = None
        assert a is None
        print(isinstance(a, tuple))

    def test_assert3(self):
        a = None
        with self.assertRaises(TypeError):
            print(len(a))
