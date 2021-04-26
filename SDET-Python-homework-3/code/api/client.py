import json
import logging
from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict
from api.urls import URLS
from api.headers import HEADERS


logger = logging.getLogger('test')

MAX_RESPONSE_LENGTH = 500


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None

    @staticmethod
    def log_pre(method, url, headers, data, expected_status):
        logger.info(f'Performing {method} request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n\n'
                    f'expected status: {expected_status}\n\n')

    @staticmethod
    def log_post(response):
        log_str = 'Got response:\n' \
                  'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n')
            elif logger.level == logging.DEBUG:
                logger.debug(f'{log_str}\n'
                             f'RESPONSE CONTENT: {response.text}\n\n')
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n\n')

    def _request(self, method, url, headers=None, data=None, expected_status=200, jsonify=True):

        self.log_pre(method, url, headers, data, expected_status)
        response = self.session.request(method, url, headers=headers, data=data)
        self.log_post(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
                                              f'Expected status_code: {expected_status}.')

        if jsonify:
            json_response = response.json()
            if json_response.get('bStateError'):
                error = json_response.get('bErrorMsg', 'Unknown')
                raise ResponseErrorException(f'Request "{url}" return error "{error}"!')
            return json_response
        return response

    def get_token(self):
        headers = self._request('GET', self.base_url, jsonify=False).headers['Set-Cookie'].split(';')
        token_header = [h for h in headers if 'csrftoken' in h]
        if not token_header:
            raise Exception('CSRF token not found in main page headers')

        token_header = token_header[0]
        token = token_header.split('=')[-1]
        self.csrf_token = token
        return token

    def post_login(self, user, password):
        response = self.session.get(URLS.MAIN_PAGE)
        response = self.session.get(URLS.SESSION)
        response = self.session.get(URLS.SETTINGS)
        data = {
            'email': user,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        response = self.session.request('POST', URLS.AUTH, data=data, headers=HEADERS.headers_auth(self))
        response = self.session.get(URLS.LOGIN)
        response = self.session.get(URLS.MAIN_PAGE)
        try:
            self.csrf_token = self.get_token(response)
            print(self.csrf_token)
        except Exception as e:
            raise InvalidLoginException(e)
        return response

    def get_token(self, response):
        head = self.session.get(URLS.CSRF).headers['Set-Cookie'].split(';')
        token_header = [h for h in head if 'csrftoken' in h]
        token_header = token_header[0]
        token = token_header.split('=')[-1]
        return token

    def post_create_company(self, name):
        response = self.session.get(URLS.SEGMENTS_LIST)
        img_id = self.post_send_file()
        contents = open('data.json', 'rb').read()
        dictData = json.loads(contents)
        dictData["name"] = name
        url_id = self.get_url_id('mail.ru')
        dictData['banners'][0]['urls']['primary']['id'] = url_id
        dictData['banners'][0]['content']['image_240x400']['id'] = img_id

        response = self.session.request('POST', URLS.CAMPAGINS, json=dictData, headers=HEADERS.headers_create_campagin(self))
        print(response.text)
        id = response.text.split(':')
        id = id[3].replace('}', '').replace(' ', '')
        print(id)
        return id

    def post_send_file(self):
        files = {'file': open('../test_api/image.jpg', 'rb'),
                 "width":0, "height":0}
        response = self.session.request('POST', URLS.UPLOAD, files=files, headers=HEADERS.headers_upload(self))
        id = response.text
        id = id.split(',')
        id = id[0].split(' ')
        print(response.text)
        print(id[1])
        data = {"description": "image.jpg",
                "content":
                    {"id": int(id[1])}
                }
        response = self.session.request('POST', URLS.MEDIATEKA, json=data, headers=HEADERS.headers_mediateka(self))
        return id[1]

    def get_url_id(self, url):
        response = self.session.get(URLS.URL_ID + url)
        dictData = json.loads(response.text)
        return dictData["id"]


    def post_delete_company(self, id):
        data = [{
            'id': int(id),
            'status': 'deleted'
        }]
        response = self.session.request('POST', URLS.DELETE_CAMPAGIN, data=data, headers=HEADERS.headers_delete_campagin(self))
        return response

    def post_create_segment(self, name):
        contents = open('segment.json', 'rb').read()
        dictData = json.loads(contents)
        dictData["name"] = name
        response = self.session.request('POST', URLS.CREATE_SEGMENT, json=dictData, headers=HEADERS.headers_create_segment(self))
        jsonData = response.text
        dictData = json.loads(jsonData)
        id = int(dictData["id"])
        return id

    def post_delete_segment(self, id):
        data = [
        {
            "source_id": id,
            "source_type": "segment"
        }
        ]
        response = self.session.request('POST', URLS.DELETE_SEGMENT, json=data, headers=HEADERS.headers_delete_segment(self))
        return response

    def get_segments(self):
        response = self.session.get(URLS.SEGMENTS)
        return response.json()

    def get_campagins(self):
        response = self.session.get(URLS.CAMAPAGINS_LIST)
        return response.json()



