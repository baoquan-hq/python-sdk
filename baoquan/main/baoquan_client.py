import uuid
import requests
import datetime
import json
from baoquan.main.exception.server_exception import ServerException
from baoquan.main.exception.invalid_argument_exception import InvalidArgumentException
from baoquan.main.util import utils


def _check_create_attestation_payload(payload):
    """
    check create attestation payload
    :param payload:
    :return:
    """
    if not isinstance(payload, dict):
        raise InvalidArgumentException('payload can not be empty')
    if payload.get('template_id') is None:
        raise InvalidArgumentException('payload.template_id can not be empty')
    if payload.get('identities') is None:
        raise InvalidArgumentException('payload.identities can not be empty')
    if payload.get('factoids') is None:
        raise InvalidArgumentException('payload.factoids can not be empty')


def _check_add_factoids_payload(payload):
    """
    check add factoids payload
    :param payload:
    :return:
    """
    if not isinstance(payload, dict):
        raise InvalidArgumentException('payload can not be empty')
    if payload.get('ano') is None:
        raise InvalidArgumentException('payload.ano can not be empty')
    if payload.get('factoids') is None:
        raise InvalidArgumentException('payload.factoids can not be empty')


def _check_apply_ca_payload(payload):
    """
    check apply ca payload
    :param payload:
    :return:
    """
    if not isinstance(payload, dict):
        raise InvalidArgumentException('payload can not be empty')
    if payload.get('type') is None:
        raise InvalidArgumentException('payload.type can not be empty')
    if payload['type'] == 'ENTERPRISE':
        if payload.get('name') is None:
            raise InvalidArgumentException('payload.name can not be empty')
        if payload.get('ic_code') is None:
            raise InvalidArgumentException('payload.ic_code can not be empty')
        if payload.get('org_code') is None:
            raise InvalidArgumentException('payload.org_code can not be empty')
        if payload.get('tax_code') is None:
            raise InvalidArgumentException('payload.tax_code can not be empty')
    if payload.get('link_name') is None:
        raise InvalidArgumentException('payload.link_name can not be empty')
    if payload.get('link_id_card') is None:
        raise InvalidArgumentException('payload.link_id_card can not be empty')
    if payload.get('link_phone') is None:
        raise InvalidArgumentException('payload.link_phone can not be empty')
    if payload.get('link_email') is None:
        raise InvalidArgumentException('payload.link_email can not be empty')


def _check_seal(seal):
    if not isinstance(seal, dict):
        raise InvalidArgumentException('seal can not be null when ca type is enterprise')
    filename = seal.get('resource_name')
    if not isinstance(filename, str):
        raise InvalidArgumentException('seal file name must be like xxx.png or xxx.jpg')
    file_type = filename[filename.index('.') + 1:]
    if file_type != 'jpg' and file_type != 'png':
        raise InvalidArgumentException('seal file name must be like xxx.png or xxx.jpg')


def _build_check_sum(payload, attachments):
    """
    build check sum
    :param payload:
    :param attachments:
    :return:
    """
    payload_attachments = {}
    if isinstance(attachments, dict):
        signs = None
        if 'signs' in payload:
            signs = payload['signs']
            payload.pop('signs')
        factoids = payload['factoids']
        factoids_count = 0
        if isinstance(factoids, list):
            factoids_count = len(factoids)
        for i in range(factoids_count):
            i_attachments = attachments.get(i)
            i_signs = signs.get(i)
            if isinstance(i_attachments, list):
                objects = []
                for j in range(len(i_attachments)):
                    j_attachment = i_attachments[j]
                    checksum = utils.checksum(j_attachment['resource'])
                    j_signs = None
                    if isinstance(i_signs, dict):
                        j_signs = i_signs.get(j)
                    if not isinstance(j_signs, dict):
                        objects.append(checksum)
                    else:
                        objects.append({
                            'checksum': checksum,
                            'sign': j_signs
                        })
                payload_attachments[i] = objects
    return payload_attachments


def _build_stream_body_map(attachments):
    """
    build stream body map
    :param attachments:
    :return:
    """
    multipart_files = {}
    if isinstance(attachments, dict):
        for i in attachments.keys():
            multipart_files['attachments[%s][]' % i] = attachments[i]
    return multipart_files


class BaoquanClient(object):
    def __init__(self):
        self.host = 'https://baoquan.com'
        self.version = 'v1'
        self.access_key = None
        self._request_id_generator = uuid.uuid4
        self.pem_path = None

    @property
    def request_id_generator(self):
        return self._request_id_generator

    @request_id_generator.setter
    def request_id_generator(self, request_id_generator):
        assert request_id_generator is not None
        self._request_id_generator = request_id_generator

    def create_attestation(self, payload, attachments=None):
        """
        create attestation with attachments, one factoid can have more than one attachments
        :param payload:
        :param attachments:
        :return:
        :raise: ServerException
        """
        _check_create_attestation_payload(payload)
        payload['attachments'] = _build_check_sum(payload, attachments)
        stream_body_map = _build_stream_body_map(attachments)
        return self._post('attestations', payload, stream_body_map)

    def add_factoids(self, payload, attachments=None):
        """
        add factoids to attestation with attachments, one factoid can have more than one attachments
        :param payload:
        :param attachments:
        :return:
        :raise: ServerException
        """
        _check_add_factoids_payload(payload)
        payload['attachments'] = _build_check_sum(payload, attachments)
        stream_body_map = _build_stream_body_map(attachments)
        return self._post('factoids', payload, stream_body_map)

    def apply_ca(self, payload, seal=None):
        """
        apply ca
        :param payload:
        :param seal:
        :return:
        :raise: ServerException
        """
        _check_apply_ca_payload(payload)
        if payload['type'] == 'ENTERPRISE':
            _check_seal(seal)
        stream_body_map = None
        if seal is not None:
            stream_body_map = {
                'seal': [seal]
            }
        return self._post('cas', payload, stream_body_map)

    def _post(self, api_name, payload, attachments):
        """
        post
        :param api_name:
        :param payload:
        :param attachments:
        :return:
        :raise: ServerException
        """
        assert self.access_key is not None
        assert self.pem_path is not None
        path = '/api/%s/%s' % (self.version, api_name)
        request_id = str(self.request_id_generator())
        tonce = int(datetime.datetime.now().timestamp())
        payload_json = json.dumps(payload)
        # build the data to sign
        sign_data = 'POST' + path + request_id + self.access_key + str(tonce) + payload_json
        signature = utils.sign(self.pem_path, sign_data)
        post_data = {
            'request_id': request_id,
            'access_key': self.access_key,
            'tonce': tonce,
            'payload': payload_json,
            'signature': signature
        }
        # build post request
        uri = self.host + path
        files = []
        if isinstance(attachments, dict):
            for name in attachments.keys():
                if isinstance(attachments[name], list):
                    for item in attachments[name]:
                        files.append((name, (item['resource_name'], item['resource'], item['resource_content_type'])))
        response = requests.post(uri, data=post_data, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            response_json = response.json()
            raise ServerException(request_id, response_json['message'], response_json['timestamp'])
