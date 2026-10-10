# Week 5: Image & Video Prompting and Workflow Design

[Back to the course homepage](./readme.md)

**Duration:** 2 h 30 min, including a 10-minute break.  
**Delivery:** Online or in person, to be confirmed. Activities and learning goals are the same in either format.  
**Class:** 30 students, working in six groups of five for Artistic Telephone.  
**Tools:** Replicate web UI, a prepared Jupyter Notebook, and SWITCHdrive.

Start with the [Replicate basics notebook](./notebooks/01_replicate_basics.ipynb), then use the [Artistic Telephone notebook](./notebooks/02_artistic_telephone.ipynb) for the game. Read the [Jupyter setup instructions](./notebooks/README.md) before class. [Teaching notes](./notes/day01.md) provide demonstration cues and preparation checks.

## Focus

- Prompt structure and techniques for image and video generation
- Storyboarding, scene descriptions, and visual consistency
- Designing and iterating multi-step image/video workflows

We will follow a concrete process:

**Concept → storyboard → scene prompts → generated images/video → refinement**

Artistic Telephone explores how meaning changes through reinterpretation. We then use that experience to decide which details to preserve deliberately.

## Learning goals

By the end of the session, you should be able to:

- Write scene prompts describing subject, style, lighting, composition, and camera position.
- Distinguish an image description from instructions for subject motion and camera movement.
- Observe and explain interpretation drift in a chain of generated images.
- Plan a short visual sequence and identify what should remain consistent.
- Document an iteration and explain why you changed the prompt.

## Session schedule

| Block | Activity | Duration |
| --- | --- | --- |
| 1 | Visual workflow introduction | 10 min |
| 2 | Replicate web UI and visual prompt craft | 20 min |
| 3 | Notebook walkthrough and first generation | 20 min |
| | Break | 10 min |
| 4 | Artistic Telephone | 45 min |
| 5 | Chain reveal and discussion | 15 min |
| 6 | Storyboard, refinement, and video demonstration | 20 min |
| 7 | Save work and wrap up | 10 min |
| | **Total** | **150 min** |

## Block 1: Visual workflow introduction

Start with a completed example: **a quiet city gradually waking up**.

A three-shot sequence might move from a wide view of a misty street, to a cyclist crossing a bridge, to a close-up of a bicycle wheel on the wet pavement. Show the concept, storyboard, scene prompts, generated images, and one short video result.

Ask: what connects the shots? What must stay the same, and what changes from one scene to the next?

Keep the model explanation brief. The practical focus is how a description guides an output, how the model interprets it, and where it fails to match our intention.

## Block 2: Replicate web UI and visual prompt craft

### Build a scene prompt

Use this structure as a starting point, not a mandatory formula:

**Subject and action → setting → medium/style → lighting → composition/camera → mood**

Think like a director: **Who? What? Where? When? How?**

Compare a plain prompt:

> A cyclist crosses a bridge.

With a more specific scene:

> At dawn, a cyclist wearing a mustard-yellow raincoat crosses a foggy stone bridge. Warm orange light cuts through the mist. Wide shot from street level, muted blue-grey palette, cinematic photography.

Identify which details describe content, which describe visual treatment, and which may be ambiguous.

### Explore style and composition

In pairs, rewrite a plain scene in three styles: realistic, surreal, and graphic. Generate one selected version and discuss what changed.

Demonstrate the instructor-selected model in Replicate's web UI. Distinguish prompt descriptions from actual model settings, such as image dimensions when supported. Negative prompts and other controls should only be demonstrated when the selected model supports them.

Use prepared outputs for optional comparisons across models so the class can discuss differences without waiting for extra generations.

## Block 3: Notebook walkthrough and first generation

Continue the same task in Jupyter using the [short API notebook](./notebooks/01_replicate_basics.ipynb). It starts with an offline practice diagram; switch to live mode for real generation with the instructor:

1. Enter your API token privately using the supplied setup method.
2. Use the initial class model example and edit the prompt. The basics notebook uses one model; the Telephone notebook adds a curated dropdown.
3. Run the generation cell.
4. Display and save the image.
5. Record the prompt, model, relevant settings, and a short observation.

The notebook should make the relationship between web UI inputs and API inputs visible. Students edit text and a few settings; they do not need to write Python from scratch.

Keep a baseline and one revised prompt in the record. Choose one intentional change, such as camera angle or lighting, and explain what you expected it to do. A single pair of outputs is an observation, not proof that a prompt change always works.

Use provided example images if generation is unavailable. Never include API tokens in saved notebooks or submissions.

## Block 4: Artistic Telephone

**Purpose:** practice scene and style prompting while experiencing how meaning shifts through reinterpretation.

### Group structure

Form six groups of five. All passing stays within each group, following a fixed circular order:

**S01 → S02 → S03 → S04 → S05 → S01**

The working H26 format uses five rounds with everyone active. Each student starts a separate chain in round one. In subsequent rounds, they describe the image received from the previous student and generate a new interpretation.

### Each round

1. Inspect only the image assigned to you.
2. Write your own scene description without seeing the previous prompt.
3. Generate an attempt from that description. Revise and try again within the round's time and spending budget.
4. Save each attempt privately, compare the results, and select the one you want to pass.
5. Upload only the image to your group's SWITCHdrive folder for the next participant.

Use one shared, instructor-selected image model during the game. Do not pass a Replicate generation-page link, because it may reveal the prompt. Keep prompt records private until the reveal.

Retain the familiar filename notation, such as `01.png`, `01_02.png`, and `01_02_03.png`. The Telephone notebook calculates file assignments and exports the selected PNG with that attempt's prompt and settings hidden in its pixels for the instructor's reveal. Pass the original file without resizing or converting it. Students transfer it through SWITCHdrive. Shared folders rely on the rule to open only the assigned image.

Starter themes can include *Serenity*, *Ritual*, *Metropolis*, *Decay*, *Connection*, and *Chaos*. Encourage playful drift: ambiguity and unexpected interpretation are part of the activity.

The 45-minute block includes instructions and image transfers. Round pacing will be checked with the chosen model before teaching.

[Artistic Telephone guide](./notes/artistic_telephone.md): the five-round flow, original notation, starter themes, and handoff instructions for 30 students.

## Block 5: Chain reveal and discussion

Use [the instructor reveal notebook](./notebooks/03_telephone_reveal.ipynb) to decode all selected PNGs from the group folders and display each chain in order, with prompts revealed on demand. Each group selects one chain to discuss.

- Which subjects, colours, or compositions persisted?
- Which details disappeared or changed?
- Where did wording suggest a change, and where might generation variability have contributed?
- When was drift interesting, and when did it conflict with the intended result?

Keep the mini-gallery playful, with optional highlights for Most Surprising Transformation or Best Scene Composition.

## Block 6: Storyboard, refinement, and video demonstration

Use a prepared three-shot template to keep this segment focused.

### Plan and refine (12 minutes)

Choose a group image and sketch a short sequence around it. Simple boxes and written descriptions are sufficient.

| Shot | Scene and composition | What stays consistent? | What changes? |
| --- | --- | --- | --- |
| 1 | Establish the location | Palette, style, subject descriptors | Wide framing |
| 2 | Show an action | Same selected descriptors | Action and viewpoint |
| 3 | Show a detail | Same selected descriptors | Close-up framing |

Identify one detail lost during the game, or one inconsistency to repair. Revise a scene prompt to address it. Generate one refinement if time permits and record the result; otherwise save the revised prompt and what you would check next.

### Image-to-video demonstration (8 minutes)

The instructor uses a selected image to demonstrate a short video request. Make the distinction between **subject movement** and **camera movement** explicit:

> The cyclist moves slowly across the bridge while the camera tracks alongside. Mist drifts above the water; retain the dawn lighting and muted palette.

Show how the starting image, motion description, and supported model settings feed into the next workflow step. Discuss unexpected motion, changes to appearance, and what to revise. Keep a prepared video available so the demonstration does not depend on generation finishing live.

Student video generation is an optional extension. A completed video is not required.

## Block 7: Save work and wrap up

Keep the following together:

- Your image-chain contributions and associated prompts.
- Model/settings information and short observations.
- A three-shot storyboard with consistency notes.
- One revised prompt, why you changed it, and an output comparison if generated.

Preserve the first and revised outputs where available. Selected visuals can guide the audio work in Week 6 and support discussion in Week 8.

## Delivery and preparation notes

Use breakout rooms online or table groups in person. The same notebooks, SWITCHdrive folders, image-passing rules, and digital submissions apply in both settings. Use screen sharing or projection for the gallery and video demonstration.

Before teaching, check the notebook setup, one complete group handoff, and model latency. Prepare image/video examples and provide the class folder links. The initial API example uses FLUX.1 schnell from the previous guide; confirm the final model choice and live behaviour before class. The notebooks' offline diagrams rehearse mechanics and do not replace prepared generated examples.

