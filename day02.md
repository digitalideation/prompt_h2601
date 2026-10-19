# Session 2: Prompting for Audio, Music & Multimodal Workflows

[Back to the course homepage](./readme.md)

![Abstract rhythm and sound for Session 2](./assets/session02.svg)

**Duration:** 140 minutes including a 10-minute break. **Teams:** 2–3 students (roughly 10–15 countries). **Tools:** browser audio and image generators, SWITCHdrive, [ScoreWiz](https://scorewiz.eu).

## PromptVision 2026: A Country You Can Hear

Invent an imaginary digital country and create its sonic identity from **one source image**: an Artistic Telephone image, a different image you made, or one provided in class. Multiple teams may start from the same image. Identify three visual qualities and translate them into musical decisions. Go beyond narrating the pictured objects.

Create one original AI-generated composition **between 1 and 2 minutes long**. If your chosen model creates a longer song, export or trim a 60–120-second excerpt for the competition. Songs, instrumentals, ambient music and experimental soundscapes are all welcome. Compare at least two prompt directions or iterations where feasible, then generate **one new cover image** that represents the *resulting sound*, not necessarily the original subject.

At the listening party we see your cover prominently, with the source image beside it. We listen to all entries first, then each team votes as one national jury for other countries using Eurovision-style points in ScoreWiz. We reveal prompts after the voting.

## Learning goals

- Translate three visual qualities into deliberate sonic choices.
- Prompt for mood, genre, rhythm, instrumentation and development over time.
- Compare alternatives and explain a purposeful revision.
- Distinguish listening enjoyment from success at communicating the intended visual-to-audio identity.

## Session schedule

| Activity | Minutes |
| --- | ---: |
| Visual-to-audio introduction | 10 |
| Audio models and prompt demonstration | 15 |
| Mini experiment: vary one parameter | 10 |
| Break | 10 |
| Form teams, choose country and source image | 10 |
| Generate audio, compare and create cover | 30 |
| Submit and check playback | 10 |
| Listening party | 20 |
| ScoreWiz voting and results | 20 |
| Reflection | 5 |
| **Total** | **140** |

## Block 1: From image to sound (10 minutes)

### How can an image become audible?

In Session 1, we used words to create images and watched ideas change as they passed between people. This time, we start with a picture and try to express its atmosphere **through sound rather than describing the objects in it**.

Imagine a photograph of a cyclist crossing a foggy bridge at dawn. We could describe the bicycle literally, but we could also translate what the scene *feels* like:

| Visual quality | Possible musical decision |
| --- | --- |
| Fog obscures the distance | Soft, layered synthesizers with blurred edges |
| The cyclist moves steadily | A quiet, repeating rhythmic pulse |
| Warm dawn light emerges | A bright melody gradually appears |

These are interpretations, not fixed rules. Another team could choose very different sounds for the same image. What musical choices would make your own version recognizable?

### How do audio generators work?

Different systems turn a written description into musical or sound structures, then render an audio waveform. Some generate music with rhythm and harmony; others specialize in sound effects or textures. Unlike a still image, **sound unfolds over time**, so a prompt can describe an opening, a change, and an ending.

Think of a simple workflow: **image → interpretation → audio prompt → generated sound → listening and revision**.

**Further reading:** [How AI Generates Music (2026): A One-Page Technical Overview](./notes/annex-ai-music-generation.md)

## Block 2: Audio models and prompt craft (15 minutes)

### Choose the right kind of generation

We will look at examples of three related approaches:

| Approach | Typical use | What to listen for |
| --- | --- | --- |
| Text-to-music | Songs, instrumentals, musical themes | Rhythm, instruments, melody, structure, vocals |
| Text-to-sound | Atmospheres, ambiences, effects, textures | Timbre, space, realism, layers, movement |
| Audio-to-audio | Transforming or extending an existing recording | What is preserved, changed or distorted |

Not every model supports all three approaches. For the mini experiment we use [Google Lyria 3](https://replicate.com/google/lyria-3), which produces a short 30-second musical sketch. For the competition we use [MiniMax Music 2.6](https://replicate.com/minimax/music-2.6). Check the interface for text, lyrics, instrumental mode and other supported settings. **Words in the prompt are not the same as model controls**, and instructions such as an exact BPM or a specific musical transition may not be followed precisely. We will compare a few examples before choosing a model for PromptVision.

### Build a purposeful audio prompt

Start with this flexible structure:

**Style or genre → mood → rhythm/tempo → instrumentation and texture → development over time → optional vocals/lyrics**

Compare a broad instruction:

> Music for a foggy bridge at dawn.

With a more directed interpretation:

> A restrained instrumental electronic piece with a slow, steady pulse, soft layered synthesizers and sparse metallic notes. Begin with distant, hazy textures. Gradually introduce a warm, simple melody as the piece grows brighter, then end quietly. No vocals.

Which words describe **what it sounds like**, and which describe **how it develops**? Does the revised prompt express the source image more convincingly, or has it introduced ideas that are not in the original?

### Short web-interface demonstration

Open [Lyria 3 on Replicate](https://replicate.com/google/lyria-3) in its browser interface. We will inspect its supported inputs, enter a baseline prompt, generate or play a prepared example, and compare it with the more directed version.

Listen for differences in mood, pulse, instruments and progression. Notice also what the model ignores. Two generations can differ even with the same prompt; a difference between outputs does not automatically prove that a particular word caused it.

We will use tools and media we have permission to use. Avoid requests to imitate a real person's voice, and check each service's download and reuse conditions.

### Lyrics and vocal choices

A **music prompt** describes the style, mood, instruments and progression; **lyrics** are the words intended to be sung. A song can use lyrics written by your team, lyrics generated by the model, or no vocals at all. MiniMax Music 2.6 supports instrumental music and lyric input; structure labels such as `[Verse]` and `[Chorus]` can help organize a song, although the model may not follow them precisely. For example, a country that lives without sunrise might sing about finding its own light. Do not copy existing song lyrics or imitate a real singer's voice.

## Block 3: Mini experiment: change one thing (10 minutes)

Work in pairs or small groups using **Lyria 3**. Choose one image (your own or a provided example), and try a quick **A/B prompt comparison**. Its 30-second clips are just for the experiment; the later competition requires 1–2 minutes.

1. Identify three qualities in the image, such as texture, motion, lighting or mood. Write a sonic decision for each.
2. Write a short baseline audio prompt using the structure above.
3. Create a revised version that changes **one intentional element**, for example the tempo, instruments, density or how the sound evolves.
4. Generate and compare short excerpts if time and account access allow. Otherwise, compare prepared examples and discuss what you would test.
5. Keep one observation: **What did you change, what did you expect, and what did you actually hear?**

Do not aim for a polished composition yet. The goal is to make a deliberate creative choice and discover how much control the prompt gives you. You will use this approach during PromptVision after the break.

## After the break: PromptVision creation sprint

Form a team of 2–3, invent your country and write a **40–60-word fictional backstory** about its people, places, traditions or history. Choose a source image. Use the three visual-to-sonic decisions from the mini experiment to plan your composition. Use **MiniMax Music 2.6** to generate and compare attempts, select a **60–120-second competition track**, then create a new cover image inspired by the final sound. Multiple teams may start from the same source image.

No editing software, slide deck, flag design or notebook is required. See the [PromptVision guide](./activities/promptvision.md) for the four required files and submission template.

## Show and reflection

The instructor runs a local listening presentation. The country backstory appears alongside the large cover and smaller source image. The live player has a 75-second excerpt mode and a full-track option; with 15 teams we will play shorter excerpts to fit the 20-minute show. Take notes while listening, then agree on one ranked ballot per team (never voting for your own country). Submit your rankings using the ScoreWiz jury link, then watch the animated scoreboard reveal. We discuss the hidden prompts and optional lyrics after the results. See the [PromptVision voting instructions](./activities/promptvision.md) for details. Consider how the cover diverged from the source, which prompt decisions mattered, and whether different listeners interpreted the same sound differently.
