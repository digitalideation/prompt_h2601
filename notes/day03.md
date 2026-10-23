# Session 3: Evaluation Clinic teaching notes

Student pages: [Session 3](../day03.md) and [working sheet](../activities/evaluation_clinic.md).

## Status and scope

This is the agreed teaching skeleton. The worksheet specifies an image case, a text case, example scenarios and shared generation models. Sample outputs, worked ratings, reference answers and the evaluation notebook are still to be developed. No new notebook or dependency is introduced in this change.

Keep the session at 140 minutes, including a 10-minute break. It must work online or in person. Use pairs or small groups for interviews, either in breakout rooms or around tables.

The central sequence is: define success, draft criteria manually, test with people, revise, compare, then automate selected checks. LLM help with criteria is optional if students get stuck. Human feedback remains central. PromptVision supplies a short opening, not the theme of every exercise. Students test both image and text with people, then focus image revision and automated evaluation on the same images. Audio/video evaluation remains a brief discussion.

## Agreed sequence

| Block | Minutes | Facilitation focus |
| --- | ---: | --- |
| PromptVision opening | 10 | Revisit one country's story, images and a short excerpt, then reveal the prompt. Discuss identity, enjoyment and evidence; derive one possible criterion. |
| Criteria and scenarios | 15 | Test both cases, draft two observable criteria per case, choose one scenario for each, and make LLM help optional. |
| Human evaluation | 25 | Test both image and text with short interviews, recording ratings and evidence. |
| Revision and comparison | 15 | Revise the image in Replicate, compare with the same criteria and optionally revise the text. |
| Break | 10 | |
| Small automated evaluator | 30 | Run the standalone vision evaluator on original and revised PNGs, comparing model and human feedback. |
| Arena and other approaches | 15 | A/B preference versus task-specific feedback; a brief introduction to specialised decision models. |
| Project application | 15 | Students outline a small evaluation procedure for their own modality and audience. |
| Wrap-up | 5 | One evidence-based next change. |
| **Total** | **140** | |

## Criteria and human feedback

Ground the opening in the actual [PromptVision brief](../activities/promptvision.md) and [submitted entries](../results/promptvision/). Students created imaginary countries and translated a visual identity into sound. They did not previously build a formal evaluation rubric. Use their story and prompt to uncover creative intentions, then invite one possible criterion now.

[Lumora](../results/promptvision/01_Lumora/entry.txt) offers a concrete example: the story describes a mountain kingdom with musical traditions, and the prompt requests bells, flute and choir. Let students discuss what the excerpt and images communicate, using specific details as evidence. Do not assume that the generated result fulfils the prompt. There is no requirement for a particular energy progression across the track, and recognising an exact fictional story is not the test. Move from this open interpretation to the smaller image/text tasks.

Keep the scale agreed during planning: **not met / partly met / clearly met / cannot judge**. Each criterion needs task-specific anchors and an observation supporting its rating. "Cannot judge" means insufficient evidence, not failure.

Manual drafting is the default and preferred approach. Begin with the audience's task, essential information and likely confusion, then compare ideas with a partner. The worksheet's LLM prompt is optional support for students who get stuck. If used, students should examine assumptions, remove vague or irrelevant criteria, add omissions and own the final wording. Do not present an LLM-generated rubric as an objective standard. Keep criteria stable for the baseline/revision comparison; if wording changes, reassess both versions.

Interviews should elicit understanding and reasons. Let participants respond before creators defend or explain their output. Separate quotes/observations from interpretations and proposed changes. Preserve disagreements rather than forcing a single average. Discuss the limits of testing only with classmates.

The worksheet offers two cases: an illustration of repotting a plant for beginners, and visitor instructions based on a fictional plant-swap event brief. Each has two suggested scenarios. Students test both cases in Blocks 2 and 3, then focus the revision on the image. A text revision is optional. Block 7 remains the dedicated project application.

For the image interview, describe an activity guide without naming the action before the participant's first response. Ask what they see happening and what helps or confuses them. For text, ask readers to locate the practical details and identify anything they still need to know. Use a few prepared outputs; students do not need to collect a dataset of good and bad examples. Provide reference information that allows valid paraphrases. Keep viewing contexts and input briefs fixed when comparing baseline and revision within each scenario.

## Generation and revision in Blocks 2 to 4

Students use both cases in Blocks 2 and 3 with the supplied brief, original prompt, settings and actual baseline outputs. They start with one scenario per case, adding a second if time allows. Blocks 2 to 4 use Replicate's web UI and a simple document, not Jupyter. Block 4 prioritises revising the image via Nano Banana 2.1 with the original settings; revising the text via Gemini 3.5 Flash is optional. Keep the baseline and revised PNGs for Block 5.

**Preparation:** The baseline image and text outputs are not yet included, because no classroom Replicate credentials were provided. Generate authentic outputs from the worksheet prompts and record actual settings, or provide them in class. Do not present invented images or handwritten text as model outputs. Pilot the interview schedule and retain fallback saved outputs.

## Automated exercise: boundaries

The [standalone image evaluator notebook](../notebooks/05_image_evaluator.ipynb) and [text evaluator notebook](../notebooks/06_text_evaluator.ipynb) each use one `%pip install -q openai` cell, a hidden OpenRouter key input and two uploaded image filenames. The image evaluator assesses PNGs with a vision model; the text evaluator compares pasted generated instructions with an event brief. Both use OpenRouter, a small rubric and the four human rating categories. No extra image dependencies, embeddings or helper modules. Each notebook offers an optional criterion-change experiment on the same output; students must keep the original rubric fixed for baseline-versus-revision comparisons. It is designed for JupyterHub or Colab.

Use the same scenario, criteria, model and evaluator instructions for both images. Students compare the model's visible evidence with their interviews. The vision model knows the brief, so it cannot replicate an unaided interview participant's interpretation. Responses may vary; no single judgment is ground truth.

The notebooks have not been live-tested against OpenRouter because no class token is available. Before class, confirm the `google/gemini-3.5-flash` evaluator model still supports image input and test calls with real PNGs and actual generated text in Colab and JupyterHub. Prepare a clearly labelled fallback result.

Ragas, Promptfoo and ImageReward are not required installations. Keep Block 6 open for later discussion of Arena, qualitative methods, text evaluation frameworks and a short student research task.

The sample images and a combined annotated comparison are prepared separately for instructor review. Keep the annotated comparison **off** the student page so it does not prime their judgments. The optional text-example asset is already linked in Block 5; image binaries must be made available before class.

## Arena discussion

Use [Arena](https://arena.ai/leaderboard) for text and image comparisons. Discuss what an A/B preference captures, what interview comments add, and whether the tasks and participants behind a ranking match a student's own project. Avoid turning a broad leaderboard position into a guarantee of success on the class brief.

Reference: [Arena's explanation of preference-based rankings](https://help.arena.ai/articles/7011479247-how-to-see-ai-rankings-in-arena-leaderboards-2-0-wip).

## Next development steps

1. Produce genuine baseline outputs for the repotting illustration and plant swap text case, recording the prompts and model settings.
2. Test brief interviews with both cases and one image revision.
3. Test both notebooks in Colab and JupyterHub against real PNGs and text, including the optional criterion-change experiment.
4. Plan the wider evaluation-method exploration for Block 6.

Student-facing materials stay in the session page and worksheet. Sessions 1 and 2 are unchanged.
