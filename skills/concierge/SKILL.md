---
name: concierge
description: >-
  Scans the whole repo at a high level and recommends the few libraries, tools, and helpers that
  would pay off most across it (or across one layer): ones that simplify repeated code and ones that
  open new opportunities, without editing files. Use when the user asks what to add to a young
  codebase, which amenities or tooling it is missing, or what would give the best value for the
  effort.
---

# Concierge

Find the best-value add-ons for the codebase: small things adopted once and used everywhere (or
across a whole layer). Some simplify code that already exists (e.g. `cn` to join and merge
Tailwind classes). Others open doors (e.g. Testcontainers for integration tests against a real
database). This pays off most while the codebase is young and adopting things is cheap. The user
decides and installs, so never edit files or install anything.

## Commands

Prefer plain, read-only commands (`git`, `cat`, `ls`, `grep`), one at a time, to avoid permission
prompts: no pipes, `&&`, redirects, or `$(...)`.

## Map the repo

Stay high level: learn the shape, not every line.

- Stack: manifests and lock files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`,
  ...), framework and build configs, CI, scripts.
- Layers: the top-level directories and what each one does (UI, API, data, infra, tests, ...).
- What is already adopted, so you never suggest it again.
- The repo's rules file (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) if any: never suggest something
  it rules out.

## Find the picks

- **Simplifies:** look for the same small problem solved by hand in several places: string
  joining, validation, date handling, fetch and error wrapping, env parsing, logging, test setup.
  Each spot is evidence. One spot is not a pattern.
- **Opens doors:** look for what the code already does but the stack leaves hard, untested, or
  unseen: database queries with no integration tests, untyped calls between layers, schema
  changes made by hand, no observability, slow CI feedback. Point at the code that suffers today,
  never at a future the project might grow into.

Rules for a pick:

- An add-on, not a rewrite: no switching frameworks, languages, or databases.
- It fits the stack and its versions, and is the usual choice there, not a niche one.
- Confirm with a web search that it is maintained and still the common pick. Your knowledge has a
  cutoff and libraries die. Mark a pick unverified when you could not check.
- The value clearly beats the cost (a new dependency, setup, lock-in, a learning curve). A small
  helper the repo can write itself beats a dependency for the same job: say so when it does.

## Report

At most 7 picks, in two groups (**Simplifies**, then **Opens doors**), best value first in each.
For each:

- Name, and the layer it is for (or "whole repo").
- What it does, in one line.
- The evidence: `file:line` spots it would clean up, or that show the gap it fills.
- The cost, in one line.

Nothing worth adding: say so. Do not invent picks to fill the report.
