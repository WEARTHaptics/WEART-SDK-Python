# Changelog
All significant changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.0.3] - 2026-02-06
### Added
- sensorsCalibDate field to G2DeviceStatus
- Logging of sensor calibration date in examples

### Changed
- Changelog file
- Readme file

## [2.0.2] - 2025-11-25
### Changed
- Fix typo "pinkky" in WeArtMessages.py
- Fix fallback zero-data Sample (AttributeError bug) in WeArtTrackingRawData.py
- Changelog file

## [2.0.1] - 2025-06-06
### Added
- Warning messages are now handled

### Changed
- Readme file
- Changelog file

## [2.0.0] - 2025-04-03
### Added
- Changelog file
- Documentation for all classes and methods
- DeviceStatusListener
- TDProStateListener
- Examples folder with 3 examples
- \_\_str\_\_ funcions for some enums

### Changed
- Readme completely rewritten is now a complete documentation
- MiddlewareStatusListener is now compatible with Touch Diver PRO device
- WeArtMessageSerializer.__createMessage() now uses python-friendly dictionary instead of hashes
- WeArtClient sendMessage method is now 'private' (SendMessage -> _sendMessage)
- WeArtEffect solved a bug: Set() method now returns true only if some effect has been changed
- Code formatting adjustment to make it more consistent

### Removed
- Unused code
- Unused import
- test.py example (now replaced by examples folder)
---
Version format: `[MAJOR.MINOR.PATCH] - YYYY-MM-DD`
