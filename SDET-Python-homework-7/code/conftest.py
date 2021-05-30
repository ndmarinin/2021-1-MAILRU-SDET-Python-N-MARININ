import logging
import os
import signal
import subprocess
import time
from copy import copy

import pytest
import requests
from requests.exceptions import ConnectionError

import settings

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))  # code

env = copy(os.environ)
env['APP_HOST'] = settings.APP_HOST
env['APP_PORT'] = settings.APP_PORT

env['STUB_HOST'] = settings.STUB_HOST
env['STUB_PORT'] = settings.STUB_PORT

env['MOCK_HOST'] = settings.MOCK_HOST
env['MOCK_PORT'] = settings.MOCK_PORT


def start_app(config):
    app_path = os.path.join(repo_root, 'app', 'app.py')

    app_out = open(os.path.join(repo_root, 'tests', 'app_stdout.log'), 'w')
    app_err = open(os.path.join(repo_root, 'tests', 'app_stderr.log'), 'w')

    print(app_path)
    proc = subprocess.Popen(['py', app_path], stdout=app_out, stderr=app_err, env=env)

    config.app_proc = proc
    config.app_out = app_out
    config.app_err = app_err

    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{settings.APP_HOST}:{settings.APP_PORT}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError('App did not started in 5s!')


def start_stub(config):
    #stub_path = os.path.join(repo_root, 'stub', 'flask_stub.py')
    stub_path = os.path.join(repo_root, 'stub', 'simple_http_server_stub.py')
    stub_out = open(os.path.join(repo_root, 'tests', 'stub_stdout.log'), 'w')
    stub_err = open(os.path.join(repo_root, 'tests', 'stub_stderr.log'), 'w')

    proc = subprocess.Popen(['py', stub_path], stdout=stub_out, stderr=stub_err, env=env)

    config.stub_proc = proc
    config.stub_out = stub_out
    config.stub_err = stub_err

    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{settings.STUB_HOST}:{settings.STUB_PORT}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError('Stub did not started in 5s!')


def start_mock():
    from mock import flask_mock
    flask_mock.run_mock()
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError('Mock did not started in 5s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        start_mock()
        start_stub(config)
        start_app(config)


def stop_app(config):
    config.app_proc.send_signal(signal.CTRL_BREAK_EVENT)
    exit_code = config.app_proc.wait()

    config.app_out.close()
    config.app_err.close()

    assert exit_code == 0


def stop_stub(config):
    config.stub_proc.send_signal(signal.CTRL_BREAK_EVENT)
    config.stub_proc.wait()

    config.stub_out.close()
    config.stub_err.close()


def stop_mock():
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_app(config)
        stop_stub(config)
        stop_mock()


@pytest.fixture(scope='session', autouse=True)
def logger():
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(os.path.join(repo_root, "tests"), 'test.log')

    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
