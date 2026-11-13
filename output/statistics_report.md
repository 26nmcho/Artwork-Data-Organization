# Artwork data: every stat so far

## Overview

| Dataset | Paintings | Unique IDs | Passed script filter | Avg words (filtered) |
|---|---|---|---|---|
| Chicago | 1,132 | 1,132 | 1,064 | 131.3 |
| Cleveland, new API | 2,338 | 2,179 | 2,338 | 91.7 |
| Cleveland, old API | 4,233 | 4,233 | 1,442 | 109.5 |

## Chicago

### Original scrape

Accepted: **1,189** files


### Paintings with a description, date, and place

#### Word counts and dates

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| Description words | 1,064 | 131.3 | 71.1 | 19 | 98 | 113 | 138 | 974 |
| Start year | 1,064 | 1823.9 | 187.2 | -1069 | 1764 | 1890 | 1938.25 | 2020 |

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/chicago_dates.png)
![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/chicago_words.png)
![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/chicago_date_vs_words.png)

#### Top 10 places of origin

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

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/chicago_origins.png)

#### Paintings per era

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

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/chicago_eras.png)

## Cleveland

### New API (`cleveland_harvested_data.json`)

| Count | Value |
|---|---|
| Rows | 2,338 |
| Duplicate IDs | 159 |
| Unique IDs | 2,179 |
| Unique IDs with no local image | 0 |

#### Word counts and dates

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| Description words | 2,338 | 91.7 | 43.0 | 1 | 62 | 87 | 108 | 507 |
| Earliest year | 2,338 | 1631.3 | 210.7 | -300 | 1555 | 1650 | 1788 | 1949 |

### Old API (`cleveland_historical_api.json`)

| Count | Value |
|---|---|
| All artworks | 61,791 |
| Paintings | 4,233 |
| Paintings with an image and a wall or digital description | 1,442 |
| ...with a wall description | 1,402 |
| ...with a digital description | 119 |
| Paintings with a description, date, and image | 1,442 |
| Descriptions with HTML tags | 235 |

#### Missing values per column (out of 1,442)

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
| wall_description | 40 | 2.8% |
| creators | 365 | 25.3% |
| inscriptions | 984 | 68.2% |
| digital_description | 1,323 | 91.7% |

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/cleveland_missing.png)

#### Number summary (image + wall or digital description)

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| ID | 1,442 | 145966.8 | 29604.2 | 78982 | 136016.5 | 148358.5 | 154913.25 | 315934 |
| Earliest year | 1,442 | 1653.5 | 187.2 | 25 | 1555 | 1695 | 1800 | 1915 |
| Latest year | 1,442 | 1683.9 | 181.9 | 37 | 1595 | 1716 | 1817.75 | 1940 |

#### Word counts and dates (description + date + image, HTML removed)

| What | Count | Mean | Std | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| Description words | 1,442 | 109.5 | 66.9 | 1 | 70 | 99 | 132 | 559 |
| Start year | 1,442 | 1653.5 | 187.2 | 25 | 1555 | 1695 | 1800 | 1915 |
| Date range (years) | 1,442 | 30.5 | 39.6 | 0 | 3 | 10 | 50 | 299 |

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/cleveland_dates.png)
![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/cleveland_words.png)
![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/cleveland_date_ranges.png)
![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/cleveland_date_vs_words.png)

#### Top 10 places of origin

| Place | Paintings |
|---|---|
| Japan | 375 |
| India | 207 |
| France | 181 |
| China | 159 |
| Italy | 121 |
| America | 85 |
| Netherlands | 61 |
| Korea | 28 |
| Northern India | 28 |
| England | 27 |

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/cleveland_origins.png)

#### Paintings per era

| Era | Paintings |
|---|---|
| classical | 4 |
| medieval | 120 |
| renaissance | 363 |
| early modernity | 657 |
| 19th century | 155 |
| impressionist period | 97 |
| post-impressionist | 43 |
| modern | 3 |
| contemporary | 0 |

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/cleveland_eras.png)

#### Oldest paintings

| ID | Title | Date | Start year |
|---|---|---|---|
| 145925 | Funerary Portrait of a Young Girl | c. 25-37 | 25 |
| 145923 | Funerary Portrait of a Man | c. 138-192 | 138 |
| 145924 | Funerary Portrait of a Woman | c. 138-192 | 138 |
| 138881 | Mural Fragment with Elite Male and Maguey Cactus Leaves | 500-550 | 500 |
| 133068 | Seven Leaves from a Manuscript of the Gandavyuha-sutra | 1000s-1100s | 1000 |

#### Example: oldest painting

![Funerary Portrait of a Young Girl / ID 145925 / c. 25-37 / 156 words](/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/145925.jpg)

> Traditional Egyptian burial practices continued well into Roman times. These lifelike portraits were made for a specific purpose, namely, to cover the head of the mummified individual represented in the portrait. Typically, they were painted with encaustic (pigment mixed with beeswax) on wooden panels, as was the case with the Funerary Portrait of a Young Girl. Less frequently, they were painted directly onto the linen shrouds that covered the mummy, which is how the other two examples shown here were made. Hairstyles, jewelry, and clothing are carefully rendered according to contemporary fashion. Meticulously rendered details such as skin tone, facial hair, and bone structure suggest a keen sense of the subject's individuality, and with it, an inevitable sense of mortality. The addition of gilded details on the lips and jewelry of the young girl is a rare detail that alludes to the individual's transformation in death into a blessed spirit, or akh, a being of light.

#### Shortest descriptions

| ID | Title | Words |
|---|---|---|
| 160048 | Bodhisattva Padmapani | 1 |
| 150872 | Falcon | 14 |
| 155382 | Dipak Raga, One of the Thirty-Six Melodies (Ragamala): Personifying Love | 14 |
| 146174 | Shakyamuni under the Bodhi Tree | 16 |
| 148960 | Trees and a Stream on a Hillside | 16 |

#### Example: shortest description

![Falcon / ID 150872 / 1615-1867 / 14 words](/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/150872.jpg)

> This otsu-e painting depicts a hunting falcon, a lucky charm for a bountiful harvest.

#### Longest descriptions

| ID | Title | Words |
|---|---|---|
| 143752 | Flowers of the Four Seasons | 550 |
| 143753 | Flowers of the Four Seasons | 550 |
| 149652 | The Four Accomplishments | 559 |
| 149653 | The Four Accomplishments | 559 |
| 149654 | The Four Accomplishments | 559 |

#### Example: longest description

![The Four Accomplishments / ID 149654 / late 1500s / 559 words](/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/149654.jpg)

> At first this scene appears a bit strange, if not bizarre: men, young and old, sit in a vast wilderness playing a board game or executing an ink painting. The furniture and ceramic wares are elegant, the attire is fashionably informal, and the young attendants outnumber the gentlemen of leisure. Clouds and mist roll through the landscape, whose bleakness suggests late fall or early spring, a chilly time to be outdoors engaged in what Westerners would call pastimes or hobbies. But we are viewing the past, a pictorial vision of a cultured gentleman’s ideal in classical East Asian history: the Four Accomplishments. This enduring Confucian theme embraces the arts of calligraphy, painting, music, and go (a game of strategy akin to chess), each of which is portrayed or suggested in this pair of 16th-century folding screens, or byøbu. In the left screen, the multiple brushes and a large flat rock surface for writing refer to painting and calligraphy; in the right screen, a seven-stringed musical instrument called a qin, protected in cloth and resting on the large wooden table close to the game players, indicates music and the game of go. The daily pursuit of one or more of these activities has a venerated history in ancient China, one that was transmitted to Korea and Japan by at least the 1400s, when interest in Chinese culture pervaded medieval Japanese society. In Kyoto, Zen culture favored this theme, introducing it into mural painting programs organized for temple interiors as early as the late 1400s. The Kano school painters, in particular, are noted as the most prolific exponents of this theme, and their popularity reached a high point in the early 1600s. The Kano atelier produced many hundreds of paintings in various formats for private and institutional clients, guided by the work ethic, management skills, and academic painting style of Kano Motonobu (1476–1559). These byøbu follow that master’s style as exemplified in the sliding-door panel paintings depicting Zen patriarchs from the Daisen-in subtemple at the Daitoku-ji in Kyoto (c. 1513). Traditionally attributed to his son Kano Shøei, those byøbu show Motonobu’s legacy of distinctive “nailhead” brushstrokes (in the depiction of robing), spiky and elongated plant forms, and crystalline rock formations. The new, more relaxed pictorial elements and broader painting techniques that give this composition a distinct sense of quietude, however, suggest the hand of Kano Yukinobu, who was also active in the later 1500s in Kyoto. Comparison with the narrative and compositional elements of Horses and Grooms in the Stable (1934.373) is as enlightening as it is instructive in helping distinguish yamato-e and kara-e painting styles, parallel streams in medieval Japan. Two unobtrusive elements in the byøbu here provide insights into the evolution of the Four Accomplishments theme in the 1500s. First is the greater importance placed on the depiction of a landscape setting. Second, these lofty exemplars of classical China are portrayed in groupings that convey a distinctive relaxed ambience when compared to earlier Chinese or Japanese presentations. To understand this important leitmotif emerging in conventional ink painting circles at mid-century, one need only gaze at the young page slouched beside the stream watching fish swimming nearby. Confucian ideals as well as notions of Zen rectitude have been superseded in these byøbu by a series of beguiling vignettes showing human engagement and companionship in an open and receptive natural setting.

### New API vs. old API

| Check | Artworks |
|---|---|
| New API unique IDs | 2,179 |
| ...also anywhere in the old API | 2,096 |
| ...not in the old API at all | 83 |
| Old API usable paintings | 1,442 |
| ...also in the new API | 1,306 |
| ...only in the old API | 136 |

## Description generation

### Samples

| Count | Value |
|---|---|
| Rows (one per artwork per prompt) | 246 |
| Different artworks | 82 |
| Prompts | 3 |

#### Artworks per era

| Era | Chicago not abstract | Chicago abstract | Cleveland not abstract | Cleveland abstract |
|---|---|---|---|---|
| classical | 1 | 0 | 4 | 0 |
| medieval | 5 | 0 | 4 | 0 |
| renaissance | 5 | 0 | 5 | 0 |
| early modernity | 5 | 0 | 5 | 0 |
| 19th century | 5 | 0 | 5 | 0 |
| impressionist period | 5 | 0 | 5 | 0 |
| post-impressionist | 5 | 0 | 5 | 0 |
| modern | 5 | 4 | 7 | 1 |
| contemporary | 0 | 1 | 0 | 0 |

![](/Users/noahshomefolder/Code/Data Projects/Artwork Data Organization/output/charts/samples_per_era.png)

#### Abstract artworks

| Museum | ID | Title | Year | Era |
|---|---|---|---|---|
| Chicago | 242223 | Étude No. 1 | 1917 | modern |
| Chicago | 109819 | Lozenge Composition with Yellow, Black, Blue, Red, and Gray | 1921 | modern |
| Chicago | 65821 | Composition (No. 1) Gray-Red | 1935 | modern |
| Chicago | 186682 | Grey Diamond | 1955 | modern |
| Chicago | 146988 | Rodeo | 1971 | contemporary |
| Cleveland | 143278 | Composition with Red, Yellow, and Blue | 1927 | modern |
