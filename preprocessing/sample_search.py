import pandas as pd 
import numpy as np 

df = pd.read_excel(
    "preprocessing/Liquid Nitrogen Storage.xlsx",
    keep_default_na=False,
    engine="openpyxl"
)

cols = [
    "Blood",
    "Spleen",
    "Lung\n Lymph\n Nodes",
    "Mesenteric\n Lymph\n Nodes",
]

df[cols] = (
    df[cols]
    .replace(r"N=\s*", "", regex=True)
    .apply(pd.to_numeric, errors="coerce")
)

df['Age(y): 45(+/-20)'] = pd.to_numeric(df['Age(y): 45(+/-20)'], errors='coerce')
filtered = df[(df[cols] > 0).sum(axis=1) == 3]
filtered = filtered[(filtered['Age(y): 45(+/-20)'] > 20) & (filtered['Age(y): 45(+/-20)'] < 50)]
print(filtered.Donor.unique())