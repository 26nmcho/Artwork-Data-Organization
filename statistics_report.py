import html
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# python3 statistics_report.py                -> turns your edited .md into the pdf
# python3 statistics_report.py --recalculate  -> redoes the numbers, overwrites the .md (old one saved as .bak)

PROJECT = Path(__file__).parent
OUTPUT_DIR = PROJECT / "output"
REPORT_MD = OUTPUT_DIR / "statistics_report.md"
REPORT_PDF = OUTPUT_DIR / "statistics_report.pdf"
ERA_MD = OUTPUT_DIR / "era_paintings.md"
ERA_PDF = OUTPUT_DIR / "era_paintings.pdf"
CHARTS_DIR = OUTPUT_DIR / "charts"

CHICAGO_COLOR = "#2a78d6"
CLEVELAND_COLOR = "#eb6834"
INK = "#0b0b0b"
MUTED_INK = "#52514e"
GRID = "#e6e5e0"

DESCRIPTIONS_FILE = PROJECT / "descriptions" / "descriptions.json"
ERA_NOTES_FILE = PROJECT / "descriptions" / "era_notes.json"
IMAGES_ROOT = Path("/Users/noahshomefolder/Code/Data Projects/Museum Data")
CLEVELAND_IMAGES = IMAGES_ROOT / "cleveland_images"
CHICAGO_RAW = Path("/Users/noahshomefolder/Downloads/artic-api-data/json/artworks")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

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


def load_json(name):
    with open(PROJECT / "data" / name, "r", encoding="utf-8-sig") as file:
        return json.load(file)


# ---------- little stat helpers ----------

def percentile(ordered, fraction):
    position = (len(ordered) - 1) * fraction
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def plain_number(value):
    return f"{value:.2f}".rstrip("0").rstrip(".")


def describe_row(label, values):
    ordered = sorted(values)
    return [
        label,
        f"{len(ordered):,}",
        f"{statistics.mean(ordered):.1f}",
        f"{statistics.stdev(ordered):.1f}",
        plain_number(ordered[0]),
        plain_number(percentile(ordered, 0.25)),
        plain_number(percentile(ordered, 0.5)),
        plain_number(percentile(ordered, 0.75)),
        plain_number(ordered[-1]),
    ]


DESCRIBE_HEADERS = ["What", "Count", "Mean", "Std", "Min", "25%", "Median", "75%", "Max"]


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for row in rows:
        cells = [str(cell).replace("|", "/").replace("\n", " ") for cell in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def era_table(counts):
    rows = [[era, counts.get(era, 0)] for era in ERA_ORDER]
    return table(["Era", "Paintings"], rows)


def top_table(values, label, top=10):
    return table([label, "Paintings"], Counter(values).most_common(top))


def word_count(text):
    return len(re.sub(r"<[^>]+>", " ", text).split())


def is_missing(value):
    return value is None or (isinstance(value, list) and len(value) == 0)


def clean_text(text):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", text)).split())


# ---------- charts, same ones the scripts plot ----------

def new_chart(title, xlabel, ylabel=None, grid_axis="x"):
    figure, ax = plt.subplots(figsize=(3.45, 2.5))
    ax.set_title(title, loc="left", fontsize=9, fontweight="bold", color=INK, pad=8)
    ax.set_xlabel(xlabel, fontsize=7.5, color=MUTED_INK)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=7.5, color=MUTED_INK)
    ax.tick_params(labelsize=7, colors=MUTED_INK, length=0)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED_INK)
    ax.spines["bottom"].set_linewidth(0.6)
    return figure, ax


def save_chart(figure, name):
    CHARTS_DIR.mkdir(exist_ok=True)
    path = CHARTS_DIR / f"{name}.png"
    figure.tight_layout()
    figure.savefig(path, dpi=220, facecolor="white")
    plt.close(figure)
    return f"![]({path})"


def bar_chart(name, title, xlabel, labels, values, color):
    figure, ax = new_chart(title, xlabel)
    positions = range(len(labels))
    ax.barh(positions, values, height=0.62, color=color)
    ax.set_yticks(positions, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(values) * 1.14)
    for position, value in zip(positions, values):
        ax.text(value + max(values) * 0.015, position, f"{value:,}", va="center", fontsize=6.5, color=MUTED_INK)
    return save_chart(figure, name)


def histogram_chart(name, title, xlabel, values, color):
    figure, ax = new_chart(title, xlabel, "Paintings", grid_axis="y")
    ax.hist(values, bins=50, color=color, edgecolor="white", linewidth=0.3)
    return save_chart(figure, name)


def scatter_chart(name, title, years, words, color):
    figure, ax = new_chart(title, "Start year", "Description words", grid_axis="both")
    ax.scatter(years, words, s=8, alpha=0.35, color=color, linewidths=0)
    return save_chart(figure, name)


def era_bar_chart(name, title, counts, color):
    return bar_chart(name, title, "Paintings", ERA_ORDER, [counts.get(era, 0) for era in ERA_ORDER], color)


def origin_bar_chart(name, title, values, color):
    top = Counter(values).most_common(10)
    return bar_chart(name, title, "Paintings", [place for place, _ in top], [count for _, count in top], color)


# ---------- the numbers, one function per program ----------

def chicago_scrape_counts():
    # same counting rules as chicago/artwork_processing.py, minus the writing
    counts = Counter()
    for file_name in os.listdir(CHICAGO_RAW):
        counts["scanned"] += 1
        try:
            with open(CHICAGO_RAW / file_name, "r", encoding="utf-8-sig") as file:
                art = json.load(file)
        except Exception:
            counts["rejected"] += 1
            counts["errors"] += 1
            continue

        kind = art.get("artwork_type_title")
        if art.get("id") is None:
            counts["no_id"] += 1
        elif art.get("title") is None:
            counts["no_title"] += 1
        elif art.get("description") is None:
            counts["no_description"] += 1
        elif art.get("short_description") is None:
            counts["no_short_description"] += 1
        elif art.get("image_id") is None:
            counts["no_image_id"] += 1
        elif kind is None:
            counts["no_artwork_type"] += 1
        if kind is not None and "painting" not in kind.lower():
            counts["not_painting"] += 1

        has_text = art.get("description") is not None or art.get("short_description") is not None
        complete = art.get("id") is not None and art.get("title") is not None and has_text
        complete = complete and art.get("image_id") is not None and kind is not None
        if complete and "painting" in kind.lower():
            counts["accepted"] += 1
        else:
            counts["rejected"] += 1
    return counts


def chicago_section():
    data = load_json("chicago_harvested_data.json")
    ids = {art["id"] for art in data}

    usable = [
        art for art in data
        if art.get("description") is not None
        and art.get("date_start") is not None
        and art.get("place_of_origin") is not None
    ]
    for art in usable:
        art["era"] = return_era(art["date_start"])

    words = [len(art["description"].split()) for art in usable]
    years = [art["date_start"] for art in usable]
    places = [art["place_of_origin"] for art in usable]
    eras = Counter(art["era"] for art in usable)

    parts = ["## Chicago\n"]

    if CHICAGO_RAW.exists():
        print("Scanning the raw Chicago files, this takes a minute...")
        scrape = chicago_scrape_counts()
        parts.append("### Original scrape\n")
        parts.append(f"Accepted: **{scrape['accepted']:,}** files\n")
        parts.append("")

    parts.append("### Paintings with a description, date, and place\n")
    parts.append("#### Word counts and dates\n")
    parts.append(table(DESCRIBE_HEADERS, [
        describe_row("Description words", words),
        describe_row("Start year", years),
    ]))
    parts.append("")
    parts.append(histogram_chart("chicago_dates", "Start years", "Start year", years, CHICAGO_COLOR))
    parts.append(histogram_chart("chicago_words", "Description lengths", "Description words", words, CHICAGO_COLOR))
    parts.append(scatter_chart("chicago_date_vs_words", "Start year vs. description length", years, words,
                               CHICAGO_COLOR))
    parts.append("\n#### Top 10 places of origin\n")
    parts.append(top_table(places, "Place"))
    parts.append("")
    parts.append(origin_bar_chart("chicago_origins", "Top 10 places of origin", places, CHICAGO_COLOR))
    parts.append("\n#### Paintings per era\n")
    parts.append(era_table(eras))
    parts.append("")
    parts.append(era_bar_chart("chicago_eras", "Paintings per era", eras, CHICAGO_COLOR))
    return "\n".join(parts), {"rows": len(data), "unique": len(ids), "usable": len(usable),
                              "words": statistics.mean(words)}


def cleveland_new_section():
    data = load_json("cleveland_harvested_data.json")
    ids = {art["id"] for art in data}
    local = {image.stem for image in CLEVELAND_IMAGES.glob("*.jpg")}
    words = [len(art["description"].split()) for art in data]

    parts = ["## Cleveland\n"]
    parts.append("### New API (`cleveland_harvested_data.json`)\n")
    parts.append(table(["Count", "Value"], [
        ["Rows", f"{len(data):,}"],
        ["Duplicate IDs", len(data) - len(ids)],
        ["Unique IDs", f"{len(ids):,}"],
        ["Unique IDs with no local image", sum(str(i) not in local for i in ids)],
    ]))
    parts.append("\n#### Word counts and dates\n")
    parts.append(table(DESCRIBE_HEADERS, [
        describe_row("Description words", words),
        describe_row("Earliest year", [art["creation date early"] for art in data]),
    ]))
    return "\n".join(parts), {"rows": len(data), "unique": len(ids), "usable": len(data),
                              "words": statistics.mean(words)}


def cleveland_old_section(data):
    paintings = [art for art in data if art.get("type") == "Painting"]

    # the filter from historical_data_processing()
    processed = [
        art for art in paintings
        if (art.get("digital_description") is not None or art.get("wall_description") is not None)
        and art.get("images") is not None
    ]
    columns = ["id", "title", "creation_date", "creation_date_earliest", "creation_date_latest", "creators",
               "culture", "technique", "type", "inscriptions", "wall_description", "digital_description"]
    missing = sorted(
        ((column, sum(is_missing(art.get(column)) for art in processed)) for column in columns),
        key=lambda pair: pair[1],
    )

    # the filter from historical_api_visualization()
    usable = []
    for art in paintings:
        wall = art.get("wall_description")
        description = wall if wall is not None else art.get("digital_description")
        if description is None or art.get("creation_date_earliest") is None or art.get("images") is None:
            continue
        culture = art.get("culture")
        usable.append({
            "id": art["id"],
            "title": art.get("title"),
            "creation_date": art.get("creation_date"),
            "start": art["creation_date_earliest"],
            "latest": art.get("creation_date_latest"),
            "words": word_count(description),
            "description": clean_text(description),
            "has_html": bool(re.search(r"<[a-zA-Z/]", description)),
            "origin": culture[0].split(",")[0] if culture else None,
            "era": return_era(art["creation_date_earliest"]),
        })

    by_date = sorted(usable, key=lambda art: art["start"])
    by_words = sorted(usable, key=lambda art: art["words"])
    words = [art["words"] for art in usable]
    years = [art["start"] for art in usable]
    ranges = [art["latest"] - art["start"] for art in usable if art["latest"] is not None]
    places = [art["origin"] for art in usable if art["origin"]]
    eras = Counter(art["era"] for art in usable)

    def example(label, art):
        caption = f"{art['title']} / ID {art['id']} / {art['creation_date']} / {art['words']} words"
        return (f"\n#### Example: {label}\n\n![{caption}]({CLEVELAND_IMAGES / str(art['id'])}.jpg)\n\n"
                f"> {art['description']}")

    parts = ["### Old API (`cleveland_historical_api.json`)\n"]
    parts.append(table(["Count", "Value"], [
        ["All artworks", f"{len(data):,}"],
        ["Paintings", f"{len(paintings):,}"],
        ["Paintings with an image and a wall or digital description", f"{len(processed):,}"],
        ["...with a wall description", f"{sum(art.get('wall_description') is not None for art in processed):,}"],
        ["...with a digital description", f"{sum(art.get('digital_description') is not None for art in processed):,}"],
        ["Paintings with a description, date, and image", f"{len(usable):,}"],
        ["Descriptions with HTML tags", f"{sum(art['has_html'] for art in usable):,}"],
    ]))
    parts.append(f"\n#### Missing values per column (out of {len(processed):,})\n")
    parts.append(table(["Column", "Missing", "Percent"],
                       [[c, f"{m:,}", f"{m / len(processed):.1%}"] for c, m in missing]))
    parts.append("")
    parts.append(bar_chart("cleveland_missing", "Missing values per column", f"Paintings (out of {len(processed):,})",
                           [c for c, _ in missing], [m for _, m in missing], CLEVELAND_COLOR))
    parts.append("\n#### Number summary (image + wall or digital description)\n")
    parts.append(table(DESCRIBE_HEADERS, [
        describe_row("ID", [art["id"] for art in processed]),
        describe_row("Earliest year", [art["creation_date_earliest"] for art in processed
                                       if art.get("creation_date_earliest") is not None]),
        describe_row("Latest year", [art["creation_date_latest"] for art in processed
                                     if art.get("creation_date_latest") is not None]),
    ]))
    parts.append("\n#### Word counts and dates (description + date + image, HTML removed)\n")
    parts.append(table(DESCRIBE_HEADERS, [
        describe_row("Description words", words),
        describe_row("Start year", years),
        describe_row("Date range (years)", ranges),
    ]))
    parts.append("")
    parts.append(histogram_chart("cleveland_dates", "Start years", "Start year", years, CLEVELAND_COLOR))
    parts.append(histogram_chart("cleveland_words", "Description lengths", "Description words", words,
                                 CLEVELAND_COLOR))
    parts.append(histogram_chart("cleveland_date_ranges", "Years between earliest and latest date", "Years", ranges,
                                 CLEVELAND_COLOR))
    parts.append(scatter_chart("cleveland_date_vs_words", "Start year vs. description length", years, words,
                               CLEVELAND_COLOR))
    parts.append("\n#### Top 10 places of origin\n")
    parts.append(top_table(places, "Place"))
    parts.append("")
    parts.append(origin_bar_chart("cleveland_origins", "Top 10 places of origin", places, CLEVELAND_COLOR))
    parts.append("\n#### Paintings per era\n")
    parts.append(era_table(eras))
    parts.append("")
    parts.append(era_bar_chart("cleveland_eras", "Paintings per era", eras, CLEVELAND_COLOR))
    parts.append("\n#### Oldest paintings\n")
    parts.append(table(["ID", "Title", "Date", "Start year"],
                       [[a["id"], a["title"], a["creation_date"], a["start"]] for a in by_date[:5]]))
    parts.append(example("oldest painting", by_date[0]))
    parts.append("\n#### Shortest descriptions\n")
    parts.append(table(["ID", "Title", "Words"], [[a["id"], a["title"], a["words"]] for a in by_words[:5]]))
    # 160048's whole description is just "a", so the example skips one-word data bugs
    parts.append(example("shortest description", next(art for art in by_words if art["words"] > 1)))
    parts.append("\n#### Longest descriptions\n")
    parts.append(table(["ID", "Title", "Words"], [[a["id"], a["title"], a["words"]] for a in by_words[-5:]]))
    parts.append(example("longest description", by_words[-1]))
    return "\n".join(parts), usable, {"rows": len(paintings), "unique": len({a["id"] for a in paintings}),
                                      "usable": len(usable),
                                      "words": statistics.mean(words)}


def overlap_section(old_data, old_usable):
    new_ids = {art["id"] for art in load_json("cleveland_harvested_data.json")}
    old_ids = {art["id"] for art in old_data}
    usable_ids = {art["id"] for art in old_usable}

    parts = ["### New API vs. old API\n"]
    parts.append(table(["Check", "Artworks"], [
        ["New API unique IDs", f"{len(new_ids):,}"],
        ["...also anywhere in the old API", f"{len(new_ids & old_ids):,}"],
        ["...not in the old API at all", len(new_ids - old_ids)],
        ["Old API usable paintings", f"{len(usable_ids):,}"],
        ["...also in the new API", f"{len(usable_ids & new_ids):,}"],
        ["...only in the old API", len(usable_ids - new_ids)],
    ]))
    return "\n".join(parts)


def load_samples():
    return json.loads(DESCRIPTIONS_FILE.read_text(encoding="utf-8"))


def samples_section(samples):
    artworks = {(s["museum"], s["id"]): s for s in samples}.values()

    rows = []
    for era in ERA_ORDER:
        row = [era]
        for museum in ("chicago", "cleveland"):
            matching = [a for a in artworks if a["museum"] == museum and a["era"] == era]
            row += [sum(not a["abstract"] for a in matching), sum(a["abstract"] for a in matching)]
        rows.append(row)

    flagged = sorted((a for a in artworks if a["abstract"]), key=lambda a: (a["museum"], a["creation date early"]))

    parts = ["## Description generation\n"]
    parts.append("### Samples\n")
    parts.append(table(["Count", "Value"], [
        ["Rows (one per artwork per prompt)", len(samples)],
        ["Different artworks", len(artworks)],
        ["Prompts", len({s["prompt_name"] for s in samples})],
    ]))
    parts.append("\n#### Artworks per era\n")
    parts.append(table(["Era", "Chicago not abstract", "Chicago abstract",
                        "Cleveland not abstract", "Cleveland abstract"], rows))
    parts.append("")
    parts.append(sample_era_chart(rows))
    parts.append("\n#### Abstract artworks\n")
    parts.append(table(["Museum", "ID", "Title", "Year", "Era"],
                       [[a["museum"].title(), a["id"], a["title"], a["creation date early"], a["era"]] for a in flagged]))
    return "\n".join(parts)


def sample_era_chart(rows):
    figure, ax = new_chart("Sampled artworks per era", "Artworks")
    positions = list(range(len(rows)))
    chicago = [row[1] + row[2] for row in rows]
    cleveland = [row[3] + row[4] for row in rows]
    ax.barh([p - 0.2 for p in positions], chicago, height=0.36, color=CHICAGO_COLOR, label="Chicago")
    ax.barh([p + 0.2 for p in positions], cleveland, height=0.36, color=CLEVELAND_COLOR, label="Cleveland")
    ax.set_yticks(positions, [row[0] for row in rows])
    ax.invert_yaxis()
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.legend(fontsize=7, frameon=False, labelcolor=MUTED_INK, loc="lower right", ncol=2, borderaxespad=0.1)
    return save_chart(figure, "samples_per_era")


def era_paintings_section(samples):
    grouped = {}
    for sample in samples:
        grouped.setdefault((sample["museum"], sample["id"]), []).append(sample)

    era_notes = json.loads(ERA_NOTES_FILE.read_text(encoding="utf-8"))
    notes_by_artwork = {(entry["museum"], entry["id"]): entry["notes"] for entry in era_notes["paintings"]}
    used_notes = set()

    parts = ["# One painting per era\n"]
    for era in ERA_ORDER:
        choices = [rows for rows in grouped.values() if rows[0]["era"] == era]
        # most prompts first so paintings with the full set win, then not abstract, then oldest
        rows = min(choices, key=lambda r: (-len(r), r[0]["abstract"], r[0]["creation date early"], r[0]["id"]))
        art = rows[0]
        parts.append(f"\n## {era[0].upper()}{era[1:]}\n")
        parts.append(f"![{art['title']}]({art['local_image']})\n")
        parts.append(table(["Museum", "ID", "Title", "Year", "Abstract"], [
            [art["museum"].title(), art["id"], art["title"], art["creation date early"],
             "yes" if art["abstract"] else "no"],
        ]))
        parts.append("")
        for row in sorted(rows, key=lambda r: r["prompt_name"]):
            label = row["prompt_name"].replace("_", " ")
            parts.append(f"> **{label}:** {' '.join(row['generated_description'].split())}\n")
        key = (art["museum"], art["id"])
        if key in notes_by_artwork:
            used_notes.add(key)
            parts.append("#### Notes\n")
            parts.extend(f"- {note}" for note in notes_by_artwork[key])
            parts.append("")

    # a note can only drop off if its painting stops being the pick for its era
    for key in notes_by_artwork.keys() - used_notes:
        print(f"Warning: notes for {key} aren't in the era pdf because that painting isn't picked")

    if era_notes["overall"]:
        parts.append("### Overall notes\n")
        parts.extend(f"- {note}" for note in era_notes["overall"])
    return "\n".join(parts)


def calculate():
    OUTPUT_DIR.mkdir(exist_ok=True)
    old_data = load_json("cleveland_historical_api.json")

    chicago_text, chicago = chicago_section()
    new_text, new = cleveland_new_section()
    old_text, old_usable, old = cleveland_old_section(old_data)
    overlap_text = overlap_section(old_data, old_usable)
    samples = load_samples()

    def quick_row(name, info):
        return [name, f"{info['rows']:,}", f"{info['unique']:,}", f"{info['usable']:,}", f"{info['words']:.1f}"]

    intro = "\n".join([
        "# Artwork data: every stat so far",
        "",
        "## Overview",
        "",
        table(["Dataset", "Paintings", "Unique IDs", "Passed script filter", "Avg words (filtered)"], [
            quick_row("Chicago", chicago),
            quick_row("Cleveland, new API", new),
            quick_row("Cleveland, old API", old),
        ]),
    ])

    if REPORT_MD.exists():
        shutil.copy(REPORT_MD, REPORT_MD.with_suffix(".md.bak"))
    sections = [intro, chicago_text, new_text, old_text, overlap_text, samples_section(samples)]
    REPORT_MD.write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    if ERA_MD.exists():
        shutil.copy(ERA_MD, ERA_MD.with_suffix(".md.bak"))
    ERA_MD.write_text(era_paintings_section(samples) + "\n", encoding="utf-8")


# ---------- markdown to pdf, using the Chrome you already have ----------

CSS = """
@page { size: letter; margin: 0.8in 0.8in; }
body { font: 10.5pt/1.45 -apple-system, "Helvetica Neue", Arial, sans-serif; color: #24231f; }
h1 { font-size: 23pt; margin: 0 0 8pt; }
h2 { font-size: 17pt; margin: 18pt 0 8pt; padding-bottom: 4pt; border-bottom: 1.5px solid #24231f; break-after: avoid; }
h2:not(:first-of-type) { break-before: page; margin-top: 0; }
h3 { font-size: 12.5pt; margin: 18pt 0 6pt; break-after: avoid; }
h4 { font-size: 10pt; margin: 14pt 0 4pt; color: #52514e; break-after: avoid; }
p { margin: 5pt 0 7pt; }
p.example { font-size: 9.5pt; padding-left: 9pt; border-left: 2px solid #d9d7cf; }
ul { margin: 5pt 0; padding-left: 16pt; }
li { margin: 3pt 0; }
code { font: 9pt Menlo, monospace; background: #f0efea; padding: 0 2pt; border-radius: 2pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 4pt 0 8pt; }
table.narrow { width: 62%; }
table:not(.long) { break-inside: avoid; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { text-align: left; border-bottom: 1px solid #24231f; padding: 3pt 6pt; }
td { border-bottom: 0.5px solid #d9d7cf; padding: 2.5pt 6pt; vertical-align: top; }
th.num, td.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12pt 10pt; margin: 6pt 0 10pt; }
.gallery.pair { grid-template-columns: repeat(2, 1fr); }
figure { margin: 0; break-inside: avoid; }
figure img { display: block; width: 100%; height: 1.75in; object-fit: contain; object-position: left top; }
.pair figure img { height: 1.6in; }
.gallery.single { grid-template-columns: 3.2in; }
.single figure img { width: auto; max-width: 100%; height: auto; max-height: 2.3in; }
.gallery.charts { grid-template-columns: repeat(2, 1fr); gap: 10pt; }
.charts figure img { height: auto; }
figcaption { font-size: 7.5pt; line-height: 1.3; margin-top: 3pt; color: #52514e; }
"""


# each painting and its notes should fit on one page
ERA_CSS = """
@page { margin: 0.55in 0.75in; }
body { font-size: 9.5pt; line-height: 1.35; }
h1 { font-size: 18pt; margin-bottom: 2pt; }
h2 { margin: 6pt 0 6pt; }
h4 { margin: 8pt 0 2pt; }
.gallery { margin: 4pt 0 5pt; }
.single figure img { max-height: 1.55in; }
table { margin: 2pt 0 4pt; }
p.example { font-size: 8.8pt; margin: 3pt 0 4pt; }
li { margin: 2pt 0; }
"""


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)


def is_number(cell):
    return re.fullmatch(r"-?[\d,]+(\.\d+)?%?", cell) is not None


def table_html(lines):
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    headers, body = rows[0], rows[2:]
    numeric = [
        bool(body) and all(is_number(row[i]) for row in body if i < len(row))
        for i in range(len(headers))
    ]
    out = [f'<table class="{"narrow" if len(headers) == 2 else ""}"><thead><tr>']
    for i, cell in enumerate(headers):
        out.append(f'<th class="{"num" if numeric[i] else ""}">{inline(cell)}</th>')
    out.append("</tr></thead><tbody>")
    for row in body:
        cells = "".join(
            f'<td class="{"num" if i < len(numeric) and numeric[i] else ""}">{inline(cell)}</td>'
            for i, cell in enumerate(row)
        )
        out.append(f"<tr>{cells}</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def gallery_html(lines, folder):
    figures = []
    is_charts = True
    for line in lines:
        caption, source = re.fullmatch(r"!\[(.*)\]\((.*)\)", line).groups()
        number = len(list(Path(folder).glob("picture_*")))
        if source.endswith(".png"):
            small = Path(folder) / f"picture_{number}.png"
            shutil.copy(source, small)
        else:
            # shrink paintings first so the pdf stays a reasonable size
            is_charts = False
            small = Path(folder) / f"picture_{number}.jpg"
            subprocess.run(["sips", "-Z", "700", "-s", "format", "jpeg", "-s", "formatOptions", "75",
                            source, "--out", str(small)], check=True, capture_output=True)
        label = f"<figcaption>{inline(caption)}</figcaption>" if caption else ""
        figures.append(f'<figure><img src="{small.name}">{label}</figure>')
    if is_charts:
        kind = "gallery charts"
    elif len(lines) == 1:
        kind = "gallery single"
    elif len(lines) == 2:
        kind = "gallery pair"
    else:
        kind = "gallery"
    return f'<div class="{kind}">{"".join(figures)}</div>'


def markdown_to_html(text, folder, title, extra_css):
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("!["):
            block = []
            while i < len(lines) and lines[i].startswith("!["):
                block.append(lines[i])
                i += 1
            out.append(gallery_html(block, folder))
        elif line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(table_html(block))
        elif line.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("</ul>")
        elif line.startswith("> "):
            out.append(f'<p class="example">{inline(line[2:])}</p>')
            i += 1
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            out.append(f"<h{level}>{inline(line[level:].strip())}</h{level}>")
            i += 1
        else:
            out.append(f"<p>{inline(line)}</p>")
            i += 1
    body = "\n".join(out)
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}{extra_css}</style></head><body>{body}</body></html>'


def render_pdf(markdown_file, pdf_file, title, extra_css=""):
    with tempfile.TemporaryDirectory() as folder:
        page = markdown_to_html(markdown_file.read_text(encoding="utf-8"), folder, title, extra_css)
        html_file = Path(folder) / "report.html"
        html_file.write_text(page, encoding="utf-8")
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={folder}/chrome",
            f"--print-to-pdf={pdf_file}", html_file.as_uri(),
        ], check=True, capture_output=True, timeout=120)
    print(f"Saved {pdf_file}")


def main():
    if "--recalculate" in sys.argv or not REPORT_MD.exists() or not ERA_MD.exists():
        calculate()
    render_pdf(REPORT_MD, REPORT_PDF, "Artwork stats")
    render_pdf(ERA_MD, ERA_PDF, "One painting per era", ERA_CSS)


if __name__ == "__main__":
    main()
