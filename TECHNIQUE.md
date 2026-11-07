# BOSS DE RIEN — Code Film Technique

## Core idea
An episode is a deterministic function of time. The project describes what is visible and audible at each timestamp; the renderer produces frames; the audio pipeline builds dialogue, music and effects; FFmpeg assembles the final MP4.

No generative video API is required. The first implementation should use browser rendering (Canvas 2D for reliable layered animation, with Three.js/WebGL added only where it improves the result). This is a code-driven animation pipeline, not a claim that a full 3D character model exists.

## Pipeline
```
episode brief
  -> treatment + shot list + beat timeline
  -> character/style assets and scene layout
  -> deterministic render(t) in browser
  -> frame sequence / video
  -> dialogue + foley + music + subtitles
  -> FFmpeg mix and mux
  -> MP4 + poster + SRT + source + credits
```

## Project contract
Each episode folder contains:
- `TREATMENT.md`: story, shot list, beat sheet and sound plan;
- `index.html` and source modules: scene and animation code;
- `timeline.json`: shots, events, dialogue and timing;
- `build.sh`: one-command local build;
- `CREDITS.md`: assets, fonts, sounds, licences and sources;
- `out/`: generated MP4, poster and subtitle file (build output, not source).

## Renderer contract
The scene exposes:
- `DURATION`: episode duration in seconds;
- `render(t)`: deterministic scene state/frame at time t;
- `READY`: true when fonts and assets are loaded;
- `EVENTS`: timed events for foley, dialogue and transitions;
- `SUBTITLES`: subtitle cues with start/end times.

The same timestamp must always produce the same frame. Animation uses seconds, keyframes, easing and interpolation. Keep camera coordinates and world-to-screen transforms centralized.

## Character system
Build reusable, original character rigs from layered vector shapes and/or Three.js geometry. Keep a canonical model sheet and palette for each character. Reuse the same head, hair, body, clothes and proportions across shots. Add facial controls, mouth shapes, eye direction, brows, hands and pose controls. A procedural 2.5D rig is an acceptable first production method if it looks polished and consistent; do not label it a fully rigged 3D model.

## Rendering strategy
- Start with a short 8–12 second proof, not a full one-minute render.
- Validate at 540 × 960 or 720 × 1280 and 24 fps.
- After visual approval, render the final vertical 1080 × 1920 at 30 fps.
- Use headless Chromium and FFmpeg in GitHub Actions when supported by the runner.
- Do not assume hardware GPU acceleration. Test software WebGL/Canvas rendering on the actual runner.
- Cache dependencies; keep source in Git and large generated renders as workflow artifacts.
- Check available GitHub Actions minutes and artifact retention; never assume unlimited free compute.

## Audio and subtitles
Keep voice, music, ambience and foley separate until mixing. Use original recordings or documented free/licensed resources. Generate SRT from the same dialogue timeline used by the scene. Check subtitle readability and dialogue sync.

## Validation
A build is not successful merely because FFmpeg produced a file. Validate:
- expected dimensions, frame rate, duration and audio stream;
- no black/blank frames or missing assets;
- no NaN/infinite coordinates or renderer errors;
- character identity and continuity across a contact sheet;
- key actions at normal speed and enlarged;
- dialogue/subtitle synchronization and audio levels.

## Constraints
Android/Termux is the control device. GitHub Actions is optional remote compute, not an unlimited render farm. No paid APIs, paid subscriptions, VPS or automatic social posting. Keep all external assets and licences documented.
