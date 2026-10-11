# From a still image to a short video: Replicate Web UI

[Session 1](../day01.md) | [Artistic Telephone guide](artistic_telephone.md)

**Goal:** Give a still scene simple motion instructions and see which visual details persist. This is an optional extension after the Artistic Telephone reveal, not another notebook task. No video submission is required.

## 1. Choose or recreate your starting image

Choose a scene from your group's revealed chain. To make a **landscape 16:9 starting frame**, you can recreate that scene:

1. Open [FLUX.1 schnell on Replicate](https://replicate.com/black-forest-labs/flux-schnell) and use its **Playground / Form**.
2. Paste a revealed prompt from your group as a starting point. Adjust it to restore a missing detail, if useful.
3. Set `aspect_ratio` to **16:9** and `num_outputs` to **1**. Generate and download the new still.

This generates a *new interpretation*, not an exact restoration of the group image. Keep the original exported Telephone PNG unchanged so its hidden reveal record remains intact. If you already have a suitable 16:9 image, you can skip this step.

## 2. Open the image-to-video model

Open [LTX 2.5 Fast on Replicate](https://replicate.com/lightricks/ltx-2.5-fast) and choose **Playground → Form**. Use these inputs:

| Web UI field | Value |
| --- | --- |
| `image` | Upload your prepared still image (the **first frame**) |
| `prompt` | Describe subject, environment and camera motion |
| `resolution` | **720p** |
| `duration` | **6** seconds |
| `aspect_ratio` | **16:9** |
| `fps` | **25** |
| `generate_audio` | **Off** |
| `last_frame_image` | Leave empty |

## 3. Write a motion prompt

Describe what happens *after* the still image, rather than describing only what is visible. Separate:

- **Subject movement:** What does the person or object do?
- **Environment movement:** What changes in the surroundings?
- **Camera movement:** Does the view track, pan, zoom or remain still?

For example:

> The cyclist in the mustard-yellow raincoat rides slowly across the stone bridge. Soft mist drifts above the water. The camera tracks alongside at street level. Keep the same raincoat, warm dawn lighting, and muted blue-grey palette. One continuous shot with gentle, natural motion.

## 4. Run, download and compare

Click **Run** once. When the prediction succeeds, download the MP4. If it is still processing, check the existing prediction before starting another paid run.

Compare the video against **the still image you uploaded**:

- Which subject and scene details stayed consistent?
- Did subject, environment and camera move as requested?
- What changed unexpectedly? What would you revise?

**Consistency is not guaranteed.** Each result is a new model interpretation, and drift can be interesting rather than simply an error.

**Cost reference (11 October 2026):** LTX 2.5 Fast at 720p is listed at **US$0.03 per output second**, approximately **US$0.18 for six seconds**. Recreating one still with FLUX.1 schnell is listed at **US$0.003 per image**. Each rerun may incur another charge; check the current prices on both model pages before clicking Run.

**No notebook, API key or additional editing software is needed for this web-UI activity.** You need a signed-in Replicate account with available credits.
