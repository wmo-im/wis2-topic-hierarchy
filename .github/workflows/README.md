# GitHub Actions

The following GitHub Actions are in place for this repository:

- on Pull Request: test the generation of WTH to TTL files
- on Commit/Push to `main` branch:
  - generate WTH specification document and push to `gh-pages` branch
  - generate WTH bundle and push to `gh-pages` branch
  - generate WTH Codelists to TTL files, and push to `gh-pages` branch
- on Commit/Push to `gh-pages` branch: publish the TTL files to the WMO Codes Registry testing environment

Edit `codelists/*.csv` files -> GitHub Pull Request (test generation) -> Merge Pull Request (generate and commit to `gh-pages` branch) -> Publish to WMO Codes Registry testing environment

Publication to the WMO Codes Registry operational environment is executed as a manual step.
