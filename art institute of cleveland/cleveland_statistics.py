import pandas as pd
import json

def missing_data_check(df):
    columns = df.shape[1]
    for i in range(columns):
        series = df.iloc[:,i]
        print(f"{series.name}: {series.isna().sum()}")

def duplicate_check(df):
    ids = df.duplicated(subset = ["id"])
    print(f"Duplicated IDs: {ids.sum()}")
    ##159 duplicate IDs furhter missingness data should be colleced

def description_average(df):
    df["description_length"] = df["description"].map(lambda x: len(x.split()))
    avg = df["description_length"].mean()

    print(avg)
    ## interestingly enought hte description length is about 92 words 

if __name__ == "__main__":
    with open("cleveland_harvested_data.json", "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    ##missing_data_check(df) - returned all zeros
    duplicate_check(df)



# document all findings like journal
