# Moving Miso to another Claude account

Written 2026-10-14. The old account is ddgsignin@gmail.com.

## What moves on its own and what doesn't

| Thing | Where it lives | On the new account |
| --- | --- | --- |
| The repo, `CLAUDE.md`, `claude-handoff/` | Your disk (`E:\Work\Projects\miso`) | **Carries over automatically.** Any account that opens this folder reads the same files |
| Git history, branch `thj/home-test` | Your disk | Carries over (git uses your git identity, not your Claude account) |
| Claude project "Miso" (8 docs, instructions) | Old account | **Must be recreated** (step 3) |
| "Miso Home System" doc (Design, Demo Spec, Build Log, M9 tabs) | Old account | **Share it or recreate it** (step 4) |
| Project memory | Old account | Lost. It can't be moved; the docs hold the real state |
| Chat and task history | Old account | Stays there. Exports can't be imported into another personal account |
| Connectors, skills, preferences, scheduled tasks | Old account | Re-add by hand (step 6) |

## 1. Before you switch (still on the old account)

1. The export in this folder is done: the Build Log and the Design tab are now on disk, and the other two tabs already were.
2. Optional archive of your chats: claude.ai → Settings → Privacy → **Export data**. You get an email link that expires in 24 hours. It's for your records only; it can't be loaded into the new account.
3. Decide what to do with the "Miso Home System" doc (step 4). If you want to keep the same doc, share it with the new account's email **with edit access** now, while you're still signed in to the old one.

## 2. Switch accounts on this computer

- **Claude desktop app:** click your initials (bottom-left) → **Log out**, then sign in with the new account's email. If the new account is a Team or Enterprise account under the *same* email, you don't need to log out: the same initials menu lists both accounts, and you pick one.
- **Claude in Chrome** (the browser extension) has its own sign-in: sign out there too and sign in with the new account, or Claude in the new account can't drive your browser.
- **Claude Code in a terminal** (if you use it): run `/logout`, then `/login`.
- Nothing in the repo needs to change for the switch itself.

## 3. Recreate the "Miso" project

1. Projects → **New project**, name it **Miso**.
2. Paste the description and instructions from `project-settings.md` (next to this file).
3. Upload the 8 files listed there from `claude-handoff/`. Optionally add the Demo Spec, the M9 file and `Miso-Home-System_Build-Log.md`.

## 4. The "Miso Home System" doc

Pick one:

- **A. Keep the same doc (recommended if sharing works).** After sharing it with edit access in step 1, open the link from the new account and check you can edit it. `CLAUDE.md` and the notes keep working as they are.
- **B. Make a new doc.** On the new account, ask Claude: *"Create a doc called Miso Home System with four tabs (Design, Demo Spec, Build Log, M9 Readability Pass) from these files in claude-handoff/."* Then replace the old link (`https://claude.ai/artifact/9Fi2AJKcLbf1e7evrkMxXN`) with the new one in `CLAUDE.md`, `claude-handoff/README.md` and `claude-handoff/home-system-handoff.md`. Until you do, Claude on the new account will try to open a doc it can't read.

## 5. First session on the new account

1. In the desktop app, start a new task, link it to this computer and pick the folder `E:\Work\Projects\miso`. `CLAUDE.md` loads from there, so your rules (git, tests, statics, line endings) apply from the first message.
2. Attach the new "Miso" project to that task.
3. Sanity check: ask *"Read claude-handoff/home-system-handoff.md and tell me the last commit."* It should say `e1a2deca8` (Oct 14, Hungry Moon).

## 6. Re-add what was tied to the old account

- Connectors (e.g. GitHub) under Settings → Connectors.
- Any custom skills, styles or personal preferences.
- Any scheduled tasks (they run as the old account and stop being useful once you stop using it).

## 7. Keeping things in sync from now on

- **The folder is the source of truth.** `claude-handoff/` and `CLAUDE.md` are plain files on your disk, so every account and every session sees the same version. Keep writing notes there first.
- **Then mirror to the project.** When Claude changes one of the 8 notes, have it write the same text to the new project doc. You can make it automatic by adding a line under "Notes in `claude-handoff/`" in `CLAUDE.md`, e.g. *"After editing a note that also exists in the Claude project, write the same text to the project doc."*
- **Build Log** keeps the same flow: new sections go into `Build-Log_additions.md`, then get folded into the Build Log tab of whichever doc you chose in step 4.
- **Stop working in the old account.** Two accounts writing to two projects will drift; the folder is the only thing they share. If you need something from an old chat, open it on the old account read-only.

Sources: [Export your Claude data](https://support.claude.com/en/articles/9450526-export-your-claude-data), [Log in to your Claude account](https://support.claude.com/en/articles/13189465-log-in-to-your-claude-account).
