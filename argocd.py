import os
import requests


class ArgoCD:
    def __init__(self):
        self.__username = os.getenv('ARGOCD_USERNAME')
        self.__password = os.getenv('ARGOCD_PASSWORD')
        self.__argocd_api_url = os.getenv('ARGOCD_API_URL')

        self.__token = self.__get_token()

    def __get_token(self) -> str:
        """
        Authenticates against the ArgoCD API with a username and password.
        :return: Bearer token
        """
        response = requests.post(
            url=f'https://{self.__argocd_api_url}/api/v1/session',
            json={
                'username': self.__username,
                'password': self.__password
            }
        )
        print(f'Response: {response.json()}')
        response_json = response.json()
        if response.status_code != 200:
            raise ArgoCD.InvalidCredentialsError(
                response_json.get('error') or
                response_json.get('message')
            )
        return response_json['token']

    class InvalidCredentialsError(Exception):
        def __init__(self, message):
            super().__init__(message)
