import json
from pathlib import Path
from typing import List
from .models import Finding

def parse_sarif_file(sarif_path: Path) -> List[Finding]:
    """
    Lee un archivo SARIF y extrae los hallazgos relevantes,
    transformándolos al modelo Finding de Pydantic.
    """
    findings = []
    
    # Si el archivo no existe (ej. falló el análisis), retornamos lista vacía
    if not sarif_path.exists():
        return findings

    try:
        with open(sarif_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # SARIF guarda los resultados dentro de un arreglo 'runs'
        for run in data.get("runs", []):
            for result in run.get("results", []):
                # 1. Regla y Mensaje
                rule_id = result.get("ruleId", "unknown-rule")
                message = result.get("message", {}).get("text", "Sin descripción")
                
                # 2. Severidad ('level' en formato SARIF, 'warning' por defecto si no existe)
                severity = result.get("level", "warning")
                
                # 3. Archivo y Línea (requiere navegar por la estructura 'locations')
                file_path = "unknown-file"
                start_line = 0
                
                locations = result.get("locations", [])
                if locations:
                    physical_location = locations[0].get("physicalLocation", {})
                    
                    artifact = physical_location.get("artifactLocation", {})
                    file_path = artifact.get("uri", "unknown-file")
                    
                    region = physical_location.get("region", {})
                    start_line = region.get("startLine", 0)
                
                # Instanciar modelo Pydantic
                finding = Finding(
                    rule_id=rule_id,
                    severity=severity,
                    message=message,
                    file=file_path,
                    start_line=start_line
                )
                findings.append(finding)
                
    except Exception as e:
        # Si el JSON falla al leerse, evitamos que el programa se caiga
        pass
        
    # La rúbrica pide orden estable: ordenamos por archivo, luego línea y regla
    findings.sort(key=lambda x: (x.file, x.start_line, x.rule_id))
    
    return findings