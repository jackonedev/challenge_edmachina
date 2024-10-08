"""
Primer Step en el pipeline de DS

Este modulo se encarga de la lectura de los datos, ya sea de un archivo o de una base de datos.
Hace un relevamiento en la consistencia de los tipos de datos, principalmente la existencia de fechas.
Actualiza los tipos de datos si es necesario.
Descarga una copia en formato parquet.
"""

import os
from typing import Union

import pandas as pd

from utils.config import DATASETS_PATH, PARQUET_PATH
from utils.download_dataset import download_dataset


def main_feed(csv_name: Union[str, None] = None) -> None:
    """
    Lee un archivo CSV localizado en el directorio /datasets.
    Actualiza las columnas correspondientes a formato fecha.
    Guarda una copia en formato parquet.

    Args:
    csv_name (Union[str, None]): Nombre del archivo CSV a leer ubicado en /datasets.
    """

    print("  Step 1: Data Feed Started  ".center(88, "."), end="\n\n")
    # Handling edge cases
    if csv_name is None:
        raise ValueError("No file name provided")

    # Read Local CSV file
    if not csv_name.endswith(".csv"):
        csv_name += ".csv"
    file_name = os.path.join(DATASETS_PATH, csv_name)
    # pylint: disable=bare-except
    try:
        df = pd.read_csv(file_name, sep=";")
    except:
        download_dataset()
        df = pd.read_csv(file_name, sep=";")
    finally:
        print(f"File {file_name} loaded correctly")

    # Convert to datetime the columns with 'at' in the name
    # The 'fecha_mesa_epoch' column also,
    # Update the UTC to Buenos Aires timezone
    date_sample = df[
        df.columns[df.columns.str.endswith("_at")].to_list() + ["fecha_mesa_epoch"]
    ]
    datetime_values = (date_sample.astype(int, errors="ignore") * 1e9).apply(
        pd.to_datetime
    )
    datetime_values_utc = datetime_values.apply(
        lambda col: col.dt.tz_localize("UTC").dt.tz_convert("America/Buenos_Aires")
    )
    # FutureWarning: Setting an item of incompatible dtype is deprecated
    df.update(datetime_values_utc)

    # Rest of the columns
    # pylint: disable=W0612
    non_date_sample = df[df.columns[~df.columns.isin(date_sample.columns)]]

    # Save a copy in parquet format
    df.name = csv_name.split(".")[0]
    df.to_parquet(f"{PARQUET_PATH}/{df.name}.parquet")
    print(f"File saved as {df.name}.parquet in {PARQUET_PATH}", end="\n\n")
    print("  Step 1: Data Feed Completed  ".center(88, "."), end="\n\n")
