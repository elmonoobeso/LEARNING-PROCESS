import pandas as pd
import csv
from pathlib import Path
ruta=Path(__file__).parent/"data_market.csv"
leido=pd.read_csv(ruta,sep=",",encoding="utf-8")
print(leido)
print(leido.columns)