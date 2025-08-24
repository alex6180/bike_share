from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Parsear fecha si existe columna dteday
    if "dteday" in df.columns:
        df["dteday"] = pd.to_datetime(df["dteday"], errors="coerce")
    return df


@dataclass
class DatasetProfile:
    num_rows: int
    num_cols: int
    columns: List[str]
    dtypes: pd.Series
    missing_counts: pd.Series
    describe_numeric: pd.DataFrame


def profile_dataset(df: pd.DataFrame, index_cols: Optional[Iterable[str]] = None) -> DatasetProfile:
    profile = DatasetProfile(
        num_rows=len(df),
        num_cols=df.shape[1],
        columns=list(df.columns),
        dtypes=df.dtypes.copy(),
        missing_counts=df.isna().sum(),
        describe_numeric=df.describe(include=[np.number]).T,
    )
    # No modificar el DataFrame original (evita ambigüedad índice/columna)
    return profile


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    # Este dataset no suele tener NA; por robustez, llenamos numéricas con mediana
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_clean = df.copy()
    for col in numeric_cols:
        if df_clean[col].isna().any():
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    # Para no numéricas, rellenar con modo si existiera NA
    non_numeric_cols = [c for c in df.columns if c not in numeric_cols]
    for col in non_numeric_cols:
        if df_clean[col].isna().any():
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode().iloc[0])
    return df_clean


def compute_correlations(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    if target_column not in numeric_df.columns:
        raise ValueError(f"La columna objetivo '{target_column}' no es numérica o no existe")
    corrs = numeric_df.corr(numeric_only=True)[target_column].drop(labels=[target_column])
    result = pd.DataFrame({
        "pearson": corrs,
        "pearson_abs": corrs.abs(),
    }).sort_values("pearson_abs", ascending=False)
    return result


def train_validation_split(df: pd.DataFrame, date_col: str, ratio: float = 0.8) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if date_col not in df.columns:
        raise ValueError(f"No existe la columna de fecha '{date_col}'")
    # Orden temporal
    ordered = df.sort_values(by=date_col).reset_index(drop=True)
    split_idx = int(len(ordered) * ratio)
    train_df = ordered.iloc[:split_idx].copy()
    val_df = ordered.iloc[split_idx:].copy()
    return train_df, val_df
