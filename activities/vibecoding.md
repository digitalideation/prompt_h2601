# 💫 VibeCoding: Class Flow (38 Students)

*Previous-semester material. See the [course homepage](../readme.md) for the H26 sessions.*

## Goal

Reinterpret **Rafael Rozendaal’s _Internet_ (2002)** through **vibe coding**: translating mood, rhythm, and color into generative motion using **p5.js**, then extending those visuals through **AI video generation**.
Describe visuals as _parameters_, experiment with procedural rhythm, and compare human-coded versus AI-interpreted motion.

## Links

- [Shared SwitchDrive](https://drive.switch.ch/index.php/s/jNhPTRJUXGGV8Ez): Upload folder for frames & videos
- [p5.js Web Editor](https://editor.p5js.org): Coding environment
- [Replicate Private Chat LLM](https://turbo-barnacle-w5gwvgxqg7f55vq-8501.app.github.dev/) - LLM coding assistant.
- [Google Gemini Flash 2.5](https://gemini.google.com/): Free public version.
- [Seedance-1 Lite Video Model (Replicate)](https://replicate.com/bytedance/seedance-1-lite): img2vid generation
- [Reference Artwork – _Internet_ (2002)](https://www.newrafael.com/internet/)

## Setup

- **Teams of 2 students** (≈ 19 teams total).
- Each team = one **Vibe Studio** with a chosen _theme word_ (e.g., “Flow,” “Chaos,” “Glow”).
- Each team works on a **shared p5.js sketch** (from instructor template).
- Roles:

  - 🎛 _Tuner_: edits numbers and parameters.
  - 🎨 _Vibe Director_: describes visual mood & rhythm.

Each team submits:

- 🌀 `sketch_link.txt` – public URL of their p5.js sketch
- 🖼 `frame_first.png` + `frame_last.png` – captured images
- 🎞 `ai_video.mp4` – short (3–5 s) AI video interpretation
- ✍️ `notes.txt` – 2-line description of their vibe & reflection

Example folder:

```
/VibeCoding 2025/
   Flow_Collective/
      sketch_link.txt
      frame_first.png
      frame_last.png
      ai_video.mp4
      notes.txt
   Neon_Void/
   Tranquil_Circuit/
   ...
```

## Timing Overview

| Stage | Activity                         | Duration | Notes                                         |
| :---- | :------------------------------- | :------- | :-------------------------------------------- |
| **1** | Introduce Rozendaal & _Internet_ | 10 min   | Discuss rhythm, repetition, minimalism.       |
| **2** | p5.js Demo & Account Setup       | 10 min   | Open your account and copy the template.        |
| **3** | Team VibeCoding Session          | 30 min   | Directors describe, Tuners adjust parameters. |
| **4** | Frame Export                     | 10 min   | Save first & last frames.                     |
| **5** | AI Video Generation              | 15 min   | Compare the generated videos.         |
| **6** | Showcase & Discussion            | 15 min   | Compare human vs AI motion.                   |

⏱ **Total:** ~90 min (max 2 h 30 min with setup)

## Creating a p5.js Account & Saving Sketches

1. Visit 👉 [https://editor.p5js.org](https://editor.p5js.org)
2. Click **“Sign Up”** (top-right) → sign in with Github, Google or email.
3. Once logged in:

   - Click **“New Sketch.”**
   - Rename it with your team name (`Flow_Collective`).
   - Copy the instructor template code.

4. Use **Run ▶️** to preview.
5. Use **File → Save** to keep your changes.
6. To share: click **Share → Copy Link** and paste it in `sketch_link.txt`.
7. To save use`Ctrl+S` / `Cmd+S`. The editor also auto-saves every 30 seconds when logged in.
7. To save image: **right-click inside the code editor → Save Image As** .

## Using the Starter Template

A lightweight motion seed:

```js
let dots = [];
let chaos = 0.01;
function setup() {
  createCanvas(600, 600);
  for (let i = 0; i < 80; i++)
    dots.push(createVector(random(width), random(height)));
}
function draw() {
  background(0, 10);
  stroke(255, 150);
  for (let p of dots) {
    p.x += sin(frameCount * chaos + p.y * chaos);
    p.y += cos(frameCount * chaos + p.x * chaos);
    point(p.x, p.y);
  }
}
```

Experiment by changing numbers and colors (no syntax edits). Try verbal prompts such as: “slower,” “denser,” “brighter,” “chaotic.”

## 💡 Code Assistance Tools

You may use one of the following language models to help refine parameters or interpret errors:

- 🧠 **Private LLM (class access provided)** – preferred option for guidance and feedback.
- 🌐 **Fallback:** [Google Gemini Flash 2.5](https://gemini.google.com/): free public version.

Suggested prompt for assistance:

> “I have this p5.js code. How can I make the motion slower and more organic, without adding new functions?”

## Exporting Frames

1. When the sketch looks right, stop the animation (`pause ▶️`).
2. **Right-click inside the code editor → Save Image As** to export a frame (PNG).
3. Save one **early** frame (≈ 10 s) and one **late** frame (≈ 60 s).
4. Upload both to your team folder.

## AI Video Interpretation Phase

1. Select your two frames.
2. Upload pair to **Replicate** using the [ByteDance Seedance-1 Lite](https://replicate.com/bytedance/seedance-1-lite) model (720p prefered).
3. Generate a 3–5 s video showing the interpolation between frames.
4. Optional: add audio from Day 02 _PromptVision_ for cross-modal effect.

## Showcase & Feedback

- Watch all p5 loops + AI videos side-by-side.
- Discuss:

  - “Which parameter most defined the vibe?”
  - “How did the AI interpret motion differently?”

- Optional quick votes or applause:

  - 💫 _Most Hypnotic Loop_
  - ⚡ _Best AI Transformation_
  - 🌿 _Most Organic Motion_

## Deliverables

Each team uploads:

```
sketch_link.txt
frame_first.png
frame_last.png
ai_video.mp4
notes.txt
```

Example `notes.txt`:

```
Our sketch explores the vibe of connection and flow through oscillating points and soft motion.
The AI video interpreted it as a dense wave field, amplifying the chaos and color pulses.
```

### ✅ Outcome

You can translate Rozendaal’s web-art logic into parameterized generative motion, compare it with AI video, and reflect on authorship and interpretation across media.
