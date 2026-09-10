# Tarea 3: Miner de Vulnerabilidades para Organizaciones de GitHub

Herramienta de línea de comandos (CLI) en Python para automatizar el análisis estático de seguridad con CodeQL sobre los repositorios de una organización de GitHub.

El miner consulta la REST API de GitHub (manejando paginación y límites de tasa), clona los repositorios localmente, crea bases de datos CodeQL, ejecuta reglas de seguridad, procesa los archivos SARIF y consolida los resultados en un reporte JSON estructurado mediante Pydantic.

## Requisitos Previos

* Python 3.9 o superior.
* Git y CodeQL CLI instalados y configurados en las variables de entorno (`PATH`).
* GitHub Personal Access Token con permisos de lectura.

## Instalación y Configuración

1. **Clonar el repositorio e ingresar a la carpeta:**
   `git clone https://github.com/bescobar04-ui/tarea3-miner.git`
   `cd tarea3-miner`

2. **Crear y activar el entorno virtual:**
   `python -m venv .venv`
   `.\.venv\Scripts\activate`

3. **Instalar el paquete y sus dependencias:**
   `pip install -e .`

4. **Configurar el token de GitHub:**
   Copia `.env.example` a `.env` y asigna tu credencial:
   `GITHUB_TOKEN=tu_token_de_github`

## Uso

Para ejecutar el escaneo de una organización:
`python -m miner scan --organization pallets-eco --output result.json`

## Pruebas

Para correr las pruebas unitarias:
`pytest`

## Estructura del Proyecto

* `src/miner/cli.py`: Interfaz de línea de comandos con Typer.
* `src/miner/github_api.py`: Cliente de la API de GitHub con autenticación y paginación.
* `src/miner/git_utils.py`: Gestión de clonación remota de repositorios.
* `src/miner/codeql.py`: Ejecución automatizada de comandos de CodeQL CLI.
* `src/miner/sarif_parser.py`: Extracción y mapeo de hallazgos desde archivos SARIF.
* `src/miner/models.py`: Modelos y esquemas de datos validados con Pydantic.
* `tests/`: Pruebas unitarias ejecutadas con `pytest`.
