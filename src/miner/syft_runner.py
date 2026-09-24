import json
import subprocess
from pathlib import Path
from typing import Tuple


def get_syft_version() -> str:
    """Obtiene la versión instalada de Syft en el sistema."""
    try:
        result = subprocess.run(
            ["syft", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "Unknown"


def generate_sbom(repo_dir: Path, output_file: Path) -> Tuple[bool, int, str]:
    """
    Ejecuta Syft sobre el directorio local de un repositorio.
    Genera un SBOM en formato CycloneDX JSON.
    Retorna: (exito: bool, cantidad_componentes: int, error_msg: str)
    """
    try:
        # Comando Syft para escanear directorio y exportar a CycloneDX JSON
        cmd = [
            "syft",
            f"dir:{repo_dir}",
            "-o", "cyclonedx-json",
            "--file", str(output_file)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return False, 0, f"Error al ejecutar Syft: {result.stderr.strip()}"

        if not output_file.exists():
            return False, 0, "El archivo SBOM no fue generado por Syft."

        # Abrir el JSON generado para contar cuántos componentes detectó
        with open(output_file, "r", encoding="utf-8") as f:
            sbom_data = json.load(f)

        components = sbom_data.get("components", []) or []
        return True, len(components), ""

    except Exception as e:
        return False, 0, str(e)