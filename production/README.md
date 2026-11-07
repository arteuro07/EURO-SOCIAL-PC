# BOSS DE RIEN — Production

## Goal
Build an original, code-driven short-film studio for recurring TikTok episodes. The official art direction is **hybrid manga**: hand-drawn manga sensibility, rich color, expressive ink, painterly depth and cinematic animation.

## Constraints
- Android/Termux is the control environment; GitHub Actions is the remote render worker when free quota permits.
- No paid video-generation APIs, subscriptions, VPS or automatic posting.
- Final target: vertical 1080 × 1920, 30 fps, about 60 seconds; first proofs are 8–12 seconds.
- Every render must be visually reviewed. CI success is not an artistic quality certificate.
- Do not restore deleted legacy models or episodes as canon.

## Pipeline
1. **Character bible** — approved model sheets, expressions, mouth shapes, poses, hands, costumes and props.
2. **Story & Director** — hook, comic beats, storyboard, shot sizes, camera and sound plan.
3. **Manga key art** — separate line art, color, shadows, highlights, backgrounds, props and effects.
4. **Animation** — key poses, anticipation, action, follow-through, in-betweens, facial swaps and deliberate holds.
5. **Cinematic compositing** — parallax, camera moves, depth, lighting, impact frames, speed lines and transitions.
6. **Audio & dialogue** — separate voice, foley, ambience and music; subtitles share the shot timeline.
7. **Film assembly** — deterministic frame rendering, FFmpeg, technical QC and manual review.
8. **Studio** — episode setup, preview, build and artifact access.

## Source of truth
- Hybrid manga art direction: `production/manga-pipeline/style-bible.md`
- Production workflow: `production/manga-pipeline/README.md`
- Storyboard schema: `production/manga-pipeline/schema/storyboard.schema.json`
- Current short proof storyboard: `episodes/proof-kevin/storyboard.json`

## Quality gates
Characters must retain recognizable proportions, face, hair, clothes and props across views. Shots must read on a phone screen. Assets become canon only after review. Never call an animatic finished animation.

## Build order
Approve Kévin's manga model sheet and expression atlas first; validate front/profile/three-quarter consistency; then Junior and Maya; then reusable backgrounds and props; then animate a short acting test; only after approval build a full episode.
