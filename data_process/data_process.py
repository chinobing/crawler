import pandas as pd

path = '/home/jfq/Downloads/创投网站.xlsx'

df = pd.read_excel(path)
print(df)
with open("./company.csv", 'at') as f:
    df.to_csv(f, header=False)