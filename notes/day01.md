# Session 1 teaching notes

[Session plan](../day01.md) | [Notebook setup](../notebooks/README.md) | [Artistic Telephone activity](../activities/artistic_telephone.md)

These notes support the 140-minute session: 130 minutes of activities and a 10-minute break. Use the same learning sequence online or in person. Group discussion happens in breakout rooms or around tables; media sharing stays digital in both formats.

## Prepare before class

1. Confirm students can open Jupyter and have individual Replicate accounts with API access.
2. Download the repository so the notebooks, helpers, and requirements file stay together. Follow the notebook setup guide and rehearse offline mode.
3. Confirm the instructor's model choice. The initial example is `black-forest-labs/flux-schnell`, already linked in the previous game guide. This is a provisional starting point, not a final curated list.
4. Make one instructor live test with that model, checking the returned image, save/export, latency and account cost. Repeat after changes to the model inputs or environment.
5. Prepare six SWITCHdrive group folders with student upload/download access, a separate practice folder, and a final-submission location. Supply links through the normal class channel.
6. Prepare a three-shot storyboard example, actual generated comparison images, and a short video result. The notebooks' labelled offline diagram only rehearses mechanics; it is not a creative-generation demonstration.
7. Rehearse multiple attempts, selection of an earlier attempt, one handoff, and instructor decoding. Check widgets, original PNG transfer, filenames, and timing. Keep all five rounds in each group folder; never resize or convert handoffs.

## Block 1: How models work and workflow, 10 minutes

Use the existing **How Text-to-Image / Video Models Work** slides live in PowerPoint for about five minutes. Add the PDF reference link once the instructor uploads it. Use the remaining five minutes for the workflow example; do not add another lecture block.

Show a finished example and walk backwards through its decisions:

**Concept → storyboard → scene prompts → images/video → refinement**

Suggested concept: a quiet city waking up. Ask students to name the features connecting the shots before showing the prompt text.

Explain only enough model background to support decisions. A model interprets descriptions through learned patterns; it does not guarantee every requested detail. Avoid extended diffusion/latent-space teaching here because this session focuses on creative practice and connects to the technical lecturer's material.

## Block 2: Prompt craft in the web UI, 15 minutes

### Keep the useful scene-writing exercise

Think **Who / What / Where / When / How**. Expand a one-line situation into a short scene description. Ask a partner to describe the imagined framing before generating.

| Starting idea | Detail to explore |
| --- | --- |
| A cyclist crosses a bridge | Time of day, lighting, clothing, camera position |
| A street musician plays at sunset | Subject placement, setting, colour palette |
| A small boat approaches an iceberg | Scale, fog, framing, mood |
| An astronaut plants a tree | Material, environment, visual contrast |
| A dancer stands on an empty stage | Light source, pose, negative space |

### Style comparison

Reuse one subject across realistic, surreal, and graphic versions. Ask what descriptors specify observable qualities rather than simply adding praise such as "beautiful" or "high quality".

| Visual treatment | Example direction |
| --- | --- |
| Cinematic photography | Low camera angle, warm side lighting, shallow depth of field |
| Watercolour | Soft washes, pastel palette, visible paper texture |
| Graphic poster | Flat colours, simple geometry, strong negative space |

Use supported model fields only. Do not copy tool-specific negative-prompt syntax into another model. A camera/lens description is a visual request, not a physical camera setting. Longer prompts are not automatically more controllable.

## Block 3: Simple API notebook, 20 minutes

Choose [01_replicate_basics.ipynb](../notebooks/01_replicate_basics.ipynb) for the plain prompt or [01b_replicate_scene_prompts.ipynb](../notebooks/01b_replicate_scene_prompts.ipynb) to continue Block 2 with a scene dictionary. Both follow the same API flow. Use one version during this slot, rather than running both end to end.

In the scene version, show the dictionary, assemble and read the resulting prompt, then generate. Explain that dictionary keys organise the description; they are not additional model controls. Change one field, such as lighting, rebuild the prompt and compare saved outputs if time allows.

| Time | Teaching action |
| --- | --- |
| 3 min | Show the same model and inputs used in the web UI |
| 4 min | Run offline setup; explain private token entry for live mode |
| 5 min | Edit the prompt and inspect prediction creation and waiting |
| 5 min | Generate once, save locally, display and download |
| 3 min | Change one descriptor or discuss a prepared baseline/revision pair |

Explain the four useful objects: model identifier, input dictionary, returned image URL, local saved image. Keep attention on these rather than library internals.

Paid generation is isolated in one cell and requires typing GENERATE. Display and export cells do not call the model. If a request is interrupted or fails, check the account before another attempt. Students should not share tokens or paste them into code.

The notebook saves each attempt in its own folder. Students can change a prompt without losing the first output. In practice mode, changes to the prompt do not change the test diagram.

## Break, 10 minutes

## Block 4: Artistic Telephone, 45 minutes

Use the [game guide](../activities/artistic_telephone.md) and [Telephone notebook](../notebooks/02_artistic_telephone.ipynb).

Six groups of five; five chains circulate simultaneously within each group. Keep the model fixed. Everyone describes and regenerates an image every round. Retain the original seat-sequence filenames.

Allow five minutes for setup reminder, five seven-minute rounds, then five minutes to check uploads. All seven-minute slots include transfer time. Appoint a coordinator per group and announce rounds with a visible timer.

The notebook calculates routing and retains every completed attempt privately. Students revise, compare, and explicitly choose an attempt. Export hides that selected attempt's prompt and settings in the PNG pixels. Set a small attempt/spending budget from the pilot, leaving the final minute of each round for transfer. Students still transfer files through the SWITCHdrive web interface. No private chat or direct storage integration is required.

## Block 5: Reveal, 15 minutes

Download all original group PNGs and open [the instructor reveal notebook](../notebooks/03_telephone_reveal.ipynb). Confirm all six groups are present, resolve duplicates and inspect missing positions. Reveal prompts only now. Show one chain per group, or select fewer for deeper discussion if transitions take time. Use the same questions as the guide and distinguish human reinterpretation from model variability. Do not describe every difference as an error: drift is part of the activity.

## Block 6: Storyboard, repair and video, 20 minutes

### Student planning and repair, 12 minutes

Provide this template. Students can write or sketch; a polished storyboard is not expected.

| Shot | Subject/action | Framing | Fixed descriptors | Change from previous shot |
| --- | --- | --- | --- | --- |
| 1 | | Establishing view | | |
| 2 | | Medium view | | |
| 3 | | Close-up | | |

Example fixed descriptors: mustard-yellow raincoat, misty stone bridge, warm dawn light, muted blue-grey palette. State that repeating descriptors helps communicate consistency but does not guarantee it.

Choose one detail lost during the game and write a repair prompt. Use the basics notebook for an optional new generation, so no handoff image is overwritten. Save the reason for the revision even if there is no time to generate.

### Instructor video demonstration, 8 minutes

Use the [student web UI walkthrough](../activities/image_to_video_webui.md) with **LTX 2.5 Fast** (720p, 16:9, 6 seconds, 25 fps, audio off). Prepare a suitable 16:9 frame beforehand. If useful, recreate a selected group scene in FLUX.1 schnell using its revealed prompt; do not edit or overwrite original Telephone handoff PNGs. Screen-share the Replicate Playground/Form instead of opening another notebook. The listed LTX rate on 11 October 2026 was $0.03 per second, or approximately $0.18 for six seconds; verify before the lesson. Demonstrate the handoff from still image to motion instructions:

> The cyclist rides slowly across the bridge. The camera tracks alongside at street level. Mist drifts above the water. Retain the raincoat, dawn lighting, and muted palette.

Ask students to separate subject movement, environmental movement, and camera movement. Show a prepared video promptly rather than waiting for a live request. Discuss whether subject appearance and scene details persisted, and how to revise the request.

No student video generation is required. Do not add p5.js or a full editing task.

## Block 7: Save and wrap up, 5 minutes

Students retain image-chain contributions, prompts/settings, observations, a three-shot plan and a repair prompt. The shared PNGs supply the selected-chain gallery without collecting private logs. Students keep their local attempt folders and submit reflection/storyboard/refinement work through the usual class location.

Explain that Session 2 can use one visual as the audio brief, and Session 3 will distinguish preference from adherence to a task. Do not teach the full evaluation clinic here.

## Still to verify with the instructor

- Actual Jupyter deployment and widget/file-transfer behaviour.
- Live smoke test of the selected image and LTX 2.5 Fast video models, current prices and generation latency.
- SWITCHdrive links and permissions, exact submission location.
- Live Replicate smoke test and representative generated demo media.

Technical validation completed for the draft is recorded in the [notebook preparation notes](notebooks.md). Treat offline/mocked testing separately from live generation.

## Demonstration materials and delivery

Present the model slides live in PowerPoint and add the PDF to the student page once it is uploaded. Show the city workflow from concept to storyboard, scene prompts, images and a short video. Compare prepared outputs across models if time permits.

Keep a prepared video available for the image-to-video demonstration. Use breakout rooms online or table groups in person, and screen sharing or projection for the reveal. Folder links and prepared media should be ready before class.
