import pandas as pd

file_path = "Microarray Data/Metadata/171125_1417.gal"

df = pd.read_csv(
    file_path,
    sep="\t",
)
platemap_df = pd.read_excel("Microarray Data/Metadata/Manhattan RecombiChip v2 platemap.xlsx", )

merged_df = df.merge(
    platemap_df[['ID', 'Location in box']], 
    on='ID', 
    how='left'
)