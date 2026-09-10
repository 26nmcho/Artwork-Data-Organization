import pandas as pd
import json
import matplotlib.pyplot as plt

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
    with open("harvested_data.json", "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    df = df.dropna(subset=["description", "date_start", "place_of_origin"])

    df["word_count"] = df["description"].map(
        lambda x: len(x.split())
    )

    df["era"] = df["date_start"].map(
        lambda x: return_era(x)
    )


    plot_eras(df)
    print_summary(df)
    artwork_date_word_count_plot(df)
    plot_origin_counts(df)


def print_summary(df):
    print("\nDATAFRAME SUMMARY")
    print(df.info())

    print("\nWORD COUNT SUMMARY")
    print(df["word_count"].describe())

    print("\nDATE SUMMARY")
    print(df["date_start"].describe())

    print("\nMOST COMMON PLACES OF ORIGIN")
    print(df["place_of_origin"].value_counts().head(10))


def artwork_date_word_count_plot(df):
    plt.scatter(df["date_start"], df["word_count"])
    plt.xlabel("Artwork Start Date")
    plt.ylabel("Description Word Count")
    plt.title("Artwork Date vs. Description Length")
    plt.show()

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


def plot_origin_counts(df):
    origin_counts = df["place_of_origin"].value_counts().head(10)

    plt.bar(origin_counts.index, origin_counts.values)
    plt.xlabel("Place of Origin")
    plt.ylabel("Number of Artworks")
    plt.title("Most Common Artwork Origins")
    plt.xticks(rotation=45)
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


# group years by era: classic, impressionism, post-impressionism, contemporary (abstract)
# automate the header change
# try chrome selenium
# cleveland art institute