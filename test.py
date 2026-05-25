import pandas as pd

df = pd.read_csv("goodreads_library_export.csv")
pd.set_option("display.max_rows", None)
# Force Pandas to show all columns
pd.set_option("display.max_columns", None)

print(df[["Title", "Author", "Author l-f", "My Rating", "Additional Authors"]].head(10))
