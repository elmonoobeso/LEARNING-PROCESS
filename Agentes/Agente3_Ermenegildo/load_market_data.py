import pandas as pd
import csv
from pathlib import Path
import sqlite3
ruta=Path(__file__).parent/"data_market.csv"
datos=pd.read_csv(ruta,sep=",",encoding="utf-8")
print(datos)
print(datos.columns)
ruta_bd=(ruta.parent/"market.db")
if ruta_bd.exists():
    ruta_bd.unlink()
con=sqlite3.connect(ruta_bd)
con.execute("PRAGMA foreign_keys= ON")
