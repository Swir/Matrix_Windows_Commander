from __future__ import annotations

import sys

from matrix_windows_commander import __version__


def main() -> int:
    if "--version" in sys.argv:
        print(__version__)
        return 0
    if "--smoke-gui" in sys.argv:
        from PySide6.QtWidgets import QApplication
        from matrix_windows_commander.app import MainWindow

        app = QApplication.instance() or QApplication([])
        window = MainWindow()
        window.show()
        app.processEvents()
        window.close()
        app.processEvents()
        return 0
    from matrix_windows_commander.app import run

    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
