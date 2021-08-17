import json
import logging
import random
import string
from urllib.parse import urljoin
import requests

LOGGER = logging.getLogger('test')

class ApiClient:
    GET = "GET"
    POST = "POST"

    def __init__(self, host, port):
        self.session = requests.Session()
        self.host = host
        self.port = port
        self.url = "http://" + self.host + ":" + str(self.port)
        self.cookies = None

    def auth(self, username, password):
        location = "/login"
        content_type = "application/x-www-form-urlencoded"
        connection = "keep-alive"
        headers = {
            'Content-Type': content_type,
            'Connection': connection
        }
        body = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }
        response = self._request(method=self.POST, location=location, headers=headers, data=body)
        self.cookies = response.headers['Set-Cookie'].split(';')[0]
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def add_user(self, username, password, email):
        location = "/api/add_user"
        content_type = "application/json"

        headers = {
            'Content-Type': content_type,
            'Cookie': self.cookies
        }

        body = {
            'username': username,
            'password': password,
            'email': email
        }
        body = json.dumps(body)
        response = self._request(method=self.POST, location=location, headers=headers, data=body)
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def delete_user(self, username):
        location = "/api/del_user/" + username
        response = self._request(method=self.GET, location=location)
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def block_user(self, username):
        location = "/api/block_user/" + username
        response = self._request(method=self.GET, location=location)
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def unblock_user(self, username):
        location = "/api/accept_user/" + username
        response = self._request(method=self.GET, location=location)
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def status(self):
        location = "/status"
        response = self._request(method=self.GET, location=location)
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def logout(self):
        location = "/logout"
        response = self._request(method=self.GET, location=location)
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def go_to_random_url(self):
        letters = string.ascii_lowercase
        location = "/"
        add_str = ''.join(random.choice(letters) for i in range(5))
        location = location + add_str
        LOGGER.info("Go to", location)
        response = self._request(method=self.GET, location=location)
        LOGGER.info(response.headers)
        LOGGER.info(response.status_code)
        LOGGER.info(response.text)
        return response

    def _request(self, method, url=None, location=None, headers=None, params=None, data=None, json=False,
                 allow_redirects=False):
        if location is not None and url is None:
            url = urljoin(self.url, location)

        res = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            allow_redirects=allow_redirects
        )
        LOGGER.info(res.headers)
        LOGGER.info(res.status_code)
        LOGGER.info(res.text)
        if json:
            return res.json()
        else:
            return res


if __name__ == '__main__':
    api = ApiClient(host='myapp', port=8080)
