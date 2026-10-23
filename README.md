# Bellhop

Skills that keep a codebase tidy.

| Skill | What it does | Edits files |
|---|---|---|
| `/rounds` | Finds the messiest areas and says which reviews to run there. | No |
| `/inspect` | Reviews a diff for bugs, duplication, design, dead code, and more. | No |
| `/housekeeping` | Loops: rounds, inspect, fix, inspect again, until clean. Commits each fix. | Yes |
| `/concierge` | Recommends the libraries, tools, and helpers that would pay off most. | No |

## Usage

- `/rounds`: identifies the messiest areas in the codebase.
- `/inspect`: reviews your current changes, or a specific area in the codebase.
- `/housekeeping`: runs `/rounds`, and loops `/inspect` and fixing the issues.

All three take the same optional arguments: `[types=…] [<range>] [<paths>…]`.

| You want | You type |
|---|---|
| Review your current changes | `/inspect` |
| Review another branch, no checkout | `/inspect main...feature-x` |
| Find the messy parts of your branch | `/rounds main...` |
| Clean up only your branch | `/housekeeping main...` |
| Same, but only in `src/api` | `/housekeeping main... src/api` |
| Only some review types | `/inspect types=bugs,sense src/api` |


## Install

### Claude Code

```
/plugin marketplace add hernancerm/bellhop
/plugin install bellhop@bellhop
```

### Other

Symlink.
