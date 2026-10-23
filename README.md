# bellhop

Claude Code skills that keep a codebase tidy.

| Skill | What it does | Edits files |
|---|---|---|
| `rounds` | Finds the messiest areas and says which reviews to run there. | No |
| `inspect` | Reviews a diff for bugs, duplication, design, dead code, bloated tests, and blast radius. | No |
| `housekeeping` | Loops: rounds, inspect, fix, inspect again, until clean. Commits each fix. | Yes |
| `reuse` | Finds existing code to reuse before you write something new. | No |
| `concierge` | Recommends the libraries, tools, and helpers that would pay off most. | No |

## Install

```
/plugin marketplace add hernancerm/bellhop
/plugin install bellhop@bellhop
```

Skills are then called as `/bellhop:<skill>`, e.g. `/bellhop:inspect git diff main...`.

## Develop

Load the skills from a local clone without installing: `claude --plugin-dir <clone>`.
