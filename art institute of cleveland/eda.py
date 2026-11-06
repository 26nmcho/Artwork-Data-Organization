import pandas as pd
import json

## keeping id, title, description, date start end/early late, culture
##
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

def convertChicago(chicago):
    chicago["creation date early"] = chicago["date_start"]
    chicago["creation date late"] = chicago["date_end"]
    century = (chicago["date_start"] + chicago["date_end"]) / 2
    century = century.map(lambda x: f"{x % 100}th century")
    chicago["culture"] = chicago["place_of_origin"] + ", " + century
    return chicago


if __name__ == "__main__":
    with open("cleveland_harvested_data.json", "r", encoding="utf-8-sig") as file:
        clevelandData = json.load(file)

    with open("chicago_harvested_data.json", mode = "r",encoding="utf-8-sig") as read_file:
        chicagoData = json.load(read_file)

    chicago = convertChicago(pd.DataFrame(chicagoData))["id","tite","description","creation date early","creation date late","culture"]
    cleveland = pd.DataFrame(clevelandData)
    cleveland["culture"] = cleveland["culture"].str[0]
    cleveland = cleveland["id","tite","description","creation date early","creation date late","culture"]



    print(chicago.head())
