# Data Exploration Findings

**Date explored:** 9 November 2026
**Scripts:** 'exploration/explore_archive.py', 'exploration/explore_api.py'

## Archive

- **Number of files:** 21 zip exports covering Dec 2011 – Aug 2026, in periods of different lengths (one file covers Dec 2011 – Apr 2018; recent files cover a single month)
- **Format inside each zip:** one CSV file
- **Columns (16):** Date received, Product, Sub-product, Issue, Sub-issue, Consumer complaint narrative, Company public response, Company, State, ZIP code, Tags, Submitted via, Date sent to company, Company response to consumer, Timely response?, Complaint ID
- **Types:** all columns load as text except Complaint ID (integer); dates are text
- **Download size, largest file (Dec 2011 – Apr 2018):** 135 MB (zip)

### Files profiled

| | August 2026 | July – August 2025 |
|---|---|---|
| Download size (zip) | 11MB | 81MB |
| Uncompressed size | 177 MB | 549 MB |
| Rows | 667,140 | 968,761 |
| Date range | 2026-08-01 to 2026-08-31 | 2025-07-01 to 2025-08-31 |
| Duplicate complaint IDs | 0 | 0 |
| "In progress" responses | 370,160 (55%) | 0 |
| Complaints with a narrative | ~0% | 24.2% (234,404) |
| Company public response missing | 81.5% | 42.0% |
| Credit reporting share | 93% | 90% |

### Missing values (both files)
- Tags: ~98% (optional; only tagged groups)
- Company public response: 42–82% (optional; fills in over time)
- Sub-issue: ~1% (not all issues have sub-issues)
- State, ZIP code: ~0.1%
- All other columns: 0%

### Response values
Closed with explanation, Closed with non-monetary relief, Closed with monetary relief, Untimely response, In progress

### Narratives (July – August 2025 file)
- Length: median 736, 75th percentile 1,249, mean 1,063, max 31,498 characters
- Under 50 characters: 46 (0.02%)
- Containing 'XXXX' redactions: 56%
- Narratives by product: credit reporting 185,795; debt collection 20,238; checking or savings 7,942; credit card 7,558; money transfer 3,852; mortgage 2,552; all others under 2,300 each

### Discrepancy to monitor
The archive page says complaints received through 14 August 2026, but the August 2026 file contains dates up to 31 August.

## API

- Search endpoint:
- Date filter parameters:
- Paging method:
- Rate limits documented? (yes/no, details):
- Total complaints received since 1 Oct 2026:
- Field names (compared with archive):
- Fields in archive but not in API: Consumer complaint narrative (per field reference; confirm with script)

## Implications for the design

- **Spark:** read CSV from bronze; rename columns to snake_case (names contain spaces and '?'); cast both date columns from text.
- **Deduplication:** no duplicates within files, but keep the step, since complaints can repeat across exports and between archive and API data.
- **Data model:** no consent or consumer-disputed fields exist, so remove 'consent_provided' from 'dim_complaint_profile'.
- **Closed status:** "closed" means a response starting with "Closed"; "In progress" and "Untimely response" are not closed.
- **Change tracking:** older exports hold mostly final states; changes over time come only from the API. The daily load must re-fetch a rolling 180-day window (ADR-012).
- **Data quality:** 'not_null' tests on complaint ID, both dates, product, issue, company, submitted via, response and timely; none on tags, public response, sub-issue, state or ZIP.
- **Analysis:** credit reporting is ~90% of complaints, so compare companies on rates and filter by product in dashboards.
- **AI subset:** banking-product narratives from the July – August 2025 export, 21,904 (ADR-013). Recent exports have almost no narratives.
- **Chunking:** ~800-character chunks with ~100 overlap; exclude narratives under 50 characters (ADR-014).
- **Privacy:** narratives are already anonymised with 'XXXX'; the app may display it as '[redacted]', but stored data stays unchanged.
- **Volume:** two months is ~550 MB uncompressed, so the full archive is several GB. Develop on a subset.