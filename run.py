import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QListWidget, QPushButton, QTextEdit, QDialog,
    QPlainTextEdit, QComboBox, QHBoxLayout
)
from PyQt5.QtCore import Qt

# --------------------------------------------------------------------------------
# KATEGORIE I LISTA KOMEND
# --------------------------------------------------------------------------------

categories = {
    "System Repair": [
        "sfc /scannow",
        "sfc /verifyonly",
        "DISM /Online /Cleanup-Image /RestoreHealth",
        "DISM /Online /Cleanup-Image /CheckHealth",
        "DISM /Online /Cleanup-Image /ScanHealth",
        "chkdsk /f",
        "cleanmgr",
        "systeminfo",
        "gpupdate /force"
    ],
    "Network & Internet": [
        "ipconfig /all",
        "ipconfig /release",
        "ipconfig /renew",
        "netstat -an",
        "ping 8.8.8.8",
        "tracert 8.8.8.8",
        "nslookup google.com",
        "pathping 8.8.8.8",
        "netsh wlan show profiles",
        "netsh interface ip reset",
        "netsh interface show interface",
        "nbtstat -n",
        "netsh advfirewall show allprofiles"
    ],
    "Processes & Services": [
        "tasklist",
        "taskkill /IM notepad.exe /F",
        "whoami",
        "hostname",
        "sc query",
        "sc start spooler",
        "sc stop spooler"
    ],
    "File & Disk Management": [
        "diskpart",
        "format A:",
        "label",
        "dir",
        "tree",
        "xcopy",
        "robocopy",
        "takeown /f",
        "icacls",
        "fsutil fsinfo drives",
        "manage-bde -status",
        "md C:\\TestFolder",
        "rd C:\\TestFolder /s /q"
    ],
    "Registry & Config": [
        "reg query HKLM\\Software",
        "reg add",
        "reg delete",
        "bcdedit",
        "regsvr32 /?",
        "wevtutil el",
        "logman /?",
        "wmic /?"
    ],
    "Users & Groups": [
        "net view",
        "net user",
        "net localgroup Administrators",
        "net share",
        "net start",
        "net accounts",
        "net session",
        "net group"
    ],
    "WSL & Advanced": [
        "wsl --list",
        "wsl --install",
        "wsl --unregister Ubuntu",
        "shutdown /r /t 0",
        "shutdown /s /t 0",
        "powercfg /energy",
        "powercfg /batteryreport",
        "bcdedit",
        "perfmon /report",
        "wbadmin start backup",
        "lxrun /install"
    ],
    "Misc & Others": [
        "cls",
        "help",
        "echo Hello World",
        "ver",
        "pause",
        "color 0a",
        "schtasks /query",
        "schtasks /run /tn \"\\Microsoft\\Windows\\Defrag\\ScheduledDefrag\"",
        "net time",
        "net file",
        "at /?",
        "type NUL > C:\\TestFolder\\sample.txt"
    ]
}

# --------------------------------------------------------------------------------
# SŁOWNIK KOMEND (OPISY, PRZYKŁADY, INFO O ADMIN)
# --------------------------------------------------------------------------------
commands = {
    # ===== System Repair =====
    "sfc /scannow": {
        "description": (
            "Skanuje i naprawia uszkodzone pliki systemowe.\n"
            "Może potrwać dłuższą chwilę."
        ),
        "example": "sfc /scannow",
        "admin_required": True,
        "command": ["sfc", "/scannow"]
    },
    "sfc /verifyonly": {
        "description": (
            "Skanuje pliki systemowe TYLKO w celu weryfikacji.\n"
            "Nie podejmuje prób naprawy."
        ),
        "example": "sfc /verifyonly",
        "admin_required": True,
        "command": ["sfc", "/verifyonly"]
    },
    "DISM /Online /Cleanup-Image /RestoreHealth": {
        "description": (
            "Naprawia obraz systemu Windows (pliki systemowe) przy pomocy DISM.\n"
            "Przydatne jeśli sfc /scannow nie rozwiązuje problemu."
        ),
        "example": "DISM /Online /Cleanup-Image /RestoreHealth",
        "admin_required": True,
        "command": ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"]
    },
    "DISM /Online /Cleanup-Image /CheckHealth": {
        "description": (
            "Sprawdza, czy obraz systemu jest oznaczony jako uszkodzony,\n"
            "ale nie naprawia."
        ),
        "example": "DISM /Online /Cleanup-Image /CheckHealth",
        "admin_required": True,
        "command": ["DISM", "/Online", "/Cleanup-Image", "/CheckHealth"]
    },
    "DISM /Online /Cleanup-Image /ScanHealth": {
        "description": (
            "Skanuje obraz systemu w poszukiwaniu błędów.\n"
            "Nie naprawia automatycznie."
        ),
        "example": "DISM /Online /Cleanup-Image /ScanHealth",
        "admin_required": True,
        "command": ["DISM", "/Online", "/Cleanup-Image", "/ScanHealth"]
    },
    "chkdsk /f": {
        "description": (
            "Sprawdza dysk w poszukiwaniu błędów i je naprawia (np. chkdsk C: /f).\n"
            "Może wymagać restartu w przypadku partycji systemowej."
        ),
        "example": "chkdsk C: /f",
        "admin_required": True,
        "command": ["chkdsk", "/f"]
    },
    "cleanmgr": {
        "description": "Otwiera Oczyszczanie dysku, aby usunąć zbędne pliki.",
        "example": "cleanmgr",
        "admin_required": False,
        "command": ["cleanmgr"]
    },
    "systeminfo": {
        "description": "Wyświetla szczegółowe informacje o systemie (wersja, poprawki, itp.).",
        "example": "systeminfo",
        "admin_required": False,
        "command": ["systeminfo"]
    },
    "gpupdate /force": {
        "description": "Wymusza aktualizację zasad grupy (Group Policy).",
        "example": "gpupdate /force",
        "admin_required": True,
        "command": ["gpupdate", "/force"]
    },

    # ===== Network & Internet =====
    "ipconfig /all": {
        "description": "Pełna konfiguracja sieci (adres IP, maska, DNS, brama, MAC).",
        "example": "ipconfig /all",
        "admin_required": False,
        "command": ["ipconfig", "/all"]
    },
    "ipconfig /release": {
        "description": "Zwalnia adres IP (dla DHCP).",
        "example": "ipconfig /release",
        "admin_required": False,
        "command": ["ipconfig", "/release"]
    },
    "ipconfig /renew": {
        "description": "Odnawia adres IP (dla DHCP).",
        "example": "ipconfig /renew",
        "admin_required": False,
        "command": ["ipconfig", "/renew"]
    },
    "netstat -an": {
        "description": "Wyświetla aktywne połączenia i porty nasłuchujące w formacie numerycznym.",
        "example": "netstat -an",
        "admin_required": False,
        "command": ["netstat", "-an"]
    },
    "ping 8.8.8.8": {
        "description": "Wysyła pakiety ICMP do 8.8.8.8 (Google DNS) i sprawdza osiągalność.",
        "example": "ping 8.8.8.8",
        "admin_required": False,
        "command": ["ping", "8.8.8.8"]
    },
    "tracert 8.8.8.8": {
        "description": "Śledzi trasę pakietów do 8.8.8.8 (Google DNS).",
        "example": "tracert 8.8.8.8",
        "admin_required": False,
        "command": ["tracert", "8.8.8.8"]
    },
    "nslookup google.com": {
        "description": "Sprawdza informacje DNS dla google.com.",
        "example": "nslookup google.com",
        "admin_required": False,
        "command": ["nslookup", "google.com"]
    },
    "pathping 8.8.8.8": {
        "description": "Łączy ping i tracert, analizując utratę pakietów.",
        "example": "pathping 8.8.8.8",
        "admin_required": False,
        "command": ["pathping", "8.8.8.8"]
    },
    "netsh wlan show profiles": {
        "description": "Pokazuje profile sieci Wi-Fi w systemie.",
        "example": "netsh wlan show profiles",
        "admin_required": False,
        "command": ["netsh", "wlan", "show", "profiles"]
    },
    "netsh interface ip reset": {
        "description": "Resetuje konfigurację TCP/IP (wymaga admina).",
        "example": "netsh interface ip reset",
        "admin_required": True,
        "command": ["netsh", "interface", "ip", "reset"]
    },
    "netsh interface show interface": {
        "description": "Wyświetla listę interfejsów sieciowych i ich stan.",
        "example": "netsh interface show interface",
        "admin_required": False,
        "command": ["netsh", "interface", "show", "interface"]
    },
    "nbtstat -n": {
        "description": "Pokazuje statystyki NetBIOS i nazwy NetBIOS lokalnego komputera.",
        "example": "nbtstat -n",
        "admin_required": False,
        "command": ["nbtstat", "-n"]
    },
    "netsh advfirewall show allprofiles": {
        "description": (
            "Wyświetla konfigurację wszystkich profili zapory Windows (advfirewall)."
        ),
        "example": "netsh advfirewall show allprofiles",
        "admin_required": True,
        "command": ["netsh", "advfirewall", "show", "allprofiles"]
    },

    # ===== Processes & Services =====
    "tasklist": {
        "description": "Wyświetla listę aktualnie uruchomionych procesów.",
        "example": "tasklist",
        "admin_required": False,
        "command": ["tasklist"]
    },
    "taskkill /IM notepad.exe /F": {
        "description": "Zamyka proces notatnika. /F wymusza.",
        "example": "taskkill /IM notepad.exe /F",
        "admin_required": True,
        "command": ["taskkill", "/IM", "notepad.exe", "/F"]
    },
    "whoami": {
        "description": "Pokazuje aktualnie zalogowanego użytkownika (domena\\nazwa).",
        "example": "whoami",
        "admin_required": False,
        "command": ["whoami"]
    },
    "hostname": {
        "description": "Pokazuje nazwę hosta (komputera).",
        "example": "hostname",
        "admin_required": False,
        "command": ["hostname"]
    },
    "sc query": {
        "description": "Wyświetla informacje o usługach w systemie.",
        "example": "sc query spooler",
        "admin_required": True,
        "command": ["sc", "query"]
    },
    "sc start spooler": {
        "description": "Uruchamia usługę spooler (bufor wydruku).",
        "example": "sc start spooler",
        "admin_required": True,
        "command": ["sc", "start", "spooler"]
    },
    "sc stop spooler": {
        "description": "Zatrzymuje usługę spooler.",
        "example": "sc stop spooler",
        "admin_required": True,
        "command": ["sc", "stop", "spooler"]
    },

    # ===== File & Disk Management =====
    "diskpart": {
        "description": "Zaawansowane narzędzie do zarządzania dyskami i partycjami.",
        "example": "diskpart",
        "admin_required": True,
        "command": ["diskpart"]
    },
    "format A:": {
        "description": "Formatuje wskazany napęd (A:). Usuwa wszystkie dane!",
        "example": "format E: /fs:NTFS",
        "admin_required": True,
        "command": ["format", "A:"]
    },
    "label": {
        "description": "Wyświetla lub ustawia etykietę woluminu dysku.",
        "example": "label C: NowaNazwa",
        "admin_required": True,
        "command": ["label"]
    },
    "dir": {
        "description": "Wyświetla listę plików i folderów w katalogu.",
        "example": "dir C:\\Windows\\System32",
        "admin_required": False,
        "command": ["dir"]
    },
    "tree": {
        "description": "Pokazuje strukturę katalogów w formie drzewa.",
        "example": "tree C:\\Windows",
        "admin_required": False,
        "command": ["tree"]
    },
    "xcopy": {
        "description": "Zaawansowane kopiowanie plików/folderów (np. /E, /S).",
        "example": "xcopy C:\\folder1 D:\\folder2 /E",
        "admin_required": True,
        "command": ["xcopy"]
    },
    "robocopy": {
        "description": "Kopiowanie/synchronizacja plików (idealne do backupu).",
        "example": "robocopy C:\\folder1 D:\\folder2 /mir",
        "admin_required": True,
        "command": ["robocopy"]
    },
    "takeown /f": {
        "description": (
            "Przejmuje na własność wskazany plik/folder.\n"
            "Podaj ścieżkę, np. takeown /f C:\\katalog"
        ),
        "example": "takeown /f C:\\katalog /r",
        "admin_required": True,
        "command": ["takeown", "/f"]
    },
    "icacls": {
        "description": (
            "Zarządza ACL dla plików/folderów, np. /grant, /deny.\n"
            "Wymaga ścieżki."
        ),
        "example": "icacls C:\\katalog /grant Administrator:F",
        "admin_required": True,
        "command": ["icacls"]
    },
    "fsutil fsinfo drives": {
        "description": "Wyświetla listę dysków logicznych w systemie.",
        "example": "fsutil fsinfo drives",
        "admin_required": True,
        "command": ["fsutil", "fsinfo", "drives"]
    },
    "manage-bde -status": {
        "description": (
            "Sprawdza status szyfrowania BitLocker na dostępnych dyskach (jeśli jest)."
        ),
        "example": "manage-bde -status",
        "admin_required": True,
        "command": ["manage-bde", "-status"]
    },
    "md C:\\TestFolder": {
        "description": "Tworzy nowy katalog (C:\\TestFolder).",
        "example": "md C:\\NowyFolder",
        "admin_required": True,
        "command": ["md", "C:\\TestFolder"]
    },
    "rd C:\\TestFolder /s /q": {
        "description": (
            "Usuwa folder C:\\TestFolder wraz z podfolderami (/s)\n"
            "i bez pytania o potwierdzenie (/q)."
        ),
        "example": "rd C:\\InnyFolder /s /q",
        "admin_required": True,
        "command": ["rd", "C:\\TestFolder", "/s", "/q"]
    },

    # ===== Registry & Config =====
    "reg query HKLM\\Software": {
        "description": "Przykładowe zapytanie do rejestru w kluczu HKLM\\Software.",
        "example": "reg query HKLM\\Software\\Microsoft",
        "admin_required": False,
        "command": ["reg", "query", "HKLM\\Software"]
    },
    "reg add": {
        "description": "Dodaje nowy wpis do rejestru (wymaga parametrów, np. klucz, wartość).",
        "example": "reg add HKCU\\Software\\Test /v Nazwa /t REG_SZ /d Wartosc",
        "admin_required": True,
        "command": ["reg", "add"]
    },
    "reg delete": {
        "description": (
            "Usuwa wpis w rejestrze (wymaga parametrów, np. klucz).\n"
            "Operacja nieodwracalna!"
        ),
        "example": "reg delete HKCU\\Software\\Test /v Nazwa /f",
        "admin_required": True,
        "command": ["reg", "delete"]
    },
    "bcdedit": {
        "description": "Wyświetla lub modyfikuje dane konfiguracji rozruchu (BCD).",
        "example": "bcdedit /set {default} safeboot minimal",
        "admin_required": True,
        "command": ["bcdedit"]
    },
    "regsvr32 /?": {
        "description": (
            "Rejestruje/wyrejestrowuje biblioteki DLL i kontrolki OCX.\n"
            "Z /? wyświetla pomoc."
        ),
        "example": "regsvr32 /u C:\\example.dll",
        "admin_required": True,
        "command": ["regsvr32", "/?"]
    },
    "wevtutil el": {
        "description": "Wyświetla listę logów zdarzeń w systemie (Event Viewer).",
        "example": "wevtutil el",
        "admin_required": True,
        "command": ["wevtutil", "el"]
    },
    "logman /?": {
        "description": (
            "Zarządza kolekcjami danych wydajności i śledzenia (logman)."
        ),
        "example": "logman /?",
        "admin_required": True,
        "command": ["logman", "/?"]
    },
    "wmic /?": {
        "description": (
            "Narzędzie Windows Management Instrumentation Command-line (WMIC).\n"
            "Z /? pokazuje pomoc."
        ),
        "example": "wmic cpu get name",
        "admin_required": True,
        "command": ["wmic", "/?"]
    },

    # ===== Users & Groups =====
    "net view": {
        "description": (
            "Pokazuje komputery w bieżącej grupie roboczej lub domenie."
        ),
        "example": "net view \\\\NazwaKomputera",
        "admin_required": False,
        "command": ["net", "view"]
    },
    "net user": {
        "description": (
            "Wyświetla/modyfikuje konta użytkowników lokalnych (np. /add /delete)."
        ),
        "example": "net user NowyUser Haslo /add",
        "admin_required": True,
        "command": ["net", "user"]
    },
    "net localgroup Administrators": {
        "description": (
            "Pokazuje członków grupy lokalnej Administratorzy."
        ),
        "example": "net localgroup Administrators /add NazwaUzytkownika",
        "admin_required": True,
        "command": ["net", "localgroup", "Administrators"]
    },
    "net share": {
        "description": "Wyświetla lub konfiguruje udziały sieciowe (pliki, drukarki).",
        "example": "net share Udzial=C:\\Sciezka",
        "admin_required": True,
        "command": ["net", "share"]
    },
    "net start": {
        "description": "Wyświetla uruchomione usługi lub uruchamia wybraną usługę.",
        "example": "net start Spooler",
        "admin_required": True,
        "command": ["net", "start"]
    },
    "net accounts": {
        "description": "Konfiguruje parametry kont (hasła, czasy).",
        "example": "net accounts /minpwlen:8",
        "admin_required": True,
        "command": ["net", "accounts"]
    },
    "net session": {
        "description": "Wyświetla lub rozłącza sesje na serwerze lokalnym.",
        "example": "net session /delete",
        "admin_required": True,
        "command": ["net", "session"]
    },
    "net group": {
        "description": (
            "Wyświetla/modyfikuje grupy w domenie (może wymagać Active Directory)."
        ),
        "example": "net group NazwaGrupy /add",
        "admin_required": True,
        "command": ["net", "group"]
    },

    # ===== WSL & Advanced =====
    "wsl --list": {
        "description": "Pokazuje listę zainstalowanych dystrybucji WSL.",
        "example": "wsl --list --verbose",
        "admin_required": False,
        "command": ["wsl", "--list"]
    },
    "wsl --install": {
        "description": "Instaluje WSL (domyślną dystrybucję).",
        "example": "wsl --install -d Ubuntu",
        "admin_required": True,
        "command": ["wsl", "--install"]
    },
    "wsl --unregister Ubuntu": {
        "description": (
            "Usuwa (unregister) wybraną dystrybucję WSL,\n"
            "tracąc wszystkie dane w niej."
        ),
        "example": "wsl --unregister Ubuntu",
        "admin_required": True,
        "command": ["wsl", "--unregister", "Ubuntu"]
    },
    "shutdown /r /t 0": {
        "description": "Natychmiastowy restart komputera.",
        "example": "shutdown /r /t 0",
        "admin_required": True,
        "command": ["shutdown", "/r", "/t", "0"]
    },
    "shutdown /s /t 0": {
        "description": "Natychmiastowe wyłączenie komputera.",
        "example": "shutdown /s /t 0",
        "admin_required": True,
        "command": ["shutdown", "/s", "/t", "0"]
    },
    "powercfg /energy": {
        "description": "Generuje raport efektywności energetycznej systemu.",
        "example": "powercfg /energy",
        "admin_required": True,
        "command": ["powercfg", "/energy"]
    },
    "powercfg /batteryreport": {
        "description": "Tworzy raport baterii (przydatne na laptopach).",
        "example": "powercfg /batteryreport",
        "admin_required": True,
        "command": ["powercfg", "/batteryreport"]
    },
    "bcdedit": {
        "description": (
            "Wyświetla lub modyfikuje dane konfiguracji rozruchu (BCD)."
        ),
        "example": "bcdedit /set {default} safeboot minimal",
        "admin_required": True,
        "command": ["bcdedit"]
    },
    "perfmon /report": {
        "description": "Uruchamia Performance Monitor z raportem diagnostycznym.",
        "example": "perfmon /report",
        "admin_required": True,
        "command": ["perfmon", "/report"]
    },
    "wbadmin start backup": {
        "description": (
            "Rozpoczyna backup przy użyciu wbadmin (wymaga parametrów)."
        ),
        "example": "wbadmin start backup -backupTarget:E: -include:C: -quiet",
        "admin_required": True,
        "command": ["wbadmin", "start", "backup"]
    },
    "lxrun /install": {
        "description": (
            "Instaluje i konfiguruje WSL (starsza metoda dla Windows 10)."
        ),
        "example": "lxrun /install /y",
        "admin_required": True,
        "command": ["lxrun", "/install"]
    },

    # ===== Misc & Others =====
    "cls": {
        "description": "Czyści okno konsoli (symbolicznie w tym programie).",
        "example": "cls",
        "admin_required": False,
        "command": ["cls"]
    },
    "help": {
        "description": "Wyświetla listę podstawowych poleceń w wierszu poleceń.",
        "example": "help dir",
        "admin_required": False,
        "command": ["help"]
    },
    "echo Hello World": {
        "description": "Wyświetla napis 'Hello World' w konsoli.",
        "example": "echo Test",
        "admin_required": False,
        "command": ["echo", "Hello", "World"]
    },
    "ver": {
        "description": "Pokazuje wersję systemu Windows.",
        "example": "ver",
        "admin_required": False,
        "command": ["ver"]
    },
    "pause": {
        "description": "Wstrzymuje działanie skryptu (Press any key...).",
        "example": "pause",
        "admin_required": False,
        "command": ["pause"]
    },
    "color 0a": {
        "description": "Ustawia kolor konsoli (0a = czarne tło, zielone litery).",
        "example": "color 1f",
        "admin_required": False,
        "command": ["color", "0a"]
    },
    "schtasks /query": {
        "description": "Wyświetla zaplanowane zadania w systemie.",
        "example": "schtasks /query /fo LIST /v",
        "admin_required": True,
        "command": ["schtasks", "/query"]
    },
    "schtasks /run /tn \"\\Microsoft\\Windows\\Defrag\\ScheduledDefrag\"": {
        "description": "Uruchamia wybrane zadanie Defrag (po nazwie).",
        "example": "schtasks /run /tn \"\\Microsoft\\Windows\\Defrag\\ScheduledDefrag\"",
        "admin_required": True,
        "command": ["schtasks", "/run", "/tn", "\\Microsoft\\Windows\\Defrag\\ScheduledDefrag"]
    },
    "net time": {
        "description": (
            "Wyświetla lub synchronizuje czas na komputerze z serwerem.\n"
            "Może wymagać parametrów i uprawnień."
        ),
        "example": "net time \\\\Serwer /set /y",
        "admin_required": True,
        "command": ["net", "time"]
    },
    "net file": {
        "description": (
            "Wyświetla listę otwartych plików w udostępnieniach.\n"
            "Może zamykać wybrane pliki."
        ),
        "example": "net file /close",
        "admin_required": True,
        "command": ["net", "file"]
    },
    "at /?": {
        "description": (
            "Wyświetla pomoc do starego (niezalecanego) harmonogramu zadań.\n"
            "Schtasks jest nowsze."
        ),
        "example": "at /?",
        "admin_required": True,
        "command": ["at", "/?"]
    },
    "type NUL > C:\\TestFolder\\sample.txt": {
        "description": (
            "Tworzy pusty plik sample.txt w C:\\TestFolder,\n"
            "za pomocą przekierowania (type NUL)."
        ),
        "example": "type NUL > C:\\InnyFolder\\test.txt",
        "admin_required": True,
        "command": ["type", "NUL", ">", "C:\\TestFolder\\sample.txt"]
    }
}


class MatrixWindowsCommander(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matrix Windows Commander (Enhanced)")
        self.resize(1200, 650)
        self.initUI()

    def initUI(self):
        # Styl w klimacie „Matrixa”
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                font-family: Consolas;
                color: #00ff00;
            }
            QListWidget {
                background-color: #001000;
                color: #00ff00;
            }
            QTextEdit {
                background-color: #001000;
                color: #00ff00;
            }
            QPushButton {
                background-color: #003000;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #005000;
            }
            QLabel#TitleLabel {
                font-weight: bold;
                font-size: 18pt;
                color: #00ff00;
                margin-bottom: 10px;
            }
            QLabel {
                font-weight: bold;
            }
            QComboBox {
                background-color: #001000;
                color: #00ff00;
                border: 1px solid #00ff00;
            }
            QComboBox QAbstractItemView {
                background-color: #001000;
                color: #00ff00;
                selection-background-color: #005000;
            }
        """)

        main_layout = QVBoxLayout()

        # Tytuł
        self.title_label = QLabel("MATRIX WINDOWS COMMANDER (ENHANCED)")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Górny layout: wybór kategorii
        top_layout = QHBoxLayout()
        category_label = QLabel("Kategoria:")
        self.category_combo = QComboBox()
        for cat in categories.keys():
            self.category_combo.addItem(cat)
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)

        top_layout.addWidget(category_label)
        top_layout.addWidget(self.category_combo)
        main_layout.addLayout(top_layout)

        # Lista komend
        self.list_widget = QListWidget()
        main_layout.addWidget(self.list_widget)

        # Pole opisu komendy
        self.description_box = QTextEdit()
        self.description_box.setReadOnly(True)
        main_layout.addWidget(self.description_box)

        # Przycisk uruchomienia
        self.run_button = QPushButton("Uruchom polecenie")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run_command)
        main_layout.addWidget(self.run_button)

        # Stopka
        self.footer_label = QLabel("Matrix Windows Commander by Swir - Enhanced Error Handling")
        self.footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.footer_label)

        self.setLayout(main_layout)

        # Domyślnie wczytujemy pierwszą kategorię
        self.load_commands_for_category(list(categories.keys())[0])
        self.list_widget.currentItemChanged.connect(self.display_description)

    def on_category_changed(self, index):
        cat_name = self.category_combo.currentText()
        self.load_commands_for_category(cat_name)

    def load_commands_for_category(self, cat_name):
        self.list_widget.clear()
        if cat_name in categories:
            cmd_list = categories[cat_name]
            for cmd_key in cmd_list:
                self.list_widget.addItem(cmd_key)
        self.description_box.clear()
        self.run_button.setEnabled(False)

    def display_description(self, current, previous):
        if current:
            cmd_key = current.text()
            if cmd_key in commands:
                info = commands[cmd_key]
                desc = info["description"]
                example = info.get("example", "")
                admin_info = "Tak" if info.get("admin_required", False) else "Nie"

                text = (
                    f"**Opis:**\n{desc}\n\n"
                    f"**Przykład:**\n{example}\n\n"
                    f"**Wymaga administratora?** {admin_info}"
                )
                self.description_box.setText(text)
                self.run_button.setEnabled(True)
            else:
                self.description_box.setText("Brak opisu dla tej komendy.")
                self.run_button.setEnabled(False)
        else:
            self.description_box.clear()
            self.run_button.setEnabled(False)

    def run_command(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            cmd_key = current_item.text()
            if cmd_key in commands:
                cmd_info = commands[cmd_key]
                cmd_list = cmd_info["command"]

                try:
                    result = subprocess.run(
                        cmd_list,
                        capture_output=True,
                        text=True,
                        shell=True,
                        timeout=10
                    )
                    output = result.stdout.strip() if result.stdout else ""
                    error = result.stderr.strip() if result.stderr else ""

                    if result.returncode == 0:
                        # Sukces
                        msg = output if output else "Polecenie wykonane pomyślnie (brak dodatkowego wyjścia)."
                    else:
                        # Błąd
                        msg = error if error else "Nieznany błąd (brak informacji)."
                        # Dodatkowe wskazówki w zależności od tekstu błędu
                        if "Access is denied" in error or "Odmowa dostępu" in error:
                            msg += (
                                "\n\n***Możliwe, że brakuje uprawnień administratora. "
                                "Spróbuj uruchomić program jako administrator.***"
                            )
                        if "not recognized as an internal or external command" in error or "nie jest rozpoznawalny" in error:
                            msg += (
                                "\n\n***Polecenie nie jest rozpoznawane. "
                                "Sprawdź czy wpisano poprawnie i czy znajduje się w PATH.***"
                            )
                        if "system cannot find" in error or "nie można odnaleźć" in error:
                            msg += (
                                "\n\n***Ścieżka/plik nie istnieje. Sprawdź poprawność ścieżki.***"
                            )
                        msg += "\n\n***Spróbuj uruchomić w wierszu poleceń (CMD) lub PowerShell jako administrator.***"

                    self.show_output_window(cmd_key, msg)

                except subprocess.TimeoutExpired:
                    self.show_output_window(
                        cmd_key,
                        "Polecenie trwało zbyt długo i zostało przerwane (może być interaktywne). Odpal Polecenie w CMD"
                    )
                except Exception as e:
                    self.show_output_window(cmd_key, f"Wystąpił nieoczekiwany błąd:\n{e}")

    def show_output_window(self, cmd_key, message):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Wynik polecenia: {cmd_key}")
        dialog.resize(800, 500)

        # Styl w nowym oknie
        dialog.setStyleSheet("""
            QDialog {
                background-color: black;
            }
            QPlainTextEdit {
                background-color: #001000;
                color: #00ff00;
                font-family: Consolas;
            }
        """)

        layout = QVBoxLayout()
        text_edit = QPlainTextEdit()
        text_edit.setPlainText(message)
        text_edit.setReadOnly(True)

        layout.addWidget(text_edit)
        dialog.setLayout(layout)

        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixWindowsCommander()
    window.show()
    sys.exit(app.exec_())
