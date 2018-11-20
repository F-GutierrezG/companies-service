import json
import requests

from functools import wraps
from flask import request, jsonify, current_app


def forbidden(message='forbidden'):
    return jsonify({'message': message}), 403


def parse_token(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return False

    token_parts = auth_header.split(' ')

    if len(token_parts) != 2:
        return False

    return token_parts[1]


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def authenticate_mock():
    return {
        'id': 1,
        'first_name': 'Francisco',
        'last_name': 'Gutiérrez',
        'email': 'valid@test.com'
    }


def authenticate_production(token):
    url = '{0}/auth/status'.format(current_app.config['USERS_SERVICE_URL'])
    bearer = 'Bearer {0}'.format(token)
    headers = {'Authorization': bearer}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return response, data


def do_authenticate(f, *args, **kwargs):
    token = parse_token(request)

    if token is False:
        return forbidden()

    response, data = authenticate_production(token)
    if response.status_code == 200:
        user = User(data)
        return f(user, *args, **kwargs)
    else:
        return forbidden()


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_app.config['USERS_SERVICE_MOCK']:
            user = authenticate_mock()
            return f(user, *args, **kwargs)

        else:
            return do_authenticate(f, *args, **kwargs)
    return decorated_function
