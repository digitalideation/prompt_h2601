# Session 1 notebooks

1. [Replicate basics](01_replicate_basics.ipynb): a standalone introduction with six short steps. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-replicate-basics/notebooks/01_replicate_basics.ipynb).
2. [Replicate scene prompts](02_replicate_scene_prompts.ipynb): build a complete prompt from a scene dictionary, then use the same API steps. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-replicate-basics/notebooks/02_replicate_scene_prompts.ipynb).
3. [Artistic Telephone](02_artistic_telephone.ipynb): standalone group game with automatic attempts and hidden PNG prompts. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-artistic-telephone-stegg/notebooks/02_artistic_telephone.ipynb).

## Start with the two standalone notebooks

Open `01_replicate_basics.ipynb` or `02_replicate_scene_prompts.ipynb` directly in Colab, or upload just the notebook file to JupyterHub. Follow its short instructions to install `replicate`, enter your token, write a prompt, generate, view and optionally save an image. Both make real requests and have no practice mode. You do not need the repository, helper files or shared requirements for either notebook.

The repository setup below applies to the Telephone notebooks, which still use the existing course setup.

## Open the other notebooks in JupyterHub

After the updated course material is merged into the repository's **main** branch, each student works in their **own JupyterHub account**. Open a terminal from JupyterLab (File → New → Terminal), then clone the course repository into your home directory:

```bash
cd ~
git clone https://github.com/digitalideation/prompt_h2601.git
cd prompt_h2601/notebooks
```

If you already have a checkout, do not clone again: open its `notebooks` folder instead. Open a notebook in JupyterLab's file browser and run it with **Shift+Enter**. GitHub's preview cannot run notebooks. Keep the `telephone_*.py` helpers next to the notebooks; they are included in the clone.

Use Python 3.10 or newer. In a notebook, install the shared requirements in the **active notebook kernel** (only if the JupyterHub environment does not already provide them):

```python
%pip install -r requirements.txt
```

Restart the kernel after installation if prompted. The JupyterHub administrator may choose to preinstall these packages for everyone; students should not need administrator permissions. If installation is denied or internet access from JupyterHub is restricted, ask the instructor rather than changing the shared environment.

**Before editing:** In JupyterLab, use File → Save Notebook As… to make your own working copy in the same `notebooks` folder (for example, `my_replicate_basics.ipynb`). This keeps the course starter available and keeps relative imports and `requirements.txt` in the right place. Generated results are stored in `notebooks/outputs/`, which Git ignores. Each student's JupyterHub home directory is separate; other students cannot access these results through the course checkout.

To fetch updated course material later, first back up your own notebooks and files. From the original repository folder, use `git status` to inspect changes before `git pull`; Git may refuse a pull when tracked notebooks have been edited. Do not run `git reset --hard` or `git clean -fd` on your work. If `git pull` fails, ask the instructor for help instead of deleting your work.

Telephone uses ipywidgets 8 for prompt fields, the model dropdown, file upload and attempt selection. Check that its controls appear. There is a file-path fallback for uploads; the other controls require functioning widgets.

Only Replicate image generation uses your personal Replicate API token, entered via the notebook's hidden prompt. Never paste tokens into notebook code, commit them to Git, share them through SWITCHdrive, or place them in `outputs/`.

The Telephone notebook defaults to offline practice. The labelled diagram tests saving and transfer, makes no API calls, and does not respond to prompts.

## Replicate and live attempts

Use your individual account and the hidden token input. Never paste tokens into code or submissions. In live mode, running the generation cell immediately requests a potentially paid attempt; there is no separate confirmation. Saving, comparison and export do not create predictions. Restart the kernel when finished.

The initial model is `black-forest-labs/flux-schnell`. Use the model list supplied for the activity. These examples request one square PNG.

Both introductory notebooks use the same `generate_image(inputs, client, MODEL)` function to create a prediction, wait for completion and return image URLs. They download the image for display and optionally save one PNG. Telephone also uses explicit prediction creation and waiting, and records the resolved model version and prediction ID.

## Structured scene-prompt version

In `02_replicate_scene_prompts.ipynb`, edit a `scene` dictionary and use a visible sentence template to connect subject, action, setting, time and visual details. Read the printed prompt before generating. The dictionary is a writing aid, not another API schema. Keep a copy of your notebook to retain your scene description and prompt.

For a revision, edit one field in section 3a, rerun 3a and 3b, then generate and view the result in sections 4 and 5. Save images you want to keep using different filenames in section 6.

## Artistic Telephone

The student notebook `02_artistic_telephone.ipynb` also runs **standalone in Colab or JupyterHub**. It needs only `replicate` installed in the notebook itself, your Replicate token, and a SWITCHdrive browser tab. There are no student-facing helper files, upload widgets, practice mode, separate prompt JSONs, or required repository checkout.

1. Set group and seat once. Set round to get the assigned input and output filenames.
2. Open the assigned incoming image manually in SWITCHdrive, then describe it using a plain `prompt` variable.
3. Generate: the model runs once and its PNG is automatically saved with that exact prompt embedded in a PNG text field; repeat to make numbered attempts.
4. Review images and enter an attempt number. Export copies the selected PNG, which you download (automatically in Colab) and upload to the group's SWITCHdrive folder.
5. Change only round and prompt for the next turn.

PNG text metadata can be read deliberately, so students agree not to reveal others' prompts until the final reveal. Screenshots and image transformations can strip the prompt; send the original exported file. The instructor reveal handles both the new PNG text format and older Telephone pixel-encoded records. The instructor notebook still uses its original helper files.

Colab notebook files are temporary: download your own private attempts if you want them after the runtime ends. The selected handoffs should remain in the class SWITCHdrive folder. Each generation may incur a charge.

## References

- [Replicate Python guide](https://replicate.com/docs/get-started/python/)
- [FLUX.1 schnell](https://replicate.com/black-forest-labs/flux-schnell)
