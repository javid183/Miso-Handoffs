# Narrative: the writer's sheet

Owner: coordinator (the sheet's shape); the narrative designer writes in it. Scope `thj/onboarding-demo`.

`narrative-sheet.xlsx` holds every line, tutorial page, name and bark the onboarding demo shows, each with the file it lives in, taken from the project on 2026-11-24. The writer fills the yellow columns; Claude imports the rows marked Final. Task IDs come from the tweak doc (`design/demo-tweaks-snapshot.md`); the plan is `plans/2026-11-22-onboarding-demo.md`.

## Tabs

| Tab | Rows | What it holds | Files (under `miso/Assets/_Project/`) |
| --- | --- | --- | --- |
| Read me | — | How to use the sheet, legend, progress counts | — |
| Tasks | 21 | The map: each narrative task, where it plays, its files, whether its container is built | — |
| Lines | 274 | Every dialogue line in the demo's sequences | `Resources/Sequences/{Hearth, HomeVisits, M1Ridge, Search, SistersTally, Mission 4, Intro}/**/*DialogNodeSequence.asset` (`sequenceNodes[n].Text`, speaker from `characterData`) |
| New lines | 14 | Lines with no container yet (Mary's hand-offs, the Hearth ending, Toba in M3, the house's reaction, M4's end, Kevin, Ben, Mary) | Claude creates them |
| Tutorial pages | 10 | The 8 built pages plus the Cyclone steer page (H-21) and the skill tree page (X-18) | `**/*_Panels.asset` (`pages[n].pageTitle`, `pageText`; pages also take an `image` and a `videoClip`) |
| Names and text | 51 | Mission names and descriptions (W-01), every ability title and description (X-16), enemy names (X-05), Mark's description (W-07), the quiver item (X-08) | `Content/Levels/*.asset`, `Resources/UnitSpecific/Player/<hero>/**/*.asset` (`title`, `description`) |
| Barks | 785 | Every bark line, plus 8 empty rows for Synergy barks (X-02) | `Resources/BarkSystemData/**/*.csv` (columns `Unit, Weight, PlayOnce, Dialogue[, Tag]`) |

Rows whose Container says **Hold** (M1 is being redesigned; memory 2 is THJ's, D-643) or **To be rebuilt** (M2, M3, M4) are grey: the writer writes for the moment, and Claude places the text when the level is rebuilt.

## Statuses

Draft (still working) · Final (ready to import) · Keep (no change) · Cut (remove; Claude asks THJ before deleting a node).

## Import (Claude)

1. Read the sheet; take the rows marked Final.
2. For each row, open its File and check the node still holds Current text. If it differs, someone edited it in Unity after the snapshot: skip the row and list it for THJ (dialogue edited in Unity wins, D-526).
3. Write New text (and New speaker, when set) into the node, or the page, field or CSV row. Rows in grey tabs wait for their level's rebuild.
4. New lines: build the container first (the chunk that owns it), then write the text.
5. Report what was imported, skipped and waiting; compile, run the covering tests, and update the snapshot with `extract_lines.py`.

An import script would make step 2 and 3 safe and repeatable; it is a new tool, so it waits for THJ's OK (plan chunk 4.7).

## Refreshing the sheet

`extract_lines.py` reads the project and writes the raw rows to `_extract.json` (scratch, not committed); `build_sheet.py` builds the sheet from them. Rebuilding writes a fresh sheet, so once the writer has started, Claude carries the writer's columns over by Line ID (and Page ID, Bark ID) instead of overwriting them.
