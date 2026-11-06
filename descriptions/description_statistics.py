import json
from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# python3 descriptions/description_statistics.py -> prints basic stats and saves charts to descriptions/charts

DESCRIPTIONS_FILE = Path(__file__).parent / "descriptions.json"
CHARTS_DIR = Path(__file__).parent / "charts"

COLORS = {"chicago": "#2a78d6", "cleveland": "#eb6834"}
MUSEUMS = ["chicago", "cleveland"]
ERA_ORDER = [
    "classical",
    "medieval",
    "renaissance",
    "early modernity",
    "19th century",
    "impressionist period",
    "post-impressionist",
    "modern",
    "contemporary",
]

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_columns", None)


def load_descriptions():
    df = pd.DataFrame(json.loads(DESCRIPTIONS_FILE.read_text(encoding="utf-8")))
    df["word_count"] = df["generated_description"].map(lambda x: len(x.split()))
    # the prompts ask for 100-150 words, so check how often the model listened
    df["in_requested_range"] = df["word_count"].between(100, 150)
    return df


def print_stats(df):
    # one row per painting, since each painting has several descriptions
    artworks = df.drop_duplicates(subset=["museum", "id"])

    print("\nDESCRIPTIONS PER MUSEUM AND PROMPT")
    print(df.groupby(["prompt_name", "museum"]).size().unstack(fill_value=0))

    print("\nARTWORKS PER MUSEUM")
    print(artworks["museum"].value_counts())

    print("\nABSTRACT ARTWORKS PER MUSEUM")
    print(artworks.groupby("museum")["abstract"].sum())

    print("\nARTWORKS PER ERA")
    print(artworks.groupby(["era", "museum"]).size().unstack(fill_value=0).reindex(ERA_ORDER, fill_value=0))

    print("\nWORD COUNTS BY MUSEUM")
    print(df.groupby("museum")["word_count"].describe().round(1))

    print("\nWORD COUNTS BY PROMPT")
    print(df.groupby("prompt_name")["word_count"].describe().round(1))

    print("\nWORD COUNTS BY PROMPT AND MUSEUM")
    print(df.groupby(["prompt_name", "museum"])["word_count"].describe().round(1))

    print("\nPERCENT OF DESCRIPTIONS IN THE REQUESTED 100-150 WORDS")
    print((df.groupby(["prompt_name", "museum"])["in_requested_range"].mean() * 100).round(1).unstack())


def clean_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(length=0)


def save_chart(name):
    CHARTS_DIR.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / f"{name}.png", dpi=200, facecolor="white")
    plt.close()
    print(f"Saved {CHARTS_DIR / f'{name}.png'}")


def plot_word_counts(df):
    figure, axes = plt.subplots(1, 2, figsize=(8, 3.5), sharex=True, sharey=True)
    bins = range(df["word_count"].min() // 10 * 10, df["word_count"].max() + 10, 5)
    for ax, museum in zip(axes, MUSEUMS):
        ax.axvspan(100, 150, color="#f0efea")
        ax.hist(df[df["museum"] == museum]["word_count"], bins=bins, color=COLORS[museum], edgecolor="white")
        ax.set_title(museum.title(), loc="left")
        ax.set_xlabel("Description words (shaded = requested 100-150)")
        clean_axes(ax)
    axes[0].set_ylabel("Descriptions")
    save_chart("word_counts_by_museum")


def plot_average_by_prompt(df):
    averages = df.groupby(["prompt_name", "museum"])["word_count"].mean().unstack().reindex(columns=MUSEUMS)
    ax = averages.plot.barh(color=[COLORS[museum] for museum in MUSEUMS], figsize=(8, 3.5), width=0.7)
    ax.invert_yaxis()
    ax.set_title("Average description length by prompt", loc="left")
    ax.set_xlabel("Average words")
    ax.set_ylabel("")
    ax.legend(title="", frameon=False, labels=["Chicago", "Cleveland"], bbox_to_anchor=(1, 1), loc="upper left")
    clean_axes(ax)
    save_chart("average_words_by_prompt")


def plot_eras(df):
    artworks = df.drop_duplicates(subset=["museum", "id"])
    counts = artworks.groupby(["era", "museum"]).size().unstack(fill_value=0).reindex(ERA_ORDER, fill_value=0)
    ax = counts[MUSEUMS].plot.barh(color=[COLORS[museum] for museum in MUSEUMS], figsize=(8, 4), width=0.7)
    ax.invert_yaxis()
    ax.set_title("Sampled artworks per era", loc="left")
    ax.set_xlabel("Artworks")
    ax.set_ylabel("")
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.legend(title="", frameon=False, labels=["Chicago", "Cleveland"], bbox_to_anchor=(1, 1), loc="upper left")
    clean_axes(ax)
    save_chart("artworks_per_era")


def main():
    df = load_descriptions()
    print_stats(df)
    print()
    plot_word_counts(df)
    plot_average_by_prompt(df)
    plot_eras(df)


if __name__ == "__main__":
    main()
