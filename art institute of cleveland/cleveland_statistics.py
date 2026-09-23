import pandas as pd
import json

def missing_data_check(df):
    columns = df.shape[1]
    for i in range(columns):
        df.iloc[:,i].isna

def duplicate_check(df):
    df[df.duplicated()]
    df.header()

if __name__ == "__main__":
    with open("cleveland_harvested_data.json", "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    ##missing_data_check(df)
    print(duplicate_check(df))
