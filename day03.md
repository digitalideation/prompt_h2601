# Session 3: Generative AI Evaluation Clinic

[Back to the course homepage](./readme.md) | [Evaluation worksheet](./activities/evaluation_clinic.md)

**Duration:** 140 minutes, including a 10-minute break.  
**Delivery:** Online or in person. The activities and learning goals are the same.  
**Tools:** Human feedback, an LLM for drafting criteria, and a small prepared Jupyter Notebook for automated feedback through OpenRouter. Replicate remains available for generation.

How can you tell whether a prompt or workflow change improved the result? We will define success, test outputs with people, make a revision, then compare human judgments with automated feedback.

This is the session outline. Worked examples and the evaluation notebook will be added here.

## Learning goals

- Define a few observable success criteria for a specific task and audience, using an LLM to help draft them.
- Plan two or three test scenarios with clear expected results.
- Gather useful feedback through short interviews, observations and a simple rating scale.
- Use that feedback to revise a prompt and compare the resulting outputs.
- Examine what automated feedback and model rankings can tell you, and what still needs human judgment.

## Session schedule

| Block | Activity | Minutes |
| --- | --- | ---: |
| 1 | PromptVision: preference and success | 10 |
| 2 | Draft criteria with an LLM and define scenarios | 15 |
| 3 | Human evaluation and short interviews | 25 |
| 4 | Revision and comparison | 15 |
| | Break | 10 |
| 5 | A tiny automated evaluator | 30 |
| 6 | Arena and other evaluation approaches | 15 |
| 7 | Apply the method to your project | 15 |
| 8 | Wrap-up | 5 |
| | **Total** | **140** |

## Block 1: PromptVision as a starting point

Return briefly to the [PromptVision entries](./results/promptvision/). Listen to a short excerpt and ask: do you enjoy it, and does it fulfil its intended brief?

Those questions can lead to different answers. Mood, musical structure, lyrics and personal taste may all influence your judgment. Use the discussion to identify possible criteria, then move to more manageable image and text examples for the practical exercises.

## Block 2: Draft criteria and define scenarios

Start with a task, an intended audience and the situation in which the output will be used. Ask an LLM to propose a few success criteria and possible test situations. The [worksheet](./activities/evaluation_clinic.md) includes a starting prompt.

Review the suggestions yourself. Keep two or three criteria you can actually observe, explain why they matter and rewrite anything vague. A phrase such as "high quality" needs a more precise description.

Use the same scale for each criterion, with descriptions specific to your task:

| Rating | Meaning |
| --- | --- |
| Not met | The required feature is absent or the output fails this criterion. |
| Partly met | Some of the requirement is satisfied, but something important is missing or unclear. |
| Clearly met | The output satisfies the criterion, supported by an observation. |
| Cannot judge | The available output or evidence is insufficient to assess this criterion. |

Choose two or three scenarios. For each, record the input, expected result and criteria you will check. For text, a reference answer can identify essential information while allowing different wording. For images, the expected result might describe what a viewer should recognise or understand.

## Block 3: Human evaluation and interviews

Work in pairs or small groups with image and text examples. Give a participant the task context and output, then let them respond before explaining your own intentions.

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
