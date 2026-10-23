# Prompt Engineering (PROMPT H26)

Practical prompting for images, video, music, sound, and text, with an emphasis on creative experimentation, documented workflows, and critical reflection.

![Abstract creative workflows across image, sound and evaluation](./assets/landing.svg)

## Overview

These pages cover GM's three sessions. We move from visual generation to multimodal creation, then evaluate whether changes to prompts and workflows improve the results.

Each session lasts **2 h 20 min (140 minutes), including a 10-minute break**. All sessions can run **online or in person**, with the same activities and learning goals. The delivery format will be confirmed before each session.

## Sessions

| Session | Topic | Main activity | Materials |
| --- | --- | --- | --- |
| 1 | Image & Video Prompting and Workflow Design | Artistic Telephone, storyboard, and visual refinement | [Session materials](./day01.md) |
| 2 | Prompting for Audio, Music & Multimodal Workflows | PromptVision: visual-to-audio country competition | [Session materials](./day02.md) |
| 3 | Generative AI Evaluation Clinic | Criteria, human feedback, revision and simple automated evaluation | [Session outline](./day03.md) |

### [Session 1: Image & Video Prompting and Workflow Design](./day01.md)

- Prompt structure and techniques for image and video generation
- Storyboarding, scene descriptions, and visual consistency
- Designing and iterating multi-step image/video workflows

Start with Replicate's web UI, then use a prepared Jupyter Notebook to record prompts, generate images, and compare iterations. Artistic Telephone makes interpretation drift visible; a storyboard and refinement task introduce deliberate consistency. We will also explore how to turn a still image into a short video. You can try this as an optional extension.

[Open Session 1](./day01.md), then start with the [Replicate basics notebook](./notebooks/01_replicate_basics.ipynb). For a structured version of the same API exercise, use [Replicate scene prompts](./notebooks/02_replicate_scene_prompts.ipynb). The [Artistic Telephone notebook](./notebooks/03_artistic_telephone.ipynb) adds iteration, comparison and selected-image passing. At the end of the game, we will compare the image chains and reveal their prompts. See the [game guide](./activities/artistic_telephone.md) and [Jupyter setup instructions](./notebooks/README.md).

### [Session 2: Prompting for Audio, Music & Multimodal Workflows](./day02.md)

- Prompting for music and sound: genre, mood, tempo, voice, and other characteristics
- Combining text, image, audio, and video in multimodal workflows
- Choosing and iterating with the right media and tools for a project

In [PromptVision](./day02.md), teams of 2–3 translate a source image into a sonic identity for an imaginary digital country, generate a new cover image and enter a Eurovision-style listening show. We use browser tools, a minimal automatic local presentation and ScoreWiz voting; no student notebook is required. See the [activity guide](./activities/promptvision.md).

### [Session 3: Generative AI Evaluation Clinic](./day03.md)

- Defining task-specific criteria and scenarios, with optional LLM support
- Human evaluation through interviews, observations and a concrete rating scale
- Comparing revisions and simple automated feedback across generative workflows

Start by revisiting the imaginary countries from PromptVision, then test both an image and text case with people. Draft criteria yourself, with optional LLM help if needed, revise the image prompt from the feedback, and compare human judgments with a vision-model evaluator through OpenRouter. Arena and specialised decision models introduce other evaluation approaches. The [session outline](./day03.md) and [working sheet](./activities/evaluation_clinic.md) include the case briefs and scenarios; the [small image evaluation notebook](./notebooks/05_image_evaluator.ipynb) is now available; baseline outputs will be provided in class.

For the revision exercise, prioritise [Google Nano Banana 2.1](https://replicate.com/google/nano-banana-2.1) for images. Text revision with [Google Gemini 3.5 Flash](https://replicate.com/google/gemini-3.5-flash) is optional. Keep the model and supplied settings the same as the baseline. Blocks 2 to 4 use a simple document; the prepared notebook begins in Block 5.

## Competencies

**Professional**

- Design effective prompts for diverse AI tools and contexts.
- Adapt prompts to different models and use cases.
- Understand the limits and appropriate use of generative systems.
- Recognize privacy, security, and intellectual-property risks when using AI.

**Methodological**

- Test, compare, and refine prompts systematically.
- Document the inputs, outputs, and decisions in a creative workflow.
- Choose evaluation criteria appropriate to the medium and task.

**Personal**

- Engage critically and creatively with AI tools.
- Communicate transparently about AI-assisted work.
- Reflect on ethical and societal implications.

## Working tools

- **Replicate:** use the [web UI](https://replicate.com) and prepared API calls with your individual account.
- **Jupyter Notebook:** keep prompt versions, generated media, observations, and evaluation results together. Session 1 includes [the basics notebook, a scene-prompt version and Artistic Telephone](./notebooks/README.md); you edit prompts and run supplied cells. Session 2 uses browser audio tools and a small local instructor presentation generator; no new student notebook is required.
- **OpenRouter:** use the class API access for optional criteria-drafting help and the Session 3 vision evaluation notebook.
- **Model selection:** use the model list provided for each activity.
- **SWITCHdrive:** share media within groups and submit work through the class folders. Folder links will be supplied in class.

Keep API tokens private and out of notebooks, screenshots, and submissions.

## Ethics & Reflection

Topics across the sessions include copyright and dataset provenance; bias and representation; disclosure of AI-assisted work; and authorship and responsibility when combining generated media.
