# Bellhop

Skills that keep a codebase tidy.

| Skill | What it does | Edits files |
|---|---|---|
| `/rounds` | Finds the messiest areas and says which reviews to run there. | No |
| `/inspect` | Reviews a diff for bugs, duplication, design, dead code, and more. | No |
| `/housekeeping` | Loops: rounds, inspect, fix, inspect again, until clean. Commits each fix. | Yes |
| `/concierge` | Recommends the libraries, tools, and helpers that would pay off most. | No |

## Usage

### Fix what's there

These skills improve the code you have, with what the repo already uses: its own code, its
language, and its current dependencies. They add nothing new, so you can run them often, on
any branch.

Hands-on:

1. `/rounds`: identifies the messiest areas in the codebase.
    - The output of this skill contains recommended `/inspect` invocations.
2. `/inspect`: reviews your current changes, or a specific area in the codebase.
    - You can then ask the agent to resolve the findings.

Hands-off:

1. `/housekeeping`: runs `/rounds`, and loops on `/inspect`-fix-commit.
    - This is the automated way to run `/rounds` and `/inspect`.

All three skills take the same optional arguments:

1. `[types=…]`: bugs, reuse, design, simplify, dead, tests, sense
2. `[<range>]`: a git range (e.g., `main...`, `main...feature-x`)
3. `[<paths>…]`: file or dir paths to review, optionally prefixed with `@`
4. `[-- <notes>]`: free-text notes about scope or expected behavior, last. Everything after `--`
   is the note. Paths in them (specs, plans) are background reading, not code to review.

| You want | You type |
|---|---|
| Review your current changes | `/inspect` |
| Review with plan docs and a note | `/inspect -- See .temp/plan. Increment 1 only` |
| Find the messy parts of your branch | `/rounds main...` |
| Review another branch, no checkout | `/inspect main...feature-x` |
| Only some review types on `src/api.ts` | `/inspect types=bugs,sense src/api.ts` |
| Clean up only your branch | `/housekeeping main...` |

### Add what's missing

Sometimes the best fix is something the repo does not have yet: a library, a tool, or a small
helper. Adding one is a bigger decision than a fix, since it brings setup, upkeep, and lock-in, so
it gets its own skill. It pays off most once the code shows the same problem in a few places,
while the codebase is still young enough that adopting things is cheap.

`/concierge`: recommends libraries, tools, and helpers that would replace hand-written code or fill
a gap, each backed by `file:line` spots. It takes no arguments.

## Install

### Claude Code

```
/plugin marketplace add hernancerm/bellhop
/plugin install bellhop@bellhop
```

### Other

Symlink.
