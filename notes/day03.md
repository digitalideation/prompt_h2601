# Session 3: Evaluation Clinic teaching notes

Student pages: [Session 3](../day03.md) and [working sheet](../activities/evaluation_clinic.md).

## Status and scope

The worksheet includes image and text cases and the session has two standalone evaluation notebooks. Examples and worked ratings should be checked by the instructor before class. Block 6 is a short research activity, with no additional notebook or dependency.

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
| Automated evaluators | 30 | Explore the standalone image and text notebooks; personalise criteria and compare model judgments with human evidence. |
| Exploring evaluation methods | 15 | Arena preference example (3 min), paired research into an approach (8 min), short sharing (4 min). |
| Project application | 15 | Choose one task and audience (2 min), draft criteria/scenarios/human and optional automated checks (8 min), peer review (3 min), define next test (2 min). |
| Wrap-up | 5 | One supported finding from today's exercise (2 min) and a two-sentence exit ticket with a next project test (3 min). |
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

**Preparation:** The repository includes a baseline and revised PNG pair and a text example as optional **testing materials**. These are prepared teaching samples, not authenticated output from the specified Replicate generation models or a controlled revision. For Blocks 2 to 4, prepare or identify the actual baseline outputs you intend students to evaluate and record their model settings. Do not label the sample images or manually prepared text as verified model outputs. Pilot the interviews and keep fallback files available.

## Automated exercise: boundaries

The [standalone image evaluator notebook](../notebooks/05_image_evaluator.ipynb) and [text evaluator notebook](../notebooks/06_text_evaluator.ipynb) each use one `%pip install -q openai` cell and a hidden OpenRouter key input. The image notebook uses two uploaded image filenames, while the text notebook uses pasted text and a reference brief. The image evaluator assesses PNGs with a vision model; the text evaluator compares pasted generated instructions with an event brief. Both use OpenRouter, a small rubric and the four human rating categories. No extra image dependencies, embeddings or helper modules. Each notebook offers an optional criterion-change experiment on the same output; students must keep the original rubric fixed for baseline-versus-revision comparisons. It is designed for JupyterHub or Colab.

Use the same scenario, criteria, model and evaluator instructions for both images. Students compare the model's visible evidence with their interviews. The vision model knows the brief, so it cannot replicate an unaided interview participant's interpretation. Responses may vary; no single judgment is ground truth.

The notebooks have not been live-tested against OpenRouter because no class token is available. Before class, confirm the `google/gemini-3.5-flash` evaluator model still supports image input and test calls with real PNGs and actual generated text in Colab and JupyterHub. Prepare a clearly labelled fallback result.

Ragas, Promptfoo and ImageReward are not required installations. Block 6 introduces evaluation approaches through short paired research, not hands-on framework setup.

The sample images are available as [baseline](../assets/evaluation-clinic/baseline.png) and [revised](../assets/evaluation-clinic/revised.png), with [sample text](../assets/evaluation-clinic/text-evaluator-examples.txt) for testing. The [annotated comparison](../assets/evaluation-clinic/instructor-comparison-draft.png) is for instructor review only; do **not** display it on the student page, where it could prime judgments.

## Block 6: Exploring evaluation methods

Keep the 15 minutes structured and light:

- **3 min, Arena:** show the [leaderboard](https://arena.ai/leaderboard) and explain that many rankings come from blind human head-to-head preference votes. Contrast "I like this output" with "this output meets the task requirements." The meaning of ratings and leaderboard uncertainty can be mentioned briefly, not taught as statistics.
- **8 min, pair research:** students choose one approach from the session page, read a short explanation or worked example, and record three findings in the worksheet: what it measures/needs, a limitation, and one possible use. No installation, registration or live framework demo. They may ask an LLM for an overview but should check it against the referenced documentation.
- **4 min, sharing:** invite two or three brief reports, preferably covering different approaches, then connect to Block 7. Students may investigate a different technique appropriate for text, images, music, audio, video or multimodal workflows.

Suggested starting points: [Arena](https://arena.ai/leaderboard) for human pairwise preferences; [Promptfoo](https://www.promptfoo.dev/docs/intro/) for prompt/model comparisons across repeatable test cases and assertions; [Ragas](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) for faithfulness, context relevance and other text/RAG metrics. These are **research options**, not required student tools. Optional further examples are [Laya](https://github.com/NandhaKishorM/laya) and [Kev](https://github.com/jaredpalmer/kev), but there is no need to cover them during the 15-minute activity.

Avoid implying that the highest-ranked model is always best for a specific project or that any single automated metric captures the whole user experience. End by asking how each student could select an appropriate method for their own project in Block 7.

## Blocks 7 and 8: Transfer and wrap-up

**Block 7, 15 min:** No notebook, generation or new testing. Students choose one small project task and intended audience (2 min), write two observable criteria and two scenarios including a realistic failure case (8 min), swap plans for a quick peer check (3 min), and name a first test to run later (2 min). Their plan should include a human participant/task and one automated or alternative check **only where useful**, plus limitations. Accept a provisional project idea if they have not decided on a final project. For audio or video, match the length of the sample to the criterion being evaluated.

**Block 8, 5 min:** Ask students to distinguish something they actually observed today from something they only plan to test (2 min). Then have them complete the worksheet's two-sentence exit ticket (3 min): evidence from today's tests, followed by a concrete next project test. Their project evaluation is a proposed method, not an implemented or validated experiment. Keep the worksheet and working files together; do not require a polished submission.

## Before class: final checks

1. Confirm genuine, labelled baseline outputs and actual model settings for the two human-evaluation cases, distinct from the supplied practice samples.
2. Pilot both notebooks in Colab and JupyterHub with the classroom OpenRouter token and real files. Verify the model accepts vision input, the requests complete, and the optional criterion experiment restores the original baseline rubric.
3. Rehearse the short peer interviews and prepare a fallback set of outputs for API delays.
4. Verify the Arena, Promptfoo and Ragas starting links and prepare a very brief Arena preference illustration.

Session 3 stays at 140 minutes including the break. Sessions 1 and 2, and Week 12, are unchanged.
