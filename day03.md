# Session 3: Generative AI Evaluation Clinic

[Back to the course homepage](./readme.md) | [Evaluation worksheet](./activities/evaluation_clinic.md)

**Duration:** 140 minutes, including a 10-minute break.  
**Delivery:** Online or in person. The activities and learning goals are the same.  
**Tools:** Human feedback and a small prepared Jupyter Notebook for automated feedback through OpenRouter. An LLM can offer optional help if you get stuck drafting criteria. Replicate remains available for generation.

How can you tell whether a prompt or workflow change improved the result? We will define success, test outputs with people, make a revision, then compare human judgments with automated feedback.

This is the session outline. The worksheet includes image and text cases; sample outputs and the evaluation notebook will be added here.

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

Choose one of the two cases in the [worksheet](./activities/evaluation_clinic.md#1-describe-the-task): an image showing a beginner how a plant is moved into a larger pot, or short visitor instructions written from an event brief. You can use a small part of your own project if it fits the exercise. Otherwise, use a supplied case and return to your project in Block 7.

Start with the task, audience and situation. Draft two or three criteria yourself, then discuss them with a partner. What should someone understand or be able to do? What must be present? What would make the output misleading or confusing?

Keep criteria you can actually observe and explain why they matter. A phrase such as "high quality" needs a more precise description. If you get stuck, the worksheet includes an optional LLM prompt; review any suggestions before using them.

Use the same scale for each criterion, with descriptions specific to your task:

| Rating | Meaning |
| --- | --- |
| Not met | The required feature is absent or the output fails this criterion. |
| Partly met | Some of the requirement is satisfied, but something important is missing or unclear. |
| Clearly met | The output satisfies the criterion, supported by an observation. |
| Cannot judge | The available output or evidence is insufficient to assess this criterion. |

Choose two or three scenarios. For each, record the input, expected result and criteria you will check. For text, a reference answer can identify essential information while allowing different wording. For images, the expected result might describe what a viewer should recognise or understand.

## Block 3: Human evaluation and interviews

Continue with your chosen case in pairs or small groups. Give a participant the task context and output, then let them respond before explaining your own intentions.

For the image case, ask what is happening and which visual details help or confuse them. For the text case, ask them to find when and where to attend and what to bring, and to identify anything they still need to know. Keep the same case through the revision in Block 4.

Ask a few neutral questions. What do they understand? What is confusing? What would they do next? Record short quotes or observations.

Rate the agreed criteria individually before comparing judgments. Add a reason for each rating. Discuss disagreements and distinguish what someone said from your interpretation of it. A peer test is a useful first check; consider who your actual audience would be.

## Block 4: Revise and compare

Choose one issue supported by feedback. Write a prompt revision that addresses it and explain what you expect to improve. Compare a revised output with the baseline, using the same scenarios and criteria.

Keep both versions and check for new problems as well as improvements. If you change a criterion, reassess both outputs with its new wording. A small comparison helps you choose a next step; it does not establish that the revision will always work.

## Block 5: A tiny automated evaluator

Use a prepared text example to explore a small evaluation workflow in Jupyter. Supply the scenario, output, criteria and reference information where relevant, then obtain model feedback through OpenRouter.

First read the comments. Then request a rating and brief explanation for each criterion using the same scale as the human exercise. Compare the feedback with your own observations, check its evidence and record disagreements.

Repeat the check on a revised output while keeping the evaluation instructions fixed. For a short image example, we can assess the image directly with a suitable model or work from a description. A description limits the evaluation to the information it contains.

The aim is to understand a repeatable process. Direct work with embeddings or a large evaluation framework is not required.

## Block 6: Arena and other approaches

Explore A/B preferences and model comparisons through [Arena](https://arena.ai/leaderboard). What does a preference vote capture? What can an interview or a task-specific criterion add? How relevant is a broad ranking to your own project?

We will also briefly look at specialised decision models, with [Laya](https://github.com/NandhaKishorM/laya) and [Kev](https://github.com/jaredpalmer/kev) as examples. Consider how a focused rating or decision differs from open-ended feedback.

## Block 7: Apply the method to your project

Outline a small evaluation procedure for your own text, image, audio, video or multimodal project. Use the worksheet to identify the audience, scenarios, criteria, people to involve and a possible automated check.

Decide what evidence would make you revise the prompt or workflow. For audio and video, consider what a short excerpt can reveal and what needs longer viewing or listening.

## Block 8: Keep a useful record

Keep your scenarios, criteria, human feedback, baseline and revision, automated feedback and next decision together.

Finish with one sentence: **"Based on this evidence, the next change I would test is..."**
