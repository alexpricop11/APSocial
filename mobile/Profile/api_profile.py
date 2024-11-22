import requests


class APIProfile:
    BASE_URL = 'http://127.0.0.1:8000'

    def get_user_profile(self, token):
        url = f'{self.BASE_URL}/profile'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        return response

    def edit_user_profile(self, token, data):
        url = f'{self.BASE_URL}/edit-profile'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.put(url, data=data, headers=headers)
        return response

    def change_password(self, token, data):
        url = f'{self.BASE_URL}/change-password'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, data=data, headers=headers)
        return response

    def his_profile(self, token, user_id):
        url = f'{self.BASE_URL}/profile/{user_id}/'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        return response

    def following_user(self, token, data):
        url = f'{self.BASE_URL}/following-user'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, headers=headers, data=data)
        return response
