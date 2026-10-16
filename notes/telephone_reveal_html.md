# Artistic Telephone: local reveal and website gallery

Open [the standalone HTML reveal notebook](../notebooks/03_telephone_reveal_html.ipynb). This is independent of the student notebook and needs no `telephone_*.py` files. The older widget-based presenter is not used by this workflow.

Run the install cell, set `FOLDER` to your downloaded class directory and `OUTPUT` to a new export folder, then run Export. Keep `Group_A`, `Group_B`, etc. and the original handoff PNG filenames. Private `_try` files are ignored. The exporter reads the current student notebook's ST3GG prompts; images in older formats remain visible but their prompts are unavailable.

The output is:

```text
telephone-reveal/
    index.html
    images/
        Group_A/01.png
        Group_A/01_02.png
        ...
```

Double-click `index.html`. Choose a group/chain, reveal one image and its prompt at a time, then show the five-image summary. Arrow keys navigate and P reveals/hides the prompt. No running notebook, Python server, CDN or internet connection is needed by the exported page.

The original PNGs are copied unchanged. Missing images keep their round positions. Duplicate positions are flagged rather than silently choosing a copy. A failed prompt decode leaves the image visible. Review the export warnings before publishing. Existing output folders are never overwritten; use a new name for a second export.

## Publish with Jekyll

After the classroom reveal and a content check, copy the whole output folder to `galleries/telephone/` in the course site and add this link in a Jekyll-processed page:

```liquid
[Artistic Telephone - reveal and gallery]({{ '/galleries/telephone/index.html' | relative_url }})
```

Keep the generated HTML without YAML front matter. Jekyll copies it as a [static file](https://jekyllrb.com/docs/static-files/); the [relative_url filter](https://jekyllrb.com/docs/liquid/filters/#relative-url) accounts for the website subpath. Image paths are relative to the gallery page, so the same folder can be opened locally or moved into the site. No Jekyll plugin, theme change or Python build step is needed.

All prompts are already inside the HTML, including those hidden on screen. Publish only after the reveal; hiding a prompt is not access control. Only publish the exported folder, not notebooks, tokens or private attempts. Full-resolution PNGs can be large: inspect the output folder size before adding it to Git.

## Test the exporter

```bash
python -m pip install 'stegg==3.0.0' nbformat
python -m unittest discover -s tests -p test_reveal_html.py -v
```

The tests create synthetic PNGs and make no API calls. An optional Playwright test checks direct local-file and nested website URLs when `RUN_REVEAL_BROWSER_TESTS=1` and Chromium is installed; `CHROMIUM_PATH` can select an existing browser executable. None of these testing tools are required to use the notebook.
