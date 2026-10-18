# PromptVision: instructor setup and presentation

Student instructions: [Session 2](../day02.md) and [PromptVision](../activities/promptvision.md).

## Before class

Prepare a small selection of working browser audio/image models, test generation and download times, and have example images and audio clips as a fallback. Create a SWITCHdrive `PromptVision/` folder with numbered subfolders for teams of 2–3. Reserve **unique country names** and numbers early.

Prepare a [ScoreWiz](https://scorewiz.eu) competition with one country/jury per team. Rehearse the chosen voting point scale, voting links, self-vote exclusion, projector and sound. With ten countries, standard 12-to-1 ranking is not directly applicable because a jury has only nine other countries to rank: choose a supported shorter scale. ScoreWiz is no longer maintained, so keep a manual ranked-ballot and tally fallback.

## Submission and local show

Each team uploads `track.mp3`, `source.png`, `cover.png`, `entry.txt` into its numbered folder. Alternatives to mp3/png are in the student guide. Download the whole collection locally so the numbered folders are directly under a folder called `PromptVision`. Avoid extra nesting from ZIP extraction.

From the course repository, run:

```sh
python scripts/promptvision_show.py "/path/to/PromptVision"
```

The script uses only the Python standard library and creates **`promptvision_show.html`** and **`scorewiz_countries.txt`** inside the downloaded folder. Open the HTML directly, without a server or internet connection. The show uses local audio, large cover, smaller source reference, next/previous, country selector and hidden prompt that can be revealed after listening. It limits playback to the first 45 seconds.

Read the script's `CHECK` warnings. Missing track, source image or `entry.txt` skips that team; a missing cover falls back temporarily to the source image. Incomplete metadata fields are flagged. Fix submissions and rerun; existing student files are never changed. Compare `scorewiz_countries.txt` with the contest roster before voting. The script does **not** submit votes or control ScoreWiz.

## Timing

Allow 10 minutes for final submission and playback checks, although teams should upload earlier. Then allow 20 minutes for 10–15 tracks, roughly 45 seconds of audio plus short transition per entry. Keep the cover onscreen, with the original image visible for comparison; reveal prompts afterward. Allow 20 minutes for juries to vote together and the scoreboard reveal, followed by a 5-minute reflection on interpretation, prompting and personal taste.

If ScoreWiz fails, collect rankings by chat/paper and tally manually. If the webpage fails to play an audio format on the presentation computer, play files directly in numeric order. **Rehearse the real audio formats and ScoreWiz voting before class.**

## Test

```sh
python -m unittest discover -s tests -p test_promptvision_show.py -v
```

These tests use synthetic media, make no paid generation requests and do not test actual browser codecs or ScoreWiz.
