# `thj/onboarding` commits that belong in `main` (2026-11-04)

Explore, read-only, for `linda-memory-tuning` (c). Branch = `main` + 48 commits; `main` has none the branch lacks. Not verified by a cherry-pick run.

## MAIN, in cherry-pick order

1. Grid level tool + level tooling, in branch order (they depend on each other): `81897bb7c`, `eb40ebcd5`, `459f41428` (needs `eb40ebcd5`'s `AssignBoundary`), `32f532e49` (core: `LevelBase.cs`, `PlayModeStaticReset.cs`; sandbox the grid window's Play uses), `29cad27cb`, `24bfcea3e`, `9d3ac5623`, `652f2075e` (split), `fa6af3fab`, `08cdf7035` (core: `LevelBase.cs`, after `32f532e49`), `16eee4aad`, `3c99b3ee6` (split or whole), `3153906dd`, `6184486d4`.
2. Independent, any order: `c4f85e804` (Dark Claw starts-alert variant; optional), `8826a11f1` then `106edafec` (Mark's right-hand socket + default gear; general per D-369; hunks separate from `bb9982c87`'s `unlockedAfterMission` line), `59c5a6a25` (skill tree opens on a hero / highlights a node), `35ed82daa` (selected tab look; doesn't need `59c5a6a25`).

## Splits

- `652f2075e`: take `GB_11-spread-pools`, `GB_24-nook`, `GB_27-snare`, `GB_33-deev-wave`; leave `GB_m1-linda`.
- `3c99b3ee6`: grid tool's hidden line uses `HiddenLevelUnits` (`Features/Onboarding`). Recommended: take the whole commit incl. `HiddenLevelUnits.cs`, `RevealUnitsSequence.cs` (general mechanic). Stripping it makes `6184486d4` conflict.
- Tests in `Features/Onboarding/Editor/` (`MarkWeaponSocketTests`, `SkillTabSelectedSizeTests`): folder `.meta`s arrive only in `509a634dc`. Either move the tests or also pick the two folder metas, else GUID clash on a later merge.

## Uncertain (ask THJ)

- `a7320be82` Catch & Return open from the start: game-wide design change made for the opening.
- Onboarding level components, reusable but onboarding-only today: `c772bbf34` run upgrades at level start, `ba7d19e66` + `3835af7f6` ability button hint, `8a443d66c` turn AP cap, `eda1d6df6` sleeper sight beat.
- `GridToLevelTests.Parser_EveryBlockInTheOnboardingLevelsParses` reads a handoff file; `Assert.Ignore` if missing, harmless on `main`.
- `6acefb6c0` (HomeVisits test fix) is onboarding-only.

## Onboarding-only (stay on the branch)

`38bc7db73`, `bb9982c87`, `f36da02f8`, `509a634dc`, `c772bbf34`, `a161e0956`, `9ace80c28`, `848a67fd2`, `911a5def2`, `59103e227`, `ba7d19e66`, `8a443d66c`, `29cbcd7ed`, `3835af7f6`, `1bf976b13`, `3289158db`, `a7320be82`, `eda1d6df6`, `51f109672`, `d72204178`, `cafb8de97`, `f6648ed08`, `67b07c7f8`, `b2659da27`, `cb85c30fe`, `6acefb6c0`, `4dd76b498`, `14330fd06`, `1f3df84ac`.

## Added 2026-11-04 (linda-memory-tuning)

- `83aa585f0` shared objective condition checker/tool/tests (editor-only, general).
- `9ba3b8421` `Level2-C2` split (data; after `83aa585f0`). On `main`, run the scan test; split any other level it flags.
- `266a3985c` level ability lock (general, `Features/Levels/AbilityLock` + bar partial).
- `ccfbb36d2` Encore pulse while the quiver is empty (general; needs `266a3985c`).
- `87174b9fc` (THJ) Encore icon and text + `7a1674008` cost back in the text (data, general; **confirmed D-386**).
- `89f4981fe` Level1-C1-2 sprites under Environment (THJ) + GB_m4-mark startMode default. **Goes to `main` (D-386)**; split out the `GB_m4-mark` part (onboarding-only file) when cherry-picking.
