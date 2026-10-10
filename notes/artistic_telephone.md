# Artistic Telephone: Week 5 class flow

[Week 5 session](../day01.md) | [Telephone notebook](../notebooks/02_artistic_telephone.ipynb)

## Goal

Explore how meaning, style, and composition drift when an image is described and generated again. Your interpretation is part of the game. Unexpected changes can be interesting rather than failures.

## Before play

- Complete the [short Replicate API introduction](../notebooks/01_replicate_basics.ipynb).
- Form **six groups of five** for 30 students. Use breakout rooms online or table groups in person.
- Assign group letters A to F and seats 01 to 05. Keep these assignments fixed.
- Each group uses its own shared SWITCHdrive folder. The instructor supplies links and checks upload/download access before class.
- Everyone uses an individual Replicate account and the same instructor-selected image model. The initial example is [FLUX.1 schnell](https://replicate.com/black-forest-labs/flux-schnell), carried over from the previous guide; confirm the final choice before teaching.
- Each student runs their own copy of the notebook. Tokens and prompt logs stay private.
- Choose a group coordinator to help with filenames, missing uploads, and the round timer.

All passing stays inside your group:

**S01 → S02 → S03 → S04 → S05 → S01**

## Everyone plays at the same time

There are **five simultaneous chains per group**. In round 1, everyone creates a starting image. In each following round, everyone interprets an image from the previous seat and generates another image. No student waits for four others to complete a single chain.

Five rounds give each chain five images. There is no sixth generation when it returns to its starting student.

## Timing: 45 minutes plus a separate 15-minute reveal

| Stage | Time | Activity |
| --- | --- | --- |
| Setup reminder | 5 min | Confirm group, seat, model, theme, and folder access |
| Round 1 | 7 min | Everyone writes and generates a starting scene |
| Round 2 | 7 min | Inspect the received image, describe, generate, pass |
| Round 3 | 7 min | Repeat within the group |
| Round 4 | 7 min | Repeat within the group |
| Round 5 | 7 min | Complete the fifth image; stop generating |
| Upload check | 5 min | Check each selected image is in the right group folder |
| **Game total** | **45 min** | |
| Reveal and discussion | 15 min | View selected chains and reveal prompts |

Each seven-minute round includes iteration, selection and image transfer. Reserve the last minute for choosing and uploading; students do not have to use every possible attempt. Use a visible timer and announce each round together. Pilot one round before class; if latency is too high, shorten the number of rounds explicitly rather than rushing students or adding unplanned API calls.

## What to do in each round

1. Select the round in your notebook and run the round-instructions cell.
2. In round 1, use your group's theme. Later, download only the assigned image from your group folder and load it into the notebook.
3. Write a new prompt describing what you see. Do not inspect the previous prompt or earlier images in the chain.
4. Generate and save an attempt privately. If time and budget allow, revise the prompt and try again. Compare saved attempts and choose one to pass.
5. Run **Save selected image for passing**, then download the handoff PNG using the notebook link. Upload that PNG to your group's SWITCHdrive folder with the filename unchanged.
6. Wait for the next round signal. Keep sending to the same next seat.

The image is for you to interpret. This is a text-to-image game; the received image is not sent as an image-to-image input.

## Original filename notation

Keep the sequence of participating seats in the filename:

```text
Group_A/
    01.png
    01_02.png
    01_02_03.png
    01_02_03_04.png
    01_02_03_04_05.png
    02.png
    02_03.png
    02_03_04.png
    ...
```

For example, **seat 01** receives `05.png` in round 2 and exports `05_01.png`. In round 3, that same seat receives `04_05.png` and exports `04_05_01.png`. The notebook calculates this for you.

Filenames can repeat across groups because the folders are separate. Do not rename a file to pretend it belongs to another chain. If your browser adds a suffix such as `(1)`, retrieve the correct file and restore its assigned name before loading it.

## Share images only

- Use the notebook's handoff export. It removes ordinary image metadata and hides the selected attempt's own prompt and settings in the PNG pixels for the reveal. This is simple steganography, not encryption; do not decode prompts during play.
- Pass the original PNG. Screenshots, resizing, editing, and JPEG conversion can destroy its hidden record. Keep every round's PNG in the shared folder.
- Do not share Replicate prediction-page links, notebooks, JSON logs, or the final submission ZIP during play.
- The notebook does not connect directly to SWITCHdrive. Download the PNG to your computer, then upload it through the folder page.
- Shared folders do not hide other images. The rule is to open only the file assigned to you.
- Keep practice diagrams in a separate practice folder. They are not generated outputs and should not enter a live chain.

Each successful generation is saved privately. The handoff export protects the already selected file for a round from accidental replacement. If a selected image needs to change, stop and coordinate with the instructor and next student first.

## If something is late or fails

Do not keep clicking Generate. Check whether a prediction already exists in Replicate before retrying. Tell your group coordinator which file is missing. Pause the affected chain; do not substitute an image from another chain. The instructor can shorten the game and discuss the partial chain at the reveal.

Offline practice supports a rehearsal of naming, transfers, and exports without API calls. It uses a clearly labelled test diagram and cannot demonstrate model interpretation. For a teaching fallback, the instructor should prepare actual image chains before class.

## Starter themes

Assign one theme per group: **Serenity, Ritual, Metropolis, Decay, Connection, Chaos**.

Example for Serenity:

> At dawn, a monk stands in a quiet temple courtyard. Warm mist surrounds the stone walls, soft light, wide cinematic composition.

Students may change era, medium, or emotion as a chain develops. Keep subject, style, lighting, and composition vocabulary in mind.

## Reveal and discussion

After all rounds stop, the instructor downloads the group folders and opens [03_telephone_reveal.ipynb](../notebooks/03_telephone_reveal.ipynb). It decodes the selected PNGs, orders each chain, and shows missing or duplicate positions. Reveal prompts under each image. Each group chooses one complete or partial chain to discuss. The instructor can export a self-contained HTML gallery for later viewing.

- What persisted: subject, colour, framing, or mood?
- What drifted, and where?
- Which words might explain a change? What could be generation variability?
- When was drift creatively useful?

Optional highlights: **Most Surprising Transformation**, **Best Stylistic Leap**, **Strongest Narrative Continuity**.

After the reveal, write a short reflection in your own notes and complete the three-shot storyboard. Identify a lost detail and write one repair prompt. An extra generation is optional and can use the basics notebook, keeping the game's passed files unchanged.

## Final submission

The shared group folders already contain everything needed for the instructor's selected-chain gallery. No separate prompt-log upload is needed. Retain the local `private` folder with all attempts, and submit your reflection, storyboard, and refinement comparison to the location supplied by the instructor after the reveal. Do not submit API tokens or the entire notebook environment.

## Instructor checks

Test one complete handoff with the actual Jupyter and SWITCHdrive setup. The working format produces **150 selected class-wide images**, or five per student. Total generations can be higher because students iterate. Set a per-round attempt and spending budget based on a timed pilot, including walkthroughs and refinement. Check current model cost and latency with the class budget. Confirm the model list, sample media, folder links, and accessible audio/video playback before teaching.

