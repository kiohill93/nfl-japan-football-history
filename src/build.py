"""Build the static site.

Reads the research notes in content/ and the datasets in data/, and writes HTML pages,
CSS/JS assets and copies of the CSVs into docs/ (the GitHub Pages root).

Run from the project root:  .venv/Scripts/python.exe src/build.py   (Windows)
                            .venv/bin/python src/build.py           (macOS/Linux)
"""
from __future__ import annotations

import csv
import html
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
SRC = ROOT / "src"

SITE_TITLE = "NFL and Japan Football History"
COMPILED = "Compiled November 2026 from public sources"
NAV = [("index.html", "Overview"), ("nfl.html", "NFL history"), ("japan.html", "Football in Japan"),
       ("people.html", "People"), ("data.html", "Data"), ("methodology.html", "Methodology")]
PAGES = {"nfl": ("nfl.html", "NFL history"), "japan": ("japan.html", "Football in Japan")}


# --------------------------------------------------------------------------- data

def load_catalog() -> list[dict]:
    cat = json.loads((DATA / "catalog.json").read_text(encoding="utf-8"))
    return cat["datasets"]


def load_csv(name: str) -> list[dict]:
    with open(DATA / f"{name}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(v):
    """Number or None. Blank cells stay None: missing is missing, not zero."""
    if v is None or str(v).strip() == "":
        return None
    try:
        f = float(v)
    except ValueError:
        return None
    return int(f) if f.is_integer() else f


# --------------------------------------------------------------------------- charts
# Each chart: id, dataset, title, caveat, placement (page key + heading prefix) and a
# Plotly spec. Colours are slot numbers (1-4) resolved from CSS variables in charts.js.

def chart_specs(cat: dict[str, dict]) -> list[dict]:
    C = []

    def add(id, dataset, title, caveat, traces, layout, place=None, subtitle=None, index=False):
        C.append({"id": id, "dataset": dataset, "dataset_title": cat[dataset]["title"], "title": title,
                  "subtitle": subtitle, "caveat": caveat, "place": place, "index": index,
                  "spec": {"traces": traces, "layout": layout}})

    # Super Bowl audience
    sb = load_csv("super_bowl_us_audience")
    pts = [(int(r["year"]), num(r["viewers_m"]), r["super_bowl"]) for r in sb if num(r["viewers_m"]) is not None]
    add("super-bowl", "super_bowl_us_audience", "Super Bowl average US TV audience, 1967-2026 (millions)",
        "Nielsen counted more streaming and out-of-home viewing from the 2025 season, which helped the 2025-26 records; Super Bowl LX is NBC only (Nielsen's all-platform figure is 125.6M).",
        [{"type": "scatter", "mode": "lines", "x": [p[0] for p in pts], "y": [p[1] for p in pts],
          "text": [p[2] for p in pts], "name": "Super Bowl", "color": 1,
          "hovertemplate": "Super Bowl %{text} (%{x})<br>%{y} million viewers<extra></extra>"}],
        {"yaxis": {"title": "Million viewers", "range": [0, 140]}, "hovermode": "x",
         "annotations": [{"x": 2025, "y": 127.7, "text": "LIX 2025: 127.7M", "showarrow": True, "ax": -60, "ay": -6}]},
        place=("nfl/09", "2. Super Bowl audiences"), index=True)

    # Salary cap
    cap = load_csv("nfl_salary_cap")
    xs = [int(r["year"]) for r in cap if num(r["cap_usd_m"]) is not None]
    ys = [num(r["cap_usd_m"]) for r in cap if num(r["cap_usd_m"]) is not None]
    add("salary-cap", "nfl_salary_cap", "NFL salary cap per team, 1994-2026 (US$ millions)",
        "2010 was an uncapped year, so it has no bar. Nominal dollars; Spotrac differs slightly in four years (see the table).",
        [{"type": "bar", "x": xs, "y": ys, "name": "Salary cap", "color": 1,
          "hovertemplate": "%{x}: $%{y}M<extra></extra>"}],
        {"yaxis": {"title": "US$ millions"}, "xaxis": {"dtick": 4}},
        place=("nfl/03", "2. Salary cap by year"), index=True)

    # Japan registered players
    jp = load_csv("japan_registered_players")
    jpp = [(int(r["year"]), num(r["players"]), r["year_label"], r["series"]) for r in jp if num(r["players"]) is not None]
    add("japan-players", "japan_registered_players", "Registered American football players in Japan",
        "Two counting methods are mixed (JAFA history pages and the SSF survey); the gaps between points are years with no figure. FY2020 (15,756) and FY2022 (13,809) rest on one secondary summary and are not plotted.",
        [{"type": "scatter", "mode": "markers+text", "x": [p[0] for p in jpp], "y": [p[1] for p in jpp],
          "text": [f"{p[1]:,}" for p in jpp], "textposition": "top center", "customdata": [[p[2], p[3]] for p in jpp],
          "name": "Players", "color": 1, "marker": {"size": 10},
          "hovertemplate": "%{customdata[0]}: %{y:,} players<br>%{customdata[1]}<extra></extra>"}],
        {"yaxis": {"title": "Registered players", "rangemode": "tozero"}, "xaxis": {"range": [1925, 2032]}},
        place=("japan/07", "1. Registered players over time"), index=True)

    # NFL games in Japan
    g = load_csv("nfl_games_in_japan")
    known = [r for r in g if num(r["attendance"]) is not None]
    unknown = [r for r in g if num(r["attendance"]) is None]
    add("nfl-japan-games", "nfl_games_in_japan", "NFL games in Japan, 1976-2005: 14 games, one reported crowd",
        "Only the 1976 crowd (38,000) was found as a single figure. 1989 has two conflicting reports (43,000 vs more than 45,000) and is shown as not found; crowds for 1990-2005 were not found.",
        [{"type": "bar", "x": [r["year"] for r in known], "y": [num(r["attendance"]) for r in known],
          "customdata": [[r["result"], r["venue"]] for r in known], "name": "Crowd reported", "color": 1, "width": 0.6,
          "hovertemplate": "%{x}: %{customdata[0]}<br>%{customdata[1]}<br>%{y:,} fans<extra></extra>"},
         {"type": "scatter", "mode": "markers", "x": [r["year"] for r in unknown], "y": [0] * len(unknown),
          "customdata": [[r["result"], r["venue"], r["note"]] for r in unknown], "name": "Crowd not found",
          "color": "muted", "marker": {"symbol": "circle-open", "size": 10},
          "hovertemplate": "%{x}: %{customdata[0]}<br>%{customdata[1]}<br>%{customdata[2]}<extra></extra>"}],
        {"xaxis": {"type": "category", "title": "Year"}, "yaxis": {"title": "Attendance", "rangemode": "tozero"}},
        place=("japan/08", "NFL games in Japan (1976–2005)"), index=True)

    # International games by year
    ig = load_csv("nfl_international_games")
    played = [r for r in ig if num(r["attendance"]) is not None]
    groups = ["UK", "Mexico", "Germany"]
    years = sorted({int(r["year"]) for r in played})
    cnt = Counter((int(r["year"]), r["country"] if r["country"] in groups else "Elsewhere") for r in played)
    traces = []
    for i, gname in enumerate(groups + ["Elsewhere"]):
        traces.append({"type": "bar", "x": years, "y": [cnt.get((y, gname), 0) for y in years], "name": gname,
                       "color": i + 1, "hovertemplate": f"%{{x}}: %{{y}} game(s) in {gname}<extra></extra>"})
    add("intl-games", "nfl_international_games", "NFL regular-season games played outside the US, by year",
        "Counts games played by the compile date: three more 2026 games (Madrid, Munich, Mexico City) were scheduled for November. 'Elsewhere' is Brazil, Ireland, Spain, Australia and France. None has been played in Asia.",
        traces, {"barmode": "stack", "legend": {"traceorder": "normal"}, "yaxis": {"title": "Games", "dtick": 1}, "xaxis": {"dtick": 2}},
        place=("nfl/09", "International regular-season attendance by game"), index=True)

    # International attendance by game (scatter, 3 groups)
    ggroups = {"London": 1, "Mexico City": 2}
    tr = defaultdict(list)
    for r in played:
        key = r["city"] if r["city"] in ggroups else "Elsewhere"
        tr[key].append(r)
    traces = []
    for key, color in [("London", 1), ("Mexico City", 2), ("Elsewhere", 3)]:
        rows = tr[key]
        traces.append({"type": "scatter", "mode": "markers", "name": key, "color": color,
                       "x": [int(r["year"]) for r in rows], "y": [num(r["attendance"]) for r in rows],
                       "customdata": [[r["teams"], r["city"], r["venue"] or "venue not given"] for r in rows],
                       "hovertemplate": "%{x} %{customdata[1]} (%{customdata[2]})<br>%{customdata[0]}: %{y:,}<extra></extra>"})
    add("intl-attendance", "nfl_international_games", "Attendance at each international regular-season game",
        "International games sell out, so stadium size sets these numbers (Tottenham about 61,000, Wembley about 84,000-86,000).",
        traces, {"yaxis": {"title": "Attendance", "rangemode": "tozero"}},
        place=("nfl/09", "International regular-season attendance by game"))

    # League size
    ls = load_csv("nfl_league_size")
    add("league-size", "nfl_league_size", "Number of NFL teams at each expansion step",
        "Only the steps listed in the research table; the 1960 point counts NFL teams only (the AFL had 8 more).",
        [{"type": "scatter", "mode": "lines+markers", "line": {"shape": "hv"}, "x": [int(r["year"]) for r in ls],
          "y": [num(r["nfl_teams"]) for r in ls], "text": [r["change"] for r in ls], "name": "Teams", "color": 1,
          "hovertemplate": "%{x}: %{y} teams<br>%{text}<extra></extra>"}],
        {"yaxis": {"title": "Teams", "range": [0, 35]}},
        place=("nfl/01", "6. League size over time"))

    # Media deals
    md = [r for r in load_csv("nfl_media_rights_deals") if num(r["total_usd_m"]) is not None]
    labels = [f"{r['start_year']}–{r['end_year']}" if r["end_year"] and r["end_year"] != r["start_year"] else r["start_year"] for r in md]
    add("media-deals", "nfl_media_rights_deals", "National TV contract totals as reported (US$ millions, log scale)",
        "Totals cover different numbers of years and packages; 2014-22 is broadcast only and 2023-33 is 'over $100B'. Nominal dollars. Log scale: each gridline is ten times the last.",
        [{"type": "bar", "x": labels, "y": [num(r["total_usd_m"]) for r in md], "customdata": [r["value_as_reported"] for r in md],
          "name": "Contract total", "color": 1, "hovertemplate": "%{x}<br>%{customdata}<extra></extra>"}],
        {"yaxis": {"type": "log", "title": "US$ millions"}, "xaxis": {"type": "category", "tickangle": -45}},
        place=("nfl/02", "3. TV and media deals by era"))

    # Franchise values
    fv = load_csv("nfl_franchise_values")
    traces = []
    for kind, color, name in [("Average team value (Forbes)", 1, "Forbes"), ("Average team value (Sportico)", 2, "Sportico")]:
        rows = [r for r in fv if r["kind"] == kind]
        traces.append({"type": "scatter", "mode": "lines+markers", "x": [int(r["year"]) for r in rows],
                       "y": [num(r["value_usd_b"]) for r in rows], "name": name, "color": color,
                       "hovertemplate": f"{name} %{{x}}: $%{{y}}B<extra></extra>"})
    add("franchise-values", "nfl_franchise_values", "Average NFL team value (US$ billions)",
        "Publication estimates, not audited values; Forbes figures come via Quartz. No average before 2022 was collected.",
        traces, {"yaxis": {"title": "US$ billions", "rangemode": "tozero"}, "xaxis": {"dtick": 1}},
        place=("nfl/02", "6. Team values over time"))

    # Average salary (AP series only)
    av = [r for r in load_csv("nfl_average_salary") if r["series"] == "AP/NFLPA series"]
    add("avg-salary", "nfl_average_salary", "Average NFL salary, 1970-1999 (AP/NFLPA series, US$)",
        "Expensivity's lower 1970s figures (for example $62,535 in 1978) conflict with this series and are not plotted. Nominal dollars.",
        [{"type": "scatter", "mode": "lines+markers", "x": [int(r["year"]) for r in av], "y": [num(r["average_usd"]) for r in av],
          "text": [r["note"] for r in av], "name": "Average salary", "color": 1,
          "hovertemplate": "%{x}: $%{y:,}<br>%{text}<extra></extra>"}],
        {"yaxis": {"title": "US dollars", "rangemode": "tozero"}},
        place=("nfl/04", "Average salary, 1970–1999"))

    # Minimum salary
    ms = [r for r in load_csv("nfl_minimum_salary") if num(r["rookie_minimum_usd"]) is not None]
    add("min-salary", "nfl_minimum_salary", "NFL rookie minimum salary (US$)",
        "2020-2026 are derived from the 2020 CBA term sheet's step increases; no values for 1971-2019 were collected, so the gap is not a flat line.",
        [{"type": "bar", "x": [r["year"] for r in ms], "y": [num(r["rookie_minimum_usd"]) for r in ms], "name": "Rookie minimum",
          "color": 1, "hovertemplate": "%{x}: $%{y:,}<extra></extra>"}],
        {"xaxis": {"type": "category"}, "yaxis": {"title": "US dollars"}},
        place=("nfl/04", "2. Minimum salary"))

    # Record contracts
    rc = load_csv("nfl_record_contracts")
    add("record-contracts", "nfl_record_contracts", "Record contract value per year when signed (US$ millions)",
        "Derived from nflverse/Over The Cap contract history; only years that set a new high appear.",
        [{"type": "scatter", "mode": "lines+markers", "line": {"shape": "hv"}, "x": [int(r["year_signed"]) for r in rc],
          "y": [num(r["apy_usd_m"]) for r in rc], "text": [r["player"] for r in rc], "name": "Record APY", "color": 1,
          "hovertemplate": "%{x}: %{text}, $%{y}M a year<extra></extra>"}],
        {"yaxis": {"title": "US$ millions a year", "rangemode": "tozero"}},
        place=("nfl/04", "3. Record contracts"))

    # CTE
    cte = load_csv("nfl_cte_brain_bank")
    add("cte", "nfl_cte_brain_bank", "Share of donated former-NFL brains with CTE (Boston University)",
        "Donated brains, often from families who already suspected disease: these shares do not measure how common CTE is among all players.",
        [{"type": "bar", "x": [f"{r['year_published']}" + (f" ({r['journal']})" if r["journal"] else "") for r in cte],
          "y": [num(r["share_pct"]) for r in cte], "text": [f"{r['cte_cases']} of {r['brains_studied']}" for r in cte],
          "textposition": "inside", "name": "Share with CTE", "color": 1, "width": 0.5,
          "hovertemplate": "%{x}: %{y}% (%{text})<extra></extra>"}],
        {"xaxis": {"type": "category", "title": "Study published"}, "yaxis": {"title": "%", "range": [0, 100]}},
        place=("nfl/06", "2. CTE research results"))

    # Regular-season TV by package, 2025
    tv = [r for r in load_csv("nfl_regular_season_tv") if r["season"] == "2025"]
    tv.sort(key=lambda r: num(r["avg_viewers_m"]))
    add("tv-2025", "nfl_regular_season_tv", "2025 regular season: average US viewers by package (millions)",
        "Measured with Nielsen's Big Data + Panel method from 2025, which raised recent numbers.",
        [{"type": "bar", "orientation": "h", "y": [r["package"] for r in tv], "x": [num(r["avg_viewers_m"]) for r in tv],
          "name": "2025 average", "color": 1, "hovertemplate": "%{y}: %{x}M<extra></extra>"}],
        {"xaxis": {"title": "Million viewers", "rangemode": "tozero"}, "yaxis": {"type": "category"}},
        place=("nfl/09", "2025 season by package"))

    # Season attendance
    sa = [r for r in load_csv("nfl_season_attendance") if num(r["total_attendance"]) is not None]
    add("season-attendance", "nfl_season_attendance", "NFL regular-season attendance, selected seasons (millions)",
        "Only the seasons with a figure; 1960 and 1989 are rounded ('about'). League size changed from 10 teams (1940) to 32.",
        [{"type": "bar", "x": [r["season"] for r in sa], "y": [num(r["total_attendance"]) / 1e6 for r in sa],
          "customdata": [[r["teams"], r["note"]] for r in sa], "name": "Total attendance", "color": 1,
          "hovertemplate": "%{x}: %{y:.2f}M (%{customdata[0]} teams)<br>%{customdata[1]}<extra></extra>"}],
        {"xaxis": {"type": "category"}, "yaxis": {"title": "Millions"}},
        place=("nfl/09", "4. Game attendance over time"))

    # Gallup
    ga = [r for r in load_csv("gallup_favorite_sport") if num(r["football_pct"]) is not None]
    add("gallup", "gallup_favorite_sport", "Gallup: share naming football their favourite sport to watch (%)",
        "Only the readings the research collected, not all 23 since 1972; the axis is in reading order, not to scale in time.",
        [{"type": "scatter", "mode": "lines+markers", "x": [r["year"] for r in ga], "y": [num(r["football_pct"]) for r in ga],
          "text": [r["note"] for r in ga], "name": "Football", "color": 1,
          "hovertemplate": "%{x}: %{y}%<br>%{text}<extra></extra>"}],
        {"xaxis": {"type": "category"}, "yaxis": {"title": "%", "range": [0, 50]}},
        place=("nfl/09", "5. Polls: football"))

    # JAFA revenue
    jr = [r for r in load_csv("jafa_revenue_fy2025") if r["parent"] in ("Business revenue", "Subsidies and grants")]
    jr.sort(key=lambda r: num(r["amount_jpy_m"]))
    add("jafa-revenue", "jafa_revenue_fy2025", "JAFA revenue lines, FY2025 (¥ millions)",
        "Itemised lines only; other small lines are not shown, so the bars do not add up to the ¥298.6M total.",
        [{"type": "bar", "orientation": "h", "y": [r["line"] for r in jr], "x": [num(r["amount_jpy_m"]) for r in jr],
          "customdata": [r["parent"] for r in jr], "name": "FY2025", "color": 1,
          "hovertemplate": "%{y}: ¥%{x}M<br>(%{customdata})<extra></extra>"}],
        {"xaxis": {"title": "¥ millions"}, "yaxis": {"type": "category"}},
        place=("japan/02", "5. JAFA's money"))

    # Participation
    sp = [r for r in load_csv("japan_sport_participation") if "US high-school" not in r["sport"]]
    sp.sort(key=lambda r: num(r["registered_players"]))
    add("participation", "japan_sport_participation", "Registered players in Japan by sport, FY2024 (log scale)",
        "Federations count registration differently. For scale, US high-school boys' tackle football had 1,029,588 players in 2024-25.",
        [{"type": "bar", "orientation": "h", "y": [r["sport"] for r in sp], "x": [num(r["registered_players"]) for r in sp],
          "name": "Registered players", "color": 1, "hovertemplate": "%{y}: %{x:,}<extra></extra>"}],
        {"xaxis": {"type": "log", "title": "Registered players (log scale)"}, "yaxis": {"type": "category"}},
        place=("japan/07", "2. Japan's size next to other sports"))

    # Big-game attendance
    ba = load_csv("japan_big_game_attendance")
    traces = []
    for ev, color in [("Rice Bowl", 1), ("Koshien Bowl", 2), ("Corporate final", 3)]:
        rows = [r for r in ba if r["event"] == ev and num(r["attendance"]) is not None]
        traces.append({"type": "scatter", "mode": "markers", "name": ev, "color": color,
                       "x": [int(r["year"]) for r in rows], "y": [num(r["attendance"]) for r in rows],
                       "customdata": [r["note"] or r["venue"] for r in rows],
                       "hovertemplate": f"{ev} %{{x}}: %{{y:,}}<br>%{{customdata}}<extra></extra>"})
    add("big-games", "japan_big_game_attendance", "Crowds at Japan's big games, years named in the research",
        "Announced, mostly rounded crowds for the years the research names; the era table gives typical ranges. January 2025's Rice Bowl is left out because two JAFA sources disagree (17,694 vs 17,885).",
        traces, {"yaxis": {"title": "Attendance", "rangemode": "tozero"}},
        place=("japan/08", "Rice Bowl (national final)"))

    # Pageviews
    pv = load_csv("ja_wikipedia_pageviews")
    traces = []
    for art, color, name in [("アメリカンフットボール", 1, "American football (アメリカンフットボール)"), ("NFL", 2, "NFL"),
                             ("野球", 3, "Baseball (野球), for comparison")]:
        rows = [r for r in pv if r["article_ja"] == art and num(r["views"]) is not None and not r["period_note"]]
        traces.append({"type": "scatter", "mode": "lines+markers", "name": name, "color": color,
                       "x": [int(r["year"]) for r in rows], "y": [num(r["views"]) for r in rows],
                       "hovertemplate": f"{name} %{{x}}: %{{y:,}} views<extra></extra>"})
    add("pageviews", "ja_wikipedia_pageviews", "Japanese Wikipedia yearly views (human users)",
        "2017, 2020 and 2022 were not pulled, and 2026 (January to October only) is left out. Wikipedia traffic is falling overall, so compare the lines with each other, not with their own past.",
        traces, {"yaxis": {"title": "Views per year", "rangemode": "tozero"}, "xaxis": {"dtick": 1}},
        place=("japan/08", "Japanese Wikipedia pageviews"))

    return C


# --------------------------------------------------------------------------- markdown

CODE_SPAN = re.compile(r"(`[^`]*`)")
BARE_URL = re.compile(r"(?<!\]\()(?<!<)(?<![\w/\"'=])(https?://[^\s<>|`\"]+)")
MARKER = re.compile(r"<strong>\[(unconfirmed|\?|conflict|derived|inferred|snippet|not collected|search snippet|JA|EN|Yahoo Sports citing Gallup|Sportico citing a survey)([^\]<]*)\]</strong>")


def autolink(text: str) -> str:
    """Turn bare URLs into links (markdown leaves them as text). Skips code spans and links."""
    def fix(m):
        url = m.group(1)
        trail = ""
        while url and url[-1] in ".,;:":
            trail = url[-1] + trail
            url = url[:-1]
        if url.endswith(")") and url.count("(") < url.count(")"):
            url, trail = url[:-1], ")" + trail
        return f"<{url}>{trail}"
    parts = CODE_SPAN.split(text)
    return "".join(p if p.startswith("`") else BARE_URL.sub(fix, p) for p in parts)


def marker_class(kind: str) -> str:
    if kind in ("conflict",):
        return "m-conflict"
    if kind in ("derived", "inferred"):
        return "m-derived"
    if kind in ("JA", "EN"):
        return ""
    return "m-unconfirmed"


def render_md(text: str, id_prefix: str = "", shift: int = 0) -> str:
    md = markdown.Markdown(extensions=["tables", "sane_lists", "toc"],
                           extension_configs={"toc": {"slugify": slugify_unicode}})
    out = md.convert(autolink(text))
    if id_prefix:
        out = re.sub(r'<(h\d) id="([^"]+)"', lambda m: f'<{m.group(1)} id="{id_prefix}{m.group(2)}"', out)
    if shift:
        def sh(m):
            n = min(int(m.group(2)) + shift, 6)
            return f"<{m.group(1)}h{n}"
        out = re.sub(r"<(/?)h([1-6])", sh, out)
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

    def mk(m):
        cls = marker_class(m.group(1))
        return f'<strong class="marker {cls}">[{m.group(1)}{m.group(2)}]</strong>' if cls else m.group(0)
    out = MARKER.sub(mk, out)
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener"', out)
    return out


def insert_charts(html_text: str, charts: list[dict], env) -> str:
    """Put each chart right after the heading whose text starts with its anchor."""
    tpl = env.get_template("_chart.html")
    for c in charts:
        anchor = c["place"][1]
        pat = re.compile(r"(<h([2-6])[^>]*>)(.*?)(</h\2>)", re.S)
        done = False
        for m in pat.finditer(html_text):
            inner = html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()
            if inner.startswith(anchor):
                pos = m.end()
                html_text = html_text[:pos] + "\n" + tpl.render(c=c) + html_text[pos:]
                done = True
                break
        if not done:
            raise SystemExit(f"Chart anchor not found: {c['place']}")
    return html_text


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


# --------------------------------------------------------------------------- build

def build():
    catalog = load_catalog()
    cat = {d["id"]: d for d in catalog}
    charts = chart_specs(cat)

    env = Environment(loader=FileSystemLoader(SRC / "templates"), autoescape=select_autoescape(["html"]))
    common = {"site_title": SITE_TITLE, "compiled": COMPILED, "nav": NAV}

    if DOCS.exists():
        shutil.rmtree(DOCS)
    (DOCS / "assets").mkdir(parents=True)
    (DOCS / "data").mkdir()
    for f in (SRC / "static").iterdir():
        shutil.copy2(f, DOCS / "assets" / f.name)
    for f in DATA.glob("*.csv"):
        shutil.copy2(f, DOCS / "data" / f.name)
    shutil.copy2(DATA / "catalog.json", DOCS / "data" / "catalog.json")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    def chart_json(cs):
        return json.dumps({c["id"]: c["spec"] for c in cs}, ensure_ascii=False).replace("</", "<\\/")

    def write(name, tpl, **ctx):
        page = env.get_template(tpl).render(current=name, **common, **ctx)
        (DOCS / name).write_text(page, encoding="utf-8")
        print(f"  wrote docs/{name}")

    # Topic pages
    topic_meta = {
        "nfl": ("History of the NFL",
                "From the 1920 founding in Canton, Ohio to the streaming era: business and media, labor and salaries, governance, health and safety, the military, culture, and how many people watch.",
                "The history of the NFL, 1920 to 2026, with data and sources."),
        "japan": ("American football in Japan",
                  "From the 1934 student league in Tokyo to the X League's 2026 crisis: media and business, money, governance, safety, US ties, participation, crowds and TV.",
                  "The history of American football in Japan, 1934 to 2026, with data and sources."),
    }
    for key, (heading, lede, desc) in topic_meta.items():
        sections = []
        for f in sorted((CONTENT / key).glob("*.md")):
            num_ = f.name[:2]
            sec_key = f"{key}/{num_}"
            text = f.read_text(encoding="utf-8")
            title = first_heading(text)
            h = render_md(text, id_prefix=f"{key}-{num_}-", shift=1)
            sec_charts = [c for c in charts if c["place"] and c["place"][0] == sec_key]
            h = insert_charts(h, sec_charts, env)
            sections.append({"id": f"{key}-{num_}", "title": title, "html": h, "charts": sec_charts})
        page_charts = [c for s in sections for c in s["charts"]]
        write(PAGES[key][0], "topic.html", title=heading, heading=heading, lede=lede, description=desc,
              sections=sections, charts=chart_json(page_charts))

    # People
    ptext = (CONTENT / "people.md").read_text(encoding="utf-8")
    phtml = render_md(ptext)
    phtml = re.sub(r"^<h1[^>]*>.*?</h1>", "", phtml, count=1, flags=re.S)
    write("people.html", "topic.html", title="Important people", heading=first_heading(ptext),
          lede=None, description="The major names behind the NFL's history and American football in Japan.",
          sections=[{"id": "people", "title": "People", "html": phtml}], charts=None)

    # Data page
    sec_pages = {"nfl": PAGES["nfl"], "japan": PAGES["japan"]}
    ds_view = []
    for d in catalog:
        rows = load_csv(d["id"])
        key, n = d["section"].split("/")
        href = f"{sec_pages[key][0]}#{key}-{n}"
        ds_view.append(dict(d, preview=rows[:8], page_href=href, page_label=f"{sec_pages[key][1]}, section {n}"))
    write("data.html", "data.html", title="Data", description="Every dataset behind the site, with sources and CSV downloads.",
          datasets=ds_view, charts=None)

    # Methodology
    mtext = (CONTENT / "methodology.md").read_text(encoding="utf-8")
    intro_md, rest_md = mtext.split("<!-- datasets -->")
    write("methodology.html", "methodology.html", title="Methodology",
          description="How the research was done: sources, checks, markers, confidence and gaps.",
          intro=render_md(intro_md), rest=render_md(rest_md), datasets=catalog, charts=None)

    # Overview
    sb = {r["year"]: r for r in load_csv("super_bowl_us_audience")}
    cap = {r["year"]: r for r in load_csv("nfl_salary_cap")}
    ig = load_csv("nfl_international_games")
    n_played = sum(1 for r in ig if num(r["attendance"]) is not None)
    jg = load_csv("nfl_games_in_japan")
    jp = {r["year_label"]: r for r in load_csv("japan_registered_players")}
    rb = [r for r in load_csv("japan_big_game_attendance") if r["event"] == "Rice Bowl"]
    rb_2026 = next(r for r in rb if r["year"] == "2026")
    rb_max = max((r for r in rb if num(r["attendance"]) is not None), key=lambda r: num(r["attendance"]))
    tiles = [
        {"value": f"{num(sb['2025']['viewers_m'])}M", "label": "US viewers for Super Bowl LIX (2025), the US TV record",
         "sub": "Super Bowl I drew 51.18M in 1967"},
        {"value": f"${num(cap['2026']['cap_usd_m'])}M", "label": "Salary cap per team, 2026: the first above $300M",
         "sub": f"${num(cap['1994']['cap_usd_m'])}M when the cap began in 1994"},
        {"value": str(n_played), "label": "Regular-season games played abroad, 2005 to Nov 2026",
         "sub": "None in Asia; a record 9 scheduled in 2026"},
        {"value": str(len(jg)), "label": "NFL games played in Japan, all exhibitions",
         "sub": f"From {jg[0]['year']} to {jg[-1]['year']}; none since"},
        {"value": f"{num(jp['FY2024']['players']):,}", "label": "Registered football players in Japan, FY2024",
         "sub": f"Peak: {num(jp['1992']['players']):,} in 1992"},
        {"value": f"{num(rb_2026['attendance']):,}", "label": "Rice Bowl crowd, January 2026",
         "sub": f"Record: {num(rb_max['attendance']):,} in {rb_max['year']}"},
    ]
    index_charts = [c for c in charts if c["index"]]
    order = ["super-bowl", "salary-cap", "intl-games", "nfl-japan-games", "japan-players"]
    index_charts.sort(key=lambda c: order.index(c["id"]))
    write("index.html", "index.html", title="Overview",
          description="A data-driven history of the NFL and of American football in Japan, compiled from public sources.",
          tiles=tiles, chart_list=index_charts, charts=chart_json(index_charts), n_datasets=len(catalog))
    print(f"Built {len(catalog)} datasets, {len(charts)} charts into {DOCS}")


if __name__ == "__main__":
    build()
