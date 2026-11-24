# Academic Map

[![Build Status](https://github.com/CURIOSSorg/academic-map/actions/workflows/deploy-book.yml/badge.svg)](https://github.com/CURIOSSorg/academic-map/actions/workflows/deploy-book.yml)

> A Jupyter Book of resources for open source in academia

## Usage

Go to the website where this is rendered. Currently, that is [here](https://curioss.org/academic-map/intro.html). You can also build this locally - see below.

## Install

This is a Jupyter Book, and depends on the Jupyter Book tooling to work. [Their documentation](https://jupyterbook.org/en/stable/intro.html) has an excellent intro to get started. For now:

- Clone this repository locally.
- Edit any Markdown locally.
- Add any pages that you want to be in the Table of Contents to `_toc.yml`.
- Run `scripts/build.sh` in order to automatically build the changes. You may need to run `chmod +x scripts/build.sh` to make this executable, first.

## Development

### Automatic Deployment

The site automatically builds and deploys when you push to the `main` branch, and once a day, to pick up changes to the CURIOSS data. The GitHub Action (`.github/workflows/deploy-book.yml`) will:

1. Fetch CURIOSS member logos and open funding calls from curioss.org (`python scripts/sync_curioss.py`)
2. Build the Jupyter book (`jupyter-book build --all .`)
3. Lint all markdown files (`npm run lint`)
4. Check that every page is in `_toc.yml`, its folder's `index.md`, and any member lists it belongs on (`npm run check-toc`)
5. Publish the site at [curioss.org/academic-map](https://curioss.org/academic-map/intro.html), by pushing the built HTML into the `static/academic-map` folder of the [curioss.org repository](https://github.com/CURIOSSorg/curioss.org). That push triggers the curioss.org site's own deploy.

If any step fails, the deployment will stop and you'll receive a notification (if enabled in your GitHub notification settings).

External links are not checked during deploys, so a third-party outage can't block the site. Instead, `.github/workflows/link-check.yml` checks them on every pull request and once a week.

### Local Development

To work on the site locally:

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Lint markdown
npm run lint

# Check links
npm run links

# Check TOC completeness (ensures all files are in _toc.yml, index pages, and member lists)
npm run check-toc

# Build the book locally (this first fetches CURIOSS member logos and
# funding calls into _curioss/; see scripts/sync_curioss.py)
npm run build

# View the built site
open _build/html/index.html
```

### Manual Deployment

To deploy without pushing to `main`, run the `deploy-book` workflow by hand from the repository's Actions tab.

To run every check and build the site locally, without deploying, use:

```bash
./scripts/build.sh
```

## Contribute

Please! All contributions are welcome. As is written in the intro page currently:

- [**Open an issue**](https://github.com/CURIOSSorg/academic-map/issues/new) to add data. If you are unsure how to use Git easily or you are unsure where something goes, just open an issue with your suggestions or comments.
- Add a page directly to the Git repository using a **Pull Request**. The GitHub repo is [here](https://github.com/CURIOSSorg/academic-map/). If you have a university, community, or so on, and you know how to use Git and GitHub, please open a PR with the resource!
- **Complain**. If this isn't working for you, tell us why, and we'd be more than happy to work to make it better.
- **Send an email.** Richard Littauer is the main editor for this repository, at the moment, and he's happy to incorporate any changes or to build a more welcoming and inclusive structure for collaboration here if any of the above options is less than ideal. Email [info@curioss.org](mailto:info@curioss.org).

## Code of Conduct

By interacting with this repository you agree to the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE).

### Disclaimer

This site was sponsored by the Alfred P. Sloan Foundation under Grant Number G-2023-21015. Any opinions, findings, conclusions or recommendations expressed herein are those of the author(s) and do not reflect the views of the Alfred P. Sloan Foundation or Carnegie Mellon University.
