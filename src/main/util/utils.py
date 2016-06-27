import rsa
import base64
import hashlib


def sign(key_path, data):
    """
    use rsa 256 to sign data
    :param key_path: private key file path, must be PKCS#1 PEM-encoded
    :param data: data to sign
    :return: signed data
    """
    with open(key_path) as private_file:
        key_data = private_file.read()
    private_key = rsa.PrivateKey.load_pkcs1(key_data)
    return base64.b64encode(rsa.sign(data.encode('utf-8'), private_key, 'SHA-256')).decode()


def checksum(bytes):
    """
    use sha256 to create the checksum of file content
    :param bytes: file content as bytes
    :return: hex hash
    """
    m = hashlib.sha256()
    m.update(bytes)
    return m.hexdigest()
