# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Free-text notes argument for `/rounds`, `/inspect`, and `/housekeeping`: everything after a
  standalone `--`, about scope or expected behavior. Paths in them (specs, plans) are read as
  background, not reviewed.
- `/rounds` and `/inspect` skip findings that the notes mark as intentional or out of scope.

## [0.1.0] - 2026-10-22

### Added

- `/rounds` skill: finds the messiest areas and says which reviews to run there.
- `/inspect` skill: reviews a diff for bugs, duplication, design, dead code, and more.
- `/housekeeping` skill: loops rounds, inspect, fix, and inspect again until clean, committing
  each fix.
- `/concierge` skill: recommends the libraries, tools, and helpers that would pay off most.
- Shared optional arguments for `/rounds`, `/inspect`, and `/housekeeping`:
  `[types=…] [<range>] [<paths>…]`.
- Claude Code plugin marketplace install.
- MIT license.

[Unreleased]: https://github.com/hernancerm/bellhop/compare/0.1.0...HEAD
[0.1.0]: https://github.com/hernancerm/bellhop/releases/tag/0.1.0
