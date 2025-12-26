# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2025-01-25

### Fixed

- Fixed test_main.py: Added missing mock_open import and corrected test parameter issues
- Fixed test_themes.py: Resolved syntax errors, import order issues, and removed non-existent function imports
- Fixed test_data_generator.py: Corrected syntax errors and invalid import statements
- Fixed utils/__init__.py: Removed duplicate __all__ definition causing potential confusion

### Changed

- Improved test coverage reliability by fixing all failing tests
- Enhanced code quality by removing duplicate definitions

## [1.2.0] - 2024-12-24

### Added

- JSON output format with `-j` or `--json` flag for programmatic access
- Progress percentage display in full test mode
- Comprehensive user guide and troubleshooting documentation
- Design decision record document
- Type annotations for all functions and methods
- Comprehensive docstrings for all classes and functions
- Code quality checking module with flake8 integration
- Code standardization module with automated style checks

### Changed

- Improved error handling with specific exception types (HTTPError, TimeoutError, ConnectionError)
- Enhanced code quality with extracted constants and reduced code duplication
- Optimized code structure following PEP 8 guidelines
- Updated test coverage from 52% to 81% (29 test cases, all passing)
- Enhanced user feedback with detailed status messages and suggestions
- Improved command line argument handling with better help messages

### Fixed

- Fixed flake8 code style issues (E128, E131, E501 errors)
- Resolved code duplication through constant extraction
- Corrected type hints and improved code readability
- Addressed missing documentation strings in helper functions

### Docs

- Updated README.md with v1.2 features and API documentation
- Created comprehensive user guide with troubleshooting steps
- Added design decision record documenting technical choices
- Updated project tracking document with v1.2 progress
- Enhanced code comments and documentation strings

## [1.1.0] - 2024-12-23

### Added

- Full test mode with `-n` or `--full-test` flag to perform multiple checks
- Dynamic status messages with detailed network condition descriptions
- Average response time calculation for successful targets
- Spinner animation during normal check for better user feedback
- Command line argument parsing for enhanced usability
- Detailed comments and documentation in Chinese for all functions
- GitHub Actions workflow for code quality checking with flake8

### Changed

- Improved status judgment logic with more granular thresholds
- Enhanced error messages with specific suggestions for different network issues
- Optimized output formatting with better visual hierarchy
- Updated README with installation instructions, usage examples, and FAQ section
- Refactored code structure with detailed function documentation

### Fixed

- Fixed missing timeout handling in network requests
- Resolved animation thread management issues
- Corrected average response time calculation in message generation
- Addressed potential reference errors in exception handling

## [1.0.0] - 2024-12-23

### Added

- Initial release of GitHub Network Status Checker
- Basic functionality to check GitHub accessibility
- Network request implementation with configurable timeout
- Simple command line interface
- Status determination based on response times
