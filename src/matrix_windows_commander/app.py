from __future__ import annotations

import locale
import time
import webbrowser
from pathlib import Path

from PySide6.QtCore import QProcess, QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton,
    QSplitter, QStatusBar, QVBoxLayout, QWidget
)

from .catalog import CATEGORIES, get_command, search_catalog
from .history import HistoryEntry, HistoryStore, utc_now
from .i18n import detect_language, tr
from .models import CommandSpec, Risk
from .platform_utils import is_admin, is_windows, relaunch_as_admin, resource_path

STYLE = """
QWidget { background: #050b17; color: #d9ecff; font-family: 'Segoe UI'; font-size: 10pt; }
QMainWindow { background: #050b17; }
QFrame#Panel { background: #081426; border: 1px solid #163a61; border-radius: 10px; }
QLineEdit, QComboBox, QListWidget, QPlainTextEdit { background: #07101f; border: 1px solid #24527c; border-radius: 7px; padding: 7px; color: #e8f6ff; }
QListWidget::item { padding: 8px; border-radius: 5px; }
QListWidget::item:selected { background: #123a60; color: #7bdcff; }
QPushButton { background: #102b49; border: 1px solid #2a74ad; border-radius: 7px; padding: 8px 12px; color: #dff5ff; font-weight: 600; }
QPushButton:hover { background: #17466f; border-color: #4dc7ff; }
QPushButton:disabled { color: #60758a; border-color: #263747; background: #0a1622; }
QPushButton#Primary { background: #0d4f78; border-color: #48d1ff; color: white; }
QPushButton#Danger { background: #3a1621; border-color: #aa4960; }
QLabel#Title { color: #61d7ff; font-size: 22pt; font-weight: 800; }
QLabel#Badge { background: #0f2942; color: #7bdcff; border: 1px solid #245a83; border-radius: 8px; padding: 4px 8px; }
QStatusBar { background: #07101f; color: #8fb6cf; border-top: 1px solid #163a61; }
"""


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.language = detect_language(); self.current: CommandSpec | None = None; self.process: QProcess | None = None; self.started_monotonic = 0.0; self.started_at = ""; self.history = HistoryStore()
        self.setWindowTitle(f"{tr(self.language,'app')} 2.0")
        self.resize(1260, 760); self.setMinimumSize(960, 620); self.setStyleSheet(STYLE)
        icon = resource_path("assets/matrix-windows-commander.svg")
        if icon.exists(): self.setWindowIcon(QIcon(str(icon)))
        self._build(); self._populate(); self._update_admin_badge()
        if not is_windows(): QMessageBox.information(self, tr(self.language,"app"), tr(self.language,"not_windows"))

    def _panel(self) -> QFrame:
        frame = QFrame(); frame.setObjectName("Panel"); return frame

    def _build(self) -> None:
        root=QWidget(); outer=QVBoxLayout(root); outer.setContentsMargins(14,14,14,10); outer.setSpacing(10)
        header=QHBoxLayout(); title=QLabel(tr(self.language,"app")); title.setObjectName("Title"); header.addWidget(title); header.addStretch(1)
        self.admin_badge=QLabel(); self.admin_badge.setObjectName("Badge"); header.addWidget(self.admin_badge)
        self.lang=QComboBox(); self.lang.addItems(["PL","EN"]); self.lang.setCurrentText("PL" if self.language=="pl" else "EN"); self.lang.currentTextChanged.connect(self._change_language); header.addWidget(self.lang); outer.addLayout(header)
        splitter=QSplitter(Qt.Horizontal); splitter.setChildrenCollapsible(False)
        left=self._panel(); left_l=QVBoxLayout(left); self.search=QLineEdit(); self.search.setPlaceholderText(tr(self.language,"search")); self.search.textChanged.connect(self._populate); left_l.addWidget(self.search)
        self.category=QComboBox(); self.category.addItem(tr(self.language,"all"),"All");
        for item in CATEGORIES: self.category.addItem(item,item)
        self.category.currentIndexChanged.connect(self._populate); left_l.addWidget(self.category); self.commands=QListWidget(); self.commands.currentItemChanged.connect(self._select); left_l.addWidget(self.commands,1); splitter.addWidget(left)
        middle=self._panel(); mid=QVBoxLayout(middle); self.detail_title=QLabel(tr(self.language,"details")); self.detail_title.setStyleSheet("font-size:15pt;font-weight:700;color:#7bdcff"); mid.addWidget(self.detail_title); self.description=QPlainTextEdit(); self.description.setReadOnly(True); mid.addWidget(self.description,1)
        self.command_preview=QLineEdit(); self.command_preview.setReadOnly(True); mid.addWidget(self.command_preview)
        row=QHBoxLayout(); self.run_btn=QPushButton(tr(self.language,"run")); self.run_btn.setObjectName("Primary"); self.run_btn.clicked.connect(self._run); row.addWidget(self.run_btn); self.copy_btn=QPushButton(tr(self.language,"copy")); self.copy_btn.clicked.connect(self._copy); row.addWidget(self.copy_btn); self.admin_btn=QPushButton(tr(self.language,"admin")); self.admin_btn.clicked.connect(self._elevate); row.addWidget(self.admin_btn); mid.addLayout(row); self.legacy_note=QLabel(tr(self.language,"legacy_note")); self.legacy_note.setWordWrap(True); self.legacy_note.setStyleSheet("color:#6f94ad;font-size:9pt"); mid.addWidget(self.legacy_note); splitter.addWidget(middle)
        right=self._panel(); right_l=QVBoxLayout(right); out_title=QLabel(tr(self.language,"output")); out_title.setStyleSheet("font-size:15pt;font-weight:700;color:#7bdcff"); right_l.addWidget(out_title); self.output=QPlainTextEdit(); self.output.setReadOnly(True); self.output.setLineWrapMode(QPlainTextEdit.NoWrap); right_l.addWidget(self.output,1); out_buttons=QHBoxLayout(); self.stop_btn=QPushButton(tr(self.language,"stop")); self.stop_btn.setObjectName("Danger"); self.stop_btn.setEnabled(False); self.stop_btn.clicked.connect(self._stop); out_buttons.addWidget(self.stop_btn); clear=QPushButton(tr(self.language,"clear")); clear.clicked.connect(self.output.clear); out_buttons.addWidget(clear); right_l.addLayout(out_buttons); splitter.addWidget(right); splitter.setSizes([270,430,520]); outer.addWidget(splitter,1)
        footer=QHBoxLayout(); self.footer=QLabel(tr(self.language,"footer")); self.footer.setCursor(Qt.PointingHandCursor); self.footer.mousePressEvent=lambda _e:webbrowser.open("https://github.com/Swir"); footer.addWidget(self.footer); footer.addStretch(1); outer.addLayout(footer); self.setCentralWidget(root); self.setStatusBar(QStatusBar()); self.statusBar().showMessage(tr(self.language,"ready"))
        self.timeout=QTimer(self); self.timeout.setSingleShot(True); self.timeout.timeout.connect(self._timed_out); self._sync_buttons()

    def _populate(self,*_args) -> None:
        selected_id=self.current.id if self.current else None; self.commands.clear(); category=self.category.currentData() if hasattr(self,"category") else "All"; query=self.search.text() if hasattr(self,"search") else ""
        values=search_catalog(query,category)
        for spec in values:
            item=QListWidgetItem(spec.title); item.setData(Qt.UserRole,spec.id); item.setToolTip(spec.command_line); self.commands.addItem(item)
        if not values: self.commands.addItem(tr(self.language,"empty")); self.commands.item(0).setFlags(Qt.NoItemFlags)
        elif selected_id:
            for index in range(self.commands.count()):
                if self.commands.item(index).data(Qt.UserRole)==selected_id: self.commands.setCurrentRow(index); break
        if self.commands.currentRow()<0 and values: self.commands.setCurrentRow(0)

    def _select(self,current: QListWidgetItem | None,_previous=None) -> None:
        self.current=get_command(current.data(Qt.UserRole)) if current and current.data(Qt.UserRole) else None
        if not self.current: self.description.clear(); self.command_preview.clear(); self._sync_buttons(); return
        spec=self.current; desc=spec.description_pl if self.language=="pl" else spec.description_en; risk_label=tr(self.language,spec.risk.value); admin=tr(self.language,"yes") if spec.admin_required else tr(self.language,"no")
        self.description.setPlainText(f"{desc}\n\n{tr(self.language,'category')}: {spec.category}\n{tr(self.language,'risk')}: {risk_label}\n{tr(self.language,'requires_admin')}: {admin}\nTimeout: {spec.timeout_seconds}s")
        self.command_preview.setText(spec.command_line); self._sync_buttons()

    def _sync_buttons(self) -> None:
        running=self.process is not None and self.process.state()!=QProcess.NotRunning if self.process else False; can_run=bool(self.current) and not running and is_windows(); self.run_btn.setEnabled(can_run); self.copy_btn.setEnabled(bool(self.current)); self.stop_btn.setEnabled(running); self.admin_btn.setVisible(is_windows() and not is_admin())

    def _run(self) -> None:
        spec=self.current
        if not spec or not is_windows(): return
        if spec.admin_required and not is_admin(): QMessageBox.warning(self,tr(self.language,"app"),tr(self.language,"need_admin")); return
        if spec.risk in (Risk.REPAIR,Risk.CHANGE):
            text=tr(self.language,"confirm_repair" if spec.risk==Risk.REPAIR else "confirm_change")
            if QMessageBox.question(self,tr(self.language,"confirm_title"),text,QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes:return
        self.output.clear(); self.output.appendPlainText(f"> {spec.command_line}\n"); self.process=QProcess(self); self.process.setProgram(spec.executable); self.process.setArguments(list(spec.args)); self.process.setProcessChannelMode(QProcess.SeparateChannels); self.process.readyReadStandardOutput.connect(self._stdout); self.process.readyReadStandardError.connect(self._stderr); self.process.errorOccurred.connect(self._process_error); self.process.finished.connect(self._finished); self.started_monotonic=time.monotonic(); self.started_at=utc_now(); self.process.start(); self.timeout.start(spec.timeout_seconds*1000); self.statusBar().showMessage(f"{tr(self.language,'running')}: {spec.title}"); self._sync_buttons()

    def _decode(self,data: bytes) -> str:
        for enc in (locale.getpreferredencoding(False),"utf-8","cp1250","cp850","cp437"):
            try:return data.decode(enc)
            except (UnicodeDecodeError,LookupError):pass
        return data.decode("utf-8",errors="replace")
    def _stdout(self) -> None:
        if self.process:self.output.moveCursor(self.output.textCursor().End); self.output.insertPlainText(self._decode(bytes(self.process.readAllStandardOutput())))
    def _stderr(self) -> None:
        if self.process:self.output.moveCursor(self.output.textCursor().End); self.output.insertPlainText(self._decode(bytes(self.process.readAllStandardError())))
    def _process_error(self,_error) -> None:
        if self.process and self.process.state()==QProcess.NotRunning:self.output.appendPlainText(f"\n[{tr(self.language,'start_failed')}] {self.process.errorString()}")
    def _finished(self,exit_code:int,_status) -> None:
        self.timeout.stop(); spec=self.current; duration=int((time.monotonic()-self.started_monotonic)*1000) if self.started_monotonic else 0; self.output.appendPlainText(f"\n[{tr(self.language,'finished')}: exit {exit_code}, {duration/1000:.1f}s]")
        if spec:self.history.append(HistoryEntry(spec.id,spec.title,int(exit_code),self.started_at,duration)); self.statusBar().showMessage(f"{tr(self.language,'finished')}: {exit_code}"); self.process.deleteLater(); self.process=None; self._sync_buttons()
    def _timed_out(self) -> None:
        if self.process and self.process.state()!=QProcess.NotRunning:self.output.appendPlainText(f"\n[{tr(self.language,'timeout')}]"); self.process.kill()
    def _stop(self) -> None:
        if self.process and self.process.state()!=QProcess.NotRunning:self.process.kill()
    def _copy(self) -> None:
        if self.current: QApplication.clipboard().setText(self.current.command_line); self.statusBar().showMessage(tr(self.language,"copied"),3000)
    def _elevate(self) -> None:
        if relaunch_as_admin(): QApplication.quit()
    def _update_admin_badge(self) -> None:self.admin_badge.setText(tr(self.language,"admin_mode" if is_admin() else "standard_mode"))
    def _change_language(self,value:str) -> None:
        lang="pl" if value=="PL" else "en"
        if lang==self.language:return
        self.language=lang; self.close(); replacement=MainWindow(); replacement.language=lang; replacement.show()


def run() -> None:
    app=QApplication.instance() or QApplication([]); app.setApplicationName("Matrix Windows Commander"); window=MainWindow(); window.show(); app.exec()
