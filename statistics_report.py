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
from datetime import date
from pathlib import Path

# python3 statistics_report.py                -> turns your edited .md into the pdf
# python3 statistics_report.py --recalculate  -> redoes the numbers, overwrites the .md (old one saved as .bak)

PROJECT = Path(__file__).parent
OUTPUT_DIR = PROJECT / "output"
REPORT_MD = OUTPUT_DIR / "statistics_report.md"
REPORT_PDF = OUTPUT_DIR / "statistics_report.pdf"
SAMPLES_OUT = OUTPUT_DIR / "samples_abstract_boolean.json"

SAMPLES_DIR = PROJECT / "Description Generation Samples"
IMAGES_ROOT = Path("/Users/noahshomefolder/Code/Data Projects/Museum Data")
CLEVELAND_IMAGES = IMAGES_ROOT / "Cleveland Musuem Images"
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
    with open(PROJECT / name, "r", encoding="utf-8-sig") as file:
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


# ---------- the numbers, one function per program ----------

def chicago_scrape_counts():
    # same counting rules as art institute of chicago/artwork_processing.py, minus the writing
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
    skipped = load_json("skipped_artworks.json")
    second = load_json("skipped_artworks_second_round.json")
    ids = {art["id"] for art in data}

    local = set()
    for folder in sorted(IMAGES_ROOT.glob("art institute of chicago*")):
        if folder.is_dir():
            local |= {image.stem for image in folder.glob("*.jpg")}
    has_image = sum(str(i) in local for i in ids)

    usable = [
        art for art in data
        if art.get("description") is not None
        and art.get("date_start") is not None
        and art.get("place_of_origin") is not None
    ]
    for art in usable:
        art["era"] = return_era(art["date_start"])

    parts = ["## Art Institute of Chicago\n"]

    if CHICAGO_RAW.exists():
        print("Scanning the raw Chicago files, this takes a minute...")
        scrape = chicago_scrape_counts()
        parts.append("### The original scrape\n")
        parts.append("From `artwork_processing.py`. Heads up: the missing-field counts stop at the first "
                     "thing missing, so one artwork only ever gets counted once.\n")
        parts.append(table(["Count", "Files"], [
            ["Scanned", f"{scrape['scanned']:,}"],
            ["Accepted", f"{scrape['accepted']:,}"],
            ["Rejected", f"{scrape['rejected']:,}"],
            ["Errors", f"{scrape['errors']:,}"],
            ["No ID", f"{scrape['no_id']:,}"],
            ["No title", f"{scrape['no_title']:,}"],
            ["No description", f"{scrape['no_description']:,}"],
            ["No short description", f"{scrape['no_short_description']:,}"],
            ["No image ID", f"{scrape['no_image_id']:,}"],
            ["No artwork type", f"{scrape['no_artwork_type']:,}"],
            ["Not a painting", f"{scrape['not_painting']:,}"],
        ]))
        parts.append("")

    parts.append("### After image hunting and cleaning\n")
    parts.append(table(["Count", "Value"], [
        ["Paintings left in the dataset", f"{len(data):,}"],
        ["Unique IDs", f"{len(ids):,}"],
        ["Skipped in round one", len(skipped)],
        ["Skipped in round two", len(second)],
        ["Second-round skips still in the dataset", sum(art["id"] in ids for art in second)],
        ["Paintings with a local .jpg", f"{has_image:,}"],
        ["Have a description, date, and place of origin", f"{len(usable):,}"],
    ]))
    parts.append("\nEverything below uses that last group, same as `data-visualization.py`.\n")

    parts.append("### Word counts and dates\n")
    parts.append(table(DESCRIBE_HEADERS, [
        describe_row("Description words", [len(art["description"].split()) for art in usable]),
        describe_row("Start year", [art["date_start"] for art in usable]),
    ]))
    parts.append("\n### Top 10 places of origin\n")
    parts.append(top_table([art["place_of_origin"] for art in usable], "Place"))
    parts.append("\n### Paintings per era\n")
    parts.append(era_table(Counter(art["era"] for art in usable)))
    return "\n".join(parts), {"rows": len(data), "unique": len(ids), "usable": len(usable),
                              "words": statistics.mean(len(art["description"].split()) for art in usable)}


def cleveland_new_section():
    data = load_json("cleveland_harvested_data.json")
    ids = {art["id"] for art in data}
    local = {image.stem for image in CLEVELAND_IMAGES.glob("*.jpg")}
    words = [len(art["description"].split()) for art in data]

    columns = list(data[0].keys())
    rows = []
    for column in columns:
        values = [art.get(column) for art in data]
        kinds = {type(value).__name__ for value in values if value is not None}
        rows.append([
            column,
            "/".join(sorted(kinds)),
            sum(value is None for value in values),
            sum(value == "" for value in values),
            sum(value == [] for value in values),
            sum(value == 0 and not isinstance(value, bool) for value in values),
        ])

    parts = ["## Cleveland: new API (`cleveland_harvested_data.json`)\n"]
    parts.append("From `cleveland_statistics.py` and `image_metadata_check()`. These count every row, "
                 "so the duplicates are still in here.\n")
    parts.append(table(["Count", "Value"], [
        ["Rows", f"{len(data):,}"],
        ["Duplicate IDs", len(data) - len(ids)],
        ["Unique IDs", f"{len(ids):,}"],
        ["Unique IDs with no local image", sum(str(i) not in local for i in ids)],
    ]))
    parts.append("\n### Missing data and types per column\n")
    parts.append(table(["Column", "Type", "Null", "Empty text", "Empty list", "Zeros"], rows))
    parts.append("\nNote: the empty-string, zero, and null lines in `missing_data_check` use `.sum()` on "
                 "the matching values and don't really count them, so they're counted properly here.\n")
    parts.append("### Word counts and dates\n")
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
            "has_html": bool(re.search(r"<[a-zA-Z/]", description)),
            "origin": culture[0].split(",")[0] if culture else None,
            "era": return_era(art["creation_date_earliest"]),
        })

    by_date = sorted(usable, key=lambda art: art["start"])
    by_words = sorted(usable, key=lambda art: art["words"])

    parts = ["## Cleveland: old API (`cleveland_historical_api.json`)\n"]
    parts.append("From `historical_data_processing()` and `cleveland_visualization.py`.\n")
    parts.append(table(["Count", "Value"], [
        ["All artworks", f"{len(data):,}"],
        ["Paintings", f"{len(paintings):,}"],
        ["Paintings with an image and a wall or digital description", f"{len(processed):,}"],
        ["...with a wall description", f"{sum(art.get('wall_description') is not None for art in processed):,}"],
        ["...with a digital description", f"{sum(art.get('digital_description') is not None for art in processed):,}"],
        ["Paintings with a description, date, and image", f"{len(usable):,}"],
        ["Descriptions with HTML tags", f"{sum(art['has_html'] for art in usable):,}"],
    ]))
    parts.append(f"\n### Missing values per column (out of {len(processed):,})\n")
    parts.append(table(["Column", "Missing", "Percent"],
                       [[c, f"{m:,}", f"{m / len(processed):.1%}"] for c, m in missing]))
    parts.append("\n### Number summary for that same group\n")
    parts.append(table(DESCRIBE_HEADERS, [
        describe_row("ID", [art["id"] for art in processed]),
        describe_row("Earliest year", [art["creation_date_earliest"] for art in processed
                                       if art.get("creation_date_earliest") is not None]),
        describe_row("Latest year", [art["creation_date_latest"] for art in processed
                                     if art.get("creation_date_latest") is not None]),
    ]))
    parts.append("\nEverything below uses the description, date, and image group. HTML tags get removed "
                 "before counting words.\n")
    parts.append("### Word counts and dates\n")
    parts.append(table(DESCRIBE_HEADERS, [
        describe_row("Description words", [art["words"] for art in usable]),
        describe_row("Start year", [art["start"] for art in usable]),
        describe_row("Date range (years)", [art["latest"] - art["start"] for art in usable
                                            if art["latest"] is not None]),
    ]))
    parts.append("\n### Top 10 places of origin\n")
    parts.append(top_table([art["origin"] for art in usable if art["origin"]], "Place"))
    parts.append("\n### Paintings per era\n")
    parts.append(era_table(Counter(art["era"] for art in usable)))
    parts.append("\n### Oldest paintings\n")
    parts.append(table(["ID", "Title", "Date", "Start year"],
                       [[a["id"], a["title"], a["creation_date"], a["start"]] for a in by_date[:5]]))
    parts.append("\n### Shortest descriptions\n")
    parts.append(table(["ID", "Title", "Words"], [[a["id"], a["title"], a["words"]] for a in by_words[:5]]))
    parts.append("\n### Longest descriptions\n")
    parts.append(table(["ID", "Title", "Words"], [[a["id"], a["title"], a["words"]] for a in by_words[-5:]]))
    return "\n".join(parts), usable, {"rows": len(paintings), "unique": len({a["id"] for a in paintings}),
                                      "usable": len(usable),
                                      "words": statistics.mean(a["words"] for a in usable)}


def overlap_section(old_data, old_usable):
    new_ids = {art["id"] for art in load_json("cleveland_harvested_data.json")}
    chicago_ids = {art["id"] for art in load_json("chicago_harvested_data.json")}
    old_ids = {art["id"] for art in old_data}
    usable_ids = {art["id"] for art in old_usable}

    parts = ["## How the datasets overlap\n"]
    parts.append("Cleveland images are saved as `{id}.jpg`, so comparing artwork IDs covers the image overlap too.\n")
    parts.append(table(["Check", "Artworks"], [
        ["New API unique IDs", f"{len(new_ids):,}"],
        ["...also anywhere in the old API", f"{len(new_ids & old_ids):,}"],
        ["...not in the old API at all", len(new_ids - old_ids)],
        ["Old API usable paintings", f"{len(usable_ids):,}"],
        ["...also in the new API", f"{len(usable_ids & new_ids):,}"],
        ["...only in the old API", len(usable_ids - new_ids)],
        ["Same ID number at Chicago and Cleveland (new API)", len(chicago_ids & new_ids)],
    ]))
    parts.append("\nThat last row is just two museums reusing a number. They're different artworks, so "
                 "the combined data needs a `museum` column.")
    return "\n".join(parts)


def load_sample_file(path):
    # one file has a personal note above the json, so start reading at the first [
    text = path.read_text(encoding="utf-8")
    return json.loads(text[text.index("["):])


def build_boolean_samples(old_data):
    chicago_years = {a["id"]: a.get("date_start") for a in load_json("chicago_harvested_data.json")}
    cleveland_years = {a["id"]: a["creation date early"] for a in load_json("cleveland_harvested_data.json")}
    cleveland_years.update({a["id"]: a.get("creation_date_earliest") for a in old_data
                            if a.get("creation_date_earliest") is not None})

    samples = []
    for museum, years in (("chicago", chicago_years), ("cleveland", cleveland_years)):
        for path in sorted((SAMPLES_DIR / museum).glob("*/*.json")):
            for art in load_sample_file(path):
                year = years.get(art["id"])
                is_abstract = art["era"] == "abstract"
                samples.append({
                    "museum": museum,
                    "prompt_name": path.stem,
                    "id": art["id"],
                    "title": art["title"],
                    "year": year,
                    # abstract used to be an era, so those get their real era from the date
                    "era": return_era(year) if is_abstract else art["era"],
                    "abstract": is_abstract,
                    "local_image": art["local_image"],
                    "generated_description": art["generated_description"],
                    "description_model": art["description_model"],
                    "description_prompt": art["description_prompt"],
                })
    return samples


def samples_section(samples):
    artworks = {(s["museum"], s["id"]): s for s in samples}.values()

    rows = []
    for era in ERA_ORDER:
        row = [era]
        for museum in ("chicago", "cleveland"):
            matching = [a for a in artworks if a["museum"] == museum and a["era"] == era]
            row += [sum(not a["abstract"] for a in matching), sum(a["abstract"] for a in matching)]
        rows.append(row)

    flagged = sorted((a for a in artworks if a["abstract"]), key=lambda a: (a["museum"], a["year"]))

    parts = ["## Description samples, now with abstract as true/false\n"]
    parts.append("`abstract` is its own field now, and those paintings got a real era based on their date. "
                 "This version lives in `output/samples_abstract_boolean.json`. The original sample files "
                 "haven't been changed.\n")
    parts.append(table(["Count", "Value"], [
        ["Rows (one per artwork per prompt)", len(samples)],
        ["Different artworks", len(artworks)],
        ["Prompts", len({s["prompt_name"] for s in samples})],
    ]))
    parts.append("\n### Artworks per era\n")
    parts.append(table(["Era", "Chicago not abstract", "Chicago abstract",
                        "Cleveland not abstract", "Cleveland abstract"], rows))
    parts.append("\n### The abstract ones\n")
    parts.append(table(["Museum", "ID", "Title", "Year", "Era"],
                       [[a["museum"].title(), a["id"], a["title"], a["year"], a["era"]] for a in flagged]))
    parts.append("\nJudgment call: the note in `openAI_description_generation.py` says only the Mondrian "
                 "is fully abstract at Cleveland and the other four are near-abstract. They're all `true` "
                 "here because they were all in the abstract group.")
    return "\n".join(parts)


def calculate():
    OUTPUT_DIR.mkdir(exist_ok=True)
    old_data = load_json("cleveland_historical_api.json")

    chicago_text, chicago = chicago_section()
    new_text, new = cleveland_new_section()
    old_text, old_usable, old = cleveland_old_section(old_data)
    overlap_text = overlap_section(old_data, old_usable)
    samples = build_boolean_samples(old_data)
    SAMPLES_OUT.write_text(json.dumps(samples, indent=4, ensure_ascii=False), encoding="utf-8")

    def quick_row(name, info):
        return [name, f"{info['rows']:,}", f"{info['unique']:,}", f"{info['usable']:,}", f"{info['words']:.1f}"]

    intro = "\n".join([
        "# Artwork data: every stat so far",
        "",
        f"Numbers last calculated {date.today():%B %-d, %Y}. Everything our scripts have calculated so far, "
        "all in one spot. Nothing fancy.",
        "",
        "**Want to change something?** Edit `output/statistics_report.md`, then run "
        "`python3 statistics_report.py` to rebuild this PDF. Your edits stick unless you run it with "
        "`--recalculate`, which redoes the numbers and saves your old version as a `.bak` file.",
        "",
        "## The quick version",
        "",
        table(["Dataset", "Paintings", "Unique IDs", "Usable", "Avg words"], [
            quick_row("Chicago", chicago),
            quick_row("Cleveland, new API", new),
            quick_row("Cleveland, old API", old),
        ]),
        "",
        "\"Usable\" means it passed that script's filter, and the average word count is for that group. "
        "The new API pull only kept complete records in the first place, so all of its rows count.",
    ])

    outro = "\n".join([
        "## What's not in here",
        "",
        "- **Cleveland scrape counters** (no ID, no title, and so on): they only ever printed to the terminal "
        "and were never saved. Getting them back means calling the API again.",
        "- **Deleted duplicate image count** from `chicago_manual_data_cleaning.py`: same deal, it only printed.",
        "- **Combined Chicago + Cleveland stats:** our scripts haven't calculated these yet.",
        "- **Charts:** this is just the numbers.",
    ])

    if REPORT_MD.exists():
        shutil.copy(REPORT_MD, REPORT_MD.with_suffix(".md.bak"))
    sections = [intro, chicago_text, new_text, old_text, overlap_text, samples_section(samples), outro]
    REPORT_MD.write_text("\n\n".join(sections) + "\n", encoding="utf-8")


# ---------- markdown to pdf, using the Chrome you already have ----------

CSS = """
@page { size: letter; margin: 0.8in 0.8in; }
body { font: 10.5pt/1.45 -apple-system, "Helvetica Neue", Arial, sans-serif; color: #24231f; }
h1 { font-size: 23pt; margin: 0 0 8pt; }
h2 { font-size: 15pt; margin: 22pt 0 6pt; padding-bottom: 3pt; border-bottom: 1.5px solid #24231f; break-after: avoid; }
h3 { font-size: 11pt; margin: 14pt 0 4pt; break-after: avoid; }
p { margin: 5pt 0 7pt; }
ul { margin: 5pt 0; padding-left: 16pt; }
li { margin: 3pt 0; }
code { font: 9pt Menlo, monospace; background: #f0efea; padding: 0 2pt; border-radius: 2pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 4pt 0 8pt; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { text-align: left; border-bottom: 1px solid #24231f; padding: 3pt 6pt; }
td { border-bottom: 0.5px solid #d9d7cf; padding: 2.5pt 6pt; vertical-align: top; }
th.num, td.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
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
    out = ["<table><thead><tr>"]
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


def markdown_to_html(text):
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
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
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            out.append(f"<h{level}>{inline(line[level:].strip())}</h{level}>")
            i += 1
        else:
            out.append(f"<p>{inline(line)}</p>")
            i += 1
    body = "\n".join(out)
    return f'<!doctype html><html><head><meta charset="utf-8"><title>Artwork stats</title><style>{CSS}</style></head><body>{body}</body></html>'


def render_pdf():
    page = markdown_to_html(REPORT_MD.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as folder:
        html_file = Path(folder) / "report.html"
        html_file.write_text(page, encoding="utf-8")
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={folder}/chrome",
            f"--print-to-pdf={REPORT_PDF}", html_file.as_uri(),
        ], check=True, capture_output=True, timeout=120)
    print(f"Saved {REPORT_PDF}")


def main():
    if "--recalculate" in sys.argv or not REPORT_MD.exists():
        calculate()
    render_pdf()


if __name__ == "__main__":
    main()
