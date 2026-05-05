# Codex Pet Generator

<p align="center">
  <img src="assets/demo.gif" alt="Codex Pet Generator — workflow and final pet running in Codex UI" width="720">
</p>

Reusable skill for building Codex desktop pets without getting trapped by broken full-sheet generations, unreadable micro-gestures, scale drift, or naive slicing.

This package turns pet creation into a repeatable workflow:

- character bible first
- row semantics second
- tiny-UI readability before polish
- approved vs unapproved gating
- manual slicing with explicit guidance (no automated slicer)
- deterministic packing of per-frame inputs
- validator before install (sheet + `pet.json` install contract)

## What This Solves

The common failure mode is simple:

- a generated strip looks fine when large
- but the app needs a tiny, loopable sprite
- then the result collapses into crop bugs, stretched rows, muddy gestures, extra limbs, or wrong semantics

This skill encodes the fixes for those problems.

## What's Included

```text
codex-pet-generator/
  SKILL.md
  README.md
  LICENSE
  requirements.txt
  agents/openai.yaml
  references/
    row-semantics.md
    acceptance-checklist.md
    packing-and-slicing.md
  scripts/
    pack_codex_pet.py
    validate_codex_pet.py
```

## Core Ideas

1. Treat each row as one loopable state machine, not eight poses.
2. Design for tiny UI readability, not for large preview beauty.
3. Keep explicit canon anchors for scale, standing body, seated body, and prop language.
4. Mark every candidate `approved` or `unapproved`.
5. Never trust naive equal-column slicing unless the strip geometry is actually uniform.

## Install as a Skill

Copy or symlink this folder into your Codex skills directory under a stable name such as:

```text
~/.codex/skills/codex-pet-generator
```

Then invoke it in prompts as:

```text
Use $codex-pet-generator to turn these character refs into a validated Codex desktop pet.
```

## Typical Workflow

1. Gather character references.
2. Write the character bible.
3. Define all 9 row semantics.
4. Generate one row strip at a time.
5. Reject bad rows early.
6. Approve exactly one candidate per row.
7. Extract frames into per-row directories — manually, using the slicing guidance in `references/packing-and-slicing.md`. The skill does not ship an automated slicer.
8. Pack the final `1536x1872` sheet with `scripts/pack_codex_pet.py`.
9. Validate the sheet and `pet.json` with `scripts/validate_codex_pet.py`.
10. Install under a new pet id.

## Included Scripts

Install dependencies first:

```bash
pip install -r requirements.txt
```

Pack frames:

```bash
python scripts/pack_codex_pet.py <rows-root> <output.webp>
```

Validate the result:

```bash
python scripts/validate_codex_pet.py <spritesheet.webp>
```

## Publishing Notes

- This folder is licensed under MIT.
- If your local copy contains private example projects, references, or client material, remove those before publishing your bundle.
- The shareable core is the generic skill itself: `SKILL.md`, `references/`, `scripts/`, `agents/openai.yaml`, and `LICENSE`.

## Tweet-Sized Summary

> I made a Codex pet creation skill that stops desktop mascot generation from turning into 72-frame roulette: row semantics, tiny-UI readability, approved/unapproved gating, safe slicing, deterministic packing, validator, install.

## Author

By [Daniil Makeev](https://wyddy.tech) — AI Engineer.

GitHub: [wyddy7](https://github.com/wyddy7)
