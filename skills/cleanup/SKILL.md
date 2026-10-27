---
name: cleanup
description: >-
  Cleans up the codebase, a branch, a range, or a set of paths in a loop: finds the dirtiest areas
  with the hotspots skill, reviews each with the inspect skill, fixes the findings, and reviews again
  until clean. Edits files and commits. Use when the user asks to clean up, tidy, or do housekeeping
  on the codebase or an area of it.
argument-hint: "[types=bugs,reuse,design,simplify,dead,tests,sense] [<range>] [<paths>...] [-- <notes>]"
---

# Cleanup

Review and fix the dirtiest areas of the code, one at a time, until each review comes back
clean. Unlike the hotspots and inspect skills, this skill edits files and commits each fix.

## Commands

Prefer plain commands, one at a time, to avoid permission prompts: no pipes, `&&`, redirects, or
`$(...)`.

## Arguments

All optional, the same for the hotspots, inspect, and cleanup skills:

- `types=` and a comma-separated list of review types (e.g. `types=simplify` or
  `types=bugs,reuse`), from `bugs`, `reuse`, `design`, `simplify`, `dead`, `tests`, `sense`. An
  unknown type: ask instead of guessing.
- A git range (e.g. `main...`, `HEAD~5..`, `main...feature-x`).
- Paths (e.g. `src/api src/db/models.py`): files, directories, or a mix. Drop a leading `@` (a
  Claude Code file mention).
- Free-text notes, last: everything after a standalone `--` (e.g. `-- See .temp/plan. Increment
  1 only; 404 masking is intentional`). Paths inside the notes (specs, plans) are background
  reading, not code to review.

Before the `--`, an argument that exists on disk is a path. Otherwise, one that `git rev-parse`
accepts is a range. Anything else: ask instead of guessing.

Pass all of them on to the hotspots and inspect skills. Without `types=`, each area gets the types
the hotspots skill suggests for it.

## Before you start

- The hotspots or inspect skill is not installed: say to install them with
  `npx skills add hernancerm/upkeep`, and stop.
- The working tree has uncommitted changes: say so and stop, so the user's own work does not end
  up in your commits.
- The range ends on a branch that is not checked out (e.g. `main...feature-x`): say to check it
  out first, and stop. Fixes go on the current branch.
- A range: turn its start into a hash now (`git merge-base <a> HEAD` for `<a>...`, else
  `git rev-parse <start>`), and use `<hash>..` from here on, so each review also covers your fix
  commits.
- Read `git log` to learn the repo's commit message style.

## Pick the areas

Run the hotspots skill once with the arguments and take its areas, dirtiest first. Do not run it
again during the loop: it always finds something, so the loop would never end. It found nothing:
say so and stop.

## Loop over each area

1. Run the inspect skill with the area's types, the range if any, and the area's paths. Print its
   findings in full, so the user sees what each round fixes, then go on without waiting for them.
2. Fix every finding except the ones marked as a guess and the `sense` ones (they add behavior,
   which is the user's call), one at a time. Follow the repo's rules file and keep behavior the
   same unless the finding is a bug. Skip a fix that would break something or that you are not
   sure about, and say why. After each fix:
   1. Run the repo's tests or linters for the files you touched, if it has them. Fix what you
      broke.
   2. Commit it on the current branch: `git add <paths>`, then `git commit`, in the repo's
      message style. One commit per fix, so each can be reverted alone. Findings that share one
      fix share one commit. Never push.
3. Run the inspect skill again on the same area, with the same arguments. Print its findings the
   same way.
4. New findings: go back to step 2. Stop after 2 rounds of fixes, so two fixes can't undo each
   other forever.

## Report

For each area:

- The paths, and whether it ended clean.
- Your commits, one line each: short hash and subject.
- What you left: guesses, `sense` findings, skipped fixes, and findings still open after 2
  rounds, with `file:line` and why.
- The tests or linters you ran, and the result.
