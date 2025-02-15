# Changelog

## [0.3.3] - 2025-02-15

### Added

- Levelup func now displays reached level and amber reward.

### Fixed

- Wages func now correctly determines if wages can be collected.
- Levelup func now correctly claims levelup reward.



## [0.3.2] - 2025-02-14

### Added

- Skiller func now displays current attributes when they are increased.



## [0.3.1] - 2025-02-13

### Added

- Support for Snap. Firefox on Ubuntu/Kubuntu.

### Fixed

- Int to Str crash in Farming func.



## [0.3.0] - 2025-02-08

### Added

- Skiller now increases 'Accuracy' for every 6 points in all others attributes.
- World can now be defined in config.

### Changed

- Refactored Skiller func to include Amber Preserver.
- World-specific hardcoded links are now general and use World variable.
- Can handle more edge-cases. Eg. Turning in quest from previous day after script restart.

### Fixed

- Skiller & Amber Preserver functions.

