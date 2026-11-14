# Artwork Data Organization

The data side of a mentored research study on how well large language models write museum descriptions of artworks. This repo collects artwork records and images from two museum open-access sources, generates LLM descriptions of a fixed sample under three prompts, and builds statistics and era-analysis reports.

*Last updated Nov 13, 2026 (commit [`3ea28ed`](https://github.com/26nmcho/Artwork-Data-Organization/commit/3ea28ed)).*

## At a glance

| | |
|---|---|
| Study goal | Benchmark LLMs on writing useful museum descriptions; this repo is the data side |
| Museums in the code | Art Institute of Chicago, Cleveland Museum of Art |
| Also named as sources | Met, Smithsonian, Getty (no code yet) |
| Comparable datasets studied | ArtCap, ArtEmis, Artpedia, SemArt, BibleVSA, WikiArt |
| Description sample | 82 artworks (41 per museum) × 3 prompts = **246 descriptions** |
| Model | `gpt-5-mini`, image sent at high detail |
| Outputs | `output/statistics_report.pdf`, `output/era_paintings.pdf` |
| Current assignment | Statistical audit of the Cleveland API dataset (2,338 rows) |

## Repository layout

```
chicago/        Art Institute of Chicago: JSON harvest, semi-manual image collection, cleaning, charts
cleveland/      Cleveland Museum of Art: Open Access API harvest, image download, EDA, stats, charts
data/           Harvested datasets, skipped-artwork lists, removed_artworks.json
                (cleveland_historical_api.json is gitignored: 61,791 artworks)
descriptions/   generate_descriptions.py, descriptions.json (246 rows), era_notes.json, notes.md, charts
output/         statistics_report.{md,pdf}, era_paintings.{md,pdf}, charts/
old_scripts/    Archived pre-reorganization scripts (API key scrubbed)
statistics_report.py   Builds the statistics report and the era PDF
```

Images are kept outside the repo in `../Museum Data/chicago_images` and `../Museum Data/cleveland_images`.

## How to run

```bash
python3 descriptions/generate_descriptions.py --dry-run   # list missing (artwork, prompt) pairs
python3 descriptions/generate_descriptions.py             # generate only what's missing
python3 statistics_report.py --era                        # rebuild only the era PDF
```

`OPENAI_API_KEY` is read from a gitignored `.env`. `statistics_report.py --recalculate` rebuilds all numbers and charts, but it overwrites hand edits in `output/statistics_report.md`.

## Methods (decisions in force)

**Chicago data** (since Aug 22). Artwork JSON files, kept only if they have an `id`, `title`, `description` and `image_id`; HTML stripped from descriptions. Every rejected artwork is logged rather than dropped silently.

**Chicago images** (since Oct 9). Cloudflare blocked scripted downloads (header changes and Selenium both failed, Sep 9). Workaround: open each artwork by hand; the script waits for the file, renames it to the artwork ID, and `s` skips. Artworks still skipped after a second round leave the dataset; exact-duplicate images are deleted by hash.

**Cleveland data** (since Sep 10–11). Live Open Access API: `type=Painting`, `has_image=1`, 25 per request, keeping id, title, description, dates, creators, technique, culture, images, url and license. Culture is trimmed to the country (e.g. "France") for place of origin.

**Cleveland historical export** (since Oct 15). Used for comparison: paintings with an image and a wall or digital description (1,442 of 4,233 paintings). Wall description is used first; HTML is stripped before counting words.

**Eras** (since Oct 15), by start year:

| Era | Up to |
|---|---|
| Classical | 500 |
| Medieval | 1400 |
| Renaissance | 1600 |
| Early modernity | 1800 |
| 19th century | 1860 |
| Impressionist | 1886 |
| Post-impressionist | 1905 |
| Modern | 1970 |
| Contemporary | after 1970 |

**Sample** (Oct 16, finalized Nov 6). About 5 paintings per era per museum plus an abstract subset: 82 artworks, 41 per museum. Cleveland had only 4 classical, 3 modern and 0 contemporary paintings to draw from.

**Prompts** (all 100–150 words). A new prompt gets a new name; rewording an existing one won't regenerate it.

| Name in code | Added | Intent |
|---|---|---|
| `high_restrictions_context_for_project` | Oct 16 | Museum curator, museum-style tone |
| `less_restriction_alt_text_method` | Oct 28 | Alt text for blind and low-vision readers |
| `plain_description` | Nov 6 | "Write a description of this picture" |

**Abstract label** (since Nov 13). A work is abstract only if a museum or catalogue source calls it abstract. Six qualify: 5 Chicago works plus Cleveland's Mondrian. Night Café, Church Street El, Rock at Sea and Morning Glory with Black were relabeled false.

**Removals** (since Nov 6). Every removed artwork is logged with reason and date in `data/removed_artworks.json`:

| ID | Museum | Reason | Removed |
|---|---|---|---|
| 117658 | Cleveland | Manuscript cover, not a painting | Nov 6 |
| 220168 | Chicago | Duplicate of 185008 (same image, title, description) | Nov 13 |
| 160048 | Cleveland | Description is just "a" | Nov 13 |

**Reporting** (Nov 6, Nov 13). Statistics report with each chart directly under its table; a separate era PDF for qualitative analysis, using one fixed sample painting per era (`ERA_SAMPLE` in `statistics_report.py`) so notes can't drift onto a different painting.

## Timeline

### August 2026: Chicago dataset

| Date | Commit | Work |
|---|---|---|
| Aug 22 | [`b40feb8`](https://github.com/26nmcho/Artwork-Data-Organization/commit/b40feb8), [`82f6385`](https://github.com/26nmcho/Artwork-Data-Organization/commit/82f6385) | Baseline Chicago collection: read artwork JSON, strip HTML, save keepers to `harvested_data.json`. To-do set: scrape images, pandas stats (start date, origin, word count), matplotlib charts, a Cleveland pipeline |
| Aug 23 | [`b7891dc`](https://github.com/26nmcho/Artwork-Data-Organization/commit/b7891dc), [`e71aa2c`](https://github.com/26nmcho/Artwork-Data-Organization/commit/e71aa2c) | Image processing with trackers for errors and rejected objects |

### September 2026: Cloudflare, Cleveland pipeline, audit scope

| Date | Commit | Work |
|---|---|---|
| Sep 9 | [`ab2e4f0`](https://github.com/26nmcho/Artwork-Data-Organization/commit/ab2e4f0) | Chart and image-processing progress; Cloudflare blocks Chicago image downloads. A Selenium attempt lives on the `chrome-selenium` branch. Plan set: 3–4 paintings per era from classical to contemporary/abstract. Working idea: more concrete or classic paintings get more descriptive text |
| Sep 10 | [`123b327`](https://github.com/26nmcho/Artwork-Data-Organization/commit/123b327) → [`3d6bcd5`](https://github.com/26nmcho/Artwork-Data-Organization/commit/3d6bcd5) (10 commits) | Split into Chicago and Cleveland; Cleveland metadata retrieval (bug traced to one parameter's capitalization); first validation checks; paging by 25; dataset renames; Cleveland image download and tracker |
| Sep 11 | [`70a329a`](https://github.com/26nmcho/Artwork-Data-Organization/commit/70a329a) | Added culture as a field and reran the Cleveland collection |
| Sep 13 | [`15092b4`](https://github.com/26nmcho/Artwork-Data-Organization/commit/15092b4) | Backup |
| Sep 23 | [`61c6ad1`](https://github.com/26nmcho/Artwork-Data-Organization/commit/61c6ad1) | Metadata check: missing values per column and duplicate IDs. The null check "returned all zeros" |
| Sep 24 | — | Cleveland audit scoped (see below) |
| Sep 25 | [`440f62d`](https://github.com/26nmcho/Artwork-Data-Organization/commit/440f62d) | Pandas processing file started |

### October 2026: images unblocked, first LLM descriptions

| Date | Commit | Work |
|---|---|---|
| Oct 9 | [`9c81f40`](https://github.com/26nmcho/Artwork-Data-Organization/commit/9c81f40) | Semi-manual Chicago image collection and cleaning (hash dedup). Round 1 skipped 77 artworks |
| Oct 15 | [`fba27a8`](https://github.com/26nmcho/Artwork-Data-Organization/commit/fba27a8), [`d768e78`](https://github.com/26nmcho/Artwork-Data-Organization/commit/d768e78) | Reorganized; Cleveland historical export (61,791 artworks, gitignored); OpenAI script created; 60 second-round skips saved; historical-data prep and sanity-check charts; era bins defined |
| Oct 16 | [`655d632`](https://github.com/26nmcho/Artwork-Data-Organization/commit/655d632) | First `gpt-5-mini` descriptions for 37 hand-picked Cleveland paintings with the curator prompt |
| Oct 28 | [`2c836ca`](https://github.com/26nmcho/Artwork-Data-Organization/commit/2c836ca) | Alt-text prompt; 5 abstract artworks added; side-by-side prompt samples; description-length stat; API key moved to `.env` |

### November 2026: one pipeline, report, cleanup

| Date | Commit | Work |
|---|---|---|
| Nov 6 | [`eb97992`](https://github.com/26nmcho/Artwork-Data-Organization/commit/eb97992), [`3824dcb`](https://github.com/26nmcho/Artwork-Data-Organization/commit/3824dcb) | Samples for both museums; EDA script; `statistics_report.py` (Markdown + PDF); abstract stored as boolean |
| Nov 6 | [`a31cafd`](https://github.com/26nmcho/Artwork-Data-Organization/commit/a31cafd) | Reorganized into `data/ chicago/ cleveland/ descriptions/ output/`; single `descriptions.json` and `generate_descriptions.py`; plain prompt run on both museums (246 descriptions); report split into Chicago, Cleveland and Description generation sections with annotations applied; era analysis moved to its own PDF; old scripts archived with key removed; removals log started |
| Nov 13 | [`91b35bb`](https://github.com/26nmcho/Artwork-Data-Organization/commit/91b35bb) | Era notes (`era_notes.json`) added to the era PDF |
| Nov 13 | [`1633234`](https://github.com/26nmcho/Artwork-Data-Organization/commit/1633234) | Removed 220168 and 160048; abstract relabeling (6 works) |
| Nov 13 | [`3ea28ed`](https://github.com/26nmcho/Artwork-Data-Organization/commit/3ea28ed) | Era PDF split into "Sampling and notes" and "All generated descriptions"; `--era` flag |

## Findings so far

**Average description length** across all 82 artworks: curator 122.0 words, alt text 127.1, plain 116.5.

**Era notes** (qualitative, from `descriptions/era_notes.json` and `descriptions/notes.md`):

- **Classical**, *Funerary Papyrus of Tayuhenutmut*: only the curator prompt names the New Kingdom Book of the Dead; alt text gives dimensions; the plain prompt still identifies a deity.
- **Medieval**, *The White Path to the Western Paradise*: the plain description leans into rhetoric when the painting ties to a widely known religion.
- **Renaissance**, *Virgin and Child*: all three descriptions are nearly the same. With famous religious figures the text shifts to characters and context; the papyrus got size and palette instead.
- **Early modernity**, *Ruins in a Rocky Landscape*: the plain description stresses subjects over mood.
- **19th century**, *Aurora and Cephalus*: curator and alt text are close, alt text more physical; plain drifts into commentary.
- **Modern**, *Souvenir of an "International Ball"*: plain says "figure" where the others say "woman"; the curator prompt is the one that skips mood.
- **Overall**: the more abstract the painting, the less the plain description differs from the other two. For older works, descriptions tend to mention framing or physical condition.
- Not yet noted: impressionist, post-impressionist and contemporary samples.

## Cleveland audit status

Scope (Sep 24): row and field counts; four kinds of missing (`None`, missing key, empty/whitespace text, empty collection); description-length distribution; missingness by category; selection-bias caveats; short interpretation; reproducible regeneration. The collector itself is not to be rewritten.

| Deliverable | Exists now | Gap |
|---|---|---|
| Row and field counts | API file: 2,338 rows, 2,179 unique IDs, 159 duplicate IDs; every unique ID has a local image | No field-by-field counts; word stats (mean 91.7) include duplicate rows |
| Missingness, four kinds | Missing-per-column table for the historical export (creators 25.3%, inscriptions 68.2%, digital description 91.7%) | Not done for the API file. A plain null check can't see empty strings or empty lists (160048 had `creators: []` and a one-letter description) |
| Missingness figure | `cleveland_missing.png` (historical export) | Redo for the API file |
| Description-length figure | `cleveland_words.png` (historical export) | API file has a table but no figure |
| Missingness by category | — | Not started (e.g. by era or culture) |
| Selection-bias caveats | — | Candidates: paintings only; only works with an image and description; Cleveland leans older (median earliest year 1650) |
| Short interpretation | — | Not written |
| Reproducible regeneration | `statistics_report.py --recalculate` | Paths are hard-coded to one machine; historical export and images aren't in the repo |

## Known issues

- Report counts outside the abstract section still include 160048 and 220168; they weren't recalculated to preserve hand edits in `statistics_report.md`.
- `local_image` paths in `descriptions.json` are absolute paths to one machine.
- `cleveland/eda.py` labels the museums "Chicago Institute of Art" and "Cleveland Institute of Art".

## Next steps

- [ ] Resolve the 159 repeated IDs in the Cleveland API file before reporting its stats
- [ ] Count the four kinds of missing on that file, then draw its missingness and description-length figures
- [ ] Missingness by category (era, culture)
- [ ] Write the selection-bias caveats and the short interpretation
- [ ] Replace hard-coded paths with project-relative ones so others can rerun the report
- [ ] Era notes for the impressionist, post-impressionist and contemporary samples
- [ ] Fix museum names in `cleveland/eda.py`
- [ ] Add Met, Smithsonian and Getty sources
