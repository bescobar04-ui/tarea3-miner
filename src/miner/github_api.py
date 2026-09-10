import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

def get_repositories(organization: str, token: str = None) -> List[Dict[str, Any]]:
    """
    Obtiene todos los repositorios de una organización de GitHub manejando la paginación.
    """
    # Si no se pasa el token como parámetro, se busca en las variables de entorno
    token = token or os.getenv("GITHUB_TOKEN")
    
    if not token:
        raise ValueError("Error: No se encontró GITHUB_TOKEN en el archivo .env")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repositories = []
    page = 1
    per_page = 100

    # Bucle para manejar la paginación de la API de GitHub
    while True:
        url = f"https://api.github.com/orgs/{organization}/repos?per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise RuntimeError(f"Error de GitHub ({response.status_code}): {response.text}")
            
        data = response.json()
        
        # Si la página ya no trae más elementos, terminamos la consulta
        if not data:
            break
            
        for repo in data:
            repositories.append({
                "name": repo.get("name"),
                "clone_url": repo.get("clone_url"),
                "language": repo.get("language")
            })
            
        page += 1

    return repositories