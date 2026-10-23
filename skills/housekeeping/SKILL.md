---
name: housekeeping
description: >-
  Args: [types=bugs,reuse,design,simplify,dead,tests,blast] [<command>]. Cleans up the codebase
  in a loop: finds the dirtiest areas with the rounds skill (or takes the one area the user
  gives), reviews each with the inspect skill, fixes the findings, and reviews again until clean.
  Edits files and commits. Use when the user asks to clean up, tidy, or do housekeeping on the
  codebase or an area of it.
argument-hint: "[types=bugs,reuse,design,simplify,dead,tests,blast] [<command>]"
---

# Housekeeping

Review and fix the dirtiest areas of the code, one at a time, until each review comes back
clean. Unlike the rounds and inspect skills, this skill edits files and commits each fix.

## Commands

In Antigravity only (skip this section in Claude Code): strongly prefer commands that the user's
auto-approve whitelist allows. Read the whitelist once at the start:
`cat ~/dev/repos/agy-auto-mode/policy.json`. No such file: skip this section. Run one plain
command at a time: any of `` ;|&><$`()\ `` or a newline makes the command need manual approval,
so no pipes, `&&`, redirects, or `$(...)`. Use a command outside the whitelist only when no
allowed one can do the job, and say why.

## Arguments

Both optional, the same as the inspect skill takes them:

- `types=`: the review types to run. Default: the ones the rounds skill suggests for each
  area, or the inspect skill's default when a command was given.
- A command that outputs the code (e.g. `git diff main...`, `cat src/foo.py`): work only on that
  area and skip the rounds skill.

## Before you start

- The working tree has uncommitted changes: say so and stop, so the user's own work does not end
  up in your commits.
- Read `git log` to learn the repo's commit message style.

## Pick the areas

- A command was given: that is the only area.
- Otherwise: run the rounds skill once and take its areas, dirtiest first. Do not run it
  again during the loop: it always finds something, so the loop would never end. It found
  nothing: say so and stop.

## Loop over each area

1. Run the inspect skill with the area's types and command. Print its findings in full, so the
   user sees what each round fixes, then go on without waiting for them.
2. Fix every finding except the ones marked as a guess, one at a time. Follow the repo's rules
   file and keep behavior the same unless the finding is a bug. Skip a fix that would break
   something or that you are not sure about, and say why. After each fix:
   1. Run the repo's tests or linters for the files you touched, if it has them. Fix what you
      broke.
   2. Commit it on the current branch: `git add <paths>`, then `git commit`, in the repo's
      message style. One commit per fix, so each can be reverted alone. Findings that share one
      fix share one commit. Never push.
3. Run the inspect skill again on the same area. The command only shows commits (e.g.
   `git diff A..B`, `git diff main...`): use `git diff <base> -- <paths>` instead, so all the fix
   commits show. Print its findings the same way.
4. New findings: go back to step 2. Stop after 2 rounds of fixes, so two fixes can't undo each
   other forever.

## Report

For each area:

- The paths, and whether it ended clean.
- Your commits, one line each: short hash and subject.
- What you left: guesses, skipped fixes, and findings still open after 2 rounds, with
  `file:line` and why.
- The tests or linters you ran, and the result.
