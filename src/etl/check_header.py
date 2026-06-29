import pandas as pd

print("Program Started")

file = "data/raw/companies.xlsx"

df = pd.read_excel(file, header=None)

print(df.head(10))

print("Program Finished")