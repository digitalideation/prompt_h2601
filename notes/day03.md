# Session 3: Evaluation Clinic teaching notes

Student pages: [Session 3](../day03.md) and [working sheet](../activities/evaluation_clinic.md).

## Status and scope

This is the agreed teaching skeleton. The worked image example, text exercise, reference answers and evaluation notebook are still to be developed. No new notebook, dependency or model selection is introduced in this change.

Keep the session at 140 minutes, including a 10-minute break. It must work online or in person. Use pairs or small groups for interviews, either in breakout rooms or around tables.

The central sequence is: define success, draft criteria with an LLM, test with people, revise, compare, then automate selected checks. Human feedback remains central. PromptVision supplies a short opening, not the theme of every exercise. Practical work moves to images and text; text is the main automated exercise. Audio/video evaluation remains a brief discussion.

## Agreed sequence

| Block | Minutes | Facilitation focus |
| --- | ---: | --- |
| PromptVision opening | 10 | One short excerpt; distinguish enjoyment from fulfilment of a brief. Avoid detailed musical analysis or another competition. |
| Criteria and scenarios | 15 | Let students ask an LLM for candidate criteria and test situations, then critique and select two or three. Define the rating anchors. |
| Human evaluation | 25 | Short interviews and observations with manageable image/text examples. Collect individual ratings and reasons before discussion. |
| Revision and comparison | 15 | Translate feedback into one change; compare using the same scenarios and criteria. |
| Break | 10 | |
| Small automated evaluator | 30 | Obtain model feedback on text through OpenRouter, structure it with the same scale, and compare with human judgments. Include a short image demonstration only if it fits. |
| Arena and other approaches | 15 | A/B preference versus task-specific feedback; a brief introduction to specialised decision models. |
| Project application | 15 | Students outline a small evaluation procedure for their own modality and audience. |
| Wrap-up | 5 | One evidence-based next change. |
| **Total** | **140** | |

## Criteria and human feedback

Keep the scale agreed during planning: **not met / partly met / clearly met / cannot judge**. Each criterion needs task-specific anchors and an observation supporting its rating. "Cannot judge" means insufficient evidence, not failure.

LLM assistance is part of criterion discovery. Students should examine assumptions, remove vague or irrelevant criteria, add omissions and own the final wording. Do not present an LLM-generated rubric as an objective standard. Keep criteria stable for the baseline/revision comparison; if wording changes, reassess both versions.

Interviews should elicit understanding and reasons. Let participants respond before creators defend or explain their output. Separate quotes/observations from interpretations and proposed changes. Preserve disagreements rather than forcing a single average. Discuss the limits of testing only with classmates.

Use a few supplied scenarios and outputs. Students do not need to collect a large dataset of good and bad examples. Provide reference information that allows valid paraphrases in the text task.

## Automated exercise: boundaries

The class has OpenRouter tokens in addition to Replicate access. Use OpenRouter as the planned route to a feedback model. Choose the model and minimum notebook setup after the exercise is concrete.

The intended notebook should make the process visible: task/scenario, output, criteria, optional reference, model comments, then structured ratings with short explanations. Compare with human feedback and repeat on a revision. Record the evaluator model and instructions, and hold them fixed across the comparison.

Keep dependencies and code small, using the JupyterHub/Colab approach students know. Avoid a required local model installation, custom helper system or new interface. Do not implement the notebook during this skeleton stage.

Embeddings are optional. An image demonstration may use direct image input or an image description. Explain that a description-based evaluator cannot assess omitted visual details, and that a model's feedback needs checking against human observations.

Ragas and Promptfoo are set aside. There is no committed ImageReward exercise. [Laya](https://github.com/NandhaKishorM/laya) and [Kev](https://github.com/jaredpalmer/kev) are brief decision-model references, not required practical tools.

## Arena discussion

Use [Arena](https://arena.ai/leaderboard) for text and image comparisons. Discuss what an A/B preference captures, what interview comments add, and whether the tasks and participants behind a ranking match a student's own project. Avoid turning a broad leaderboard position into a guarantee of success on the class brief.

Reference: [Arena's explanation of preference-based rankings](https://help.arena.ai/articles/7011479247-how-to-see-ai-rankings-in-arena-leaderboards-2-0-wip).

## Next development steps

1. Select one short PromptVision excerpt, one image brief and one text task. Keep the practical exercises independent of music analysis.
2. Prepare a small set of scenarios, baseline/revised outputs and essential reference information for text.
3. Work through the criteria-drafting prompt and check that a short interview can produce useful evidence.
4. Build one small evaluation notebook with an OpenRouter call and a readable comparison table. Include prepared results if API access fails.
5. Pilot the flow, including model feedback that misses something or disagrees with a person. Check time, access and generation cost.
6. Choose the brief Arena and decision-model demonstration. Keep further technical detail optional.

Student-facing material belongs in the session page and activity sheet. Preparation, technical decisions and unresolved details stay here. Sessions 1 and 2, and Week 12, are outside this change.
