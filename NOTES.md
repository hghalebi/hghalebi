# Profile animation

The GitHub README uses a self-contained animated SVG and a static SVG for reduced-motion readers. The animated asset has no scripts, external images, external fonts, or network dependencies.

The animation is a design illustration, not telemetry from a deployed service.

## Files

- README.md: profile with the new visual already embedded.
- assets/production-ai.svg: editable 18-second animation.
- assets/production-ai-static.svg: still-image alternative.
- assets/production-ai.gif: optional raster animation; this GIF is included here, not committed to GitHub.
- preview.html: browser preview; keep the assets directory beside it.
- embed.html: just the embeddable HTML.
- build_animation.py: standard-library Python SVG generator.
- validate_render.py: local Chromium checks and GIF exporter; requires Pillow, Playwright, and Chromium at /usr/bin/chromium.
- validation.json: local checks and verified remote Git blob hashes.

## Rebuild

```sh
python3 build_animation.py
```

## Publication and validation

Published to hghalebi/hghalebi on main, final commit 8b2318f10df3f354ce47343b1ae89bd7591c3eb8.
The three committed blobs were checked against the locally rendered files.
Playback in an HTML img, narrow viewport sizing, and picture-based reduced-motion fallback were tested in local Chromium.
Live GitHub visual playback was not inspected in this environment.
