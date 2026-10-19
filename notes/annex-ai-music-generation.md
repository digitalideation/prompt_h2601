# Annex: How AI Generates Music (2026)

[← Back to Session 2](./day02.md)

**The big idea:** AI music generators learn patterns from recordings paired with descriptions, lyrics or other information. Given a prompt, they create new audio with recognizable instruments, rhythms, moods and sometimes vocals. Most generate _sound itself_, rather than first writing a traditional musical score.

## 1. The basic pipeline: from words to sound

**Prompt / lyrics / reference audio → text or audio conditioning → generative model → compressed audio representation → neural audio decoder → playable waveform**

A few minutes of uncompressed audio contain millions of sample values. Generating these values directly would be costly. Many current systems therefore work in a **compressed representation** of sound:

- **Audio tokens** are discrete symbols, a little like a vocabulary of sound fragments or features.
- **Audio latents** are compact numerical representations of musical and acoustic information.
- A **neural audio codec or autoencoder** learns to compress recordings and reconstruct them. Its decoder turns generated tokens or latents back into the audible waveform.

During training, the model learns how these representations relate to text, musical patterns and what happens before or after a moment in a recording. During generation, the prompt guides the model toward one plausible result; it does not retrieve a ready-made song or execute a precise score.

## 2. Three main generation approaches

| Approach                              | What's happening technically                                                                                                                                                       | Intuition and documented examples                                                                                                                                                                                                                                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Autoregressive generation**         | A model predicts the **next audio token** based on previous tokens and the prompt, extending a sequence step by step.                                                              | _Like an LLM predicting the next word._ Meta's **[MusicGen](https://ai.meta.com/resources/models-and-libraries/audiocraft/)** uses a Transformer and compressed EnCodec audio tokens.                                                                                                                        |
| **Diffusion / flow-based generation** | A model starts from **noise in an audio latent space** and transforms it over multiple steps into an audio representation consistent with the prompt.                              | _Like progressively bringing sound out of noise._ Examples: Google's **[Lyria 3 / 3.5](https://deepmind.google/models/model-cards/lyria-3-5/)** and **[Stable Audio 3](https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models)**. |
| **Hybrid generation**                 | Different models share the task: for example, a language model proposes song-level information (structure, lyrics or descriptions), while a diffusion model synthesizes the audio. | _A rough musical plan followed by sound production._ **[ACE-Step 1.5](https://huggingface.co/docs/diffusers/api/pipelines/ace_step)** combines an LM planner with a diffusion Transformer.                                                                                                                   |

**Where do Transformers fit?** A **Transformer** is a neural-network architecture that uses _attention_ to connect information across a sequence. It is **not** a competing fourth approach: Transformers can predict tokens autoregressively or operate inside diffusion models (often called _Diffusion Transformers_, or DiTs). Likewise, not all commercial music systems disclose their full architecture.

## 3. What can we ask these models to do?

- **Text-to-music:** Generate a song, instrumental or musical texture from a description; some tools accept separate lyrics and vocal instructions.
- **Text-to-sound:** Generate environmental sounds, cinematic effects, ambience or abstract sonic textures rather than a conventional song.
- **Audio-to-audio:** Continue, vary, restyle or edit an existing recording. Depending on the system, this can include replacing a segment (_inpainting_) or working from an audio reference.

The important difference from image generation is **time**. A track needs not only plausible sounds but also relationships between what happens at the beginning, middle and end: rhythm, recurring motifs, tension, transitions and resolution.

**A broad prompt:** “Dreamy electronic music.”

**A more directed prompt:** “A slow electronic instrumental with hazy synth pads and a steady, quiet pulse. Begin with sparse textures; gradually introduce a warmer melody and denser percussion; finish with a soft atmospheric outro. No vocals.”

The second prompt gives the model a _temporal trajectory_, not just a sonic style. It may help, but precise instructions such as an exact BPM, a transition at 35 seconds or a particular chord sequence are not guaranteed.

## 4. Where is the technology now, and what is still difficult?

**What has improved:** By 2026, systems can produce impressive timbres and arrangements, generate songs with vocals, use lyrics and audio references, and offer longer outputs or targeted editing. Quality and available controls vary considerably across tools.

**Four ongoing challenges:**

1. **Long-range coherence.** A short excerpt can sound convincing while a longer track loses its motifs, repeats aimlessly or introduces awkward transitions. Good sound quality is not the same as good composition.
2. **Precise control.** Genre and mood are often easier to steer than an exact rhythm, harmony, instrument entry, structure or time-coded change. The prompt is guidance, not a musical programming language.
3. **Reliable revision.** Asking to “change only the drums” may also alter the melody, timing or overall texture. Even the same prompt can give noticeably different outputs because generation involves sampling and randomness.
4. **Rights, attribution and identity.** Training data, licensed reuse, stylistic imitation and recognizable voices raise questions of consent, copyright and authorship. Tool-specific terms matter, especially for publishing or commercial use.

## 5. What this means for our image-to-sound exercise

**Image → three perceived qualities → sonic choices → prompt with progression → generate → listen → revise.**

For example, _fog_ might become blurred synthesizer pads, _steady movement_ a repeating pulse, and _emerging sunlight_ a melody that gradually brightens. These are **creative interpretations**, not fixed translations. Compare two prompt versions, listen for what the model followed or ignored, and explain the decision you made after hearing the result.

**Key takeaway:** AI music generation is now good at producing convincing _sound_. The harder, more interesting problem is shaping that sound into a coherent, controllable **musical experience over time**.

---

_Further reading (technical sources): [Meta AudioCraft / MusicGen](https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-ai-audio/) · [Google DeepMind Lyria 3.5 model card](https://deepmind.google/models/model-cards/lyria-3-5/) · [Stability AI: Stable Audio 3](https://stability.ai/research/stable-audio-3) · [ACE-Step 1.5 documentation](https://huggingface.co/docs/diffusers/api/pipelines/ace_step)._
