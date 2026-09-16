from __future__ import annotations

import locale

STRINGS = {
    "en": {
        "app":"Matrix Windows Commander", "search":"Search commands…", "all":"All", "run":"Run", "stop":"Stop", "copy":"Copy command", "admin":"Restart as administrator", "clear":"Clear output", "details":"Command details", "output":"Output", "category":"Category", "command":"Command", "risk":"Risk", "requires_admin":"Administrator", "yes":"Yes", "no":"No", "ready":"Ready", "running":"Running", "finished":"Finished", "failed":"Failed", "not_windows":"This utility runs Windows commands and is intended for Windows 10/11.", "need_admin":"This command requires administrator rights. Restart the application as administrator first.", "confirm_title":"Confirm system change", "confirm_change":"This command changes Windows configuration. Run it only on a computer you own or administer. Continue?", "confirm_repair":"This repair command can modify Windows system files. Continue?", "copied":"Command copied to clipboard", "timeout":"Command exceeded its safety timeout and was stopped.", "start_failed":"Could not start the command.", "admin_mode":"Administrator mode", "standard_mode":"Standard mode", "footer":"by Swir · GitHub", "read_only":"Read-only", "repair":"Repair", "change":"System change", "empty":"No commands match the current filter.", "legacy_note":"Dangerous legacy actions such as format, diskpart, registry deletion, shutdown and WSL unregister are intentionally not one-click actions in v2."},
    "pl": {
        "app":"Matrix Windows Commander", "search":"Szukaj poleceń…", "all":"Wszystkie", "run":"Uruchom", "stop":"Zatrzymaj", "copy":"Kopiuj polecenie", "admin":"Uruchom ponownie jako administrator", "clear":"Wyczyść wynik", "details":"Szczegóły polecenia", "output":"Wynik", "category":"Kategoria", "command":"Polecenie", "risk":"Ryzyko", "requires_admin":"Administrator", "yes":"Tak", "no":"Nie", "ready":"Gotowe", "running":"Uruchomiono", "finished":"Zakończono", "failed":"Błąd", "not_windows":"To narzędzie uruchamia polecenia Windows i jest przeznaczone dla Windows 10/11.", "need_admin":"To polecenie wymaga uprawnień administratora. Najpierw uruchom aplikację ponownie jako administrator.", "confirm_title":"Potwierdź zmianę systemu", "confirm_change":"To polecenie zmienia konfigurację Windows. Uruchamiaj je tylko na komputerze, którego jesteś właścicielem lub administratorem. Kontynuować?", "confirm_repair":"To polecenie naprawcze może modyfikować pliki systemowe Windows. Kontynuować?", "copied":"Polecenie skopiowane do schowka", "timeout":"Polecenie przekroczyło limit czasu i zostało zatrzymane.", "start_failed":"Nie udało się uruchomić polecenia.", "admin_mode":"Tryb administratora", "standard_mode":"Tryb standardowy", "footer":"by Swir · GitHub", "read_only":"Tylko odczyt", "repair":"Naprawa", "change":"Zmiana systemu", "empty":"Brak poleceń pasujących do filtra.", "legacy_note":"Niebezpieczne stare akcje, takie jak format, diskpart, usuwanie rejestru, shutdown i WSL unregister, celowo nie są akcjami jednego kliknięcia w v2."},
}


def detect_language() -> str:
    try:
        value = locale.getlocale()[0] or ""
    except Exception:
        value = ""
    return "pl" if value.lower().startswith("pl") else "en"


def tr(language: str, key: str) -> str:
    lang = language if language in STRINGS else "en"
    return STRINGS[lang].get(key, STRINGS["en"].get(key, key))
