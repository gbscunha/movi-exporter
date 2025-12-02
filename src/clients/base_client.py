import requests

class BaseClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get(self, path: str, params=None):
        url = f"{self.base_url}/{path}"
        response = requests.get(url, headers=self._headers(), params=params)

        if response.status_code != 200:
            raise Exception(f"Erro na requisição GET {url}: {response.text}")

        return response.json()
