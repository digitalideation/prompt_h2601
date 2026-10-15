# Session 1 notebooks

1. [Replicate basics](01_replicate_basics.ipynb): a standalone introduction with six short steps. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-replicate-basics/notebooks/01_replicate_basics.ipynb).
2. [Replicate scene prompts](02_replicate_scene_prompts.ipynb): build a complete prompt from a scene dictionary, then use the same API steps. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-replicate-basics/notebooks/02_replicate_scene_prompts.ipynb).
3. [Artistic Telephone](02_artistic_telephone.ipynb): standalone group game with automatic attempts and hidden PNG prompts. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-artistic-telephone-stegg/notebooks/02_artistic_telephone.ipynb).

## Standalone student notebooks

Open any student notebook directly in Colab, or upload just the notebook file to JupyterHub. Follow its short instructions to install `replicate`, enter your token, write a prompt, generate, view and optionally save an image. All three make real requests and have no practice mode. You do not need the repository, helper files or shared requirements for any student notebook.

All three student notebooks are standalone. The instructor reveal notebook retains its helper files.

## Artistic Telephone

[Open the standalone game notebook in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-artistic-telephone-stegg/notebooks/02_artistic_telephone.ipynb). The student notebook uses `replicate`, `stegg` (ST3GG), `ipywidgets` and Pillow; all are installed inside the notebook. **No custom Python helper files or repository checkout are required.**

After installing packages, students connect to Replicate and set GROUP and SEAT once. A compact game panel contains the **round selector**, incoming/outgoing filename instructions, **optional incoming-PNG preview**, **prompt box**, **Generate and save** button, attempt preview/selector, and **Export selected PNG** button. Students can open their incoming PNG independently in SWITCHdrive without uploading it.

Each paid generation automatically embeds its *captured* prompt in a numbered PNG using [ST3GG](https://github.com/elder-plinius/ST3GG). A failed download/encoding can be retried with a **Retry saving** button without another model request. Export copies the chosen image to the expected group filename. Colab also downloads the exported PNG to the student's computer. Only selected PNGs go to SWITCHdrive; no separate prompt logs are required. The hidden text is **not encryption**, and students should not inspect others' prompts during the game.

The instructor reveal notebook still uses its existing course helpers, but its gallery can decode ST3GG PNGs as well as older Telephone pixel-encoded PNGs. Run the instructor notebook with ST3GG installed (`%pip install -q stegg==3.0.0`) when revealing the new images.

## References

- [Replicate Python guide](https://replicate.com/docs/get-started/python/)
- [FLUX.1 schnell](https://replicate.com/black-forest-labs/flux-schnell)
