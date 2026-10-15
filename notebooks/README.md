# Session 1 notebooks

1. [Replicate basics](01_replicate_basics.ipynb): a standalone introduction with six short steps. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-replicate-basics/notebooks/01_replicate_basics.ipynb).
2. [Replicate scene prompts](02_replicate_scene_prompts.ipynb): build a complete prompt from a scene dictionary, then use the same API steps. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-replicate-basics/notebooks/02_replicate_scene_prompts.ipynb).
3. [Artistic Telephone](02_artistic_telephone.ipynb): standalone group game with automatic attempts and hidden PNG prompts. [Open in Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/simplify-artistic-telephone-stegg/notebooks/02_artistic_telephone.ipynb).

## Standalone student notebooks

Open any student notebook directly in Colab, or upload just the notebook file to JupyterHub. Follow its short instructions to install `replicate`, enter your token, write a prompt, generate, view and optionally save an image. All three make real requests and have no practice mode. You do not need the repository, helper files or shared requirements for any student notebook.

All three student notebooks are standalone. The instructor reveal notebook retains its helper files.

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
