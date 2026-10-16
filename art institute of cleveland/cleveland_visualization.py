import pandas as pd
import json
import re
import matplotlib.pyplot as plt

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

era_order = [
    "classical",
    "medieval",
    "renaissance",
    "early modernity",
    "19th century",
    "impressionist period",
    "post-impressionist",
    "modern",
    "contemporary"
]

def main():
    historical_api_visualization()


def historical_api_visualization():
    with open("cleveland_historical_api.json", "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    df = pd.DataFrame(data)
    print(f"All artworks: {len(df)}")

    df = df[df["type"] == "Painting"].copy()
    print(f"Paintings: {len(df)}")

    # the historical api has two description fields, use the wall description first
    df["description"] = df["wall_description"].fillna(df["digital_description"])

    df = df.dropna(subset=["description", "creation_date_earliest", "images"])
    print(f"Paintings with a description, date, and image: {len(df)}")

    df["has_html"] = df["description"].map(
        lambda x: bool(re.search(r"<[a-zA-Z/]", x))
    )

    # strip html tags like <em> so they don't count as words
    df["word_count"] = df["description"].map(
        lambda x: len(re.sub(r"<[^>]+>", " ", x).split())
    )

    df["date_start"] = df["creation_date_earliest"]

    df["date_range"] = df["creation_date_latest"] - df["creation_date_earliest"]

    # culture looks like ["France, 19th-20th century"], keep just "France"
    df["place_of_origin"] = df["culture"].map(
        lambda x: x[0].split(",")[0] if x else None
    )

    df["era"] = df["date_start"].map(
        lambda x: return_era(x)
    )


    print_summary(df)
    plot_eras(df)
    plot_date_histogram(df)
    plot_word_count_histogram(df)
    artwork_date_word_count_plot(df)
    plot_date_range_histogram(df)
    plot_origin_counts(df)


def print_summary(df):
    print("\nDATAFRAME SUMMARY")
    print(df[["id", "title", "date_start", "word_count", "place_of_origin", "era"]].info())

    print("\nWORD COUNT SUMMARY")
    print(df["word_count"].describe())

    print("\nDATE SUMMARY")
    print(df["date_start"].describe())

    print("\nDATE RANGE SUMMARY (latest - earliest)")
    print(df["date_range"].describe())

    print("\nMOST COMMON PLACES OF ORIGIN")
    print(df["place_of_origin"].value_counts().head(10))

    print(f"\nDescriptions containing html tags: {df['has_html'].sum()}")

    print("\nOLDEST PAINTINGS")
    print(df.sort_values("date_start")[["id", "title", "creation_date", "date_start"]].head(5))

    print("\nSHORTEST DESCRIPTIONS")
    print(df.sort_values("word_count")[["id", "title", "word_count"]].head(5))

    print("\nLONGEST DESCRIPTIONS")
    print(df.sort_values("word_count")[["id", "title", "word_count"]].tail(5))


def plot_eras(df):
    era_counts = df["era"].value_counts()

    era_counts = era_counts.reindex(era_order, fill_value=0)

    plt.bar(era_counts.index, era_counts.values)
    plt.xlabel("Artwork Era")
    plt.ylabel("Number of Paintings per Era")
    plt.title("Visualization of Artwork Eras")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_date_histogram(df):
    plt.hist(df["date_start"], bins=50)
    plt.xlabel("Artwork Start Date")
    plt.ylabel("Number of Paintings")
    plt.title("Distribution of Artwork Dates")
    plt.tight_layout()
    plt.show()


def plot_word_count_histogram(df):
    plt.hist(df["word_count"], bins=50)
    plt.xlabel("Description Word Count")
    plt.ylabel("Number of Paintings")
    plt.title("Distribution of Description Lengths")
    plt.tight_layout()
    plt.show()


def artwork_date_word_count_plot(df):
    plt.scatter(df["date_start"], df["word_count"], alpha=0.3)
    plt.xlabel("Artwork Start Date")
    plt.ylabel("Description Word Count")
    plt.title("Artwork Date vs. Description Length")
    plt.tight_layout()
    plt.show()


def plot_date_range_histogram(df):
    plt.hist(df["date_range"], bins=50)
    plt.xlabel("Years Between Earliest and Latest Date")
    plt.ylabel("Number of Paintings")
    plt.title("How Uncertain Are the Dates?")
    plt.tight_layout()
    plt.show()


def plot_origin_counts(df):
    origin_counts = df["place_of_origin"].value_counts().head(10)

    plt.barh(origin_counts.index, origin_counts.values)
    plt.xlabel("Number of Paintings")
    plt.ylabel("Place of Origin")
    plt.title("Most Common Artwork Origins")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def return_era(year):
    if year <= 500.0:
        return "classical"
    elif 500 < year <= 1400.0:
        return "medieval"
    elif 1400.0 < year <= 1600.0:
        return "renaissance"
    elif 1600.0 < year <= 1800.0:
        return "early modernity"
    elif 1800.0 < year <= 1860.0:
        return "19th century"
    elif 1860.0 < year <= 1886.0:
        return "impressionist period"
    elif 1886.0 < year <= 1905.0:
        return "post-impressionist"
    elif 1905.0 < year <= 1970.0:
        return "modern"
    elif 1970.0 < year:
        return "contemporary"


if __name__ == "__main__":
    main()
