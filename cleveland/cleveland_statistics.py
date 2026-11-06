import pandas as pd
import json

def missing_data_check(df):
    columns = df.shape[1]
    for i in range(columns):
        series = df.iloc[:,i]
        print(f"{series.name}: {series.isna().sum()}")

        if series.dtype == str:
            print(f"Number of empty strings:  {series[series == ""].sum()}")
        if series.dtype == int:
                    print(f"Number of zeros:  {series[series == 0].sum()}")
        if series.dtype == object:
                            print(f"Number of null:  {series[series == None].sum()}")

def duplicate_check(df):
    ids = df.duplicated(subset = ["id"])
    print(f"Duplicated IDs: {ids.sum()}")
    ##159 duplicate IDs furhter missingness data should be collected

def type_check(df):
    columns = df.shape[1]
    for i in range(columns):
        series = df.iloc[:,i]
        print(f"{series.name}: {series.dtype}")
    ## checks all type in the data

def description_average(df):
    df["description_length"] = df["description"].map(lambda x: len(x.split()))
    avg = df["description_length"].mean()

    print(avg)
    ## interestingly enought hte description length is about 92 words 

if __name__ == "__main__":
    with open("data/cleveland_harvested_data.json", "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    print(df.describe("creation date early"))
    ##missing_data_check(df) - returned all zeros
    duplicate_check(df)



    type_check(df)


# document all findings like journal
