from flask import Flask, request, json, make_response, jsonify
import threading
import requests
import json

app = Flask(__name__)

users = { }
user_id_seq = 1
def run_mock(host, port):
    server = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    server.start()
    return server


def shutdown_mock():
    terminate = request.environ.get('werkzeug.server.shutdown')
    if terminate:
        terminate()


@app.route('/vk_id/<username>', methods=['GET'])
def get_user(username):
    user = users.get(username, None)
    result = {}
    if user:
        result = {'vk_id': user}
        res = make_response(result)
        res.headers['Status'] = '200 OK'
        res.headers['Content-Type'] = 'application/json'
        res.headers['Response'] = result
        return res
    else:
        res = make_response(result)
        res.headers['Status'] = '400 Not Found'
        res.headers['Content-Type'] = 'application/json'
        res.headers['Response'] = result
        return res


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_mock()
    return 'Shutting down...'


@app.route('/add_user', methods=['POST'])
def create_user():
    global user_id_seq
    user_name = json.loads(request.data)['name']
    if user_name not in users:
        users[user_name] = user_id_seq
        data = {'user_id': user_id_seq}
        user_id_seq += 1
        return jsonify(data), 201
    else:
        return jsonify(f'User name {user_name} already exists: id {users[user_name]}'), 400

if __name__ == '__main__':
    run_mock(host='0.0.0.0', port=5000)