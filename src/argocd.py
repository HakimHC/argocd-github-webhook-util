import os
import requests
from functools import wraps


def auth_header(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        headers = kwargs.get('headers', {})
        default_headers = {'Authorization': f'Bearer {self._token}'}
        headers = {**default_headers, **headers}
        kwargs['headers'] = headers
        return func(self, *args, **kwargs)
    return wrapper


class ArgoClientFactory:
    __instance = None

    @staticmethod
    def get_instance():
        if not ArgoClientFactory.__instance:
            return ArgoCDClient()
        return ArgoClientFactory.__instance


class ArgoCDClient:
    def __init__(self):
        self.__username = os.getenv('ARGOCD_USERNAME', "")
        self.__password = os.getenv('ARGOCD_PASSWORD', "")

        # TODO: Validate and sanitize the host (protocol scheme, etc)
        self.__argocd_api_url = os.getenv('ARGOCD_API_URL', "")
        if not self.__argocd_api_url:
            raise ArgoCDClient.EmptyApiUrlError('The ArgoCD API URL was not set.')
        self._token = os.getenv('ARGOCD_API_TOKEN') or self.__get_token()

    def user_info(self):
        response = self.__get('/api/v1/session/userinfo')
        if response.get('error'):
            return {}
        return response.get('username')

    def list_applications(self) -> list[str]:
        response = self.__get('/api/v1/applications')
        items = response.get('items', [])
        return [item['metadata']['name'] for item in items]

    def refresh_application(self, application: str) -> None:
        applications = self.list_applications()
        if application not in applications:
            raise ArgoCDClient.NonExistentApplicationError(f'Application "{application}" does not exist.')
        response = self.__get(
            endpoint=f'/api/v1/applications/{application}',
            params={'refresh': 'true'}
        )
        error = response.get('error')
        if error:
            raise ArgoCDClient.SyncError(error)

    def sync_application(self, application: str) -> None:
        applications = self.list_applications()
        if application not in applications:
            raise ArgoCDClient.NonExistentApplicationError(f'Application "{application}" does not exist.')
        response = self.__post(
            endpoint=f'/api/v1/applications/{application}/sync',
            json={'name': application}
        )
        error = response.get('error')
        if error:
            raise ArgoCDClient.SyncError(error)

    def __get_token(self) -> str:
        """
        Authenticates against the ArgoCD API with a username and password.
        :return: Bearer token
        """
        response = requests.post(
            url=f'{self.__argocd_api_url}/api/v1/session',
            json={
                'username': self.__username,
                'password': self.__password
            }
        )
        response_json = response.json()
        if response.status_code != 200:
            raise ArgoCDClient.InvalidCredentialsError(
                response_json.get('error') or
                response_json.get('message')
            )
        return response_json['token']

    @auth_header
    def __get(self, endpoint: str, **kwargs):
        url = f'{self.__argocd_api_url}/{endpoint}'
        response = requests.get(url, **kwargs)
        return response.json()

    @auth_header
    def __post(self, endpoint: str, json: dict, **kwargs):
        url = f'{self.__argocd_api_url}/{endpoint}'
        response = requests.post(url, json=json, **kwargs)
        return response.json()

    class InvalidCredentialsError(Exception):
        def __init__(self, message):
            super().__init__(message)

    class InvalidApiUrlError(Exception):
        def __init__(self, message):
            super().__init__(message)

    class EmptyApiUrlError(Exception):
        def __init__(self, message):
            super().__init__(message)

    class NonExistentApplicationError(Exception):
        def __init__(self, message):
            super().__init__(message)

    class SyncError(Exception):
        def __init__(self, message):
            super().__init__(message)
