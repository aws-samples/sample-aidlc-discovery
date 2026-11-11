# Prepare customer data for a Discovery workshop

Run this on your own machine before the workshop, so that the workshop's AI assistant only ever sees customer feedback with the personal information removed. Raw records never leave your environment.

Detection is done by [Microsoft Presidio](https://microsoft.github.io/presidio/), an open-source (MIT) PII detection library. It finds names with a local spaCy language model, and it recognises emails, phone numbers, card numbers, IBANs, IP addresses, and national IDs. `prepare_data.py` is a short, readable script around it. It adds what a workshop needs: what to do with each column, a few patterns Presidio does not have, and a report to review before you share. Everything runs offline, and the script prints counts but never record text. Please read it before you run it.

## Install once

In a virtual environment, with Python 3.9 to 3.13:

```bash
pip install -r requirements.txt          # Presidio, pinned to the version the tests run against
python -m spacy download en_core_web_lg  # the English language model, about 400 MB
```

## Run it

Export each source (support tickets, reviews, NPS comments, account notes) as CSV, with one record per row. Then:

```bash
python prepare_data.py exports/ --out prepared --allow YourBrand
```

For an airline, add `--preset airline` to also remove booking references and flight numbers. `--allow YourBrand` keeps your own brand's social handle.

It writes two folders:

| Folder | What it holds | Who sees it |
|---|---|---|
| `prepared/share/` | The scrubbed CSVs, and `schema.md` (columns, common values, and a few fake rows) | Copy it to `discovery/data/` for the workshop |
| `prepared/review-only/` | `report.md`: what happened to each column, before-and-after examples, and the capitalised words left in the text | You only. It contains raw text: never share it |

## What it removes

| What | How |
|---|---|
| Name, login, email, phone, address, card, and bank columns, and people columns such as requester, assignee, owner, or created by | Dropped. Their values are also removed wherever they appear in the text, logins and the part of an email before the @ included (`[LOGIN]`). Keep a column with `--keep` if it only holds team names. |
| Customer, account, booking, and member ID columns | Replaced with a random code (`P-1a2b3c4d`). The code is the same for the same customer within one run, so you can still count customers, and it cannot be reversed. |
| People's names in free text, with or without context ("Sarah sorted it out") | Presidio: `[PERSON_1]`, `[PERSON_2]`, consistent within one record |
| Emails, phone numbers, card numbers, IBANs, IP addresses, national IDs, nationalities and religious or political groups | Presidio: `[EMAIL]`, `[PHONE]`, `[CARD]`, `[NRP]` |
| Social handles, web links, long account numbers, UK postcodes, and references such as "booking ref QX7P2L" | This script's patterns: `[HANDLE]`, `[URL]`, `[REFERENCE]` |
| Specific dates in the text ("on 3 May") | `[DATE]`, because a date and a flight together can identify someone. Date columns are kept; `--dates month` shortens them to the month, in ISO or day/month formats (the year only when the column cannot tell day from month). |

Example:

> Before: Hi, my name is Maria Silva, booking ref QX7P2L on flight AB123. Call me on +44 20 7946 0958.
>
> After: Hi, my name is [PERSON_1], booking ref [REFERENCE] on flight [FLIGHT]. Call me on [PHONE].

**Kept on purpose.** Some of Presidio's entity types are switched off, because on feedback they remove the signal rather than personal data: places ("stuck in Vienna"), durations and relative times ("48 hours", "today"), organisations (it tags "Wi-Fi" and "Apple Pay"), and bare domain names. The list is at the top of the script, with the reason for each.

## Review it before you share it (about 10 minutes)

Presidio catches most personal data, but no tool catches all of it, and its documentation says so. So:

1. Open `review-only/report.md` and read the examples, both the changed and the unchanged ones.
2. Scan the list of capitalised words left in the text. It is mostly places and brands. Any person's name there was missed.
3. If something slipped through, add it and run again:
   - names and logins: `--names-file staff-and-customers.txt` (one per line). An export of your CRM's name column, or your directory's logins, works well.
   - your own identifiers: `--pattern POLICY='\bPOL-\d{6}\b'`
   - a column that should go: `--drop COLUMN`
   - a word wrongly taken for a name: `--allow Desk`
4. Share only `prepared/share/`.

Scrubbing does not remove details that identify someone only in combination, such as "the only wheelchair user on the 6am Lisbon flight". If your data is full of these, or your policy does not allow even scrubbed records to be processed by AI, keep the records and share only `schema.md`. The assistant then writes the analysis code against the schema, you run it here, and you share its output, which is counts and averages only.

**Other languages.** Pass `--language` and a spaCy model for it, for example `--language de --spacy-model de_core_news_lg`. Names, emails, phone numbers, IBANs, and IP addresses are found in other languages too, but some recognisers are English-only: in German, for example, card numbers and national IDs are not checked. The report lists what Presidio looked for, so you can see the gaps for your language.

## Synthetic data for a rehearsal

Add `--synthetic 500` to also write `prepared/synthetic/`: 500 invented rows per file, in the shape of the prepared data. It has the same columns, the common values in roughly their real shares, numbers in their usual range, and dates in the real period, by month. It is built from the scrubbed output, and values seen fewer than five times never appear.

Use it to rehearse the workshop with your own columns, or to check your export and folders, with data input `synthetic`. It is not evidence: each column is drawn on its own, so links between columns are lost, and the free text is a `[SYNTHETIC]` marker, not customer words. Keep it apart from `share/`, so it is never counted as real data. For a dataset you only made up, with no real records behind it, you do not need this script at all.

## Check what is left

```bash
grep -rnE --include='*.csv' "@|\+[0-9]{2}|[0-9]{8,}" prepared/share/   # only your own brand handles should show
```
