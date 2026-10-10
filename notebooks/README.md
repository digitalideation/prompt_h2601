# Week 5 notebooks

1. [Replicate basics](01_replicate_basics.ipynb): the short API introduction.
2. [Artistic Telephone](02_artistic_telephone.ipynb): iterate, compare, select and pass within your group.
3. [Instructor reveal](03_telephone_reveal.ipynb): decode the shared PNGs and show each chain in order.

## Open in Jupyter

Download the repository ZIP from GitHub (Code → Download ZIP), extract it, and open its `notebooks` folder in the course's existing Jupyter environment. Keep all `telephone_*.py` helpers beside the notebooks. GitHub's preview does not execute notebooks.

Use Python 3.10 or newer. Install the shared requirements in the active kernel:

```python
%pip install -r requirements.txt
```

Restart the kernel if needed. Telephone uses ipywidgets 8 for prompt fields, the model dropdown, file upload and attempt selection. Check widget rendering before class. A file-path fallback is supplied for uploads; the other controls require working widgets.

Both student notebooks default to offline practice. The labelled diagram tests saving and transfer, makes no API calls, and does not respond to prompts. Use actual prepared generated examples for artistic discussion.

## Replicate and live attempts

Students use individual accounts and hidden token input. Never paste tokens into code or submissions. Type GENERATE to request a potentially paid attempt. Saving, comparison and export do not create predictions. Restart the kernel when finished.

The initial curated dropdown contains `black-forest-labs/flux-schnell`. Edit MODELS in `telephone_helpers.py` to curate the list. Confirm each model's inputs and compatibility with version-based prediction creation and a list of HTTPS image URLs. Different output schemas require adapting the helper. Both student examples request one square PNG.

Telephone uses the same prediction lifecycle as the basics notebook: look up a model version, create a prediction, wait for completion, then download its output. It records the resolved version and prediction ID. The basics notebook remains the short introduction and does not record those extra fields in its saved prompt file.

No live generation has been performed for this update. Check the class model, costs and response format before teaching.

## The student loop

- Set session name, group and seat once. Everyone uses the same class session name.
- Start a round and load the assigned incoming PNG in rounds 2 to 5.
- Edit the prompt, generate, then save and preview privately.
- Revise and repeat within the instructor's time and spending budget.
- Refresh the comparison cell and choose any saved attempt for that round.
- Run **Save selected image for passing**. Download that PNG and upload it to the group's SWITCHdrive folder.

Every completed attempt has a separate local image and JSON record containing its exact prompt/settings snapshot. An earlier attempt can be selected after later attempts. Export does not use the current prompt-box text. Once a round has been exported, a different selection cannot overwrite it silently.

Incoming images are inspected locally, not sent as image-to-image inputs. The notebook validates the assigned filename; students must still choose the correct group folder. Passing stays within six groups of five, retaining names such as `01.png`, `01_02.png`, and `01_02_03.png`.

Files are relative to Jupyter's working directory:

```text
outputs/
    basics/<attempt>/image.png and prompt.json
    telephone/<session>/Group_A_S01/
        private/<attempt>/image.png and record.json
        handoff/Group_A/01.png
        practice_handoff/Group_A/01.png
        pending.json (only while a live prediction is pending)
    telephone_reveal.html (instructor export)
```

Keep the private attempt folders for later comparison. Only the selected handoff PNG is uploaded during play. No direct SWITCHdrive integration or private messaging system is required.

## Hidden prompts and instructor reveal

Export removes ordinary image metadata, then embeds a small JSON record in the lowest bits of RGB pixels. Only the selected attempt's own record is included. No cumulative history, secret key or ST3GG installation is needed. This discourages casual prompt reading; it is not encryption or tamper-proof storage.

Pass the original PNG without resizing, screenshots, image editing or JPEG conversion. Those operations can destroy the hidden record. Keep every round's PNG in the shared group folder.

The instructor downloads all group folders and opens notebook 03. It decodes each image, groups by session/mode/group, and reconstructs five chains per group with five positions each. Missing positions and duplicate files are shown explicitly. Unreadable records are flagged. Groups without any readable images cannot be reconstructed, so check the displayed group list.

Prompts open beneath images. Export a self-contained HTML gallery for offline presentation after the game. It includes the prompts, even when collapsed, and can be large for a full class. No student private logs are needed for the selected-chain reveal.

## Recovery

If waiting or downloading fails, retry Telephone's save cell. The existing prediction is reused. Do not create another paid attempt just to retry a download.

A live prediction ID and its snapshot are written to `pending.json`. After a kernel restart, use the same session/group/seat, reconnect, and run the documented recovery cell. It fetches the existing prediction. Confirmed failed/canceled predictions can be cleared with the supplied control. If a request failed before returning an ID, inspect Replicate before retrying.

After a normal restart, use the same identity and round, then refresh comparison to select a previously saved attempt without regenerating. Never delete or replace a passed image without coordinating with the instructor and next student.

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

## References

- [Replicate Python guide](https://replicate.com/docs/get-started/python/)
- [Official Python client](https://github.com/replicate/replicate-python)
- [FLUX.1 schnell inputs](https://replicate.com/black-forest-labs/flux-schnell/api)
- [File outputs](https://replicate.com/docs/topics/predictions/output-files)

