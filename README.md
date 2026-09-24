# Miner de Vulnerabilidades y Generación de SBOMs para GitHub

Herramienta de línea de comandos (CLI) desarrollada en Python para automatizar el análisis estático de seguridad con CodeQL y la generación de inventarios de software (SBOM) en formato CycloneDX JSON mediante Syft sobre repositorios de GitHub. Sirve para el desarrollo de la tarea 3 y 4.

---

## Requisitos Previos

- Python 3.9 o superior.
- Git y CodeQL CLI instalados y configurados en las variables de entorno (`PATH`).
- Syft CLI instalado y verificado (`syft --version`).
- GitHub Personal Access Token con permisos de lectura.

---

## Instalación y Configuración

1. **Clonar el repositorio e ingresar al directorio:**
   ```bash
   git clone [https://github.com/bescobar04-ui/tarea3-miner.git](https://github.com/bescobar04-ui/tarea3-miner.git)
   cd tarea3-miner
   ```

2. **Crear y activar el entorno virtual:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar el paquete y sus dependencias en modo editable:**
   ```bash
   pip install -e .
   ```

4. **Configurar el token de GitHub:**
   Copia el archivo `.env.example` creando un archivo `.env` y asigna tu token:
   ```env
   GITHUB_TOKEN=tu_token_de_github_aqui
   ```

---

## Uso de la CLI

### 1. Escaneo de Vulnerabilidades con CodeQL (Tarea 3)
Consulta la API de GitHub, clona repositorios, ejecuta CodeQL, procesa archivos SARIF y genera el reporte consolidado:
```bash
python -m miner scan --organization pallets-eco --output result.json
```

### 2. Generación de SBOMs con Syft (Tarea 4)
Genera inventarios SBOM en formato CycloneDX JSON a partir de repositorios localmente clonados sin repetir CodeQL:
```bash
python -m miner sbom --repos-dir ./tmp_miner --output-dir ./results
```

---

## Estructura de Salida y Resultados (Tarea 4)

Al ejecutar la generación de SBOMs (`miner sbom`), la carpeta `./results` contendrá:

- **`results/sboms/`**: Archivos `.json` individuales en formato CycloneDX por cada repositorio.
- **`results/results_summary.json`**: Reporte general estructurado mediante Pydantic que incluye:
  - `full_name`: Nombre del repositorio.
  - `commit_hash`: Commit exacto analizado.
  - `generated_at`: Fecha y hora UTC.
  - `syft_version`: Versión de Syft utilizada.
  - `status`: Estado de la ejecución (`SUCCESS` o `FAILED`).
  - `component_count`: Cantidad de componentes identificados.
  - `sbom_path`: Ruta del SBOM generado.

### Observaciones de Verificación
- **Diferenciación de Estados:** El sistema distingue entre ejecuciones fallidas (`FAILED`) y ejecuciones exitosas sin componentes (`SUCCESS` con 0 componentes).
- **Inventario de Dependencias:** Syft identifica paquetes mediante archivos manifiesto o de bloqueo (`requirements.txt`, `package.json`, `Pipfile.lock`, etc.). Si un repositorio carece de estos archivos, registrará 0 componentes.

---

## Pruebas Unitarias

Para ejecutar la suite de pruebas automáticas:
```bash
pytest
```
