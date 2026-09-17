<!-- SWIR-README-STANDARD:v2 -->

<div align="center">

<img width="100%" src="assets/readme/hero.svg" alt="Matrix Windows Commander — safe Windows diagnostics and repair command center" />

# Matrix Windows Commander

**Safe Windows diagnostics and repair command center with a blue Matrix interface.**

![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-02050A?style=for-the-badge&logo=windows11&logoColor=62E5FF)
![Python](https://img.shields.io/badge/Python-3.10%E2%80%933.14-02050A?style=for-the-badge&logo=python&logoColor=62E5FF)
![GUI](https://img.shields.io/badge/GUI-PySide6%20%7C%20Qt%206-02050A?style=for-the-badge&logo=qt&logoColor=62E5FF)
![Release](https://img.shields.io/badge/Release-v2.1.1-02050A?style=for-the-badge&logo=github&logoColor=62E5FF)

[![Author](https://img.shields.io/badge/by-Swir-0088FF?style=flat-square&logo=github)](https://github.com/Swir)
[![Stars](https://img.shields.io/github/stars/Swir/Matrix_Windows_Commander?style=flat-square&color=0088FF)](https://github.com/Swir/Matrix_Windows_Commander/stargazers)

[**Highlights**](#-highlights) · [**Quick Start**](#-quick-start) · [**Safety**](#-safety-model) · [**Progress**](#-progress) · [**Releases**](#-releases)

</div>

<img width="100%" src="https://raw.githubusercontent.com/Swir/Swir/main/assets/power-divider-v4.svg" alt="SWIR electric divider" />

## 📍 Project Status

| Item | Status |
|---|---|
| Current line | **2.1.1** — maintained diagnostic / repair utility |
| Platform | Windows 10 / 11 |
| UI languages | Polski / English, selected from the system locale with in-app support |
| Latest public release | [v2.1.1](https://github.com/Swir/Matrix_Windows_Commander/releases/tag/v2.1.1) |
| Progress model | **N/A** — the repository has no canonical roadmap with a reproducible completion denominator |

<p align="center">
  <img width="100%" src="assets/readme/progress-card.svg" alt="Matrix Windows Commander product readiness progress — N/A" />
</p>

**Product progress: N/A.** Release availability, CI health and product completion are separate facts; this repository does not currently define a numeric product-readiness roadmap.

## 🚀 Overview

**Matrix Windows Commander** is a Windows desktop command center for diagnostics, maintenance and explicitly confirmed repair actions. Version 2.1.1 uses a modular PySide6 / Qt 6 application, fixed executable-and-argument definitions and `QProcess` execution rather than passing arbitrary user text to a shell.

The current release restores much of the useful diagnostic coverage from the older monolithic build while intentionally keeping destructive one-click operations out of the catalog.

## ✨ Highlights

| Feature | What it does |
|---|---|
| 🔎 Search & categories | Quickly find diagnostic, network, storage, service, account and WSL actions. |
| 🧾 Exact command preview | Shows the executable/arguments and lets you copy the command before running it. |
| ⚡ Non-blocking execution | Streams stdout/stderr through Qt `QProcess`, with stop control and safety timeouts. |
| 🛡️ Risk model | Separates read-only, repair and system-change actions; repair/change actions require confirmation. |
| 🔐 Controlled elevation | Detects administrator state and provides a deliberate restart-as-administrator path. |
| 🌐 PL / EN UI | Supports Polish and English presentation. |
| 🗂️ Local history metadata | Stores command identity, exit code, timestamp and duration locally; command output itself is not persisted. |
| 🪟 Windows packaging | v2.1.1 provides an EXE, portable ZIP and SHA-256 checksum files. |

## 🧰 Diagnostic Coverage

The current catalog includes safe or explicitly confirmed workflows for:

- hostname, Windows version and installed-driver information;
- SFC, DISM and read-only / repair CHKDSK flows;
- Disk Cleanup and the Windows performance diagnostic report;
- DHCP release/renew, DNS cache display/flush and TCP/IP / Winsock repair;
- PathPing, route table, ARP cache and NetBIOS diagnostics;
- saved Wi-Fi **profile names only** — stored keys/passwords are not requested;
- Event Log channel listing, scheduled tasks and read-only BCD enumeration;
- Regsvr32 and Logman help without changing registration/logging state;
- local/domain users and groups, account policy, shares, SMB sessions and open shared files;
- running processes, started services and Print Spooler status/start/stop;
- an explicitly confirmed **Close Notepad** action that warns about unsaved text;
- battery and short energy reports;
- WSL status/list and explicitly confirmed default WSL installation.

Incomplete legacy placeholders such as raw `xcopy`, `robocopy`, `takeown`, `icacls` and `label` are not exposed as blind one-click actions because they require a real target/path workflow.

## ⚙️ Quick Start

### Recommended — Windows release

Download [Matrix Windows Commander v2.1.1](https://github.com/Swir/Matrix_Windows_Commander/releases/tag/v2.1.1). The release contains:

- `MatrixWindowsCommander.exe`;
- `Matrix-Windows-Commander-v2.1.1-Windows-x64.zip`;
- SHA-256 sidecar files for the EXE and ZIP.

### From source

```powershell
git clone https://github.com/Swir/Matrix_Windows_Commander.git
cd Matrix_Windows_Commander
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[gui]"
python main.py
```

Check the version without opening the GUI:

```powershell
python main.py --version
```

## 📋 Requirements / Compatibility

| Component | Verified repository contract |
|---|---|
| Python | `>=3.10`; CI currently covers 3.10–3.14 for core tests |
| GUI | PySide6 6.x / Qt 6 |
| Primary OS | Windows 10 / 11 |
| Runtime metadata | `platformdirs>=4.3,<5` |
| Windows smoke | CI starts the real GUI on Windows with Python 3.12 |

Some catalog entries depend on Windows components or administrative privileges that may not exist on every installation/edition.

## 🎮 Usage

1. Search or choose a category.
2. Read the description, risk level and exact command preview.
3. Run read-only diagnostics directly.
4. For repair/system changes, review and confirm the warning.
5. Use **Restart as administrator** only when the selected action genuinely requires elevation.
6. Stop a long-running command when needed; review stdout/stderr in the application.

## 🛡️ Safety Model

Commands are defined as fixed executable/argument lists and are launched through Qt `QProcess`; arbitrary text is not forwarded to a shell. Destructive legacy actions such as drive formatting, `diskpart`, registry deletion, forced shutdown/reboot, recursive directory deletion and `wsl --unregister` are intentionally not available as one-click commands.

Network repair operations can temporarily interrupt connectivity. Use system-changing functions only on machines you own or are authorized to administer, and keep backups appropriate to the change you are making.

## 🔒 Privacy

The application does not upload command output. Local history stores command ID/title, exit code, timestamp and duration in the current user's application-data directory; command output itself is not persisted.

## 🧠 Technology / Project Structure

| Path | Role |
|---|---|
| `src/matrix_windows_commander/app.py` | PySide6 application and execution UI |
| `src/matrix_windows_commander/catalog.py` | Fixed command catalog and safety metadata |
| `src/matrix_windows_commander/history.py` | Local execution-history metadata |
| `src/matrix_windows_commander/i18n.py` | PL / EN strings |
| `src/matrix_windows_commander/platform_utils.py` | Windows/platform helpers |
| `tests/` | Catalog, model and platform tests |
| `.github/workflows/ci.yml` | Python matrix tests and Windows GUI smoke |
| `.github/workflows/release.yml` | Windows packaging / release workflow |

The original project icon remains at `assets/matrix-windows-commander.svg` and is used by the application build tooling.

## 🗺️ Progress

<p align="center">
  <img width="100%" src="assets/readme/progress-mini.svg" alt="Matrix Windows Commander compact product progress — N/A" />
</p>

There is no authoritative checklist-based roadmap in the current repository, so **product completion is intentionally N/A** rather than an invented percentage. `tools/readme_progress.py` generates and checks the SVG state; if a real roadmap is added, the generator deliberately refuses to continue with the N/A model until it is configured for that source.

```powershell
python tools/readme_progress.py --check
```

## 🧪 Development & CI

```powershell
pip install -e ".[gui,test,build]"
pytest -q
python tools/build_icon.py
python main.py --smoke-gui
python tools/readme_progress.py --check
```

The PR workflow runs tests on Python 3.10–3.14 and a Windows GUI smoke on Python 3.12. The release workflow builds `MatrixWindowsCommander.exe` and release archives; this README migration does not trigger or publish a new release by itself.

## 📦 Releases

Latest public release: **[v2.1.1](https://github.com/Swir/Matrix_Windows_Commander/releases/tag/v2.1.1)**, published September 17, 2026. Browse [all releases](https://github.com/Swir/Matrix_Windows_Commander/releases) for existing binaries and checksums.

## ⚠️ Limitations

- The catalog does not make every historical Windows command safe for one-click use; path/target-dependent placeholders remain excluded.
- Some repair actions require elevation and can change system/network state.
- Diagnostic availability depends on the Windows edition and installed components.
- A successful CI run verifies the tested source/build paths; it is not a guarantee that every Windows command will succeed on every machine.
- No `LICENSE` file is currently present in the repository; this documentation migration does not assign or change licensing terms.

## 🔎 Search Keywords

`Windows diagnostics tool` • `Windows repair utility` • `PySide6 Windows GUI` • `Windows command center` • `SFC DISM CHKDSK GUI` • `Winsock repair tool` • `Windows network diagnostics` • `Windows service diagnostics` • `WSL status utility` • `safe system maintenance` • `Polish English Windows tool` • `Qt6 desktop utility`

<img width="100%" src="https://raw.githubusercontent.com/Swir/Swir/main/assets/power-divider-v4.svg" alt="SWIR electric divider" />

<div align="center">

<img src="assets/matrix-windows-commander.svg" width="72" alt="Matrix Windows Commander application icon" />

### `DIAGNOSE • REVIEW • REPAIR`

⭐ **If this project is useful, consider leaving a star.**

[**← SWIR profile**](https://github.com/Swir) · [**All projects →**](https://github.com/Swir?tab=repositories) · [**Report an issue**](https://github.com/Swir/Matrix_Windows_Commander/issues)

</div>
