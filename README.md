<div align="center">

# ⚡ Matrix Windows Commander 2

### Safe Windows diagnostics & repair command center

**Windows 10/11 · PySide6 / Qt 6 · PL / EN · Blue Matrix UI**

</div>

Matrix Windows Commander 2 modernizes the original single-file command launcher into a structured Windows diagnostics application. It focuses on useful, bounded system inspection and repair commands while adding safeguards around commands that can change Windows.

## Highlights

- modern **blue Matrix** desktop interface
- fast search and category filtering
- Polish/English interface with automatic system-language selection
- detailed command descriptions, exact command preview and one-click copy
- non-blocking execution with live stdout/stderr
- stop button and per-command safety timeout
- clear risk levels: read-only, repair, system change
- explicit confirmation before repair/change actions
- administrator detection with controlled UAC relaunch
- local history metadata stored in the user profile
- dedicated application icon
- modular package instead of a 31 KB monolithic script

## Command groups

The built-in catalog covers Windows system information, SFC/DISM diagnostics and repair, network diagnostics, process/service inspection, storage status, BitLocker status, firewall information, power diagnostics and WSL status.

Version 2 intentionally does **not** expose destructive legacy actions such as drive formatting, `diskpart`, registry deletion, forced shutdown/reboot, recursive directory deletion or `wsl --unregister` as one-click commands.

## Install from source

```powershell
git clone https://github.com/Swir/Matrix_Windows_Commander.git
cd Matrix_Windows_Commander
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[gui]"
python main.py
```

## Administrator mode

Most information commands run in standard mode. Commands that genuinely require elevated rights are marked. Use the **Restart as administrator** button when needed. Repair/change commands also require explicit confirmation before execution.

## Privacy

The application does not upload command output. Execution history stores only command ID/title, exit code, timestamp and duration in the current user's application-data directory. Command output itself is not persisted.

## Development

```powershell
pip install -e ".[gui,test,build]"
pytest -q
```

Core tests run on Python 3.10–3.14. The Windows release pipeline builds and smoke-tests `MatrixWindowsCommander.exe`, then publishes the EXE, portable ZIP and SHA256 checksums.

## Project layout

```text
src/matrix_windows_commander/
├── app.py
├── catalog.py
├── history.py
├── i18n.py
├── models.py
└── platform_utils.py
assets/
tests/
tools/
```

## Author

Developed by **Swir** — https://github.com/Swir
