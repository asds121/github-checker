# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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