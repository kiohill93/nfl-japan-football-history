# Methodology

Compiled November 2026 from public sources. This page explains where the numbers on this site come from, how they were checked, what the markers mean and what is missing.

## What this is

Research notes on two subjects: the history of the NFL (1920 to November 2026) and the history of American football in Japan (1934 to November 2026). The notes summarise public sources in their own words, link each fact to the page it came from, and quote sparingly. They are not official NFL, NFL Japan, JAFA or X League data, and no organisation reviewed them.

## How the research was done

- **Desk research of public sources, in Japanese and English**, carried out in late October and early November 2026. The NFL history rests mostly on English sources; the Japan history mostly on Japanese ones (JAFA, Japanese Wikipedia, Japanese newspapers and government documents).
- **Web search, then page reads.** Searches found candidate pages; facts were taken only from pages that were opened and read. Where a figure was seen only in a search-result snippet, it is marked as such.
- **Official pages and free data APIs where they exist.** Examples: JAFA's 90-year history (one page per year, 1934-2023) and its FY2025 accounts; NFL Football Operations for the salary cap; the NFL Concussion Settlement site; the Sasakawa Sports Foundation's federation survey; the Wikimedia pageviews API; PubMed's E-utilities API; nflverse's contract data (Over The Cap); Gallup.
- **Blocked pages.** When a site refused automated requests, the research tried a plain request, the site's own feeds, and archived copies (Pro Football Reference attendance tables were read through Internet Archive snapshots). Paywalled articles were used only as far as their public summary line; that is noted where it applies.
- **Numbers checked against a second source where possible.** For example: the salary cap (NFL Football Operations against Spotrac, with both shown where they differ); league revenue in 2010 (Sportico against Wikipedia); Japan's FY2024 registered players (read directly from the SSF survey PDF and matched against Flag Football Global's summary); the 1946 Atom Bowl (a fan-run list against Paleofuture's account). Where a second source disagreed, both figures are given and the row is marked **[conflict]**.
- **Arithmetic is labelled.** Shares, multiples, per-game averages and contract records that the research computed itself are marked **[derived]** (or described as "my arithmetic") and the source data is named.
- **Each topic file ends with a source list** in two parts: the sources that answered, and the ones that came up empty or only partly answered.

## How to read the markers

| Marker | Meaning |
| --- | --- |
| **[unconfirmed]** | Seen only in a search snippet or a single weak source (used in the NFL sections) |
| **[?]** | Not confirmed by a second source, or seen only in a snippet (used in the Japan sections) |
| **[conflict]** | Sources disagree; both versions are given and the disagreement is explained nearby |
| **[derived]** | Computed by the research from a cited source |
| **[inferred]** | Estimated from a source's headline rather than stated in it |
| **[snippet]** | Read from a search-result snippet; the full page was not opened |
| **[JA]** / **[EN]** | Japanese or English source |

In the CSV files, a value carrying one of the uncertainty markers ([unconfirmed], [?], [conflict], [snippet], [inferred]) is never stored as a number. It sits in the row's `note` column, and the number column is left blank. Charts are drawn only from the number columns.

## How the datasets were built

The CSVs in `data/` were transcribed from the tables in the research notes, one dataset per file, with the numbers exactly as the research gives them. Units were made explicit (for example "$54.5K" became 54500 in a column labelled US dollars), but no value was rounded, interpolated, or filled in for a missing year. Where a source gives a range ("$416M-$433M") or a split value, the number column is blank and the text goes in `note`. `data/catalog.json` describes each dataset: title, description, columns and units, source URLs, a confidence rating and caveats.

<!-- datasets -->

## Confidence levels

- **High:** an official or primary source (league, federation, court-supervised settlement, survey body, data API), or a well-maintained compilation checked against a second source.
- **Medium:** reliable secondary sources (sports-business press, Wikipedia) without a full second check, or a dataset that mixes counting methods or relies on the research's own arithmetic.
- **Low:** a few confirmed points with most of the series missing or resting on snippets and estimates.

## Source types

| Type | Examples | How they are used |
| --- | --- | --- |
| League and federation | NFL.com, NFL Football Operations, NFL media releases, NFL Japan, JAFA year pages, reports and accounts, NFA (X League) releases and spectator surveys | Primary facts and figures |
| Courts, government and public bodies | NFL Concussion Settlement site, House Judiciary staff report (June 2026), MEXT, Japan's gBizINFO register, OpenSecrets | Legal, policy and money facts |
| Survey bodies | Gallup, Sasakawa Sports Foundation, Central Research Services, Mitsubishi UFJ Research & Consulting with Macromill, Spectrum Reach (Scarborough), Nielsen | Interest, participation and audience measures |
| Research literature | Boston University CTE studies (via Wikipedia), PubMed, the Journal of the Japanese Society of Athletic Training | Health and safety |
| Press | Sportico, ESPN, CNBC, Sports Business Journal, Yahoo Sports, Jiji, Nikkei, Asahi, Yomiuri, Nikkan Sports, Gendai | Business, media and recent events |
| Reference | English and Japanese Wikipedia | History, people and compiled tables; cross-checked where possible |
| Data | nflverse (Over The Cap), Wikimedia pageviews API, Pro Football Reference via the Internet Archive | Contracts, pageviews, attendance |
| Fan and secondary sites | luckyshow.org, amefootojisan.com, Kashikapedia, fan blogs | Lowest weight; always marked **[?]** when a figure rests on them alone |

## Known gaps

- **No published NFL audience figures for Japan.** No Video Research rating was found for any NFL game or Super Bowl in Japan, and DAZN, Nittele G+ and NFL Game Pass publish no Japan viewer or subscriber numbers. The NFL's country breakdown of the Super Bowl LVIII audience did not list Japan ([NFL Japan, Mar 2024](https://nfljapan.com/headlines/98308)).
- **The NFL does not publish an international revenue share.** International game income flows into national revenue, which is split equally among the 32 clubs, but no figure for the international part was found.
- **No free year-by-year league revenue series.** Statista is paywalled and S&P Global's page was blocked, so only scattered years have figures.
- **Crowds for the American Bowls in Japan, 1990-2005,** were not found game by game; the 1989 figure has two conflicting sources.
- **Japanese TV ratings:** none were found for the Rice Bowl, the Koshien Bowl or NFL games on NHK; only three football-related ratings from 1976, 1977 and 2005.
- **X League attendance** before 2024 is not published as season totals; recent averages rest on a fan blog and a paywalled summary.
- **Fan demographics:** US fan age, gender and ethnicity data is mostly proprietary (Nielsen, the NFL); one Scarborough profile was found. Japan has no NFL fan-population figure in the surveys checked.
- **Other gaps:** stadium-subsidy totals; NFL pension amounts; the 2025 season's concussion total; Japanese injury totals by year after 2010; Japanese college programme budgets and coaching salaries; per-club X League revenue; game-by-game crowds for the Koshien Bowl in many early years.

## Rebuilding

The site is static. `src/build.py` reads `content/` and `data/` and writes the pages to `docs/`. See the README for the commands.
