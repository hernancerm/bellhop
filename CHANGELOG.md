# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `/cleanup` stops and says how to install `/hotspots` and `/inspect` when they are missing.
- `/cleanup` leaves `sense` findings for the user instead of fixing them, since they add behavior.

## [0.4.0] - 2026-10-27

### Removed

- The Claude Code plugin. Install with `npx skills add hernancerm/upkeep` instead.

## [0.3.0] - 2026-10-25

### Changed

- Renamed the plugin from `bellhop` to `upkeep`.
- Renamed skills: `/rounds` to `/hotspots`, `/housekeeping` to `/cleanup`, `/concierge` to
  `/adopt`.

## [0.2.0] - 2026-10-24

### Added

- Free-text notes argument for `/rounds`, `/inspect`, and `/housekeeping`: everything after a
  standalone `--`, about scope or expected behavior. Paths in them (specs, plans) are read as
  background, not reviewed.
- `/rounds` and `/inspect` skip findings that the notes mark as intentional or out of scope.

### Changed

- `/concierge` only recommends picks backed by `file:line` evidence of a problem the code has
  today, not by where the project might go.

### Removed

- `/concierge` vision argument.

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

[Unreleased]: https://github.com/hernancerm/upkeep/compare/0.4.0...HEAD
[0.4.0]: https://github.com/hernancerm/upkeep/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/hernancerm/upkeep/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/hernancerm/upkeep/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/hernancerm/upkeep/releases/tag/0.1.0
