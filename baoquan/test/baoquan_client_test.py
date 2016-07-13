import os
import unittest

from faker import Factory

from baoquan.main.baoquan_client import BaoquanClient
from baoquan.main.exception.invalid_argument_exception import InvalidArgumentException
from baoquan.main.exception.server_exception import ServerException
from baoquan.main.util.utils import random_id_card


class TestBaoquanClient(unittest.TestCase):
    def setUp(self):
        self._client = BaoquanClient()
        self._client.host = 'http://localhost:8080'
        self._client.access_key = 'fsBswNzfECKZH9aWyh47fc'
        self._client.pem_path = os.path.dirname(__file__) + '/resources/private_key.pem'

        self._faker = Factory.create('zh_CN')

    def test_create_attestation0(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.create_attestation(None)
        self.assertEqual(ae.exception.message, 'payload can not be empty')

    def test_create_attestation1(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.create_attestation({})
        self.assertEqual(ae.exception.message, 'payload.template_id can not be empty')

    def test_create_attestation2(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.create_attestation({
                'template_id': '2hSWTZ4oqVEJKAmK2RiyT4'
            })
        self.assertEqual(ae.exception.message, 'payload.identities can not be empty')

    def test_create_attestation3(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.create_attestation({
                'template_id': '2hSWTZ4oqVEJKAmK2RiyT4',
                'identities': {}
            })
        self.assertEqual(ae.exception.message, 'payload.factoids can not be empty')

    def test_create_attestation4(self):
        """
        template should be exist
        :return:
        """
        with self.assertRaises(ServerException) as ae:
            self._client.create_attestation({
                'template_id': '2hSWTZ4oqVEJ',
                'identities': {
                    'ID': '42012319800127691X',
                    'MO': '15857112383'
                },
                'factoids': [
                    {
                        'type': 'user',
                        'data': {
                            'name': '张三',
                            'phone_number': '13234568732',
                            'registered_at': '1466674609',
                            'username': 'tom'
                        }
                    }
                ]
            })
        self.assertEqual(ae.exception.message, '模板不存在')

    def test_create_attestation5(self):
        """
        factoid data should meet with template schema
        when you edit template schemas on line and set user.phone_number is required
        you must give a valid phone_number value in user factoid
        :return:
        """
        with self.assertRaises(ServerException) as ae:
            self._client.create_attestation({
                'template_id': '2hSWTZ4oqVEJKAmK2RiyT4',
                'identities': {
                    'ID': '42012319800127691X',
                    'MO': '15857112383'
                },
                'factoids': [
                    {
                        'type': 'user',
                        'data': {
                            'name': '张三',
                            'registered_at': '1466674609',
                            'username': 'tom'
                        }
                    }
                ]
            })
        self.assertEqual(ae.exception.message, 'invalid data : user.phone_number required')

    def test_create_attestation6(self):
        """
        factoid data type should be in template schemas
        :return:
        """
        with self.assertRaises(ServerException) as ae:
            self._client.create_attestation({
                'template_id': '2hSWTZ4oqVEJKAmK2RiyT4',
                'identities': {
                    'ID': '42012319800127691X',
                    'MO': '15857112383'
                },
                'factoids': [
                    {
                        'type': 'product',
                        'data': {
                            'name': '浙金网',
                            'description': 'p2g理财平台'
                        }
                    }
                ],
                'completed': False
            })
        self.assertEqual(ae.exception.message, 'invalid factoid type: product corresponding schema not exist')

    def test_create_attestation7(self):
        """
        factoid data should meet with template schema
        when user.phone_number is required but you only upload product
        you must call add_factoids to upload user later
        :return:
        """
        with self.assertRaises(ServerException) as ae:
            self._client.create_attestation({
                'template_id': '5Yhus2mVSMnQRXobRJCYgt',
                'identities': {
                    'ID': '42012319800127691X',
                    'MO': '15857112383'
                },
                'factoids': [
                    {
                        'type': 'product',
                        'data': {
                            'name': '浙金网',
                            'description': 'p2g理财平台'
                        }
                    }
                ]
            })
        self.assertEqual(ae.exception.message, 'invalid data : user.phone_number required')

    def test_create_attestation8(self):
        response = self._client.create_attestation({
            'template_id': '2hSWTZ4oqVEJKAmK2RiyT4',
            'identities': {
                'ID': '42012319800127691X',
                'MO': '15857112383'
            },
            'factoids': [
                {
                    'type': 'user',
                    'data': {
                        'name': '张三',
                        'phone_number': '13234568732',
                        'registered_at': '1466674609',
                        'username': 'tom'
                    }
                }
            ]
        }, {
            0: [
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/contract.pdf', 'rb').read(),
                    'resource_name': 'contract.pdf',
                    'resource_content_type': 'application/pdf'
                }
            ]
        })
        self.assertIsNotNone(response['data']['no'])

    def test_add_factoids0(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.add_factoids({})
        self.assertEqual(ae.exception.message, 'payload.ano can not be empty')

    def test_add_factoids1(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.add_factoids({
                'ano': 'D58FFFD28A8949969611883B6EABA148'
            })
        self.assertEqual(ae.exception.message, 'payload.factoids can not be empty')

    def test_add_factoids2(self):
        """
        attestation must be exist
        :return:
        """
        with self.assertRaises(ServerException) as ae:
            self._client.add_factoids({
                'ano': 'D58FFFD28A8949',
                'factoids': [
                    {
                        'type': 'product',
                        'data': {
                            'name': '浙金网',
                            'description': 'p2g理财平台'
                        }
                    }
                ]
            })
        self.assertEqual(ae.exception.message, '保全不存在')

    def test_add_factoids3(self):
        """
        attestation completed and can not add factoids
        :return:
        """
        with self.assertRaises(ServerException) as ae:
            self._client.add_factoids({
                'ano': '4E6457A5A9B94FBFB64E0D08BDFA2BD4',
                'factoids': [
                    {
                        'type': 'product',
                        'data': {
                            'name': '浙金网',
                            'description': 'p2g理财平台'
                        }
                    }
                ]
            })
        self.assertEqual(ae.exception.message, '保全已完成,不能继续追加陈述')

    def test_add_factoids4(self):
        """
        when complete attestation, factoids should meet with schemas
        :return:
        """
        response = self._client.create_attestation({
            'template_id': '5Yhus2mVSMnQRXobRJCYgt',
            'identities': {
                'ID': '42012319800127691X',
                'MO': '15857112383'
            },
            'factoids': [
                {
                    'type': 'product',
                    'data': {
                        'name': '浙金网',
                        'description': 'p2g理财平台'
                    }
                }
            ],
            'completed': False
        })
        ano = response['data']['no']
        with self.assertRaises(ServerException) as ae:
            self._client.add_factoids({
                'ano': ano,
                'factoids': [
                    {
                        'type': 'product',
                        'data': {
                            'name': '浙金网',
                            'description': 'p2g理财平台'
                        }
                    }
                ]
            })
        self.assertEqual(ae.exception.message, 'invalid data : user.phone_number required')

    def test_add_factoids5(self):
        """
        create attestation and then add factoid
        :return:
        """
        response = self._client.create_attestation({
            'template_id': '5Yhus2mVSMnQRXobRJCYgt',
            'identities': {
                'ID': '42012319800127691X',
                'MO': '15857112383'
            },
            'factoids': [
                {
                    'type': 'product',
                    'data': {
                        'name': '浙金网',
                        'description': 'p2g理财平台'
                    }
                }
            ],
            'completed': False
        })
        ano = response['data']['no']
        response = self._client.add_factoids({
            'ano': ano,
            'factoids': [
                {
                    'type': 'user',
                    'data': {
                        'name': '张三',
                        'phone_number': '13234568732',
                        'registered_at': '1466674609',
                        'username': 'tom'
                    }
                }
            ]
        })
        self.assertTrue(response['data']['success'])

    def test_apply_ca0(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.apply_ca({})
        self.assertEqual(ae.exception.message, 'payload.type can not be empty')

    def test_apply_ca1(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.apply_ca({
                'type': 'PERSONAL'
            })
        self.assertEqual(ae.exception.message, 'payload.link_name can not be empty')

    def test_apply_ca2(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.apply_ca({
                'type': 'ENTERPRISE',
                'link_name': '张三'
            })
        self.assertEqual(ae.exception.message, 'payload.name can not be empty')

    def test_apply_ca3(self):
        with self.assertRaises(InvalidArgumentException) as ae:
            self._client.apply_ca({
                'type': 'ENTERPRISE',
                'name': '浙金网',
                'ic_code': '91330105311263043J',
                'org_code': '311263043',
                'tax_code': '330105311263043',
                'link_name': self._faker.name(),
                'link_id_card': random_id_card(),
                'link_phone': self._faker.phone_number(),
                'link_email': self._faker.email(),
            })
        self.assertEqual(ae.exception.message, 'seal can not be null when ca type is enterprise')

    def test_apply_ca4(self):
        response = self._client.apply_ca({
            'type': 'PERSONAL',
            'link_name': self._faker.name(),
            'link_id_card': random_id_card(),
            'link_phone': self._faker.phone_number(),
            'link_email': Factory.create().email(),
        })
        self.assertIsNotNone(response['data']['no'])

    def test_apply_ca5(self):
        response = self._client.apply_ca({
            'type': 'ENTERPRISE',
            'name': '浙金网',
            'ic_code': '91330105311263043J',
            'org_code': '311263043',
            'tax_code': '330105311263043',
            'link_name': self._faker.name(),
            'link_id_card': random_id_card(),
            'link_phone': self._faker.phone_number(),
            'link_email': Factory.create().email(),
        }, {
            'resource': open(os.path.dirname(__file__) + '/resources/seal.png', 'rb').read(),
            'resource_name': 'seal.png',
            'resource_content_type': 'image/png'
        })
        self.assertIsNotNone(response['data']['no'])

    def test_sign0(self):
        response = self._client.create_attestation({
            'template_id': '2hSWTZ4oqVEJKAmK2RiyT4',
            'identities': {
                'ID': '42012319800127691X',
                'MO': '15857112383'
            },
            'factoids': [
                {
                    'type': 'user',
                    'data': {
                        'name': '张三',
                        'phone_number': '13234568732',
                        'registered_at': '1466674609',
                        'username': 'tom'
                    }
                }
            ],
            'signs': {
                0: {
                    0: {
                        'F98F99A554E944B6996882E8A68C60B2': ['甲方（签章）'],
                        '0A68783469E04CAC95ADEAE995A92E65': ['乙方（签章）']
                    }
                }
            }
        }, {
            0: [
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/contract.pdf', 'rb').read(),
                    'resource_name': 'contract.pdf',
                    'resource_content_type': 'application/pdf'
                }
            ]
        })
        self.assertIsNotNone(response['data']['no'])

    def test_sign1(self):
        response = self._client.create_attestation({
            'template_id': '2hSWTZ4oqVEJKAmK2RiyT4',
            'identities': {
                'ID': '42012319800127691X',
                'MO': '15857112383'
            },
            'factoids': [
                {
                    'type': 'user',
                    'data': {
                        'name': '张三',
                        'phone_number': '13234568732',
                        'registered_at': '1466674609',
                        'username': 'tom'
                    }
                }
            ],
            'signs': {
                0: {
                    0: {
                        'F98F99A554E944B6996882E8A68C60B2': ['甲方（签章）'],
                        '0A68783469E04CAC95ADEAE995A92E65': ['乙方（签章）']
                    }
                }
            }
        }, {
            0: [
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/contract.pdf', 'rb').read(),
                    'resource_name': 'contract.pdf',
                    'resource_content_type': 'application/pdf'
                },
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/seal.png', 'rb').read(),
                    'resource_name': 'seal.png',
                    'resource_content_type': 'image/png'
                }
            ]
        })
        self.assertIsNotNone(response['data']['no'])

    def test_sign2(self):
        response = self._client.create_attestation({
            'template_id': '5Yhus2mVSMnQRXobRJCYgt',
            'identities': {
                'ID': '42012319800127691X',
                'MO': '15857112383'
            },
            'factoids': [
                {
                    'type': 'product',
                    'data': {
                        'name': '浙金网',
                        'description': 'p2g理财平台'
                    }
                },
                {
                    'type': 'user',
                    'data': {
                        'name': '张三',
                        'phone_number': '13234568732',
                        'registered_at': '1466674609',
                        'username': 'tom'
                    }
                }
            ],
            'signs': {
                1: {
                    1: {
                        'F98F99A554E944B6996882E8A68C60B2': ['甲方（签章）'],
                        '0A68783469E04CAC95ADEAE995A92E65': ['乙方（签章）']
                    }
                }
            }
        }, {
            0: [
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/seal.png', 'rb').read(),
                    'resource_name': 'seal.png',
                    'resource_content_type': 'image/png'
                }
            ],
            1: [
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/seal.png', 'rb').read(),
                    'resource_name': 'seal.png',
                    'resource_content_type': 'image/png'
                },
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/contract.pdf', 'rb').read(),
                    'resource_name': 'contract.pdf',
                    'resource_content_type': 'application/pdf'
                }
            ]
        })
        self.assertIsNotNone(response['data']['no'])

    def test_sign3(self):
        response = self._client.create_attestation({
            'template_id': '5Yhus2mVSMnQRXobRJCYgt',
            'identities': {
                'ID': '42012319800127691X',
                'MO': '15857112383'
            },
            'factoids': [
                {
                    'type': 'product',
                    'data': {
                        'name': '浙金网',
                        'description': 'p2g理财平台'
                    }
                },
                {
                    'type': 'user',
                    'data': {
                        'name': '张三',
                        'phone_number': '13234568732',
                        'registered_at': '1466674609',
                        'username': 'tom'
                    }
                }
            ],
            'signs': {
                1: {
                    1: {
                        'F98F99A554E944B6996882E8A68C60B2': ['甲方（签章）'],
                        '0A68783469E04CAC95ADEAE995A92E65': ['乙方（签章）']
                    }
                }
            }
        }, {
            1: [
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/seal.png', 'rb').read(),
                    'resource_name': 'seal.png',
                    'resource_content_type': 'image/png'
                },
                {
                    'resource': open(os.path.dirname(__file__) + '/resources/contract.pdf', 'rb').read(),
                    'resource_name': 'contract.pdf',
                    'resource_content_type': 'application/pdf'
                }
            ]
        })
        self.assertIsNotNone(response['data']['no'])

    def test_get_attestation0(self):
        with self.assertRaises(ServerException) as ae:
            self._client.get_attestation('DB0C8DB14E3C44')
        self.assertEqual(ae.exception.message, '保全不存在')

    def test_get_attestation1(self):
        response = self._client.get_attestation('DB0C8DB14E3C44C7B9FBBE30EB179241')
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['data'])
        self.assertEqual('DB0C8DB14E3C44C7B9FBBE30EB179241', response['data']['no'])

    def test_get_attestation2(self):
        response = self._client.get_attestation('DB0C8DB14E3C44C7B9FBBE30EB179241', [])
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['data'])
        self.assertEqual('DB0C8DB14E3C44C7B9FBBE30EB179241', response['data']['no'])
        self.assertIsNone(response['data']['identities'])
        self.assertIsNone(response['data']['factoids'])
        self.assertIsNone(response['data']['attachments'])

    def test_get_attestation3(self):
        response = self._client.get_attestation('DB0C8DB14E3C44C7B9FBBE30EB179241', ['factoids'])
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['data'])
        self.assertEqual('DB0C8DB14E3C44C7B9FBBE30EB179241', response['data']['no'])
        self.assertIsNone(response['data']['identities'])
        self.assertIsNotNone(response['data']['factoids'])
        self.assertIsNone(response['data']['attachments'])

    def test_download_attestation0(self):
        response = self._client.download_attestation('DB0C8DB14E3C44C7B9FBBE30EB179241')
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['file_name'])
        self.assertIsInstance(response['file_content'], bytes)
        with open(response['file_name'], 'wb') as f:
            f.write(response['file_content'])
