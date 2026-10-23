# Evaluation Clinic: working sheet

[Session 3](../day03.md)

Use this sheet for a small, repeatable evaluation. Choose one case below and keep it through the criteria, interview and revision exercises. You can use a small part of your own project if it fits; otherwise, apply the method to your project in Block 7. Keep your record in a simple document for Blocks 2 to 4. The prepared notebook comes in Block 5.

Start with the supplied brief, original prompt, settings and baseline outputs. Stick with [Google Nano Banana 2.1](https://replicate.com/google/nano-banana-2.1) for images and [Google Gemini 3.5 Flash](https://replicate.com/google/gemini-3.5-flash) for text. Use Replicate's web UI when you generate the revision, keeping the same model and settings as the baseline.

## 1. Describe the task

**Image case: an activity guide for beginners.** The brief is to illustrate moving a small plant from its current pot into a larger one. The main action and the relationship between the plant and the two pots should be understandable. Test what a viewer recognises and which details help or confuse them. Before their first response, describe it only as an image for an activity guide so you do not give away the action.

**Text case: visitor instructions for an event.** Turn a short event brief into clear instructions for someone attending for the first time. Use this fictional brief: "Community plant swap. Saturday at 14:00 in Studio 2. Bring one labelled plant." Test whether readers can find the practical information and notice what is missing. The text should not invent details absent from the brief.

For your chosen case, answer:

- What should the output help someone understand, experience or do?
- Who is it for?
- What situation will you test?
- What would count as success in that situation?

## 2. Define your criteria

Draft two or three criteria yourself, then discuss them with a partner. Start with what the audience needs to understand or do. Identify what must be present and what could cause confusion.

- For the image case, possible starting points are recognising the main action and understanding the relationship between the plant and the two pots.
- For the text case, possible starting points are finding the practical information, staying faithful to the brief and making missing details clear.

Make each criterion observable. For example, replace "clear text" with "a reader can find the supplied time, location and what to bring without guessing". Choose and refine your own criteria before rating outputs.

For each criterion, describe what **not met / partly met / clearly met** would look like. Use **cannot judge** when you lack enough evidence. Record these descriptions and keep them fixed for the baseline and revision.

**Optional help if you get stuck:** replace the bracketed parts and ask an LLM:

> I am evaluating [output type] for [audience]. The task is [task], used in [situation]. Suggest three observable success criteria and two or three small test scenarios. For each criterion, describe "not met", "partly met" and "clearly met", and explain when we should use "cannot judge". Suggest a neutral interview question that could help assess it. Flag assumptions about the audience or task.

If you use these suggestions, check their assumptions and revise them yourself. Keep only criteria that matter to the audience and can be assessed with the evidence available. Using an LLM is not required.

## 3. Define the scenarios

A scenario is a specific situation in which you test the output. Start with the two scenarios for your chosen case, or adapt them to your task:

| Case | Scenario and input | Expected result |
| --- | --- | --- |
| Image | A beginner sees the illustration on its own in an activity guide. | They can describe the main action and identify the objects involved without being told the answer. |
| Image | A beginner sees the illustration alongside the instruction "Move the plant into a larger pot." | The image helps them understand the instruction; the plant, old pot and new pot have clear roles. |
| Text | The event brief includes the supplied time, location and what to bring. | The visitor instructions preserve those details and make them easy to find. Different wording is fine. |
| Text | Remove the time or location from the brief before generating instructions. | The output makes the missing detail clear instead of inventing it. The reader knows what they still need to find out. |

The image scenarios test different viewing contexts. Keep each context the same when comparing the original and revised image. For text, keep each scenario's brief the same across the comparison.

Complete one row per scenario, including the criteria you chose. Two or three are enough for this exercise.

| Scenario and input | Expected result or essential information | Criteria to check |
| --- | --- | --- |
| | | |

## 4. Test with a person

Give the task context and let the participant examine the output before explaining your own interpretation. Ask questions such as:

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

Choose one issue supported by the interview. Record the change you want to test:

| Observation or quote | Your interpretation | Prompt or workflow change to test |
| --- | --- | --- |
| | | |

Revise the original full prompt, then generate again in Replicate's web UI using the same model, settings and scenario inputs. One prompt revision is enough. For images, generate from text again. For text, start a fresh run for each scenario. Save the full prompts and both versions of each output.

Compare the original and revised outputs side by side. Ask a peer the same interview questions and apply the same criteria. Keep the original output and note anything that became worse. If you revise the criteria themselves, use the new version to reassess both outputs.

| Scenario / criterion | Baseline rating | Revised rating | What changed, and what evidence supports your judgment? |
| --- | --- | --- | --- |
| | | | |

## 6. Compare human and automated feedback

For the automated exercise, supply the same task, criteria and reference information used in the human evaluation. Ask for a rating, a brief explanation and any limits on what can be judged. Verify the explanation against the output.

| Scenario / version / criterion | Human rating and reason | Model rating and reason | Agreement or difference to investigate |
| --- | --- | --- | --- |
| | | | |

Keep the model and evaluation instructions the same when comparing baseline and revision. Record them so you know how the feedback was produced. You do not need to combine everything into one overall score.

## 7. Decide what to do next

- What improved, and what evidence supports that judgment?
- What remains uncertain or disputed?
- Which people or scenarios are still missing from the test?
- What is the next change you would test?
