import subprocess
from pathlib import Path

SUPPORTED_LANGUAGES = {"python", "javascript", "go", "java", "ruby", "csharp", "cpp", "c", "swift"}

def get_codeql_language(github_language: str) -> str:
    if not github_language:
        return None
    lang_lower = github_language.lower()
    return lang_lower if lang_lower in SUPPORTED_LANGUAGES else None

def create_database(repo_dir: Path, db_dir: Path, language: str) -> bool:
    try:
        subprocess.run(
            [
                "codeql", "database", "create", str(db_dir),
                f"--language={language}",
                f"--source-root={repo_dir}",
                "--overwrite"
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n--- ERROR AL CREAR BD ---\n{e.stderr}\n-------------------------")
        return False

def analyze_database(db_dir: Path, output_sarif: Path, language: str) -> bool:
    # AQUÍ ESTÁ LA MAGIA: Le pasamos el paquete de reglas exacto que necesita
    query_pack = f"codeql/{language}-queries"
    
    cmd = [
        "codeql", "database", "analyze", str(db_dir),
        query_pack,  # <--- Este es el parámetro que pedía el error
        "--format=sarif-latest",
        f"--output={output_sarif}",
        "--download"
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n--- DETALLE DEL ERROR DE CODEQL ---\n{e.stderr}\n-----------------------------------")
        return False