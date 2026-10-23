---
name: inspect
description: >-
  Args: [types=bugs,reuse,design,simplify,dead,tests,blast] <diff command>. Reviews the user's
  own code changes for bugs, duplication, design problems, ways to simplify, dead code, bloated
  tests, and what they break outside the diff, and gives feedback without editing files. Use
  when the user asks to review, simplify, shorten, or clean up their diff, changes, branch, or
  work before committing or opening a PR, or asks for the blast radius of a change or what it
  could break.
argument-hint: "[types=bugs,reuse,design,simplify,dead,tests,blast] <diff command>"
---

# Inspect

Review the user's changes and report findings. The user writes and owns the code, so never edit
their files: describe each fix, and show code only when it is a few lines.

## Arguments

The user may start with `types=` and a comma-separated list of review types (e.g.
`types=simplify` or `types=bugs,reuse`), then the command that outputs the code. Run only the
listed types. Without `types=`, run `bugs`, `reuse`, `design`, `simplify`, `dead`, `tests`.
`blast` runs only when listed, since it runs code and costs the most. When the user asks what a
change could break, run `types=blast`. An unknown type: ask instead of guessing.

## Commands

Prefer plain commands, one at a time, to avoid permission prompts: no pipes, `&&`, redirects, or
`$(...)`.

## Get the diff

Run the git command the user gave (e.g. `git diff main...`), or another command they gave which
outputs code, and review its output. If they gave none, ask for it instead of guessing.

## Before any type

- Read the surrounding code, not just the changed lines: callers, tests, and the rules file
  (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) if the repo has one. A suggestion must fit how the repo
  already does things.
- Skip style nits that a formatter or linter would catch.

## Types

### bugs

Issues the diff causes within itself: missed cases (null, empty, errors, concurrency), missing
tests, and breaks of the repo's own rules. What it breaks outside the diff belongs to `blast`.

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

Code in the given output that nothing uses or reaches: unused functions, classes, variables,
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

### blast

Issues the diff causes outside itself. Listing callers is not the job: grep does that in a
second. The job is the breakage grep won't show. Adapted from poteto's pstack (MIT).

A writeup that sounds right reads as convincing whether or not it is true. For each fact the
change's safety depends on, get it as far down this list as is cheap, and say where it stopped:

1. You said so. Worthless on its own.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You walked the failure step by step and showed it can't be reached.
4. You ran it: a script or test that calls the real code and fails loud if you're wrong.
5. You reproduced it in the running app or tool.

Steps:

1. Read what the change now does differently, including the part the diff doesn't spell out.
2. Find the one fact it is safe because of. Most risky-looking changes are safe because of a
   single fact, like "this call only drops cache entries that are already dead". If it holds,
   most risks clear at once. Spend your time here, not on a long list of maybes.
3. Look where grep stops: the source of the library you call (at its pinned version, with any
   local patch), when things run (startup order, async, teardown), and what a symbol search
   misses (config keys, env vars, file formats, another language or tool reading the same data,
   code a few hops downstream).
4. Keep only risks with a real chance of happening and a real cost if they do. A search that
   finds nothing is still an answer. Never make up a caller or an API.
5. Prove the one fact. Write a script or test that runs the real code, outside the repo (e.g. in
   `~/dev/temp`), run it, and paste what happened.

## Report

- Findings ranked most severe first. Rank `simplify` findings by how much easier the code gets to
  understand, then by lines saved. Rank `dead` and `tests` findings by lines saved.
- For each: the type in brackets (e.g. `[bugs]`), `file:line`, and the problem in one sentence.
  Then, for bugs, a concrete input or state that triggers it; for design, the change that would
  hurt; for simplify, why the result is simpler; for dead, what you searched to show nothing
  uses it; for tests, what value is kept and about how many lines go; for blast, how it breaks,
  how likely and how bad, and how to check.
- With `blast`, before the findings: the one fact the change is safe because of, the level above
  you got it to, and the proof with the path to your script. If you couldn't prove it, write
  unproven. After the findings: what you checked and cleared, and why it's fine.
- Mark a finding as a guess when you could not confirm it from the code.
- No findings: say so plainly. Do not invent issues to fill the report.
