import os

import pytest
import requests
import settings
import socket
import json
import logging

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'

LOGGER = logging.getLogger('test')

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))  # code
HOST = settings.APP_HOST
PORT = settings.APP_PORT_INT

class Base:

    def post_add_user(self, name):
        DATA_POST = json.dumps({'name': name})
        DATA_LEN = str(len(DATA_POST))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init TCP socket type
        s.connect((HOST, PORT))
        send_string = "POST /add_user HTTP/1.1\r\nHost: " + HOST + ":" + settings.APP_PORT + "\r\nContent-Type: application/json\r\nContent-Length: " + DATA_LEN + "\r\n\r\n" + DATA_POST
        send_as_bytes = str.encode(send_string)
        s.send(send_as_bytes)  # send DATA to server
        total_data = []
        while True:
            data = s.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                s.close()
                break
        data = ''.join(total_data).splitlines()
        status = data[0].split(' ')
        status = int(status[1])
        LOGGER.info(status)
        LOGGER.info(data[1:5])
        data = json.loads(data[-1])
        LOGGER.info(data)
        return status, data

    def get_user(self, name):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((HOST, PORT))
        params = f'/get_user/{name}'
        request = f'GET {params} HTTP/1.1\r\nHost:{HOST}\r\n\r\n'
        client.send(request.encode())
        total_data = []
        while True:
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                client.close()
                break

        data = ''.join(total_data).splitlines()
        status = data[0].split(' ')
        status = int(status[1])
        LOGGER.info(status)
        LOGGER.info(data[1:5])
        data = json.loads(data[-1])
        LOGGER.info(data)
        return status, data

    def put_update_user(self, name, surname):
        DATA_POST = json.dumps({'surname': surname})
        DATA_LEN = str(len(DATA_POST))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init TCP socket type
        s.connect((HOST, PORT))
        params = f'/update_user/{name}'
        request = f'PUT {params} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\nContent-Type: application/json\r\nContent-Length: {DATA_LEN}\r\n\r\n{DATA_POST}'
        s.send(request.encode())
        total_data = []
        while True:
            data = s.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                s.close()
                break
        data = ''.join(total_data).splitlines()
        status = data[0].split(' ')
        status = int(status[1])
        LOGGER.info(status)
        LOGGER.info(data[1:5])
        data = json.loads(data[-1])
        LOGGER.info(data)
        return status, data

    def delete_user(self, name):
        DATA_POST = json.dumps({'name': name})
        DATA_LEN = str(len(DATA_POST))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init TCP socket type
        s.connect((HOST, PORT))
        params = f'/delete_user/{name}'
        request = f'DELETE {params} HTTP/1.1\r\nHost:{HOST}\r\n\r\n'
        s.send(request.encode())
        total_data = []
        while True:
            data = s.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                s.close()
                break
        data = ''.join(total_data).splitlines()
        print(data)
        status = data[0].split(' ')
        status = int(status[1])
        LOGGER.info(status)
        LOGGER.info(data[1:5])
        data = json.loads(data[-1])
        LOGGER.info(data)
        return status, data

    def shutdown_server(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        client.connect((HOST, PORT))
        params = '/shutdown'
        request = f'GET {params} HTTP/1.1\r\nHost:{HOST}\r\n\r\n'
        client.send(request.encode())
        total_data = []
        while True:
            data = client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                client.close()
                break

        data = ''.join(total_data).splitlines()
        status = data[0].split(' ')
        status = int(status[1])
        LOGGER.info(status)
        LOGGER.info(data[1:5])
        data = json.loads(data[-1])
        LOGGER.info(data)
        return status, data

    def delete_surname(self, name):
        DATA_POST = json.dumps({'name': name})
        DATA_LEN = str(len(DATA_POST))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # init TCP socket type
        s.connect((HOST, PORT))
        params = f'/delete_surname/{name}'
        request = f'DELETE {params} HTTP/1.1\r\nHost:{HOST}\r\n\r\n'
        s.send(request.encode())
        total_data = []
        while True:
            data = s.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                s.close()
                break
        data = ''.join(total_data).splitlines()
        print(data)
        status = data[0].split(' ')
        status = int(status[1])
        LOGGER.info(status)
        LOGGER.info(data[1:5])
        data = json.loads(data[-1])
        LOGGER.info(data)
        return status, data