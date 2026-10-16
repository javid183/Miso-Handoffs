---
name: miso-tech-plan
description: Technical-director checklist for turning an approved Miso feature, bug or tool into an implementation plan in claude-handoff/plans/. Use when the coordinator plans any code work of size M or L.
---

# Writing a Miso tech plan

A tech plan is what the implementer builds from, the reviewer checks against, and the verifier tests. It must be complete enough for an agent that has seen nothing else. Write it from `claude-handoff/templates/plan.md`.

## 1. Understand before planning

- Read the request, the approved design plan (if any), and the decisions it rests on.
- Read the code you expect to change. Use Explore for wide sweeps; read the key files yourself.
- Check `tech/core-systems.md`. List every core system the work touches. **Changing a core system's public API or behavior is Tier 3**: stop and ask THJ before finishing the plan.
- Check `branches.md`. Set `Branch:` to `all` or the current branch, and note settings that differ by branch (e.g. `pointConsumptionMode` FTP vs ATB, `aPConsumptionMode`).

## 2. Break it into chunks

- Each chunk is buildable and checkable on its own (compiles, has a visible or testable result).
- Order chunks so the riskiest one comes first.
- One chunk = one implementer run. Don't plan chunks for parallel writers.
- For each chunk: goal, files likely touched, acceptance criteria, model (`opus` if it touches a core system or is subtle, otherwise `sonnet`).
- Shape chunks so they become clean commits: independent units apart, core-system and risky changes in their own chunk, so each can be reverted alone.

## 3. Name the risks this project always has

Go through each; write down the ones that apply and how the plan handles them:

- [ ] New statics, singletons or caches → play-mode reset (domain reload is off).
- [ ] Code the AI reads → worker-thread safe, no Unity-object APIs.
- [ ] Serialized field renames → `[FormerlySerializedAs]`.
- [ ] Saved data shape changes → migration, or THJ's OK.
- [ ] Assets, prefabs, scenes → small YAML edits, or an editor script for anything non-trivial.
- [ ] AI content touched → `AIRegressionTest` will move; say whether the plan includes a deliberate re-baseline (only with THJ's OK).
- [ ] Event subscriptions, coroutines that hide or lock state → cleanup on abort.
- [ ] Other branches that will need the same change.

## 4. Define done

- Acceptance criteria: checkable outcomes, not activities. "The Workshop report card shows the ordered weapon's icon" beats "add icon support".
- Test plan: which criteria get EditMode tests, which need quiet checks, which need a play session (and therefore THJ's time). If the work touches M2's win path, per-level drops or rollback, include a win playthrough.
- Docs to update: which `tech/`, `design/` or other docs change, and who owns each.

## 5. Check the plan before dispatch

- Tier: does anything in the plan fall in THJ's areas or the Tier 3 list? If so, it's asked before dispatch, not after.
- Could someone who has read only this plan, `CLAUDE.md` and `conventions.md` build it? If not, add what's missing.
- Is anything in scope that the request didn't ask for? Remove it or flag it.
