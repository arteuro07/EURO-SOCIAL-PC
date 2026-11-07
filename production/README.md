# BOSS DE RIEN — Production

## Goal
Build an original, code-driven short-film studio for recurring TikTok comedy episodes. The production approach is inspired by procedural filmmaking: the director plans the story and shots, the renderer draws each frame from a deterministic timeline, and audio/subtitles are mixed into a finished MP4.

## Non-negotiable constraints
- Android/Termux is the control environment.
- Use GitHub Actions for remote builds only when free quotas permit.
- No paid video-generation APIs, paid subscriptions, VPS or auto-publication.
- Final target: vertical 1080 × 1920, 30 fps, approximately 60 seconds.
- First proof: 8–12 seconds at reduced resolution before attempting a full episode.
- The finished video must be manually reviewed; a successful workflow is not proof of visual quality.
- Do not reintroduce deleted legacy models or episodes as production assets.

## Production architecture
1. **Story & Director** — treatment, hook, comic timing, shot list, camera and sound plan.
2. **Character System** — stable reusable rigs, model sheets, expressions, costumes and continuity for Kévin, Junior and Maya.
3. **Scene & Camera** — reusable locations, props, lighting, framing, camera motion and depth.
4. **Timeline Renderer** — deterministic frame-by-frame browser rendering using Canvas 2D first and Three.js/WebGL where useful.
5. **Audio & Dialogue** — voice, timing, foley, ambience, music and subtitles.
6. **Film Assembly** — FFmpeg render, mix, mux, poster and validation.
7. **Studio** — episode configuration, preview, build launch and artifact access.

## Visual direction
Target a polished cinematic cartoon with expressive faces, appealing silhouettes, detailed hair and clothing, controlled lighting, depth and smooth acting. A reusable 2.5D rig may be used as a stepping stone only if it meets the quality bar and preserves character identity. Never call it a full 3D model unless it really is one. No cube mannequins or disposable placeholder characters.

## Build order
1. Establish Kévin's model sheet and a reusable character rig.
2. Render a short acting test with front, profile and three-quarter views.
3. Validate expressions, hands, props, movement, camera and lighting.
4. Add Junior and Maya using the same character system.
5. Build a reusable set and a complete 8–12 second scene.
6. Validate audio, subtitles and export.
7. Scale to a full 60-second episode only after the proof passes.

## Quality gates
- Character identity remains consistent between frames and camera angles.
- Silhouette, face, hands, hair and clothes are clean at phone size.
- Acting uses anticipation, action and follow-through with smooth interpolation.
- Shots have deliberate framing and readable comic timing.
- Audio, subtitles and picture are synchronized.
- Build output has correct dimensions, frame rate, duration and no blank frames.
- Sources, build instructions and asset licences are documented.

See [DIRECTOR.md](../DIRECTOR.md) and [TECHNIQUE.md](../TECHNIQUE.md) for the production rules.
