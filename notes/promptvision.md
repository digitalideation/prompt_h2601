# PromptVision: instructor setup and presentation

Student instructions: [Session 2](../day02.md) and [PromptVision](../activities/promptvision.md).

## Before class

Test [Lyria 3](https://replicate.com/google/lyria-3) for the 30-second mini-experiment and [MiniMax Music 2.6](https://replicate.com/minimax/music-2.6) for the 1–2-minute competition. MiniMax may produce longer tracks, so rehearse trimming or exporting a shorter excerpt. Check costs and available controls before class; have prepared examples and a working image model as fallbacks. Create a SWITCHdrive `PromptVision/` folder with numbered subfolders for teams of 2–3. Reserve **unique country names** and numbers early.

Prepare a [ScoreWiz](https://scorewiz.eu) competition with one country/jury per team. Rehearse the chosen voting point scale, voting links, self-vote exclusion, projector and sound. With ten countries, standard 12-to-1 ranking is not directly applicable because a jury has only nine other countries to rank: choose a supported shorter scale. ScoreWiz is no longer maintained, so keep a manual ranked-ballot and tally fallback.

## Submission and local show

Each team uploads `track.mp3`, `source.png`, `cover.png`, `entry.txt` into its numbered folder. Alternatives to mp3/png are in the student guide. Download the whole collection locally so the numbered folders are directly under a folder called `PromptVision`. Avoid extra nesting from ZIP extraction.

From the course repository, run:

```sh
python scripts/promptvision_show.py "/path/to/PromptVision"
```

The script uses only the Python standard library and creates **`promptvision_show.html`** and **`scorewiz_countries.txt`** inside the downloaded folder. Open the HTML directly, without a server or internet connection. The show uses local audio, large cover, smaller source reference, next/previous, country selector, the country's 40–60-word story and hidden prompt/optional lyrics that can be revealed after listening. The live mode stops after 75 seconds; tick **Play entire track** for the complete 1–2-minute submission.

Read the script's `CHECK` warnings. Missing track, source image or `entry.txt` skips that team; a missing cover falls back temporarily to the source image. Incomplete metadata fields are flagged. Fix submissions and rerun; existing student files are never changed. Compare `scorewiz_countries.txt` with the contest roster before voting. The script does **not** submit votes or control ScoreWiz.

## Timing

Allow 10 minutes for final submission and playback checks, although teams should upload earlier. Then allow 20 minutes for 10–15 tracks, roughly 75 seconds of audio for smaller rosters or a shorter excerpt when 15 teams compete. A 75-second excerpt plus transitions for 15 countries will exceed 20 minutes, so either extend the listening block or deliberately use shorter excerpts via the audio controls. Keep the cover onscreen, with the original image visible for comparison; reveal prompts afterward. Allow 20 minutes for juries to vote together and the scoreboard reveal, followed by a 5-minute reflection on interpretation, prompting and personal taste.

If ScoreWiz fails, collect rankings by chat/paper and tally manually. If the webpage fails to play an audio format on the presentation computer, play files directly in numeric order. **Rehearse the real audio formats and ScoreWiz voting before class.**

## Preview the viewer without student files

From the repository root run:

```sh
python scripts/promptvision_show.py --demo
```

This creates `PromptVision-demo/` with **two fictional countries**, simple generated images, **70-second synthetic audio tones** (not AI music), `entry.txt` metadata, and a working `promptvision_show.html`. Open that HTML in a browser, press play, switch countries, inspect the story and cover/source comparison, and click **Reveal prompt**. The `scorewiz_countries.txt` file contains the matching roster. The demo folder is disposable and is ignored by Git. To rebuild, delete or rename that demo folder first.

For a real show, download numbered submission folders and run `python scripts/promptvision_show.py "/path/to/PromptVision"` again. Note that the show page refers to the nearby media files; keep the folders together.

## Test

```sh
python -m unittest discover -s tests -p test_promptvision_show.py -v
```

These tests use synthetic media, make no paid generation requests and do not test actual browser codecs or ScoreWiz.
