import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno (opcional, si configuras la URL base en un .env)
load_dotenv()

class APIClient:
    def __init__(self):
        # Se obtiene la URL base desde variables de entorno o se utiliza un valor por defecto
        self.base_url = os.getenv("API_BASE_URL")

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()

# Instancia global para utilizar en otros módulos
api_client = APIClient()
