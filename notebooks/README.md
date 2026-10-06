# Week 5 notebooks

1. [Replicate basics](01_replicate_basics.ipynb): one visible API call, then display and save. Use during the 20-minute introduction.
2. [Artistic Telephone](02_artistic_telephone.ipynb): the same call plus group routing, image loading, private prompt history and handoff export. Use during the game.

## Open in Jupyter

Download the repository ZIP from GitHub (Code → Download ZIP), extract it, and open its `notebooks` folder in your usual Jupyter environment. Keep `telephone_helpers.py` beside the notebooks. Do not simply open the GitHub preview and expect it to execute.

Use Python 3.10 or newer. In a temporary notebook cell, run:

```python
%pip install -r requirements.txt
```

Restart the kernel afterwards. The requirements install libraries into the selected kernel environment; students should use the Jupyter environment already established in the course. The offline walkthrough still needs Pillow, IPython and, for Telephone, ipywidgets, but makes no API calls.

Run cells from top to bottom with Shift+Enter. Notebooks open in offline practice mode. They draw a labelled test diagram rather than use a real generated image. This is suitable for testing saving and transfer only. The instructor supplies actual prepared media for artistic discussion or a generation outage.

## Live generation

Switch to live mode and enter your individual API token through the hidden prompt. Never paste it into notebook code. Type GENERATE only when ready to make one potentially paid request. Display, saving, history and export do not generate again. Restart the kernel when finished to clear the client from memory.

Initial model: `black-forest-labs/flux-schnell`, from the existing course guide. The short notebook uses this one model. The Telephone dropdown initially contains one corresponding entry; the instructor can curate `MODELS` in `telephone_helpers.py` after verifying each model's identifier, supported inputs and list-of-file-outputs behaviour. Both notebooks request one square PNG. Adding a model that returns a different output shape requires adapting the read step too.

The model identifier is not version-pinned. Logs do not claim to record a resolved model version. Confirm the class model and runtime before teaching; no live generation has been performed for this draft.

## Passing and saving

The Telephone notebook calculates the original filenames and requires the assigned incoming filename in rounds 2 to 5. It cannot verify the semantic content of the file or which SWITCHdrive folder it came from; students must use their group's folder.

Handoff export rebuilds a PNG from pixels, removing embedded prompt metadata. Download the file using the notebook link, then upload it through SWITCHdrive. There is no direct SWITCHdrive API integration or need for a messaging platform.

Files are saved relative to the notebook's working directory:

```text
outputs/
    basics/<attempt>/image.png and prompt.json
    telephone/<session>/Group_A_S01/
        private/<attempt>/image.png and record.json
        handoff/Group_A/01.png
        practice_handoff/Group_A/01.png
        reflection.json
        after_reveal_<id>.zip
```

These outputs are ignored by Git. They are not a shared service. Prompt records stay on the student's Jupyter server until explicitly submitted. Only the handoff PNG is passed during play. The after-reveal ZIP contains prompts and must not be used for passing.

After a kernel restart, set the same session/group/seat and use the history section to inspect saved attempts. To re-export a saved attempt, assign its displayed directory to `saved_run = Path("...")`, then run the export cell. Do not regenerate merely to recover a saved image.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Missing library | Install requirements in the active kernel and restart |
| Widgets do not render | Check ipywidgets support in the existing Jupyter installation; the notebook documents plain-value and file-browser fallbacks |
| Helper import fails | Keep the helper beside the notebook and launch from the `notebooks` folder |
| Missing/wrong incoming file | Check group and round, preserve the original filename, and wait for the correct upload |
| Token/access/credit problem | Check your Replicate account privately; use practice mode meanwhile |
| Long or interrupted generation | Check Replicate predictions before retrying; there may already be a charged request |
| Download/save fails | Retry the save cell first; it does not generate again |
| Handoff already selected | Reuse the exported file; coordinate with the instructor before replacing a passed image |

## Validation and remaining classroom checks

The draft is validated by executing all code cells in order in-process and by using mocked API responses. Nine checks passed; the separate full-kernel test is optional. The restricted development environment prevented a Jupyter kernel from opening its local sockets, so kernel/UI execution is not claimed as verified. Tests cover notebook structure, within-group routing across all five rounds, prompt-free exports, saved history, cancelled requests and prevention of generation from save/display steps. Test dependencies are separate from classroom dependencies. The tested SDK is Replicate 1.0.7, with ipywidgets 8.1.9 and Python 3.12.

Remaining checks: real Replicate credentials/model availability, billed live generation, the institution's Jupyter UI and download behaviour, SWITCHdrive permissions, and a timed class handoff. No student credentials are required for the offline tests. The offline diagram is not evidence of model quality.

## Instructor/developer checks

From the repository root:

```sh
python -m pip install -r notebooks/requirements.txt -r tests/requirements.txt
python -m unittest discover -s tests -v
```

The tests use temporary output folders and mocked requests. They do not make paid API calls.

To additionally execute both notebooks with a real local kernel in a suitable environment:

```sh
RUN_JUPYTER_KERNEL_TESTS=1 python -m unittest discover -s tests -v
```

This still uses offline practice mode. It does not replace testing file download and upload in the actual Jupyter browser interface.

## References

- [Replicate Python guide](https://replicate.com/docs/get-started/python/)
- [Official Python client](https://github.com/replicate/replicate-python)
- [FLUX.1 schnell inputs](https://replicate.com/black-forest-labs/flux-schnell/api)
- [File outputs](https://replicate.com/docs/topics/predictions/output-files)
