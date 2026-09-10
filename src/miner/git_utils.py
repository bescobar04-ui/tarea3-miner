import subprocess
import shutil
from pathlib import Path

def cleanup_directory(directory: Path) -> None:
    """
    Elimina un directorio y todo su contenido. 
    Útil para limpiar los repositorios clonados.
    """
    if directory.exists() and directory.is_dir():
        shutil.rmtree(directory, ignore_errors=True)

def clone_repository(repo_url: str, target_dir: Path) -> bool:
    """
    Clona un repositorio git. Retorna True si es exitoso, False si falla.
    """
    # PREVENCIÓN: Si la carpeta quedó de un intento cancelado anterior, la borramos.
    cleanup_directory(target_dir)
    
    try:
        subprocess.run(
            ["git", "clone", repo_url, str(target_dir)],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False