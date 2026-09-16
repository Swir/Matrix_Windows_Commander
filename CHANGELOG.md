# Changelog

## 2.0.0 - 2026-09-17

### Changed
- Rebuilt the 31 KB single-file PyQt5 application as a modular PySide6 / Qt 6 project.
- Replaced shell-based execution with fixed executable/argument lists through `QProcess`.
- Redesigned the interface as a responsive blue Matrix command center.
- Added Polish/English UI with system-language default.

### Added
- Search and category filters.
- Risk labels and explicit confirmation before repair/system-changing commands.
- Administrator-mode detection and controlled UAC relaunch.
- Asynchronous command execution, output streaming, cancellation and per-command safety timeouts.
- Command preview/copy and lightweight local execution history.
- Custom Matrix Windows Commander icon.
- Python 3.10-3.14 core CI.
- Automated Windows EXE, portable ZIP and SHA256 release pipeline.

### Safety
- Removed one-click destructive legacy actions including disk formatting, `diskpart`, registry deletion, shutdown/reboot, recursive folder deletion and WSL unregister.
- Saved Wi-Fi passwords are never displayed by the default command catalog.
