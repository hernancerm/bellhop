---
name: reuse
description: >-
  Searches the repo for existing code the user can reuse or extend before they write something
  new, without editing files. Use when the user describes something they are about to build and
  asks whether it, or something close, already exists.
---

# Reuse

The user describes what they are about to write. Find what already exists that they can reuse,
extend, or derive it from. The user writes and owns the code, so never edit files.

## Commands

In Antigravity only (skip this section in Claude Code): strongly prefer commands that the user's
auto-approve whitelist allows. Read the whitelist once at the start:
`cat ~/dev/repos/agy-auto-mode/policy.json`. No such file: skip this section. Run one plain
command at a time: any of `` ;|&><$`()\ `` or a newline makes the command need manual approval,
so no pipes, `&&`, redirects, or `$(...)`. Use a command outside the whitelist only when no
allowed one can do the job, and say why.

## Search

Every piece of logic or data should have one owner, so the goal is to find that owner if it
exists. If the description is too vague to search for, ask what it does before searching.

- Search by what the thing does, not only by the name the user gave: the repo may call it
  something else. List a few candidate names and terms, and search each.
- Look at every kind of owner it could have: a function, class, component, hook, type, field,
  piece of state, constant, or config. Include the data it needs: it may already be computed or
  stored somewhere the new code can read or derive it from.
- Read each candidate before reporting it, to confirm what it does and how it is used.

## Report

- Candidates ranked by how much of the need they cover. For each: name, `file:line`, what it
  does, and how to use it: as is, extended (say what to add), or derived from.
- Say what is left that nothing covers, so the user knows what they actually have to write.
- Mark a candidate as a guess when you could not confirm it from the code.
- Nothing found: say so plainly and list the terms you searched, so the user can judge the search.
