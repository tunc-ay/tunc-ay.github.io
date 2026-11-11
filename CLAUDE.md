# CLAUDE.md

Personal portfolio site of Tuncay Kayaoglu, Lead Technical Writer at Analog Devices (microcontroller documentation). Live at https://tunc-ay.github.io.

## Stack

- Jekyll on GitHub Pages, built by GitHub Actions ([.github/workflows/jekyll.yml](.github/workflows/jekyll.yml), Ruby 3.3).
- Theme: `minimal-mistakes-jekyll` (gem, v4.26.2), skin `air`. Custom styles live in [assets/css/main.scss](assets/css/main.scss). Accent color is navy `#1f3a5f`.
- Pushing to `main` deploys the site. There is no staging branch, so check changes locally first.

## Commands

- Build check: `bundle exec jekyll build --destination "$TEMP/site-check"`. The Sass deprecation warnings come from the theme and can be ignored.
- Preview: `bundle exec jekyll serve`, then open http://localhost:4000.
- `_site/` and `.jekyll-cache/` are build output. Never edit or commit them.

## Structure

- [_config.yml](_config.yml): site settings, author sidebar, collections, front-matter defaults. Restart `jekyll serve` after editing it.
- [_data/navigation.yml](_data/navigation.yml): top menu (Portfolio, How it works, About, Contact).
- [index.md](index.md): splash home page. [_pages/projects.md](_pages/projects.md): Portfolio, built from `feature_row` cards defined in its front matter. [_pages/about.md](_pages/about.md): bio, work history, and education.
- [_visuals/](_visuals/): the "How it works" collection, one Markdown page per peripheral. [_pages/visuals.md](_pages/visuals.md) is its index page (grid layout, sorted by `order`).
- [assets/images/visuals/](assets/images/visuals/): SVG diagrams for the series.
- [assets/images/projects/](assets/images/projects/): Portfolio card thumbnails. [assets/projects/](assets/projects/): the PDFs the cards link to.
- [_posts/](_posts/): contains only a "Hello world" placeholder. The blog is not linked from the navigation.

## The "How it works" series

Illustrated explainers on how MCU peripherals work (UART done; I2C, SPI, and others planned).

To add a peripheral:
1. Put the SVG in `assets/images/visuals/<name>.svg`.
2. Create `_visuals/<name>.md` with `title`, `order` (next number), `excerpt`, and `header.teaser`. Copy the structure of [_visuals/uart.md](_visuals/uart.md): the figure with `alt` text, a numbered walkthrough, the waveform or timing in a text table, and "Things to remember".
   Start with a "← All explainers" link (`<p class="visuals-back">`) and end the page with `{% include visuals-nav.html %}`, which builds previous/next links from `order`.
3. Add a card to the `visuals` list in [_pages/projects.md](_pages/projects.md).

Diagram conventions, so the series looks consistent:
- SVG with live text, plus a `<title>` and `<desc>`. Use a 1536-pixel-wide `viewBox`.
- TX is blue (`#1f6fd1`) and RX is green (`#1e5a33`). Keep these signal colors the same in every diagram.
- Waveforms are drawn from exact coordinates. Check bit order and bit count against the example byte (UART sends the least significant bit first).
- Ground is a plain line with no arrowhead.
- Show what happens inside the chip (shift register, FIFO, baud-rate generator, sampling), not only the wire waveform.

## Accuracy and publishing rules

- Technical accuracy matters more than polish. Check every waveform, bit count, and timing figure by hand. Typical errors are bit order, idle level, clock polarity and phase (SPI), and open-drain behavior (I2C).
- Keep the content generic and publicly known. Do not add confidential Analog Devices material, unreleased product details, or internal register names or pinouts. Tuncay should confirm employer approval for work related to the job.
- Voice: clear, precise, reader-first. No marketing slogans.
- Every image needs useful `alt` text. Do not rely on color alone to carry meaning.

## Working notes

- `HowUARTworks.png` (1.7 MB, in `assets/images/visuals/`) is a local source image and is deliberately not committed. Do not commit it unless asked.
- Git on this Windows machine warns that LF will be replaced by CRLF. That is harmless.
- Commits and pushes happen only when Tuncay asks. Pushing to `main` publishes immediately.
- Shell commands run in Git Bash. Some commands (moving files, launching a browser) have been blocked by the permission classifier, so ask Tuncay to do those steps or to add a narrow permission rule.
