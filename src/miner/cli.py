import json
import subprocess
from datetime import datetime
from pathlib import Path
import typer

from miner.models import SbomMetadata, SbomStatus
from miner.syft_runner import generate_sbom, get_syft_version

app = typer.Typer()


def get_repo_commit_hash(repo_path: Path) -> str:
    """Obtiene el commit actual del repositorio usando git."""
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return "unknown"


@app.command()
def sbom(
    repos_dir: Path = typer.Option(
        ..., "--repos-dir", "-r", help="Ruta a la carpeta con repositorios clonados"
    ),
    output_dir: Path = typer.Option(
        Path("./results"), "--output-dir", "-o", help="Ruta para guardar resultados"
    ),
):
    """Genera inventarios SBOM (CycloneDX JSON) para repositorios previamente clonados."""
    if not repos_dir.exists():
        typer.secho(f"El directorio {repos_dir} no existe.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    output_dir.mkdir(parents=True, exist_ok=True)
    sboms_dir = output_dir / "sboms"
    sboms_dir.mkdir(exist_ok=True)

    syft_ver = get_syft_version()
    summary_results = []

    typer.echo(f"Usando Syft versión: {syft_ver}")
    typer.echo("Iniciando generación de SBOMs...\n")

    for repo_path in repos_dir.iterdir():
        if not repo_path.is_dir():
            continue

        repo_name = repo_path.name
        commit_hash = get_repo_commit_hash(repo_path)

        safe_name = repo_name.replace("/", "_")
        sbom_file = sboms_dir / f"{safe_name}_cyclonedx.json"

        typer.echo(f"Procesando: {repo_name}...")

        success, count, error_msg = generate_sbom(repo_path, sbom_file)

        if success:
            status = SbomStatus.SUCCESS
            typer.secho(f"  [OK] Componentes identificados: {count}", fg=typer.colors.GREEN)
        else:
            status = SbomStatus.FAILED
            typer.secho(f"  [ERROR] {error_msg}", fg=typer.colors.RED)

        meta = SbomMetadata(
            full_name=f"organizacion/{repo_name}",
            commit_hash=commit_hash,
            generated_at=datetime.utcnow(),
            syft_version=syft_ver,
            status=status,
            component_count=count,
            sbom_path=str(sbom_file) if success else None,
            error_message=error_msg if not success else None
        )

        summary_results.append(meta.dict())

    global_json_path = output_dir / "results_summary.json"
    with open(global_json_path, "w", encoding="utf-8") as f:
        json.dump(summary_results, f, indent=2, default=str)

    typer.secho(f"\nGeneración finalizada.", fg=typer.colors.BRIGHT_BLUE)
    typer.echo(f"Resumen general guardado en: {global_json_path}")
    typer.echo(f"Archivos SBOM guardados en: {sboms_dir}")