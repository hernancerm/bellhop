---
name: inspect
description: >-
  Reviews the user's code changes (or given files) for bugs, duplication, design problems, ways to
  simplify, dead code, bloated tests, and what a change of that kind usually needs but is missing,
  and gives feedback without editing files. Use when the user asks to review, simplify, shorten, or
  clean up their diff, changes, branch, or work before committing or opening a PR.
argument-hint: "[types=bugs,reuse,design,simplify,dead,tests,sense] [<range>] [<paths>...] [-- <notes>]"
---

# Inspect

Review the user's changes and report findings. The user writes and owns the code, so never edit
their files: describe each fix, and show code only when it is a few lines.

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

Here, `types=` means: run only the listed types. Without it, run them all.

## Commands

Prefer plain commands, one at a time, to avoid permission prompts: no pipes, `&&`, redirects, or
`$(...)`.

## Get the code

- A range: review `git diff <range> -- <paths>`.
- Only paths: review those files whole, as they are now.
- Neither: review the user's current changes, committed on this branch or not. Find the default
  branch (`git symbolic-ref refs/remotes/origin/HEAD`, else `main` or `master`), run
  `git merge-base HEAD <default>`, then review `git diff <that hash>`. Add new files from
  `git status --short`, since the diff leaves them out. Nothing changed: say so and stop.

## Before any type

- Read the free-text notes and any files they point to. Skip findings that they mark as
  intentional, required for parity, or out of scope for the current step.
- Read the surrounding code, not just the changed lines: callers, tests, and the rules file
  (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) if the repo has one. A suggestion must fit how the repo
  already does things.
- Skip style nits that a formatter or linter would catch.

## Types

### bugs

Issues the diff causes within itself: missed cases (null, empty, errors, concurrency), missing
tests, and breaks of the repo's own rules. What the change leaves out entirely belongs to `sense`.

### reuse

The user cares about duplication as much as bugs. Every piece of logic or data should have one
owner. For each thing the diff adds (a function, class, component, type, field, piece of state,
constant), search the repo and ask: does this already exist, or can it be derived from something
that does? If so, name the existing owner and its file, and say how to reuse, extend, or derive
from it. This also covers repetition within the diff itself.

### design

Will the next likely change be easy? Flag what makes it hard, e.g. adding one more case means
editing several places, a hardcoded assumption that will stop holding, or logic placed in the
wrong layer or owner. Name the concrete future change that would hurt; skip needs that are only
hypothetical.

### simplify

Make the code simpler while it keeps doing exactly the same thing. Two goals, in this order:

1. Easier to understand: fewer concepts, cases, and moving parts a reader has to hold in their
   head.
2. Fewer lines of code.

When the two clash, pick the easier one to understand. Never cut lines in a way that makes the
code harder to follow (e.g. clever one-liners).

- Look for: checks that can never fail, deep nesting that early returns can flatten, branches
  that can merge, hand-written logic the language, stdlib, or an existing helper in the repo
  already does, layers or abstractions with one caller that add nothing, and names that hide what
  a thing is. Unused code belongs to `dead`.
- Every suggestion must keep behavior the same, including edge cases (null, empty, errors). If you
  are not sure it does, say what could differ.
- Skip changes that only swap one style for another of equal length.

### dead

Code under review that nothing uses or reaches: unused functions, classes, variables,
imports, parameters, and config, branches that can never run, and commented-out code. Before you
call it dead, search the whole repo for what a symbol search misses: config keys, strings, dynamic
lookups, other languages or tools, and public API that code outside the repo may use. Unsure: mark
it a guess.

### tests

Can the tests in the diff be fewer lines of code and keep their value? A test's value is the bugs
it would catch. Look for:

- Tests that differ only in inputs and expected values: merge them into one parameterized test,
  the way the repo's test framework does it.
- Tests that pretend to test something but do not: e.g. mocks so heavy the test only checks the
  mocks, or convoluted unit tests for behavior that only an integration test can check. Say to
  remove them, and name the integration test to write instead if one is worth it.
- Low-value tests: they check the language, a library, or trivial code, or repeat what another
  test covers. Name the test that already covers it.
- Setup repeated across tests that a fixture or helper (new or already in the repo) can own.

Never cut a test that catches a bug no other test catches.

### sense

What a change of this kind usually needs but the diff leaves out. Ask what an experienced
engineer would expect from it, e.g.:

- An HTTP client with no connect or read timeout.
- A retry with no backoff or limit.
- A new endpoint with no auth check or input validation.
- A cache with no expiry or size limit.

Point at how the repo or library already does it, if it does. Skip what the repo leaves out on
purpose (e.g. a comment or its rules file says so).

## Report

- Findings ranked most severe first. Rank `simplify` findings by how much easier the code gets to
  understand, then by lines saved. Rank `dead` and `tests` findings by lines saved.
- For each: the type in brackets (e.g. `[bugs]`), `file:line`, and the problem in one sentence.
  Then, for bugs, a concrete input or state that triggers it; for design, the change that would
  hurt; for simplify, why the result is simpler; for dead, what you searched to show nothing
  uses it; for tests, what value is kept and about how many lines go; for sense, what goes wrong
  without it.
- Mark a finding as a guess when you could not confirm it from the code.
- No findings: say so plainly. Do not invent issues to fill the report.
