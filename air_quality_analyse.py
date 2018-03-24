import pandas as pd
import numpy as np

df = pd.read_table("air_quality.csv", sep="\t", header =0)
rows = df[df['humi'].isnull().sum()]
print(rows)




