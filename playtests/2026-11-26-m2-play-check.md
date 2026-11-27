# M2 The River: THJ's first play check (2026-11-26)

Level `GB_m2-river` (chunk 3.2, `reports/onboarding-3-2-m2-river.md`), uncommitted. THJ's notes, as given:

1. Lucy's follow-up does not attack worms: they die and nobody is on that tile at that moment. When the new worm child spawns in its place, Lucy no longer attacks it.
2. Lock the John–Lucy Duo.
3. Explain "Sheltered by John".
4. After beat 1, Lucy should also move automatically to a tile from which her primary (embers) reaches John's shield.
5. Hint Lucy's fireball (Fire Embers) just after Lucy runs into John's reach.
6. THJ tweaked the level: deleted the last right column, and added tiles to the second chunk that lead out of it (corridors). After all chunk 2 enemies are defeated, the Archer at 12,2 escapes toward one exit and disappears, a horn sounds, then the other 4 Archers (sitting at the ends of the corridors) run toward the main part of chunk 2 and stay there (e.g. the Archer at 15,-3 runs to 13,0), and a wave of worms and Claws spawns in the middle. After defeating all, the level ends.
7. Add a health potion to the inventory and tutorial it after the ambush begins. The HP tutorial here and in M1 are the same; only one should show. M1 and M2 can be played in either order, so the first one the player sees cancels the other.

## THJ's prefab after the tweak (tool read, prefab coordinates; bottom row y = -3)

```grid id=m2-river-thj title="GB_m2-river after THJ's tweak (prefab coordinates, y from -3)"
_ _ _ _ _ _ a . . _ _ _ _ . . a
_ _ _ _ _ _ _ _ . _ _ _ _ . _ _
_ _ _ _ _ _ _ _ . _ _ _ _ . _ _
_ _ . . . . . _ . . . . . . _ _
_ . . . . . c _ c . c . . . _ _
U J . . . w . . . . . . a . _ _
_ . . . . . c _ c . c . . . _ _
_ _ . . . . . _ . . . . . . _ _
_ _ _ _ _ _ _ _ . _ _ _ _ . _ _
_ _ _ _ _ _ _ _ . _ _ _ _ . _ _
_ _ _ _ _ _ a . . _ _ _ _ . . a
--
level hidden ring 8,3 10,3 8,1 10,1 12,2
```

Note: the drawn rows here start at y = -3, so the clearing row with Lucy is y = 2 as in the wiring. Tool notes: the five `ring` units are active in the prefab (expected inactive); 5 Archer Goblins (12,2 in the ring; four at the corridor ends 6,7 · 15,7 · 6,-3 · 15,-3, not hidden, so alert from the start), 6 Dark Claws, 1 Dark Worm.
