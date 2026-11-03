# Locals (working name): London resident rewards site

Static site in `site/`, deployed to GitHub Pages by `.github/workflows/pages.yml`.

## Rebuild
- `python3 scripts/prep_data.py`: venue map data from the sibling `london-pulse` project.
- `python3 scripts/prep_offers.py`: validates `internal/offers_raw.json` into `site/data/offers.json`.
- `python3 scripts/build_pages.py`: regenerates all pages from `scripts/templates/` (commit the output).
- `node tests/test_model.js`: model tests.

## Audiences
Resident pages: `index`, `offers`. Business pages: `business`, `money` (partner briefing, noindex, unlinked).

## Before the deploy workflow will pass (it checks these)
Set in `site/config.js`: `FORM_ENDPOINT`, `SITE_URL`, `CONTACT_EMAIL`. Fill the controller details in `scripts/build_pages.py` (PRIVACY) and rebuild.
Also: brand name and domain check, ICO registration, update the privacy notice if analytics is enabled.

## Private (git-ignored, never deploy)
`internal/`, `plan.html`, `playbook.html`.
