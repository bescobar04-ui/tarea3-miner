import os
import typer
from pathlib import Path
from dotenv import load_dotenv

# Importamos nuestros módulos locales
from . import github_api, git_utils, codeql, sarif_parser
from .models import OrganizationResult, Summary, Repository

# Inicializamos la app de Typer
app = typer.Typer(help="Miner de vulnerabilidades para organizaciones de GitHub mediante CodeQL.")

@app.callback()
def main():
    pass

@app.command()
def scan(
    organization: str = typer.Option(..., help="Nombre de la organización en GitHub"),
    output: Path = typer.Option(..., help="Ruta del archivo JSON resultante")
):
    """
    Escanea los repositorios de una organización buscando vulnerabilidades con CodeQL.
    """
    # 1. Cargar variables de entorno y validar el token
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        typer.secho("Error: No se encontró la variable GITHUB_TOKEN en el entorno.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(f"Iniciando escaneo para la organización: {organization}")

    # 2. Obtener repositorios desde GitHub
    try:
        github_repos = github_api.get_repositories(organization, token)
    except Exception as e:
        typer.secho(f"Error al consultar la API de GitHub: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not github_repos:
        typer.secho("No se encontraron repositorios o la organización no existe.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=0)

    typer.echo(f"¡Éxito! Se encontraron {len(github_repos)} repositorios.")
    
    # Ordenar repositorios alfabéticamente como pide la rúbrica
    github_repos.sort(key=lambda r: r.get("name", "").lower())

    # Inicializar contadores para el Summary
    summary = Summary(repositories=len(github_repos))
    processed_repos = []

    # Directorios temporales de trabajo
    tmp_dir = Path("./tmp_miner")
    tmp_dir.mkdir(exist_ok=True)

    # 3. Iterar y procesar cada repositorio
    for repo_data in github_repos:
        repo_name = repo_data.get("name")
        repo_url = repo_data.get("clone_url")
        github_lang = repo_data.get("language")
        
        typer.echo(f"\nProcesando: {repo_name}...")
        
        repo_model = Repository(name=repo_name, url=repo_url, status="pending")
        
        # Verificar si el lenguaje está soportado
        codeql_lang = codeql.get_codeql_language(github_lang)
        if not codeql_lang:
            typer.secho(f"  -> Omitido: Lenguaje '{github_lang}' no soportado por CodeQL.", fg=typer.colors.YELLOW)
            repo_model.status = "unsupported"
            if github_lang:
                repo_model.languages.append(github_lang)
            summary.unsupported += 1
            processed_repos.append(repo_model)
            continue
            
        repo_model.languages.append(codeql_lang)
        
        # Rutas temporales específicas para este repositorio
        repo_path = tmp_dir / repo_name
        db_path = tmp_dir / f"{repo_name}_db"
        sarif_path = tmp_dir / f"{repo_name}.sarif"

        try:
            # Clonar
            if not git_utils.clone_repository(repo_url, repo_path):
                typer.secho("  -> Error: No se pudo clonar el repositorio.", fg=typer.colors.RED)
                repo_model.status = "clone_error"
                summary.failed += 1
                continue

            # Crear BD de CodeQL
            if not codeql.create_database(repo_path, db_path, codeql_lang):
                typer.secho("  -> Error: Falló la creación de la base de datos CodeQL.", fg=typer.colors.RED)
                repo_model.status = "db_error"
                summary.failed += 1
                continue

            # Analizar BD (Pasando también el lenguaje)
            if not codeql.analyze_database(db_path, sarif_path, codeql_lang):
                typer.secho("  -> Error: Falló el análisis de CodeQL.", fg=typer.colors.RED)
                repo_model.status = "analyze_error"
                summary.failed += 1
                continue

            # Extraer hallazgos
            findings = sarif_parser.parse_sarif_file(sarif_path)
            repo_model.findings = findings
            repo_model.status = "analyzed"
            
            summary.analyzed += 1
            summary.findings += len(findings)
            typer.secho(f"  -> Completado: Se encontraron {len(findings)} vulnerabilidades.", fg=typer.colors.GREEN)

        finally:
            # Se ejecuta siempre para asegurar la limpieza del disco y registro del repositorio
            repo_model.status = repo_model.status if repo_model.status != "pending" else "failed"
            processed_repos.append(repo_model)
            
            git_utils.cleanup_directory(repo_path)
            git_utils.cleanup_directory(db_path)
            if sarif_path.exists():
                sarif_path.unlink()

    # 4. Generar el resultado final validado y exportar a JSON
    git_utils.cleanup_directory(tmp_dir) # Limpieza general final
    
    final_result = OrganizationResult(
        organization=organization,
        summary=summary,
        repositories=processed_repos
    )

    typer.echo(f"\nGuardando resultados en {output}...")
    with open(output, "w", encoding="utf-8") as f:
        f.write(final_result.model_dump_json(indent=2))
        
    typer.secho("¡Proceso finalizado con éxito!", fg=typer.colors.GREEN, bold=True)

if __name__ == "__main__":
    app()