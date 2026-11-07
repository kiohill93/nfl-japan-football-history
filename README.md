# NFL and Japan Football History

A static research site on two subjects: the history of the National Football League (1920 to November 2026) and the history of American football in Japan (1934 to November 2026). It covers the timeline, business and media, money and salaries, policy, health and safety, links to the military and government, culture, and viewership and fans, plus a list of the people who shaped each story.

Compiled November 2026 from public sources.

**This is not official data.** These are research notes summarised from public sources (league and federation pages, government documents, survey bodies, the press and Wikipedia). They are not published, reviewed or endorsed by the NFL, NFL Japan, the Japan American Football Association (JAFA), the X League or any other organisation.

## What is on the site

| Page | Contents |
| --- | --- |
| `index.html` | Overview: headline figures, a short summary of each subject and the key charts |
| `nfl.html` | NFL history in nine sections |
| `japan.html` | American football in Japan in eight sections |
| `people.html` | Important people in both stories |
| `data.html` | Every dataset with its description, columns, sources, confidence, caveats, a preview and a CSV download |
| `methodology.html` | How the research was done, what the markers mean, confidence ratings and known gaps |

## Architecture

```
content/        Markdown research notes (one file per topic) and methodology.md
  nfl/          01-timeline.md ... 09-viewership-and-fans.md
  japan/        01-timeline.md ... 08-viewership-and-fans.md
  people.md
data/           Tidy CSV datasets plus catalog.json (titles, columns and units, sources, confidence, caveats)
src/
  build.py      Reads content/ and data/, renders the pages and writes docs/
  templates/    Jinja2 templates shared by every page
  static/       style.css (light and dark mode) and charts.js (Plotly rendering)
tools/
  check_private.py   Scans the sources and the built site for strings that must not be published
docs/           The built site, served by GitHub Pages (generated; do not edit by hand)
```

`src/build.py` converts each Markdown file to HTML, inserts the charts after the headings they belong to, and writes the chart specifications as JSON into each page. `charts.js` draws them with Plotly (pinned to 2.35.2 from `cdn.plot.ly`) using colours from the stylesheet, so the charts follow the reader's light or dark setting. Every chart is drawn only from numbers in `data/`, and every chart carries a caveat.

## Rebuilding

Requires Python 3.10 or later.

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe src\build.py
```

On macOS or Linux use `.venv/bin/python` instead of `.venv\Scripts\python.exe`.

The build deletes and recreates `docs/`. To preview it locally:

```
python -m http.server 8000 --directory docs
```

then open http://localhost:8000/.

Before publishing, run the privacy check. It reads its patterns from `tools/private-patterns.txt`, which is kept out of version control; create that file with one string per line (a `re:` prefix makes a line a regular expression).

```
.venv\Scripts\python.exe tools\check_private.py
```

## Data honesty

- **Numbers are transcribed exactly.** Values in `data/` are copied from the research notes with units made explicit. Nothing is rounded, interpolated or filled in for a missing year; gaps stay blank.
- **Uncertain values are not stored as numbers.** A value marked **[unconfirmed]**, **[?]**, **[conflict]**, **[snippet]** or **[inferred]** goes in the row's `note` column, and its number column is left blank. Charts never draw it.
- **Arithmetic is labelled.** Values the research computed itself (shares, averages, per-game figures) are marked **[derived]** and the source data is named.
- **Every dataset has a confidence rating** (high, medium or low) and its caveats in `data/catalog.json` and on the data page.
- **Sources are linked.** Each topic section ends with the sources that answered and the ones that came up empty, so the gaps are visible.
- **Known gaps** are listed on the methodology page: for example, no published NFL audience figures for Japan and no NFL figure for international revenue.

Corrections with a better public source are welcome.

## Licence

The research text in `content/`, the datasets in `data/` and the built site in `docs/` are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); see `LICENSE`. You may share and adapt them, including commercially, if you give credit, link to this repository or its site, and say whether you made changes.

The licence covers this compilation and its wording. It does not cover the sources it cites: short quoted phrases, and the facts, figures and pages they come from, belong to their owners. The build code in `src/` and `tools/` is shared under the same terms.
