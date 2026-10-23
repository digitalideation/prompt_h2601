# Evaluation Clinic: working sheet

[Session 3](../day03.md)

Use this sheet for a small, repeatable evaluation. Start with the supplied examples, then adapt it to your own project. You can keep the record in a notebook or a simple document.

## 1. Describe the task

- What should the output help someone understand, experience or do?
- Who is it for?
- What situation will you test?
- What would count as success in that situation?

## 2. Use an LLM to help draft criteria

Replace the bracketed parts and try this prompt:

> I am evaluating [output type] for [audience]. The task is [task], used in [situation]. Suggest three observable success criteria and two or three small test scenarios. For each criterion, describe "not met", "partly met" and "clearly met", and explain when we should use "cannot judge". Suggest a neutral interview question that could help assess it. Flag assumptions about the audience or task.

Select and revise the suggestions. Check that each criterion matters to the intended audience and can be assessed with the evidence available. Add anything the model missed. You are responsible for the final criteria.

Record your agreed criteria and the meaning of each rating before comparing outputs. Keep this version for the baseline and revision.

## 3. Define the scenarios

Complete one row per scenario. Two or three are enough for this exercise.

| Scenario and input | Expected result or essential information | Criteria to check |
| --- | --- | --- |
| | | |

A scenario describes a situation to test. For example, a text task might need to work when a key detail is missing; an image task might need to communicate its main action to someone unfamiliar with the subject. Choose situations relevant to your brief.

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

| Observation or quote | Your interpretation | Prompt or workflow change to test |
| --- | --- | --- |
| | | |

Keep the original output. Compare the revision using the same scenarios and criteria, and note anything that became worse. If you revise the criteria themselves, use the new version to reassess both outputs.

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
