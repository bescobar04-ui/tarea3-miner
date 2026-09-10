# Tarea 3: Miner de Vulnerabilidades para Organizaciones de GitHub

Herramienta de línea de comandos (CLI) en Python para automatizar el análisis estático de seguridad con CodeQL sobre los repositorios de una organización de GitHub.
El miner consulta la REST API de GitHub (manejando paginación y límites de tasa), clona los repositorios localmente, crea bases de datos CodeQL, ejecuta reglas de seguridad, procesa los archivos SARIF y consolida los resultados en un reporte JSON estructurado mediante Pydantic.

## Requisitos Previos
* Python 3.9 o superior.
* Git y CodeQL CLI instalados y configurados en las variables de entorno (`PATH`).
* GitHub Personal Access Token con permisos de lectura.

## Instalación y Configuración
1. Clonar el repositorio e ingresar a la carpeta:
   git clone https://github.com/bescobar04-ui/tarea3-miner.git
   cd tarea3-miner

2. Crear y activar el entorno virtual:
   python -m venv .venv
# En Windows (PowerShell):
.\.venv\Scripts\activate
# En Linux/macOS:
source .venv/bin/activate

3. Instalar el paquete y sus dependencias:
   pip install -e .

4. Crear el archivo `.env` en la raíz con el token de GitHub:
   Configurar el archivo .env con el token
cp .env.example .env
Luego abre .env y coloca tu token: GITHUB_TOKEN=tu_token_aqui

## Uso
Para ejecutar el escaneo de una organización:
python -m miner scan --organization pallets-eco --output result.json

## Pruebas
Para correr las pruebas unitarias:
pytest


