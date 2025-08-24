# Proyecto: Análisis descriptivo Bike Sharing

Este proyecto implementa el análisis descriptivo solicitado en el trabajo:
- Lectura de datos (`day.csv` y `hour.csv`)
- Perfilado y tratamiento de valores faltantes
- Correlaciones y distribuciones
- Gráficos descriptivos
- Separación de conjuntos de modelización y validación

## Requisitos

- Python 3.9+ (probado en 3.9)
- macOS/Linux/Windows

### Instalación (macOS/Linux)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Instalación (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Datos
1. Descargar `day.csv` y `hour.csv` desde `https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset`.
2. Copiarlos en una carpeta `data/` en la raíz del proyecto:
```
proyecto_bikeshare/
  |- data/
  |   |- day.csv
  |   |- hour.csv
```

## Uso

Ejecutar el análisis y generar reportes/figuras:
```bash
python -m src.main --data-root ./data --output-root ./reports
```

- Resultados generados:
  - `reports/reporte.md` (reporte Markdown)
  - `reports/reporte.docx` (reporte DOCX con epígrafes y figuras)
  - `reports/day_correlations.csv` y `reports/hour_correlations.csv`
  - Figuras en `reports/figures/`:
    - `day_cnt_dist.png`, `hour_cnt_dist.png`
    - `day_corr_heatmap.png`, `hour_corr_heatmap.png`

## Estructura
```
proyecto_bikeshare/
  |- src/
  |   |- main.py
  |   |- data_utils.py
  |   |- viz.py
  |   |- report.py
  |- data/                 # colocar aquí day.csv y hour.csv
  |- reports/
  |   |- figures/
  |- requirements.txt
  |- README.md
```

## Notas
- La variable respuesta es `cnt`.
- Recomendación: no usar `registered` ni `casual` como predictores (fuga de información).
- El split se realiza 80/20 en el tiempo usando `dteday`.
