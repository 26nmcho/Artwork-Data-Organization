import pandas as pd
import json
import math

## keeping id, title, description, date start end/early late, culture
##
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

def century_label(year):
    if pd.isna(year):
        return None
    # 1900 is still the 19th century, 1901 starts the 20th
    number = max(math.ceil(abs(year) / 100), 1)
    if 11 <= number % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    era = " BC" if year < 0 else ""
    return f"{number}{suffix} century{era}"

def convert_chicago(chicago):
    chicago["creation date early"] = chicago["date_start"]
    chicago["creation date late"] = chicago["date_end"]
    century = (chicago["date_start"] + chicago["date_end"]) / 2
    century = century.map(century_label)
    # no date means no century, so keep just the place
    chicago["culture"] = (chicago["place_of_origin"] + ", " + century).fillna(chicago["place_of_origin"])
    return chicago

def merge_dataframes():
    with open("data/cleveland_harvested_data.json", "r", encoding="utf-8-sig") as file:
        clevelandData = json.load(file)

    with open("data/chicago_harvested_data.json", mode = "r",encoding="utf-8-sig") as read_file:
        chicagoData = json.load(read_file)

    chicago = convert_chicago(pd.DataFrame(chicagoData))[["id","title","description","creation date early","creation date late","culture"]]
    cleveland = pd.DataFrame(clevelandData).drop_duplicates(subset = ["id"])
    cleveland["culture"] = cleveland["culture"].str[0]
    cleveland = cleveland[["id","title","description","creation date early","creation date late","culture"]]

    chicago["average date"] = (chicago["creation date early"] + chicago["creation date late"]) / 2
    cleveland["average date"] = (cleveland["creation date early"] + cleveland["creation date late"]) / 2

    sorted_chicago = chicago.sort_values(by = "average date")
    sorted_cleveland = cleveland.sort_values(by = "average date")

    chicago["museum"] = "Chicago Institute of Art"
    cleveland["museum"] = "Cleveland Institute of Art"

    data = pd.merge(cleveland, chicago, on="average date")

    return data



if __name__ == "__main__":







