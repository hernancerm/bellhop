# Upkeep

Skills that keep a codebase tidy.

| Skill | What it does | Edits files |
|---|---|---|
| `/hotspots` | Finds the messiest areas and says which reviews to run there. | No |
| `/inspect` | Reviews a diff for bugs, duplication, design, dead code, and more. | No |
| `/cleanup` | Loops: `/hotspots`, `/inspect`, fix, inspect again, until clean. Commits each fix. | Yes |
| `/adopt` | Recommends the libraries, tools, and helpers that would pay off most. | No |

## Quickstart

```bash
# List all available skills
npx skills add hernancerm/upkeep --list

# Install a specific skill
# (/cleanup needs /hotspots and /inspect)
npx skills add hernancerm/upkeep --skill inspect

# Install all skills
npx skills add hernancerm/upkeep
```

## Usage


| You want | You type |
|---|---|
| Review your current changes | `/inspect` |
| Review with plan docs and a note | `/inspect -- See .temp/plan. Increment 1 only` |
| Only some review types on `src/api.ts` | `/inspect types=bugs,sense src/api.ts` |
| Review another branch, no checkout | `/inspect main...feature-x` |
| Find the messy parts of your branch | `/hotspots main...` |
| Clean up only your branch | `/cleanup main...` |

`/hotspots`, `/inspect` and `/cleanup` take the same optional arguments:

1. `[types=…]`: bugs, reuse, design, simplify, perf, dead, tests, sense
2. `[<range>]`: a git revision range (e.g., `main...`, `main...feature-x`)
3. `[<paths>…]`: file or dir paths to review, optionally prefixed with `@`
4. `[-- <notes>]`: free-text notes

`/adopt` takes no args.
