# Session 3: Generative AI Evaluation Clinic

[Back to the course homepage](./readme.md) | [Evaluation worksheet](./activities/evaluation_clinic.md)

**Duration:** 140 minutes, including a 10-minute break.  
**Delivery:** Online or in person. The activities and learning goals are the same.  
**Tools:** Replicate's web UI for image and text generation, a simple document for human feedback, and a small prepared Jupyter Notebook introduced in Block 5 for automated feedback through OpenRouter. An LLM can offer optional help if you get stuck drafting criteria.

How can you tell whether a prompt or workflow change improved the result? We will define success, test outputs with people, make a revision, then compare human judgments with automated feedback.

The [worksheet](./activities/evaluation_clinic.md) includes both case briefs, suggested prompts and scenarios. We will use prepared baseline outputs in class. The image evaluation notebook is linked in Block 5.

## Learning goals

- Define a few observable success criteria for a specific task and audience.
- Plan two or three test scenarios with clear expected results.
- Gather useful feedback through short interviews, observations and a simple rating scale.
- Use that feedback to revise a prompt and compare the resulting outputs.
- Examine what automated feedback and model rankings can tell you, and what still needs human judgment.

## Session schedule

| Block | Activity | Minutes |
| --- | --- | ---: |
| 1 | PromptVision: preference and success | 10 |
| 2 | Define criteria and test scenarios | 15 |
| 3 | Human evaluation and short interviews | 25 |
| 4 | Revision and comparison | 15 |
| | Break | 10 |
| 5 | A tiny automated evaluator | 30 |
| 6 | Arena and other evaluation approaches | 15 |
| 7 | Apply the method to your project | 15 |
| 8 | Wrap-up | 5 |
| | **Total** | **140** |

## Block 1: PromptVision as a starting point

In PromptVision, you invented an imaginary country and gave it a story, sound and visual identity. Return to the [entries](./results/promptvision/), read one country's story, look at its source and cover images, and listen to a short excerpt. What kind of place comes across? Which details give you that impression?

Then reveal the prompt and compare your impressions with the creative intention. For example, [Lumora's story and prompt](./results/promptvision/01_Lumora/entry.txt) connect a mountain kingdom and its musical traditions with bells, flutes and choir. Do the sound and images help convey that world? Point to something you heard or saw, and explain the connection.

Discuss briefly with a partner:

- What do you enjoy about the entry?
- Which part of the country's identity comes across, and what supports your interpretation?
- What would you change to communicate that identity more clearly?

Use those answers to propose one possible criterion, such as whether the sound and images support a chosen aspect of the country's story. We are now turning a creative intention into something we can discuss and test. You do not need to guess the exact story or agree on one interpretation.

Next, use a smaller image or text task to practise defining criteria, gathering feedback and testing a revision.

## Block 2: Draft criteria and define scenarios

Work with **both** cases in the [worksheet](./activities/evaluation_clinic.md#1-describe-the-tasks): an image showing a beginner how a plant is moved into a larger pot, and short visitor instructions based on an event brief. These are small practice tasks; your ongoing project does not need to fit them. You will return to your project in Block 7.

Start with the supplied briefs, original prompts and baseline outputs. There is no generation or notebook in this block. Keep your criteria, ratings and feedback in a simple document.

For later revision, we use the same models that produced the corresponding baseline:

| Case | Model on Replicate |
| --- | --- |
| Image | [Google Nano Banana 2.1](https://replicate.com/google/nano-banana-2.1) |
| Text | [Google Gemini 3.5 Flash](https://replicate.com/google/gemini-3.5-flash) |

For **each case**, start from the audience and task. Draft two observable criteria yourself and compare them with a partner. What should somebody recognise, understand or be able to do? What essential details should be present, and what could mislead them? You can ask an LLM for suggestions if you get stuck, but it is not required.

Use the same rating scale for both cases:

| Rating | Meaning |
| --- | --- |
| Not met | The required feature is absent or the output fails this criterion. |
| Partly met | Some of the requirement is satisfied, but something important is missing or unclear. |
| Clearly met | The output satisfies the criterion, supported by an observation. |
| Cannot judge | The available output or evidence is insufficient to assess this criterion. |

Choose **one clear scenario per case** to begin with. The worksheet offers a second scenario for each if you have time. Note the situation, expected result and criteria before collecting feedback. For images, the expectation may be what someone can identify or understand. For text, it may include essential facts and what should happen when information is missing.

## Block 3: Human evaluation and interviews

Test **both the image and the text example** with a partner. Keep the interviews short and switch roles so you both experience asking questions and giving feedback.

For the image, first show it as an illustration for an activity guide, without naming the action. Ask what the person thinks is happening and which details help or confuse them. Then show the repotting instruction and ask whether the illustration supports it.

For the text, ask the person to find when and where the event takes place, what to bring and which information is missing. Ask what they would do next.

Do not explain or defend the output before the participant responds. Record a short observation or quote, then individually rate the criteria you drafted in Block 2. Compare the ratings and discuss any differences. Keep what the person actually said separate from your interpretation.

If time allows, try the second scenario for each case. These quick peer tests are useful, but classmates do not necessarily represent the intended audience.

## Block 4: Revise and compare

**Focus on the image.** Choose one issue supported by the interview feedback and revise the original image prompt to address it. Write down what you expect to improve.

In Replicate's web UI, generate a new illustration from your revised full prompt with **Nano Banana 2.1**. Keep the supplied settings and the same scenario. Generate from text again; editing the original image is outside this exercise.

Compare the baseline and revised images side by side. Ask a peer the same questions and apply the **same criteria and scale**. Record what improved, what became worse and the visible evidence. Save both PNGs and prompts: you will use these images again in Block 5.

**If you have time**, repeat the process for the text case with **Gemini 3.5 Flash**. Run the revised prompt in a fresh request using the same brief and settings.

One prompt revision is enough. If you change any criterion, reassess both outputs using its new wording. A single comparison provides useful observations, not proof that the new prompt always performs better.

## Block 5: Two tiny automated evaluators

Explore two independent notebooks, each available in JupyterHub and Google Colab:

- [Image evaluator](./notebooks/05_image_evaluator.ipynb) ([Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/session3-evaluation-skeleton/notebooks/05_image_evaluator.ipynb)): compare baseline and revised PNGs with the **same criteria**, and check model feedback against human interviews.
- [Text evaluator](./notebooks/06_text_evaluator.ipynb) ([Colab](https://colab.research.google.com/github/digitalideation/prompt_h2601/blob/session3-evaluation-skeleton/notebooks/06_text_evaluator.ipynb)): paste your generated visitor instructions, compare them with the **original event brief**, and inspect ratings and reasons.

Both use a prepared OpenRouter model call and the four-category human rating scale. **Personalise the criteria** to match your own scenarios rather than accepting them unchanged.

Each notebook ends with an **optional criterion experiment**: change one criterion and evaluate the **same output** again. Does the rating change? Keep the original criteria fixed when comparing baseline and revised generations, otherwise you may be measuring a different evaluator instead of a better result.

If time is short, complete one notebook and explore the other as an extension. Neither requires embeddings, an evaluation framework or writing API code.

## Block 6: Arena and other approaches

Explore A/B preferences and model comparisons through [Arena](https://arena.ai/leaderboard). What does a preference vote capture? What can an interview or a task-specific criterion add? How relevant is a broad ranking to your own project?

We will also briefly look at specialised decision models, with [Laya](https://github.com/NandhaKishorM/laya) and [Kev](https://github.com/jaredpalmer/kev) as examples. Consider how a focused rating or decision differs from open-ended feedback.

## Block 7: Apply the method to your project

Outline a small evaluation procedure for your own text, image, audio, video or multimodal project. Use the worksheet to identify the audience, scenarios, criteria, people to involve and a possible automated check.

Decide what evidence would make you revise the prompt or workflow. For audio and video, consider what a short excerpt can reveal and what needs longer viewing or listening.

## Block 8: Keep a useful record

Keep your scenarios, criteria, human feedback, baseline and revision, automated feedback and next decision together.

Finish with one sentence: **"Based on this evidence, the next change I would test is..."**
