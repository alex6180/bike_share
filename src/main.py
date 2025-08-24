import argparse
from pathlib import Path

from . import data_utils
from . import viz
from . import report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Análisis descriptivo Bike Sharing")
    parser.add_argument(
        "--data-root",
        type=str,
        default="..",
        help="Directorio donde están day.csv y hour.csv",
    )
    parser.add_argument(
        "--output-root",
        type=str,
        default="../reports",
        help="Directorio de salida para reportes y figuras",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root).resolve()
    output_root = Path(args.output_root).resolve()
    figures_dir = output_root / "figures"
    output_root.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Rutas de datos
    day_csv = data_root / "day.csv"
    hour_csv = data_root / "hour.csv"

    # Cargar datos
    day_df = data_utils.load_dataset(day_csv)
    hour_df = data_utils.load_dataset(hour_csv)

    # Perfilado y missing
    day_profile = data_utils.profile_dataset(day_df, index_cols=["instant", "dteday"])
    hour_profile = data_utils.profile_dataset(
        hour_df, index_cols=["instant", "dteday", "hr"]
    )

    # Tratamiento de missing
    day_df_clean = data_utils.handle_missing(day_df)
    hour_df_clean = data_utils.handle_missing(hour_df)

    # Correlaciones con cnt
    day_corr = data_utils.compute_correlations(day_df_clean, target_column="cnt")
    hour_corr = data_utils.compute_correlations(hour_df_clean, target_column="cnt")

    # Guardar correlaciones
    day_corr_path = output_root / "day_correlations.csv"
    hour_corr_path = output_root / "hour_correlations.csv"
    day_corr.to_csv(day_corr_path, index=True)
    hour_corr.to_csv(hour_corr_path, index=True)

    # Split temporal train/val
    day_splits = data_utils.train_validation_split(day_df_clean, date_col="dteday", ratio=0.8)
    hour_splits = data_utils.train_validation_split(hour_df_clean, date_col="dteday", ratio=0.8)

    # Visualizaciones
    viz.plot_target_distribution(day_df_clean, target="cnt", title="Distribución cnt (day)", path=figures_dir / "day_cnt_dist.png")
    viz.plot_target_distribution(hour_df_clean, target="cnt", title="Distribución cnt (hour)", path=figures_dir / "hour_cnt_dist.png")
    viz.plot_correlation_heatmap(day_df_clean, title="Heatmap correlaciones (day)", path=figures_dir / "day_corr_heatmap.png")
    viz.plot_correlation_heatmap(hour_df_clean, title="Heatmap correlaciones (hour)", path=figures_dir / "hour_corr_heatmap.png")

    # Reporte markdown y docx
    report.generate_markdown_report(
        output_dir=output_root,
        day_profile=day_profile,
        hour_profile=hour_profile,
        top_day_corr=day_corr.sort_values("pearson_abs", ascending=False).head(8),
        top_hour_corr=hour_corr.sort_values("pearson_abs", ascending=False).head(8),
        figures={
            "day_cnt_dist": "figures/day_cnt_dist.png",
            "hour_cnt_dist": "figures/hour_cnt_dist.png",
            "day_corr_heatmap": "figures/day_corr_heatmap.png",
            "hour_corr_heatmap": "figures/hour_corr_heatmap.png",
        },
    )
    report.generate_docx_report(
        output_dir=output_root,
        day_profile=day_profile,
        hour_profile=hour_profile,
        top_day_corr=day_corr.sort_values("pearson_abs", ascending=False).head(8),
        top_hour_corr=hour_corr.sort_values("pearson_abs", ascending=False).head(8),
        figures={
            "day_cnt_dist": "figures/day_cnt_dist.png",
            "hour_cnt_dist": "figures/hour_cnt_dist.png",
            "day_corr_heatmap": "figures/day_corr_heatmap.png",
            "hour_corr_heatmap": "figures/hour_corr_heatmap.png",
        },
    )


if __name__ == "__main__":
    main()
