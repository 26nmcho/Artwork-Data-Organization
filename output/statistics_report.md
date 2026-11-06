# Artwork data: every stat so far

Numbers last calculated November 6, 2026. Everything our scripts have calculated so far, all in one spot. Nothing fancy.

**Want to change something?** Edit `output/statistics_report.md`, then run `python3 statistics_report.py` to rebuild this PDF. Your edits stick unless you run it with `--recalculate`, which redoes the numbers and saves your old version as a `.bak` file.

## The quick version

| Dataset | Paintings | Unique IDs | Usable | Avg words |
|---|---|---|---|---|
| Chicago | 1,132 | 1,132 | 1,064 | 131.3 |
| Cleveland, new API | 2,339 | 2,180 | 2,339 | 91.7 |
| Cleveland, old API | 4,234 | 4,234 | 1,443 | 109.5 |

"Usable" means it passed that script's filter, and the average word count is for that group. The new API pull only kept complete records in the first place, so all of its rows count.

## Art Institute of Chicago

### The original scrape

From `artwork_processing.py`. Heads up: the missing-field counts stop at the first thing missing, so one artwork only ever gets counted once.

| Count | Files |
|---|---|
| Scanned | 134,079 |
| Accepted | 1,189 |
| Rejected | 132,890 |
| Errors | 1 |
| No ID | 0 |
| No title | 1 |
| No description | 121,036 |
| No short description | 12,308 |
| No image ID | 1 |
| No artwork type | 0 |
| Not a painting | 127,469 |

### After image hunting and cleaning

| Count | Value |
|---|---|
| Paintings left in the dataset | 1,132 |
| Unique IDs | 1,132 |
| Skipped in round one | 77 |
| Skipped in round two | 60 |
| Second-round skips still in the dataset | 0 |
| Paintings with a local .jpg | 1,075 |
| Have a description, date, and place of origin | 1,064 |

Everything below uses that last group, same as `data-visualization.py`.

### Word counts and dates

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| Description words | 1,064 | 131.3 | 71.1 | 19 | 98 | 113 | 138 | 974 |
| Start year | 1,064 | 1823.9 | 187.2 | -1069 | 1764 | 1890 | 1938.25 | 2020 |

### Top 10 places of origin

| Place | Paintings |
|---|---|
| United States | 332 |
| France | 201 |
| Italy | 71 |
| Japan | 42 |
| Netherlands | 42 |
| Spain | 40 |
| Germany | 40 |
| China | 36 |
| England | 21 |
| Flanders | 20 |

### Paintings per era

| Era | Paintings |
|---|---|
| classical | 1 |
| medieval | 20 |
| renaissance | 111 |
| early modernity | 173 |
| 19th century | 73 |
| impressionist period | 122 |
| post-impressionist | 112 |
| modern | 335 |
| contemporary | 117 |

## Cleveland: new API (`cleveland_harvested_data.json`)

From `cleveland_statistics.py` and `image_metadata_check()`. These count every row, so the duplicates are still in here.

| Count | Value |
|---|---|
| Rows | 2,339 |
| Duplicate IDs | 159 |
| Unique IDs | 2,180 |
| Unique IDs with no local image | 0 |

### Missing data and types per column

| Column | Type | Null | Empty text | Empty list | Zeros |
|---|---|---|---|---|---|
| id | int | 0 | 0 | 0 | 0 |
| title | str | 0 | 0 | 0 | 0 |
| description | str | 0 | 0 | 0 | 0 |
| creation date early | int | 0 | 0 | 0 | 0 |
| creation date late | int | 0 | 0 | 0 | 0 |
| creators | list | 0 | 0 | 963 | 0 |
| technique | str | 0 | 0 | 0 | 0 |
| image | str | 0 | 0 | 0 | 0 |
| culture | list | 0 | 0 | 12 | 0 |

Note: the empty-string, zero, and null lines in `missing_data_check` use `.sum()` on the matching values and don't really count them, so they're counted properly here.

### Word counts and dates

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| Description words | 2,339 | 91.7 | 43.0 | 1 | 62 | 87 | 108 | 507 |
| Earliest year | 2,339 | 1631.1 | 210.9 | -300 | 1555 | 1650 | 1788 | 1949 |

## Cleveland: old API (`cleveland_historical_api.json`)

From `historical_data_processing()` and `cleveland_visualization.py`.

| Count | Value |
|---|---|
| All artworks | 61,792 |
| Paintings | 4,234 |
| Paintings with an image and a wall or digital description | 1,443 |
| ...with a wall description | 1,402 |
| ...with a digital description | 120 |
| Paintings with a description, date, and image | 1,443 |
| Descriptions with HTML tags | 235 |

### Missing values per column (out of 1,443)

| Column | Missing | Percent |
|---|---|---|
| id | 0 | 0.0% |
| title | 0 | 0.0% |
| creation_date | 0 | 0.0% |
| creation_date_earliest | 0 | 0.0% |
| creation_date_latest | 0 | 0.0% |
| technique | 0 | 0.0% |
| type | 0 | 0.0% |
| culture | 6 | 0.4% |
| wall_description | 41 | 2.8% |
| creators | 366 | 25.4% |
| inscriptions | 985 | 68.3% |
| digital_description | 1,323 | 91.7% |

### Number summary for that same group

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| ID | 1,443 | 145947.2 | 29603.3 | 78982 | 135914 | 148358 | 154864.5 | 315934 |
| Earliest year | 1,443 | 1653.1 | 187.7 | 25 | 1555 | 1695 | 1800 | 1915 |
| Latest year | 1,443 | 1683.5 | 182.5 | 37 | 1595 | 1716 | 1817.5 | 1940 |

Everything below uses the description, date, and image group. HTML tags get removed before counting words.

### Word counts and dates

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| Description words | 1,443 | 109.5 | 66.9 | 1 | 70 | 99 | 132 | 559 |
| Start year | 1,443 | 1653.1 | 187.7 | 25 | 1555 | 1695 | 1800 | 1915 |
| Date range (years) | 1,443 | 30.5 | 39.6 | 0 | 3 | 10 | 50 | 299 |

### Top 10 places of origin

| Place | Paintings |
|---|---|
| Japan | 375 |
| India | 208 |
| France | 181 |
| China | 159 |
| Italy | 121 |
| America | 85 |
| Netherlands | 61 |
| Korea | 28 |
| Northern India | 28 |
| England | 27 |

### Paintings per era

| Era | Paintings |
|---|---|
| classical | 4 |
| medieval | 121 |
| renaissance | 363 |
| early modernity | 657 |
| 19th century | 155 |
| impressionist period | 97 |
| post-impressionist | 43 |
| modern | 3 |
| contemporary | 0 |

### Oldest paintings

| ID | Title | Date | Start year |
|---|---|---|---|
| 145925 | Funerary Portrait of a Young Girl | c. 25-37 | 25 |
| 145923 | Funerary Portrait of a Man | c. 138-192 | 138 |
| 145924 | Funerary Portrait of a Woman | c. 138-192 | 138 |
| 138881 | Mural Fragment with Elite Male and Maguey Cactus Leaves | 500-550 | 500 |
| 133068 | Seven Leaves from a Manuscript of the Gandavyuha-sutra | 1000s-1100s | 1000 |

### Shortest descriptions

| ID | Title | Words |
|---|---|---|
| 160048 | Bodhisattva Padmapani | 1 |
| 150872 | Falcon | 14 |
| 155382 | Dipak Raga, One of the Thirty-Six Melodies (Ragamala): Personifying Love | 14 |
| 146174 | Shakyamuni under the Bodhi Tree | 16 |
| 148960 | Trees and a Stream on a Hillside | 16 |

### Longest descriptions

| ID | Title | Words |
|---|---|---|
| 143752 | Flowers of the Four Seasons | 550 |
| 143753 | Flowers of the Four Seasons | 550 |
| 149652 | The Four Accomplishments | 559 |
| 149653 | The Four Accomplishments | 559 |
| 149654 | The Four Accomplishments | 559 |

## How the datasets overlap

Cleveland images are saved as `{id}.jpg`, so comparing artwork IDs covers the image overlap too.

| Check | Artworks |
|---|---|
| New API unique IDs | 2,180 |
| ...also anywhere in the old API | 2,097 |
| ...not in the old API at all | 83 |
| Old API usable paintings | 1,443 |
| ...also in the new API | 1,307 |
| ...only in the old API | 136 |
| Same ID number at Chicago and Cleveland (new API) | 9 |

That last row is just two museums reusing a number. They're different artworks, so the combined data needs a `museum` column.

## Description samples, now with abstract as true/false

`abstract` is its own field now, and those paintings got a real era based on their date. This version lives in `output/samples_abstract_boolean.json`. The original sample files haven't been changed.

| Count | Value |
|---|---|
| Rows (one per artwork per prompt) | 166 |
| Different artworks | 83 |
| Prompts | 2 |

### Artworks per era

| Era | Chicago not abstract | Chicago abstract | Cleveland not abstract | Cleveland abstract |
|---|---|---|---|---|
| classical | 1 | 0 | 4 | 0 |
| medieval | 5 | 0 | 5 | 0 |
| renaissance | 5 | 0 | 5 | 0 |
| early modernity | 5 | 0 | 5 | 0 |
| 19th century | 5 | 0 | 5 | 0 |
| impressionist period | 5 | 0 | 5 | 0 |
| post-impressionist | 5 | 0 | 5 | 0 |
| modern | 5 | 4 | 3 | 5 |
| contemporary | 0 | 1 | 0 | 0 |

### The abstract ones

| Museum | ID | Title | Year | Era |
|---|---|---|---|---|
| Chicago | 242223 | Étude No. 1 | 1917 | modern |
| Chicago | 109819 | Lozenge Composition with Yellow, Black, Blue, Red, and Gray | 1921 | modern |
| Chicago | 65821 | Composition (No. 1) Gray-Red | 1935 | modern |
| Chicago | 186682 | Grey Diamond | 1955 | modern |
| Chicago | 146988 | Rodeo | 1971 | contemporary |
| Cleveland | 164630 | Night Café | 1918 | modern |
| Cleveland | 167456 | Rock at Sea | 1920 | modern |
| Cleveland | 149112 | Church Street El | 1920 | modern |
| Cleveland | 135420 | Morning Glory with Black | 1926 | modern |
| Cleveland | 143278 | Composition with Red, Yellow, and Blue | 1927 | modern |

Judgment call: the note in `openAI_description_generation.py` says only the Mondrian is fully abstract at Cleveland and the other four are near-abstract. They're all `true` here because they were all in the abstract group.

## What's not in here

- **Cleveland scrape counters** (no ID, no title, and so on): they only ever printed to the terminal and were never saved. Getting them back means calling the API again.
- **Deleted duplicate image count** from `chicago_manual_data_cleaning.py`: same deal, it only printed.
- **Combined Chicago + Cleveland stats:** our scripts haven't calculated these yet.
- **Charts:** this is just the numbers.
