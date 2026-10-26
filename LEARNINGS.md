# Learnings: artwright

Procedural lessons for [README.md](README.md). Research findings live in [RESEARCH.md](RESEARCH.md); every change is logged in [CHANGELOG.md](CHANGELOG.md); test runs in [TESTS.md](TESTS.md); state in `evergreen.json`. Format and write-time gate: MAINTENANCE.md (LEARNINGS-FORMAT). Retired entries go to LEARNINGS-ARCHIVE.md with a reason.

Write an entry the moment a real signal happens: a user correction, the same error twice, a discovered workaround, an environment fact, a stated preference, a failed test or a failure in use. Check existing entries first, by meaning (`evergreen.py search "<the lesson>" --kinds learnings` finds near-duplicates in every registered unit): add / update / retire / none. Trigger and Hypothesis are required. Promote after three confirmations; retire when harmful > helpful.

## Active

### L-020 · 2026-10-26 · On a JPEG, count a step only where it peaks: ringing hides a small grid
- Trigger: `aw.py pixel` read scale 2 and scale 3 palette art saved at quality 90 (and 95) as scale 1; the share of
  steps on the true lattice was 0.56 at scale 2, near chance (0.5). A low-contrast scale 2 JPEG read as scale 8.
- Hypothesis: ringing beside each real edge adds smaller steps over the tolerance one or two pixels away, off the
  lattice. Raising the tolerance recovers the grid but drops edges between close palette colours.
- Rule: on lossy input, keep a step only where it is a local peak along its row or column (non-maximum
  suppression), at the usual tolerance. Keep the 8 px block test on the plain count, since blocks are what it
  looks for. Then confirm it: with the ringing gone, a smooth JPEG's strongest remaining steps are its 8 px
  block edges, which also sit on the 2 and 4 lattices. Trust the peak reading only below 8 and when the mean step
  on the lattice is at least 1.6 times the mean off it, block rows and columns left out (smooth JPEGs 1.05-1.10,
  real grids 2.2-7.6).
- Evidence: Books12.test_jpeg_ringing_does_not_hide_a_small_grid (1, 1 and 8 before; 2, 3 and 2 after; fails with
  the peak test removed); a smooth quality 90 JPEG stays 1; 112 real JPEG renders unchanged; alignment at the true scale 0.56 to 0.97 (scale 2) and 0.42 to 0.83 (scale 3)
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-26

### L-019 · 2026-10-25 · A defect count that real sprites score as high as the fixture is a locator, not a grade
- Trigger: the book-proposed banding rule (runs whose exact span the next row repeats) found 0 hits on a disc with a one-pixel ring hugging its outline; curved bands shift one pixel a row. Widened to offsets 0 and 1, the ring scored 4.7 per 100 edge pixels, but 30 AI renders quantised to 48 px sprites scored 0 to 6.5 (median 3.3).
- Hypothesis: equal runs side by side are common in any small quantised image (eyes, belts, flat bands), so the count cannot separate a bad sprite from an ordinary one; its coordinates still point at the bands worth looking at.
- Rule: before giving a new pixel measure a pass line, score it on a real batch of the images it is for; if they overlap the defect fixture, ship it reported with coordinates and let the critique look (a degrade test still proves it rises with the defect).
- Evidence: Books13.test_banding_rises_with_a_hugging_ring; the 30-sprite run in decisions/2026-10-25-books-track13.md I2
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-25

### L-018 · 2026-10-25 · A JPEG's 8 px block edges also sit on the 2 and 4 px lattices
- Trigger: `aw.py pixel` read a smooth render saved as a quality 55 JPEG as scale 2 pixel art at 99.7% lattice alignment. The proposed fix (confirm the lattice on luma alone, blaming chroma subsampling) did not work: the luma showed the same steps.
- Hypothesis: the steps are the DCT block edges, which are in luma too; every multiple of 8 is even, so a lattice test at 2 or 4 finds them all.
- Rule: before trusting a small grid scale on a JPEG, measure the share of colour steps on the 8 px lattice; near all of them means blocks (real scale 2 art has about a quarter there). A scale of 8 or 16 on a JPEG cannot be told from blocks this way; say so and look.
- Evidence: Books12.test_jpeg_block_lattice_is_not_a_pixel_grid (2 without the guard, 1 with); 97% of the fixture's steps on the 8 px lattice, a scale 2 palette JPEG 15%; decisions/2026-10-25-books-track12.md H7
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-25

### L-017 · 2026-10-25 · Fixed measures run on the reduced copy; reduce by averaging, and estimate grain before reading derivatives
- Trigger: two book-proposed failures reproduced on fixtures: `small()` sampled by nearest neighbour above 4x (3000 px stripes read luma SD 30.4, a true box 1.3), and grain of SD 16 made comp's Laplacian hierarchy fire `uniform_sharpness` on flat shapes with one sharp place.
- Hypothesis: every 256 px measure inherits the reduction's aliasing, and a derivative measure has a noise floor proportional to the noise variance, so both read artefacts as picture content.
- Rule: a new measure reads `small()`'s area-averaged copy; one built on a derivative (Laplacian, Sobel ratios) subtracts the grain floor first (`noise_sigma`, 20 sigma squared for the 4-neighbour Laplacian) and gets a `degrade --kind noise` test. Keep `resize_box` for hashes, whose distances were tuned on it.
- Evidence: Books12.test_small_does_not_alias_fine_stripes and test_grain_is_not_detail (both fail with the fix removed); on 60 real stills the flag fired on the same 3 before and after; decisions/2026-10-25-books-track12.md H1, H5, H6
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-25

### L-016 · 2026-10-24 · A texture gap from img2img over a flat render needs a second paint pass, not a noise overlay
- Trigger: a loading screen painted by img2img over a flat 3D render came out far smoother than the series it joins (edge density 0.08 to 0.10 against the series' 0.24 to 0.36 at 960 px). A deterministic paper-grain overlay barely moved fine grain; a second img2img pass at denoise 0.5 raised edge density to 0.20.
- Hypothesis: the render's flat shading survives a single low-denoise pass, so the painting inherits its smooth fields. Pigment-scale grain is finer than the scale the series is measured at and averages out there, so an overlay adds noise without adding brushwork the measure (or a viewer at screen size) can see.
- Rule: when `setfit` fails edge density or fine grain on a painting made over a render, run a second paint pass at a higher denoise (0.5 is where it moved) and measure again; never add a noise or grain overlay to pass the gate. If the gap remains, report it with the numbers instead of gaming the measure.
- Evidence: a private game project's work folder, sawmill-3d/scene (gates/set_gate.py, paint/, finals/C2from104_g05.png and siblings, grain.py), 2026-10-24
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24

### L-015 · 2026-10-24 · Judge a measure on a painting relative to the clean render's own score in the same zone
- Trigger: mechanism gates on a scene painted over a 3D render (a water wheel: water at the upstream low rim, none at the hub, water continuing downstream) gave wrong verdicts with fixed shares. A pale painted hub tripped a "water at the hub" colour test, and per-region edge precision and recall could not separate correct paintings from broken ones even at 480 px (extends L-009), so it became a reported measure.
- Hypothesis: a fixed threshold mixes what the scene contains with what the painting lost. The clean render scores the correct layout in the same zone with the same colour test, so a ratio to it passes a correct render by construction and counts only what the painting dropped.
- Rule: score each zone on the render and on the painting with the same test and gate the painting at a fraction of the render's score (the feed gate settled at 0.7). Keep colour tests out of zones where a painted part can share the colour (a pale hub reads as foam). Edge agreement at scene scale is information, never a gate.
- Evidence: a private game project's work folder, sawmill-3d/scene/gates/scene_gates.py (rim, hub, feed, tail gates; regions reported), test_hub_stream.png, test_feed_grass.png, test_tail_grass.png and their .gates.json, 2026-10-24
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24

### L-014 · 2026-10-24 · Calibrate a gate on a known-good set member and a known-bad image before trusting its threshold
- Trigger: on one scene job, three gate thresholds set from reasoning alone were wrong. The series gate at a widen of 0.25 failed one of the series' own screens on fine grain (it sat 0.27 of the range above the others); the feed gate at 0.5 of the render's share passed a wheel standing on dry ground (0.7 fixed it).
- Hypothesis: a threshold is a guess until it has seen one case that must pass and one that must fail; the margin between them is what the threshold sits in, and reasoning alone does not know where either falls.
- Rule: before trusting a gate, run a known-good case (a set member held out as the candidate, or the clean render) that must pass and a known-bad image made for that gate (a smoother copy, grass painted over the race, a stream from the hub) that must fail; set the threshold between them and keep both images as the gate's test. `setfit`'s widen of 0.3 is the smallest that let the held-out member through.
- Evidence: a private game project's work folder, sawmill-3d/scene/gates (set_gate.py WIDEN comment; make_negatives.py and make_feed_negative.py with the test_*.png they write); `aw.py setfit` on that series puts the held-out screen's fine grain at position 1.30 and passes it at 0.3 (2026-10-24); tests SetFit.test_member_passes and test_smooth_candidate_fails_texture
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24
### L-013 · 2026-10-24 · Judges and mechanism gates miss a light no object explains; check each big shadow against the render's
- Trigger: the sawmill loading screen candidate A passed all four mechanism gates and won the blind pairwise ranking
  in both orders, yet the first thing the reviewer named was a long hard-edged diagonal shadow from the river up the
  bank to the wheel. The render and the controls have no shadow there; the painting pass invented it.
- Hypothesis: the gates only look at the parts they model (rim, hub, feed, tail), and the judge compared candidates
  with each other on the checklist (mechanism, style, set fit), so a fault common to neither the checklist nor the
  other candidate goes unnamed; shadows read as atmosphere, not as a fault.
- Rule: in an illustration painted over a render, add one question to the judge's read: does every large shadow or
  light band have a caster in the render (compare against the beauty or a shadow pass, same camera)? A dark band with
  no caster is a fault, not mood. Ask it per candidate, not in the pairwise comparison.
- Evidence: ArvumElectrum-anim-work/sawmill-3d/scene/judge/ (ranking A > C > B), scene/review/picks.json (Jenny's
  note), scene/fix_shadow/ (the band and the mend); 2026-10-24.
- Scope: artwright-judge (rubric), any judge of a painted-over-render image
- Status: active · helpful 0 · harmful 1 · last_confirmed 2026-10-24

### L-012 · 2026-10-24 · A small native sprite gets a false grid and its shading ramps read as blends
- Trigger: pixelwright's make eval (a 16x16 potion recovered exactly, 10x16 after crop): `aw.py pixel` found scale 7,
  26.7% alignment, 0% uniform blocks and 7.03% transitional pixels, so a pixel-perfect result failed the gate.
- Hypothesis: a sprite this small has too few edges for the grid search, and at native scale every one-pixel step
  between two flat colours (dark, mid, light) passes the transitional test.
- Rule: a caller that knows the image is native passes `--scale 1`; at a stated scale of 1 the transitional share is
  reported, not failed. Plain `pixel` on a tiny sprite still guesses the grid; read `grid.scale` before trusting it.
- Evidence: C-20261024-2; Pixel.test_native_ramp_passes_at_stated_scale_1; the eval's potion passes with both fixes.
- Scope: skill
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24

### L-011 · 2026-10-24 · Gate a sprite's coverage against its neighbours; a size the style check only shows gets waved through
- Trigger: a painted 2x2 game building (96x96) passed `sprite` on every gated measure at coverage 0.39 while the reference work buildings sat at 0.42 to 0.62 (median 0.52); the reviewer rejected it as too small, and the project's style guide says large buildings fill their canvas. The size was even noted as a known gap and shipped anyway.
- Hypothesis: a measure that is printed but not gated reads as advisory, so the agent explains it instead of fixing it; size relative to neighbours is the first thing a player sees at 1x.
- Rule: `sprite` fails coverage under `--min-coverage` (0.9) times the references' median; pick references of the same class (work buildings for a work building). A camera fitted to ground diamonds sets the ground scale, not how big the building reads: fix the size by massing and props first, then zoom.
- Evidence: Sawmill round 1 in a private game project, 2026-10-23 (coverage 0.39, reviewer note "the size of the building seems too small compared to the other"); test Sprite.test_too_small_sprite_fails_coverage
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-24

### L-010 · 2026-10-23 · Leave transparent pixels out of value and colour statistics
- Trigger: `aw.py stats` on a 96x96 painted building sprite (Sawmill.png, a private game project) reported `clip_white` 0.478. That was the transparent share of the canvas: every measure composited the sprite on white first.
- Hypothesis: flattening on a background is right for a photograph or a painting and wrong for a sprite or cut-out, whose canvas is not part of the picture; a white composite turns the background into clipped highlights, a high value key and a grey colour cast.
- Rule: per-pixel statistics read pixels with alpha 128 and up; spatial measures (edges, symmetry, balance, composition) keep the full frame on white; every output says which in `alpha` with the transparent share.
- Evidence: Assets/Art/Buildings/Sawmill.png in a private game project (clip_white 0.4784 before the fix, 2026-10-23); tests Alpha.test_stats_skips_transparent_pixels and test_measures_skip_transparent_pixels
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-009 · 2026-10-23 · Edge precision cannot tell brush texture from a new object; a tone-fitted residual outlier at game size can
- Trigger: on a render-then-paint sawmill, per-region edge precision against the render failed six of eight regions on good paintings (roof 0.21, building 0.15), and a disc pasted on the roof did not stand out from the brushwork.
- Hypothesis: painting moves and adds edges everywhere, so precision measures texture, not shape. A new object is a patch whose tone the render cannot explain: fit paint = a times render + b per region at the size the sprite ships (96 px), and the object is a 3x3 residual far above that region's median, while texture averages away at that size.
- Rule: gate new objects on the worst 3x3 residual over the region's median residual plus 0.01 (above 5 fails) at game size; report edge precision and recall as information only.
- Evidence: a private game project's work folder, sawmill-3d/gates/geometry_gates.py on model/renders/L1_v04_1024: the render passes itself (rim_rms 0.0006), test_squashed1024.png fails ellipse and spokes, test_roofblade.png fails regions (roof 7.48), paint/trial1 L1_beauty_d45* and L1_beauty_d60_canny70* pass, L1_beauty_d60_s2310001 fails (its wheel moved); aw.py geomgate reproduces every number (2026-10-23); edge scores in gates/r.json
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-008 · 2026-10-23 · Find a painted rim by cross-correlating the ray profile with the render's, not by the strongest edge
- Trigger: a max-gradient search along each ray for the painted wheel rim jumped between the inner rim edge, the outer rim edge and the float tips from one angle to the next, so the fitted ellipse moved on paintings whose wheel had not.
- Hypothesis: a rim is several parallel edges of similar strength, and painting changes which is strongest. The render's own profile along the same ray carries all of them, so the lag that best aligns the two profiles is the rim's movement whichever edge the brush emphasised.
- Rule: along each ray from the projected centre through the projected rim, correlate the painting's gradient profile with the render's within 15% of the radius, take the best lag (8% at most), skip angles where the render shows no rim. A move bigger than the window shows as weak matches and an RMS near the window, not as its size.
- Evidence: a private game project's work folder, sawmill-3d/gates/geometry_gates.py on model/renders/L1_v04_1024: the render passes itself (rim_rms 0.0006), test_squashed1024.png fails ellipse and spokes, test_roofblade.png fails regions (roof 7.48), paint/trial1 L1_beauty_d45* and L1_beauty_d60_canny70* pass, L1_beauty_d60_s2310001 fails (its wheel moved); aw.py geomgate reproduces every number (2026-10-23)
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-23

### L-007 · 2026-10-22 · Read the failing replies before fixing a skill: the grader may be the fault
- Trigger: action-winner-fit failed 3 of 6 after a skill edit. With `--keep-temp`, two "failures" read "None of the six renders fit the brief"; the regex wanted "none of the X". The real miss was a run that never loaded the skill.
- Hypothesis: a regex written before any reply exists encodes one phrasing; models vary the wording more than the verdict. `claude plugin eval` keeps no final messages, so a failure count alone cannot tell a wording miss from a wrong answer.
- Rule: rerun a failing case with `--keep-temp`, read `out/trace.jsonl` (tool calls and the last assistant text), and test any widened regex against the real right answers and a real wrong one before committing it.
- Evidence: TESTS.md T-20261022-7
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-006 · 2026-10-22 · Trim a museum photograph's mat before any border measure
- Trigger: `comp` flagged tangents, border pull and a blocked entrance on four of seven Cleveland images; every one was the paper, mat or grey backdrop round the work, not the art.
- Hypothesis: collection photographs frame the object with a uniform margin; a border measure reads that margin's edge as a contour on the frame. AI stills have dark vignettes and plain skies that look the same to a loose test.
- Rule: trim only when all four sides have a uniform band that ends before an eighth of the side and three of them are light; report what was trimmed (`margin_trimmed`).
- Evidence: ai-docs/decisions/2026-10-22-books-track5.md E3
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-005 · 2026-10-22 · A degrade kind must force its direction, never match a target
- Trigger: on six real images, `haze-off` lowered the far band's contrast on four. It matched the far band to the near one, and there the far band was already crisper. `tangent` drew a black line that vanished on a dark poster. The synthetic tests passed.
- Hypothesis: a degradation defined as "make A equal B" moves either way depending on where the image starts; only "push A past B" is a broken input on every image.
- Rule: define each kind as a push with a floor (at least 1.3 times; ink opposite the mean). Check it on real images as well as the drawn fixture.
- Evidence: ai-docs/decisions/2026-10-22-books-track5.md E5
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-004 · 2026-10-22 · Set a new flag's threshold from how often it fires on real images
- Trigger: thresholds taken from the book notes flagged `competing_focal` on 32 of 48 AI stills, `frame_tangent` on 31 and `blocked_entrance` on all seven museum works.
- Hypothesis: a sketch's threshold is a guess about one picture; a pointer that fires on most pictures carries no information, whatever its theory.
- Rule: before shipping a flag, run it over a mixed real set (museum works and AI stills) and set the threshold so it fires on a minority. Publish the rate beside the rule, labelled uncalibrated until owner labels exist.
- Evidence: ai-docs/decisions/2026-10-22-books-track5.md E2
- Scope: repo:artwright
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-003 · 2026-10-22 · Put a looping eval batch in a script file; never inline `$var` in `wsl -- bash -lc '...'`
- Trigger: `wsl -d Ubuntu -- bash -lc 'for c in a b c; do bash scripts/eval-wsl.sh "$c" ...; done'` from PowerShell ran the whole suite on every pass: `$c` arrived empty, `eval-wsl.sh` fell back to its `*` default, and four full-suite passes spent about $14 before it was stopped.
- Hypothesis: wsl.exe hands the joined command line to the distribution's login shell, which expands `$c` once before `bash -lc` runs the loop.
- Rule: write the loop to a `.sh` file and run `wsl -d Ubuntu -- bash /mnt/<path>/file.sh`; a case glob has no character classes either (one family per call).
- Evidence: T-20261022-2
- Scope: repo:artwright, env:windows
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-22

### L-002 · 2026-10-21 · Name the cheap mechanical jobs in the description, and name who owns their neighbours
- Trigger: "main colours and their shares" and "show these side by side" never fired a skill (0/3 each): the model wrote PIL scripts. Adding colours and contact sheets to the hub description fixed it, and at once pulled brand-palette and website requests in (2 of 9 decoy runs) until brandwright and sitewright-direction were named as owners.
- Hypothesis: a model only reaches for a skill for a job it believes it cannot do alone; plain image chores look easy, so the description must name them. Naming a broad noun (colours) widens the catch, so the exclusion must sit beside it.
- Rule: when a description adds a broad trigger noun, add the sibling that owns its neighbours in the same edit, and re-run the decoys.
- Evidence: T-20261021-3, C-20261021-3; again T-20261022-6 ("is the light consistent" answered by eye until the description named light)
- Scope: skill
- Status: active · helpful 2 · harmful 0 · last_confirmed 2026-10-22

### L-001 · 2026-10-21 · Shell eval cases need WSL2, a scaffold and `tool: Bash`
- Trigger: the action cases failed three ways in one session: native Windows refused the Bash grant (no sandbox backend); under WSL2 each run started in an empty workspace, so the fixture paths did not exist; and the `tool_used` grader with `tool: Bash|PowerShell` counted 0 calls although Bash ran.
- Hypothesis: `claude plugin eval` runs each case in a fresh temporary home and cwd, matches `tool` as a literal name, and needs an OS sandbox for shell tools. 2.1.307 makes every Bash path read-only in eval runs (a sibling plugin's finding), so the pinned 2.1.281 copy under WSL is the working harness.
- Rule: shell cases run under WSL2 with `~/.local/share/claude-pinned/claude-2.1.281 plugin eval . --scaffold --allow-tools Bash ...`; each case carries `case.yaml` with `context.scaffold_script: fixture.sh` (written by `python evals/fixtures/make_fixtures.py --emit-scaffold`); graders name `tool: Bash`.
- Evidence: T-20261021-2
- Scope: repo:artwright, env:windows
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-21

<!-- Example (delete once you have a real entry):
### L-001 · 2026-10-21 · One-line lesson in plain words
- Trigger: what happened, with dates or counts
- Hypothesis: why
- Rule: the shortest instruction that prevents the trigger
- Evidence: C-20261021-1, T-20261021-1, confirmed 2026-10-21
- Scope: skill | repo:<slug> | env:<name> | global
- Status: active · helpful 1 · harmful 0 · last_confirmed 2026-10-21
-->
