# Baoquan.com API SDK

Welcome to use Baoquan.com API SDK.

## Create Baoquan Client

```python
from baoquan import BaoquanClient

client = BaoquanClient()
client.host = 'http://baoquan.com'
client.access_key = 'fsBswNzfECKZH9aWyh47fc' # replace it with your access key
client.pem_path = 'path/to/rsa_private.pem'
```

## Create attestation

### Create attestation without sign

```python
try:
    response = client.create_attestation({
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
    print(response['data']['no'])
except ServerException as e:
    print(e.message)

```

### Create attestation with sign

```python
try:
    response = client.create_attestation({
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
    print(response['data']['no'])
except ServerException as e:
    print(e.message)
```

## Add factoid

```python
try:
    response = client.add_factoids({
        'ano': '7F189BBB5FA1451EA8601D0693E36FE7',
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
    print(response['data']['success'])
except ServerException as e:
    print(e.message)
```

## Apply Ca

### Apply personal Ca

```python
try:
    response = client.apply_ca({
        'type': 'PERSONAL',
        'link_name': '张三',
        'link_id_card': '432982198405237845',
        'link_phone': '13578674532',
        'link_email': '13578674532@qq.com'
    })
    print(response['data']['no'])
except ServerException as e:
    print(e.message)
```

### Apply enterprise Ca

```python
try:
    response = client.apply_ca({
        'type': 'ENTERPRISE',
        'name': '浙金网',
        'ic_code': '91330105311263043J',
        'org_code': '311263043',
        'tax_code': '330105311263043',
        'link_name': '张三',
        'link_id_card': '432982198405237845',
        'link_phone': '13578674532',
        'link_email': '13578674532@qq.com'
    }, {
        'resource': open(os.path.dirname(__file__) + '/resources/seal.png', 'rb').read(),
        'resource_name': 'seal.png',
        'resource_content_type': 'image/png'
    })
    print(response['data']['no'])
except ServerException as e:
    print(e.message)
```

You can look at the unit test for more examples.