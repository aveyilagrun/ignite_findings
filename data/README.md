# Data

The data files are not in the repository. Ask Azhar for them.

## Files in this folder

| File | Contents |
|---|---|
| `raw_data.7z` | `raw_data/<journal>/` holds text exports from ScienceDirect, per journal and country. |
| `extracted_data.7z` | `extracted_data/<journal>_<country>.csv` holds records parsed by `extract_data.ipynb`. |
| `elsevier_data.7z` | `elsevier_data/<journal>_<country>.csv` holds the extracted records plus Crossref citations, Scopus h-indices and PlumX metrics (`process_data.ipynb`). |
| `processed_data.7z` | `processed_data/<journal>_<country>_genders.csv` holds the Elsevier records plus Namsor gender predictions. **This is the input to all analysis.** |
| `all_singapore.csv`, `all_singapore_with_affiliations.csv` | Singapore subset plus OpenAlex affiliations (`affiliation.ipynb`). These were shared separately for name checking. |

Extract the archives into the repository root so that `processed_data/` sits next to `scripts/`:

```bash
7z x data/processed_data.7z -o.
```

[CHECK] The archives are dated 16 Apr 2025, the same as the folders, but nobody has verified they are identical. `processed_data/` also contains `*_gender.csv` files (singular), which have first-author gender only (no all-author gender columns) and appear to be an earlier stage. The analysis uses only `*_genders.csv`.

**Known problems in `*_genders.csv`, handled by `scripts/headline_stats.py`:**
- The `solar_energy_<country>_genders.csv` files also contain *Solar Energy Materials and Solar Cells* articles (2,083 rows), most of which are also in the `solar_energy_materials_and_solar_cells_<country>` files. A few files also repeat rows. The script keeps one row per DOI and country (2,247 rows removed).
- 161 rows have no `First Author` (the Scopus lookup failed). Their metrics are empty and their gender is "male" at about 0.55 because the API was called with an empty name. The script removes them.
- 755 records have a first author with initials only, so the gender label carries no information. They are kept, and a check without them is reported.
- A few rows are not journal articles (book chapters with `Editor(s): …` as the title, and *Solar Energy Advances*) or have corrupt years. The script removes them.

Note that `extracted_data/` names South Africa files `south africa` (with a space). The later stages use `south_africa`.

## Columns of `processed_data/*_genders.csv`

| Column | Meaning |
|---|---|
| Item Title, Publication Title, Journal Volume, Journal Issue, Item DOI, Keywords, URL, Content Type | Article metadata from the ScienceDirect export |
| Authors | Python-list string of the co-author names (the first author is in `First Author`) |
| Publication Year | Year. A few raw values are corrupt (e.g. 1, 8052); the analysis keeps 2010–2025. |
| Citations (Crossref) | Crossref `is-referenced-by-count` |
| First Author, First Author H-Index, Authors H-index | Scopus via `pybliometrics` AuthorRetrieval |
| Captures, Citations, Mentions, Social Media, Usages | PlumX metrics. `Citations` is the column used for the citation-gap results. |
| Gender (First Author), Gender likelihood (First Author) | Namsor `genderFullGeoBatch` label and calibrated probability |
| Gender (Authors), Gender likelihood (Authors) | The same for all listed authors (list strings). Low confidence; see FINDINGS A4. |

Country is not a column. It comes from the file name.

## Not included

- Article PDFs (needed by `analysis/4_word2vec_pretrained.ipynb`).
- UK-phase intermediate files in `data_extraction/`, which lived outside this repository.
