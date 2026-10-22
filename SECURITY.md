# Security policy

## Reporting a problem

Open an issue or a pull request and I'll take a look. A pull request with the fix is the quickest route.

You can also report privately: open the repository's **Security** tab and choose **Report a vulnerability**.

This is a one-person project with no bug bounty and no response deadline. I'll reply when I can and say what I plan to do. Good-faith testing on your own copy is welcome.

## Supported versions

Only the latest release on the default branch gets fixes.

## Scope

The skills' instructions and scripts run on your machine with your agent's permissions. `aw.py` reads image files you name, writes PNG files and JSON records where you tell it (a work folder, default `./artwright`, and `~/.artwright`), runs `ffmpeg` to decode images when Pillow is absent, and fetches a Lospec palette or makes one probe request to a museum API only when asked. In scope: anything that leads the agent to run commands, write files, fetch URLs or share data beyond what the skill says it does. That includes instructions planted in an image, a palette file or a fetched page (prompt injection), any crafted image or palette file that makes `aw.py` run code or write outside the folder it was given, and any way the private taste record could leak into a repository or output. Out of scope: bugs in the agent tool itself (Claude Code, Copilot, Codex, Cursor), in Pillow or in ffmpeg; report those to their makers.
