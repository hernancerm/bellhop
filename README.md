# Bellhop

Skills that keep a codebase tidy.

| Skill | What it does | Edits files |
|---|---|---|
| `/rounds` | Finds the messiest areas and says which reviews to run there. | No |
| `/inspect` | Reviews a diff for bugs, duplication, design, dead code, and more. | No |
| `/housekeeping` | Loops: rounds, inspect, fix, inspect again, until clean. Commits each fix. | Yes |
| `/concierge` | Recommends the libraries, tools, and helpers that would pay off most. | No |

## Usage

- Write workflow
    - `/housekeeping`: runs `/rounds`, and loops `/inspect` and fixing the issues.
- Read-only workflow
    - `/rounds`: identifies the messiest areas in the codebase.
    - `/inspect`: reviews a specific area in the codebase.
        - e.g., `/inspect git diff main...`


## Install

### Claude Code

```
/plugin marketplace add hernancerm/bellhop
/plugin install bellhop@bellhop
```

### Other

Symlink.
