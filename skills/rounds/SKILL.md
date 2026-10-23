---
name: rounds
description: >-
  Args: [<paths>...]. Finds the dirtiest areas of the codebase, or of the given files and
  directories (where a review would likely find many problems), and says which review types to
  run there, without reviewing or editing anything. Use when the user asks where the code is
  messiest, where to focus a review, or what is turning into spaghetti.
argument-hint: "[<paths>...]"
---

# Rounds

Point at the few areas where design, architecture, or reuse is drifting, so the inspect skill
can target them. This is a gut-feeling pass to keep the code from turning into spaghetti with
minimal human inspection: no findings, no fixes, never edit files.

## Commands

Prefer plain, read-only commands (`git`, `cat`, `ls`, `grep`), one at a time, to avoid permission
prompts: no pipes, `&&`, redirects, or `$(...)`.

## Arguments

Optional paths (e.g. `src/api src/db/models.py`): files, directories, or a mix. Only look at
those, by adding `-- <paths>` to every `git grep` and `git log` below. Drop a leading `@` (a
Claude Code file mention).

## Pick the scope

1. Lines per file: `git grep -c ''`. Leave out lock, generated, vendored, and data files.
2. Churn: count how often each path shows up in `git log --since=6.months --format= --name-only`.
3. Mode:
   - Up to 10k lines: **full mode**, the whole codebase (or all the given paths).
   - Past that (about 100k tokens), the code stops fitting in context: **hotspot mode**, the top
     20 or so files by churn times lines. Dirt piles up where people keep editing.
4. Say the mode, the paths if any, and why in one line. In full mode, add the lines as a
   percentage of the 10k budget (e.g. "Full mode: 7,300 lines, 73% of the budget").

## Find the smells

Read the repo's rules file (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) if any: breaking it is a
smell too. Skim, and stop at a gut feeling instead of chasing each smell down.

- **Hotspots:** big files that change often.
- **Size:** long files and functions, deep nesting, many parameters or flags.
- **Duplication:** near-copies of code, the same data computed or stored in several places.
- **Coupling:** a module everything imports, files that always change together.
- **Wrong place:** logic in the wrong layer or owner, utils dumping grounds, mixed concerns.
- **Debt markers:** piles of `TODO`, `FIXME`, `HACK`, disabled tests, commented-out code.
- **Tests:** much bigger than the code they test, heavy mocking, repeated setup.

## Report

At most 5 areas (a file, directory, or files that smell for the same reason), dirtiest first.
For each:

- The paths, or `file:line` for one spot.
- Why it smells, naming the signals (e.g. "800 lines, changed in 14 of the last 30 commits, 3
  near-copies of the date parsing"). Mark it a guess when it rests on one weak signal.
- A command to paste that runs the inspect skill with `types=<types> <command>`, with types
  from `bugs`, `reuse`, `design`, `simplify`, `dead`, `tests`. The command is `cat <files>`.

Nothing stands out: say so. Do not invent areas to fill the report.
