# Manga-to-film pipeline — BOSS DE RIEN

This pipeline treats each episode as a hand-authored comic/animation production, not as a procedural mannequin performance.

## Visual identity
Original manga drawing language + rich painted color + cinematic animation. The manga influence is a production method (clear silhouettes, expressive acting, panel composition, ink contours, speed lines and impact frames), not a copy of any existing franchise or artist.

## Production stages
1. **Character bible** — approved model sheets: front, profile, three-quarter, back, full body, face close-ups, expression atlas, hand poses, costume and prop details.
2. **Script & beats** — hook, setup, escalation, reversal, punchline, dialogue, sound cues.
3. **Storyboard / name** — every shot planned as a panel with shot size, angle, composition, action, dialogue, camera movement and duration.
4. **Key art** — draw the important poses and backgrounds as separate reusable layers. Keep line art, flats, shadows, highlights, effects and lettering separate when practical.
5. **Animation** — key poses first; then in-betweens, holds, anticipation, follow-through, facial swaps, mouth shapes and limited animation where it looks intentional.
6. **Cinematic compositing** — parallax, camera pans/zooms, depth, lighting, particles, speed lines, impact frames, transitions and color grade.
7. **Audio** — dialogue, ambience, foley, impacts and music on separate tracks; subtitles timed from the same shot timeline.
8. **Film assembly** — deterministic frame render, FFmpeg encode, technical QC and human visual review.

## Asset folder contract
Each character folder should eventually contain:
- `model-sheet/` — approved views and proportions
- `expressions/` — reusable face/expression drawings
- `poses/` — key poses and action drawings
- `mouths/` — phoneme/mouth shapes for dialogue
- `hands/` — hand pose library
- `costumes/` and `props/` — separate reusable details

Do not fill these folders with empty placeholders. An asset becomes reusable only after visual review and approval.

## Shot data
Episodes store an ordered `storyboard.json`. Each shot has an ID, start/end time, panel composition, character pose/expression, background, camera move, effects, dialogue and audio cues. Validate the timeline before rendering. See `schema/storyboard.schema.json`.

## Render strategy
- Stage A: storyboard animatic using held drawings, cuts, camera moves and temporary timing.
- Stage B: polished key art and limited animation.
- Stage C: selected full animation for important action beats.
- Stage D: final color, compositing, sound and subtitles.
- First target remains a short 8–12 second proof. Do not render a full 60-second episode until the art direction and workflow pass review.
- Final target: 1080x1920, 30 fps, vertical MP4. Preview quality may be lower.

## Quality gates
- Character proportions, face, hairstyle, clothes and signature props remain consistent.
- Every shot has a clear focal point and readable action on a phone screen.
- No unreviewed generated asset is treated as canon.
- A green CI check only means the files/timeline pass validation; it does not certify artistic quality.
- Never describe a rough animatic as finished animation.

## Constraints
Free tools and GitHub Actions where available; Android/Termux as the control device; no paid generation APIs, VPS, subscriptions or automatic social posting. Keep the pipeline source-first and reproducible.
