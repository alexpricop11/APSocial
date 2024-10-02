import requests


class APIAuth:
    BASE_URL = 'http://127.0.0.1:8000'

    def register(self, data):
        url = f'{self.BASE_URL}/register'
        response = requests.post(url, data=data)
        return response

    def login(self, data):
        url = f'{self.BASE_URL}/login'
        response = requests.post(url, data=data)
        return response

    def reset_password(self, data):
        url = f'{self.BASE_URL}/reset-password'
        response = requests.post(url, data=data)
        return response

    def verify_code(self, data):
        url = f'{self.BASE_URL}/verify-code'
        response = requests.post(url, data=data)
        return response
