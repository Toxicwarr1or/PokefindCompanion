---
title: "NewDialog vs SendMessage"
subtitle: "When to use each — the gen5 modern voice rule"
date: 2026-04-27
---

## The rule

- **`NewDialog`** = interpersonal speech. A character is talking to someone. Always paired with a colored speaker name.
- **`SendMessage`** = the world speaking to the player. Atmosphere, sights, sounds, smells, time-passage, internal sensory beats. Italicized with `&o`. No speaker.

Mixing these is the most common voice-breaking mistake when writing in the gen5 modern style.

## Examples

### NewDialog (interpersonal)

```json
"NewDialog": [
    {
        "&b&lN": "You came south. I thought you might."
    }, 60, true, true, "male_normal"
]
```

### SendMessage (atmosphere / world)

```json
"SendMessage": [
    "&7N is sitting at a low fire on the edge of the eastern ruin field, a stick in his hand, sketching wind diagrams in the dust at his feet."
]
```

### Internal vocalized thought (rare — use NewDialog with `[PLAYER]`)

```json
"NewDialog": [
    {
        "[PLAYER]": "&oHmm, this Pokémon seems to be guarding the cave! I have to get past!"
    }, 60, true, true
]
```

### Truly unspoken thought (SendMessage with `&o`)

```json
"SendMessage": "&7&oYou think about Iden Vesh, whom you have never met."
```

## Why it matters

Older gens (1–3) used a flat `Dialog` array convention; gen4–5 are NewDialog-first. When writing modern (gen5) content, NewDialog is required — the established voice depends on it.

## See also

- [Found-text framing pattern](#) — how to use letters/markers/books to deliver backstory without exposition dumps
- [No villain monologue](#) — antagonists show alignment through action, not speech
