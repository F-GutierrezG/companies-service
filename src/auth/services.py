import json
import requests

from flask import request, current_app


class AuthService:
    def status(self, token):
        url = '{0}/auth/status'.format(current_app.config['AUTH_SERVICE_URL'])
        bearer = request.headers.get('Authorization')
        headers = {'Authorization': bearer}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return response, data
