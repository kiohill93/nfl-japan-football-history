# 04 — Player salaries, 1920s to 2026

Compiled 2026-11-05. **[unconfirmed]** = search snippet only or a single weak source. **[derived]** = my arithmetic from a cited source.

## 1. Average pay by decade

Older figures come from different series that don't fully agree. Read them as orders of magnitude, not exact numbers.

| Period | Typical pay | Source |
|---|---|---|
| 1920s | $100–300 per game; star Red Grange about $100K in 1926 from a barnstorming tour | [Expensivity](https://www.expensivity.com/pro-football-salary-inflation/) |
| 1958 | Players fight for a $5,000 minimum | Expensivity; [Wikipedia: NFLPA](https://en.wikipedia.org/wiki/National_Football_League_Players_Association) |
| 1961 | Top draft pick Ernie Davis: 3 years for $80K | [House Judiciary SBA report](https://judiciary.house.gov/sites/evo-subsites/republicans-judiciary.house.gov/files/evo-media-document/nfl-sba-report-final.pdf) |
| Mid-1960s | Stars about $50K; Joe Namath (AFL, 1965) $427,000, a sign of the AFL–NFL bidding war | Expensivity; [Wikipedia: History of the NFL](https://en.wikipedia.org/wiki/History_of_the_National_Football_League) |
| 1969 | Average about $25,000 | Expensivity (citing the Kentucky Pro Football Hall of Fame) |

### Average salary, 1970–1999 (NFLPA series reported by AP in 2000)

Source: [AP via News On 6](https://www.newson6.com/story/5e3685bf2f69d76f6209b3b7/average-salaries-in-the-four-major-sports).

| Year | Average | Year | Average |
|---|---|---|---|
| 1970 | $41K | 1990 | $430K |
| 1972 | $45K | 1991 | $488K |
| 1974 | $56K | 1992 | $551K |
| 1976 | $78K | 1993 | $729K (free agency starts) |
| 1978 | $100K | 1994 | $674K (first capped year) |
| 1980 | $117K | 1995 | $752K |
| 1982 | $157K | 1996 | $807K |
| 1984 | $279K (USFL bidding war) | 1997 | $725K |
| 1986 | $288K | 1998 | $1.0M |
| 1988 | $307K | 1999 | $1.043M |
| 1989 | $389K | | |

**Conflict:** Expensivity gives lower 1970s numbers: 1974 $27,500 (or $36,444 with bonuses), 1977 $55,000, 1978 $62,535. The AP/NFLPA series probably counts differently (it may include bonuses or use another roster base). The trend is the same in both. This site uses the AP series for consistency.

### 2026 pay distribution (all active contracts)

Source: nflverse `historical_contracts` data from Over The Cap, updated 2026-11-05 ([nflverse release](https://github.com/nflverse/nflverse-data/releases/download/contracts/historical_contracts.parquet)). **[derived]** from 2,545 active contracts, using average per year (APY).

| Measure | Value |
|---|---|
| Mean APY | $4.30M |
| Median APY | $1.27M |
| At or above $1M | 73% |
| At or above $5M | 21% |
| At or above $10M | 13.5% |
| At or above $20M | 5.6% |
| At or above $40M | 0.9% |
| Top 10% threshold | about $13M |
| Top 1% threshold | about $35.3M |

The mean is more than three times the median. NFL pay is very top-heavy because most rosters are filled at or near the minimum.

## 2. Minimum salary

| Year | Rookie minimum | Source |
|---|---|---|
| 1958 | $5,000 (union goal) | Wikipedia NFLPA |
| 1968 | $9,000 rookies / $10,000 veterans | same |
| 1970 | $12,500 / $13,000 | same |
| 2020 | $610K | **[derived]** from the [2020 CBA term sheet](https://www.nfl.com/news/full-term-sheet-of-proposed-collective-bargaining-agreement-0ap3000001102608) (+$100K) |
| 2021 | $660K | **[derived]** (+$50K) |
| 2022–2026 | $705K, $750K, $795K, $840K, **$885K** | **[derived]** (+$45K a year) |

Practice-squad players earn far less: $10.5K a week in 2020 under the term sheet.

## 3. Record contracts (highest average per year when signed)

Source: nflverse/Over The Cap contract history **[derived: largest APY signed in each year that set a new high]**. The 2026 Mahomes deal was also reported by ESPN and NFL.com (June 10, 2026) per search results.

| Year signed | Player | APY | Note |
|---|---|---|---|
| 1991 | Dan Marino | $4.09M | |
| 1993 | Troy Aikman | $6.71M | first year of free agency |
| 1995 | Drew Bledsoe | $6.74M | |
| 1997 | Brett Favre | $7.87M | |
| 1998 | Steve Young | $8.2M | |
| 1999 | Deion Sanders | $11.25M | first non-QB record in the series |
| 2001 | Brett Favre | $11.5M | |
| 2004 | Peyton Manning | $14M | 7 years / $98M |
| 2005 | Carson Palmer | $16.2M | |
| 2009 | Julius Peppers | $16.7M | |
| 2010 | Tom Brady | $18M | |
| 2012 | Drew Brees | $20M | |
| 2013 | Aaron Rodgers | $22M | |
| 2016 | Andrew Luck | $24.6M | |
| 2017 | Matthew Stafford | $27M | |
| 2018 | Aaron Rodgers | $33.5M | |
| 2019 | Russell Wilson | $35M | |
| 2020 | Patrick Mahomes | $45M | 10 years / $450M |
| 2022 | Aaron Rodgers | $50.27M | |
| 2023 | Joe Burrow | $55M | |
| 2024 | Dak Prescott | $60M | |
| **2026** | **Patrick Mahomes** | **$64M** | 7 years / $448M new money; $504.75M total through 2033; the $64M APY starts in 2027 |

The record APY rose about 16× from 1991 to 2026. Over 1994–2026 it grew in step with the salary cap.

### Highest-paid players, 2026 (APY)

Source: nflverse/OTC **[derived]**; position benchmarks from [Spotrac 2025](https://www.spotrac.com/news/_/id/2968/2025-average-nfl-salaries-by-position).

| Player | Position | APY |
|---|---|---|
| Patrick Mahomes | QB | $64M |
| Dak Prescott | QB | $60M |
| Joe Burrow, Jordan Love, Trevor Lawrence, Josh Allen, Baker Mayfield, Matthew Stafford | QB | $55M each |
| Jared Goff, Brock Purdy | QB | $53M |
| Justin Herbert | QB | $52.5M |
| Lamar Jackson | QB | $52M |
| Jalen Hurts | QB | $51M |
| Will Anderson Jr. | Edge (top non-QB) | $50M |
| Micah Parsons | Edge | $46.5M |

Spotrac 2025 position tops: QB Prescott $60M, Edge Parsons $46.5M, WR Ja'Marr Chase $40.25M, RB Saquon Barkley $20.6M.

## 4. Guaranteed money

- Most NFL contracts are not fully guaranteed, unlike the NBA and MLB. Signing bonuses and some salary are guaranteed; the rest can be cut.
- Largest fully guaranteed deal: Deshaun Watson, $230M (2022), per nflverse/OTC "guaranteed at signing". Quartz reports Prescott's total guarantee at $231M ([Quartz](https://qz.com/highest-paid-nfl-quarterbacks-2026); note that this Quartz page looks out of date because it omits the 2026 Mahomes deal).

## 5. Rookie wage scale

- Before 2011, top draft picks could out-earn veterans (for example, Sam Bradford's 2010 rookie deal, about $50M guaranteed **[unconfirmed]**).
- The 2011 CBA set a rookie scale: four-year deals (five-year option for first-rounders) with pay fixed by draft slot. It moved money from rookies to veterans and retired players. Source: [Wikipedia: 2011 lockout](https://en.wikipedia.org/wiki/2011_NFL_lockout).

## 6. Players' share of revenue

| Period | Share | Source |
|---|---|---|
| 1982 demand | Union asked for 55% of gross (not won) | [Wikipedia: 1982 NFL strike](https://en.wikipedia.org/wiki/1982_NFL_strike) |
| 2006–2010 | About 57% of "total revenue" after over $1B came off the top for owners | Wikipedia: 2011 lockout |
| 2011–2020 | 55% of national media, 45% of NFL Ventures/postseason, 40% of local revenue (about 47% of all revenue) **[unconfirmed split]** | Wikipedia: 2011 lockout |
| 2020 | 47% | [2020 term sheet](https://www.nfl.com/news/full-term-sheet-of-proposed-collective-bargaining-agreement-0ap3000001102608) |
| 2021–2030 | 48%, up to 48.5% with the media kicker (48.8% often cited **[unconfirmed]**) | same |

Benefits on top of salary cost over $70M per club in 2025 ([Sportico, July 2026](https://www.sportico.com/leagues/football/2026/nfl-2025-national-revenue-per-team-1234939659/)).

## Sources

**Answered:**
- AP/NFLPA via News On 6, Expensivity, the House SBA report, the NFL.com 2020 term sheet, Wikipedia (NFLPA, 2011 lockout, 1982 strike, History of the NFL), Spotrac, Quartz and Sportico.
- nflverse contracts parquet (Over The Cap data), analysed locally.

**Came up empty or weak:**
- No clean NFL median-salary series by decade exists in free sources. Medians are only available for 2026 (nflverse); pre-2026 medians are not covered.
- Quartz's 2026 QB list is out of date.
- The nflverse `season_history` cash-paid field double-counts across contracts, so it was not used.
- The Spotrac and careertrend salary-history pages were too noisy or blocked (403).
