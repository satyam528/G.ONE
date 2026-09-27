# G.ONE

Getting a medical bill shouldn't feel like getting a second diagnosis.

G.ONE (formerly Jeevan) helps patients and families actually understand what
they're being charged for — by scanning bills with OCR, flagging things that
look off, and letting people share honest, price-tagged reviews of hospitals
so others can walk in better informed.

Started as a personal project after a family medical billing experience that
was confusing and hard to make sense of.

## What it does

- **Bill scanning & parsing** — upload a photo of a medical bill, and the app
  extracts line items automatically using OCR
- **Bill sanity checks** — flags potential duplicate charges, unusually
  high-value items, and mismatches between the line-item sum and the stated
  total
- **Hospital reviews** — patients can rate hospitals/staff and tag the actual
  price they paid for specific treatments
- **Infra photo uploads** — attach photos of hospital facilities alongside
  reviews, so others get a fuller picture before choosing where to go
- **Transparency, not accusations** — no automated "fraud" or "overcharging"
  labels, no public shaming leaderboard. Everything shown is user-submitted,
  clearly attributed, and comes with a disclaimer

## Tech stack

- **Backend:** Python, Django
- **OCR/Parsing:** EasyOCR, with custom regex-based line-item parsing
  (`ocr_utils.py`)
- **Database:** SQLite (dev) — Django's built-in User model handles auth
- **Deployment:** AWS

## Project structure

Single Django app (`billaudit`) holds all core models — `Hospital`, `Bill`,
`Review` — rather than splitting into multiple apps, to keep things simple
for the MVP.

## Status

🚧 Actively in development. Currently building out the OCR/parsing pipeline
and core Django models. MVP will ship with a seeded demo dataset (15–20
hospitals) rather than needing real user-scale data to feel usable.

## Roadmap

- [ ] Finish OCR pipeline & bill-parsing accuracy
- [ ] Hospital rating + price-tagging flow
- [ ] Infra photo uploads
- [ ] Seed demo dataset (15–20 hospitals)
- [ ] Dockerize the app
- [ ] CI/CD pipeline
- [ ] Load balancing / production-grade AWS deployment

## License

MIT — see [LICENSE](./LICENSE).
