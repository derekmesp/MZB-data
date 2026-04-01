import pandas as pd 
import numpy as np 

df = pd.read_excel(
    "Liquid Nitrogen Storage.xlsx",
    keep_default_na=False,
    engine="openpyxl"
)

cols = [
    "Blood",
    "Bone\n Marrow",
    "Spleen",
    "Inguinal\n Lymph\n Nodes",
    "Lung\n Lymph\n Nodes",
    "Mesenteric\n Lymph\n Nodes",
    "Colon\n Lamina\n Propria - Ascending",
    "Colon\n Lamina\n Propria - Descending"
]

df[cols] = (
    df[cols]
    .replace(r"N=\s*", "", regex=True)
    .apply(pd.to_numeric, errors="coerce")
)

filtered = df[df[cols].gt(0).all(axis=1)]
filtered = df[(df[cols] > 0).sum(axis=1) == 5]
print(filtered.Donor.unique())