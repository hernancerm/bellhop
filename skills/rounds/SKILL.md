---
name: rounds
description: >-
  Args: [since=<when>] [<revision range>]. Finds the dirtiest areas of the codebase (where a
  review would likely find many problems) and says which review types to run there, without
  reviewing or editing anything. Use when the user asks where the code is messiest, where to
  focus a review, or what is turning into spaghetti.
argument-hint: "[since=<when>] [<revision range>]"
---

# Rounds

Point at the few areas where design, architecture, or reuse is drifting, so the inspect skill
can target them. This is a gut-feeling pass to keep the code from turning into spaghetti with
minimal human inspection: no findings, no fixes, never edit files.

## Commands

In Antigravity only (skip this section in Claude Code): strongly prefer commands that the user's
auto-approve whitelist allows. Read the whitelist once at the start:
`cat ~/dev/repos/agy-auto-mode/policy.json`. No such file: skip this section. Run one plain
command at a time: any of `` ;|&><$`()\ `` or a newline makes the command need manual approval,
so no pipes, `&&`, redirects, or `$(...)`. Use a command outside the whitelist only when no
allowed one can do the job, and say why.

## Arguments

Both optional:

- `since=<when>` (e.g. `since=2.months`): the churn window. Default: `6.months`.
- A revision range (e.g. `main~20..main`): only look at files changed in it.

## Pick the scope

1. Lines per file: `git grep -c ''`. Leave out lock, generated, vendored, and data files.
2. Churn: count how often each path shows up in `git log --since=<when> --format= --name-only`.
3. Mode:
   - A revision range was given: **range mode**, only the files in `git diff --stat <range>`.
   - Up to 10k lines: **full mode**, the whole codebase.
   - Past that (about 100k tokens), the code stops fitting in context: **hotspot mode**, the top
     20 or so files by churn times lines. Dirt piles up where people keep editing.
4. Say the mode and why in one line. In full mode, add the lines as a percentage of the 10k
   budget (e.g. "Full mode: 7,300 lines, 73% of the budget").

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

At most 3 areas (a file, directory, or files that smell for the same reason), dirtiest first.
For each:

- The paths, or `file:line` for one spot.
- Why it smells, naming the signals (e.g. "800 lines, changed in 14 of the last 30 commits, 3
  near-copies of the date parsing"). Mark it a guess when it rests on one weak signal.
- A command to paste that runs the inspect skill with `types=<types> <command>` (in Claude Code:
  `/bellhop:inspect types=<types> <command>`), with types from `bugs`, `reuse`, `design`,
  `simplify`, `dead`, `tests`. The command is `git diff <range> -- <paths>` in range mode,
  otherwise `cat <files>`.

Nothing stands out: say so. Do not invent areas to fill the report.
