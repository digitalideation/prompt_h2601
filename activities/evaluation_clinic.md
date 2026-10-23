# Evaluation Clinic: working sheet

[Session 3](../day03.md)

Use this sheet for two small, repeatable tests. In **Blocks 2 and 3**, work with both the image and text cases. Start with one scenario per case, then try the second if time allows. In **Block 4**, revise the image prompt; revising the text is optional. In **Block 5**, use the same two images in the evaluation notebook.

Use a simple document to keep your notes and ratings. Start with the supplied briefs, prompts, model settings and baseline outputs. You do not need a notebook for Blocks 2 to 4. Image generation uses [Google Nano Banana 2.1](https://replicate.com/google/nano-banana-2.1) and text generation uses [Google Gemini 3.5 Flash](https://replicate.com/google/gemini-3.5-flash), both in Replicate's web UI. Keep the model and settings the same when revising.

## 1. Describe the tasks

**Image case: an activity guide for beginners.** The brief is to illustrate moving a small plant from its current pot into a larger one. The main action and the roles of the plant, original pot and larger pot should be understandable. For the first interview, introduce it only as an illustration for an activity guide. Do not give away the action before the participant responds.

Starting image prompt for the prepared baseline:

> Create a simple instructional illustration for beginners showing a small plant being moved from its original pot into a larger pot. Keep the background uncluttered. Do not include labels or written instructions.

**Text case: visitor instructions for an event.** Use this fictional brief:

> Community plant swap. Saturday at 14:00 in Studio 2. Bring one labelled plant.

Starting text prompt for the prepared baseline:

> Write short, friendly visitor instructions based on this event brief: [paste the brief here].

Test whether readers can find the supplied information and identify anything missing. The text must not invent facts absent from the brief.

For **each case**, note the audience, what the output should help someone understand or do, and what would count as success. The baseline outputs will be provided in class. The prompts above are starting points, not additional generation tasks for Block 2.

## 2. Define your criteria

Draft two observable criteria for **each case**, then discuss them with a partner. Start with what the audience needs to understand or do. Identify what must be present and what could cause confusion.

- For the image case, possible starting points are recognising the main action and understanding the relationship between the plant and the two pots.
- For the text case, possible starting points are finding the practical information, staying faithful to the brief and making missing details clear.

Make each criterion observable. For example, replace "clear text" with "a reader can find the supplied time, location and what to bring without guessing". Choose and refine your own criteria before rating outputs.

For each criterion, describe what **not met / partly met / clearly met** would look like. Use **cannot judge** when you lack enough evidence. Record these descriptions and keep them fixed for the baseline and revision.

**Optional help if you get stuck:** replace the bracketed parts and ask an LLM:

> I am evaluating [output type] for [audience]. The task is [task], used in [situation]. Suggest three observable success criteria and two or three small test scenarios. For each criterion, describe "not met", "partly met" and "clearly met", and explain when we should use "cannot judge". Suggest a neutral interview question that could help assess it. Flag assumptions about the audience or task.

If you use these suggestions, check their assumptions and revise them yourself. Keep only criteria that matter to the audience and can be assessed with the evidence available. Using an LLM is not required.

## 3. Define the scenarios

A scenario is a specific situation in which you test the output. Start with **one scenario for the image and one for the text**. Use the second scenario for either case if time allows:

| Case | Scenario and input | Expected result |
| --- | --- | --- |
| Image | A beginner sees the illustration on its own in an activity guide. | They can describe the main action and identify the objects involved without being told the answer. |
| Image | A beginner sees the illustration alongside the instruction "Move the plant into a larger pot." | The image helps them understand the instruction; the plant, old pot and new pot have clear roles. |
| Text | The event brief includes the supplied time, location and what to bring. | The visitor instructions preserve those details and make them easy to find. Different wording is fine. |
| Text | Remove the time or location from the brief before generating instructions. | The output makes the missing detail clear instead of inventing it. The reader knows what they still need to find out. |

The image scenarios test different viewing contexts. Keep the viewing context the same when comparing original and revised images. For text, keep each scenario's brief the same across comparisons.

Complete one row for each scenario you test, including the criteria you chose.

| Scenario and input | Expected result or essential information | Criteria to check |
| --- | --- | --- |
| | | |

## 4. Test with a person

In pairs, test both the **image and text outputs**. Let the participant respond before explaining your own interpretation. For the image, do not name the action initially. Ask questions such as:

- What do you understand from this?
- What did you notice first?
- What is unclear or missing?
- What would you do next, based on this output?
- What makes you say that?

Record what you observed, then rate each criterion. Use **not met / partly met / clearly met / cannot judge**. Keep individual ratings and reasons when people disagree.

| Scenario / output / participant label | Criterion | Rating | Observation or short quote |
| --- | --- | --- | --- |
| | | | |

## 5. Turn feedback into a revision

Start with the **image case**. Choose one issue supported by the interview and record what you want to change:

| Observation or quote | Your interpretation | Prompt or workflow change to test |
| --- | --- | --- |
| | | |

Revise the original full image prompt and generate again through Nano Banana 2.1 on Replicate. Keep the same model, settings and scenario. Use text-to-image generation, not image editing. Save the baseline and revised PNGs and the full prompts.

Compare the images side by side, ask the same interview questions and apply the same criteria. Note any new problems. You will use **both PNGs** in the evaluation notebook.

**Optional if there is time:** revise the text prompt, generate with Gemini 3.5 Flash in a fresh run using the same brief and settings, and compare the results. If you change a criterion, reassess both outputs using the new version.

| Scenario / criterion | Baseline rating | Revised rating | What changed, and what evidence supports your judgment? |
| --- | --- | --- | --- |
| | | | |

## 6. Compare human and automated feedback

Open the [simple image evaluator notebook](../notebooks/05_image_evaluator.ipynb) in JupyterHub or [Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/session3-evaluation-skeleton/notebooks/05_image_evaluator.ipynb). Upload both PNGs and use **the same criteria** you used with people. The prepared cells request feedback from a vision model through OpenRouter.

Compare each model rating and explanation with your own evidence. Does it refer to something visible? Does it miss a problem a participant noticed? The model can describe what it sees, but it cannot replace an interview about what a person understood.

| Image / scenario / criterion | Human rating and reason | Model rating and reason | Agreement or difference to investigate |
| --- | --- | --- | --- |
| | | | |

Keep the same evaluator model and instructions for baseline and revision. You do not need to combine everything into one overall score.

## 7. Decide what to do next

- What improved, and what evidence supports that judgment?
- What remains uncertain or disputed?
- Which people or scenarios are still missing from the test?
- What is the next change you would test?
