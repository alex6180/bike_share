from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from .data_utils import DatasetProfile


def _profile_to_markdown(title: str, profile: DatasetProfile) -> str:
    lines = [f"## {title}"]
    lines.append(f"Filas: {profile.num_rows} | Columnas: {profile.num_cols}")
    lines.append("")
    lines.append("### Tipos de datos")
    lines.append(profile.dtypes.to_frame("dtype").to_markdown())
    lines.append("")
    lines.append("### Valores faltantes (conteo)")
    lines.append(profile.missing_counts.to_frame("missing").to_markdown())
    lines.append("")
    lines.append("### Estadísticos (numéricos)")
    lines.append(profile.describe_numeric.to_markdown())
    lines.append("")
    return "\n".join(lines)


def generate_markdown_report(
    output_dir: Path,
    day_profile: DatasetProfile,
    hour_profile: DatasetProfile,
    top_day_corr: pd.DataFrame,
    top_hour_corr: pd.DataFrame,
    figures: Dict[str, str],
) -> Path:
    md_lines = ["# Análisis descriptivo Bike Sharing"]
    md_lines.append("")
    md_lines.append("Variable respuesta: `cnt`.")
    md_lines.append("")

    # Secciones de perfiles
    md_lines.append(_profile_to_markdown("Perfil dataset (day)", day_profile))
    md_lines.append(_profile_to_markdown("Perfil dataset (hour)", hour_profile))

    # Correlaciones top
    md_lines.append("## Correlaciones más altas con `cnt` (day)")
    md_lines.append(top_day_corr.head(8).to_markdown())
    md_lines.append("")
    md_lines.append("## Correlaciones más altas con `cnt` (hour)")
    md_lines.append(top_hour_corr.head(8).to_markdown())
    md_lines.append("")

    # Figuras
    md_lines.append("## Figuras")
    for label, rel_path in figures.items():
        md_lines.append(f"![{label}]({rel_path})")
    md_lines.append("")

    # Separación de train/val (texto)
    md_lines.append("## Conjuntos de modelización y validación")
    md_lines.append("Se realizó un split temporal 80/20 por `dteday` para ambos datasets.")

    out_path = output_dir / "reporte.md"
    out_path.write_text("\n".join(md_lines), encoding="utf-8")
    return out_path
