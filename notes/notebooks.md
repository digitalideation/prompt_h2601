# Notebook preparation and technical notes

These notes are for teaching and maintenance. Students use the [Jupyter setup guide](../notebooks/README.md).

## Before teaching

- Confirm Python, dependencies, widget rendering and file download behaviour in the class Jupyter environment.
- The initial model is `black-forest-labs/flux-schnell`. Curate the Telephone dropdown in `MODELS` in `telephone_helpers.py`.
- Check each model's supported inputs, version-based prediction creation and list of HTTPS image URLs. Other output shapes require adapting the helper.
- Run a live account/model check, including costs, output format, latency, saving and handoff export. Offline/mocked checks do not establish live availability.
- Keep actual generated examples available. The offline diagrams rehearse mechanics and do not demonstrate prompt quality.
- Choose one basics version for the 20-minute walkthrough. The scene version connects the visual prompt structure to a dictionary; it is not an additional required walkthrough.

## Instructor reveal notebook

Use [03_telephone_reveal.ipynb](../notebooks/03_telephone_reveal.ipynb) after downloading the original group PNGs. Keep the notebook beside the helper files in `notebooks/`.

The notebook separates session, mode and group, then reconstructs the chains. Check the group list against the class: a group with no readable records cannot appear. Resolve duplicates and inspect missing images. Reveal prompts during discussion and optionally export the self-contained HTML gallery.

## Validation and classroom checks

Offline tests cover notebook cell execution in process, generation/selection snapshots, retry without a new request, prediction recovery, all group routes, Unicode hidden records, corruption detection, missing/duplicate gallery positions, escaped prompt text and selection of an earlier attempt. They use temporary output folders and mocked API responses.

The full-kernel test is optional because the development sandbox blocks local kernel sockets. Browser widget interactions, real account/model availability, billed generation, Jupyter downloads, SWITCHdrive permissions and a timed classroom transfer still need an instructor pilot.

From the repository root:

```sh
python -m pip install -r notebooks/requirements.txt -r tests/requirements.txt
python -m unittest discover -s tests -v
```

Where local kernels are supported:

```sh
RUN_JUPYTER_KERNEL_TESTS=1 python -m unittest discover -s tests -v
```

Neither test mode makes paid API calls.
