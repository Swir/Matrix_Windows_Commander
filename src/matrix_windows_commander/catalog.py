from __future__ import annotations

from .models import CommandSpec, Risk


COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec("systeminfo", "System", "System information", "systeminfo", description_en="Detailed Windows version, hardware and hotfix information.", description_pl="Szczegółowe informacje o Windows, sprzęcie i poprawkach."),
    CommandSpec("hostname", "System", "Computer hostname", "hostname", description_en="Shows the local computer name.", description_pl="Pokazuje nazwę lokalnego komputera."),
    CommandSpec("ver", "System", "Windows version", "cmd.exe", ("/d", "/c", "ver"), "Shows the Windows command processor version string.", "Pokazuje wersję systemu Windows zwracaną przez wiersz poleceń."),
    CommandSpec("drivers", "System", "Installed drivers", "driverquery", ("/v",), "Lists installed Windows drivers with verbose details.", "Wyświetla zainstalowane sterowniki Windows ze szczegółami."),
    CommandSpec("reg_software", "System", "Installed software registry branch", "reg", ("query", r"HKLM\Software"), "Reads the HKLM Software registry branch without changing it.", "Odczytuje gałąź rejestru HKLM\\Software bez jej modyfikowania."),
    CommandSpec("regsvr32_help", "System", "Regsvr32 help", "regsvr32", ("/?",), "Shows Regsvr32 usage without registering or unregistering anything.", "Pokazuje pomoc Regsvr32 bez rejestrowania ani wyrejestrowywania bibliotek."),
    CommandSpec("event_logs", "System", "Event log channels", "wevtutil", ("el",), "Lists registered Windows Event Log channels.", "Wyświetla zarejestrowane kanały Dziennika zdarzeń Windows."),
    CommandSpec("scheduled_tasks", "System", "Scheduled tasks", "schtasks", ("/query", "/fo", "LIST", "/v"), "Lists scheduled tasks with verbose metadata.", "Wyświetla zaplanowane zadania wraz ze szczegółami.", timeout_seconds=180),
    CommandSpec("bcd_enum", "System", "Boot configuration", "bcdedit", ("/enum",), "Reads the current Boot Configuration Data entries without modifying them.", "Odczytuje bieżące wpisy konfiguracji rozruchu BCD bez ich modyfikowania.", True),
    CommandSpec("logman_help", "System", "Performance logging help", "logman", ("/?",), "Shows Logman usage and available performance-counter logging commands.", "Pokazuje pomoc Logman i dostępne polecenia rejestrowania liczników wydajności."),
    CommandSpec("cleanmgr", "System", "Disk Cleanup", "cleanmgr", (), "Opens the built-in Windows Disk Cleanup interface; the user chooses what to remove.", "Otwiera systemowe Oczyszczanie dysku; użytkownik sam wybiera elementy do usunięcia."),
    CommandSpec("perfmon_report", "System", "Performance diagnostic report", "perfmon", ("/report",), "Starts the built-in Windows performance diagnostic report.", "Uruchamia wbudowany raport diagnostyczny wydajności Windows.", False, Risk.CHANGE, 180),

    CommandSpec("sfc_verify", "System", "SFC verify", "sfc", ("/verifyonly",), "Checks protected system files without repairing them.", "Sprawdza chronione pliki systemowe bez naprawiania.", True),
    CommandSpec("sfc_scan", "Repair", "SFC scan & repair", "sfc", ("/scannow",), "Scans protected system files and repairs detected corruption.", "Skanuje chronione pliki systemowe i naprawia wykryte uszkodzenia.", True, Risk.REPAIR, 1800),
    CommandSpec("dism_check", "System", "DISM CheckHealth", "DISM", ("/Online", "/Cleanup-Image", "/CheckHealth"), "Quickly checks whether the Windows image is marked as corrupted.", "Szybko sprawdza, czy obraz Windows jest oznaczony jako uszkodzony.", True),
    CommandSpec("dism_scan", "System", "DISM ScanHealth", "DISM", ("/Online", "/Cleanup-Image", "/ScanHealth"), "Performs a deeper Windows component-store health scan.", "Wykonuje dokładniejsze skanowanie magazynu składników Windows.", True, Risk.READ_ONLY, 900),
    CommandSpec("dism_restore", "Repair", "DISM RestoreHealth", "DISM", ("/Online", "/Cleanup-Image", "/RestoreHealth"), "Repairs the Windows component store. This can take a long time.", "Naprawia magazyn składników Windows. Operacja może potrwać długo.", True, Risk.REPAIR, 1800),
    CommandSpec("chkdsk_readonly", "Storage", "Check C: filesystem", "chkdsk", ("C:",), "Checks the C: filesystem without requesting repair.", "Sprawdza system plików C: bez żądania naprawy.", True, Risk.READ_ONLY, 600),
    CommandSpec("chkdsk_repair", "Repair", "Repair C: filesystem", "chkdsk", ("C:", "/f"), "Requests filesystem error repair on C:. Windows may schedule the operation for reboot.", "Żąda naprawy błędów systemu plików C:. Windows może zaplanować operację przy restarcie.", True, Risk.REPAIR, 600),
    CommandSpec("gpupdate", "Repair", "Refresh Group Policy", "gpupdate", ("/force",), "Refreshes local/domain Group Policy. Use on computers you administer.", "Odświeża lokalne/domenowe zasady grupy. Używaj na komputerach, którymi administrujesz.", True, Risk.CHANGE, 600),

    CommandSpec("ip_all", "Network", "IP configuration", "ipconfig", ("/all",), "Shows detailed adapter, DHCP, DNS and address information.", "Pokazuje szczegółowe informacje o kartach, DHCP, DNS i adresach."),
    CommandSpec("ip_display_dns", "Network", "DNS resolver cache", "ipconfig", ("/displaydns",), "Displays the local DNS resolver cache.", "Wyświetla lokalną pamięć podręczną DNS."),
    CommandSpec("ip_release", "Network Repair", "Release DHCP leases", "ipconfig", ("/release",), "Releases DHCP leases. Network connectivity can be interrupted until renewed.", "Zwalnia dzierżawy DHCP. Połączenie sieciowe może zostać przerwane do czasu odnowienia.", False, Risk.CHANGE, 120),
    CommandSpec("ip_renew", "Network Repair", "Renew DHCP leases", "ipconfig", ("/renew",), "Renews DHCP leases for configured adapters.", "Odnawia dzierżawy DHCP dla skonfigurowanych kart.", False, Risk.CHANGE, 180),
    CommandSpec("flush_dns", "Network Repair", "Flush DNS cache", "ipconfig", ("/flushdns",), "Clears the local DNS resolver cache.", "Czyści lokalną pamięć podręczną resolvera DNS.", True, Risk.CHANGE),
    CommandSpec("winsock_reset", "Network Repair", "Reset Winsock", "netsh", ("winsock", "reset"), "Resets the Winsock catalog. A reboot may be required afterwards.", "Resetuje katalog Winsock. Później może być wymagany restart.", True, Risk.REPAIR),
    CommandSpec("ip_stack_reset", "Network Repair", "Reset TCP/IP stack", "netsh", ("interface", "ip", "reset"), "Resets TCP/IP configuration. A reboot may be required and custom adapter settings can be affected.", "Resetuje konfigurację TCP/IP. Może być wymagany restart, a niestandardowe ustawienia kart mogą ulec zmianie.", True, Risk.REPAIR, 180),
    CommandSpec("ping_cloudflare", "Network", "Connectivity test", "ping", ("1.1.1.1", "-n", "4"), "Sends four ICMP probes to Cloudflare DNS to test connectivity.", "Wysyła cztery pakiety ICMP do Cloudflare DNS, aby sprawdzić połączenie."),
    CommandSpec("tracert_cloudflare", "Network", "Network route", "tracert", ("-d", "1.1.1.1"), "Shows the network path without slow reverse-DNS lookups.", "Pokazuje trasę sieciową bez powolnego odwrotnego DNS.", timeout_seconds=180),
    CommandSpec("pathping_cloudflare", "Network", "PathPing diagnostics", "pathping", ("1.1.1.1",), "Measures packet loss and latency along the route to Cloudflare DNS.", "Mierzy utratę pakietów i opóźnienia na trasie do Cloudflare DNS.", timeout_seconds=420),
    CommandSpec("dns_lookup", "Network", "DNS lookup", "nslookup", ("example.com",), "Tests DNS resolution using a harmless example domain.", "Testuje rozwiązywanie DNS na bezpiecznej domenie przykładowej."),
    CommandSpec("netstat", "Network", "Connections & listeners", "netstat", ("-ano",), "Lists active TCP/UDP endpoints and owning process IDs.", "Wyświetla aktywne połączenia TCP/UDP i identyfikatory procesów."),
    CommandSpec("route_print", "Network", "Routing table", "route", ("print",), "Displays the local IPv4/IPv6 routing table.", "Wyświetla lokalną tablicę routingu IPv4/IPv6."),
    CommandSpec("arp_table", "Network", "ARP cache", "arp", ("-a",), "Displays the local ARP neighbor cache.", "Wyświetla lokalną pamięć sąsiadów ARP."),
    CommandSpec("interfaces", "Network", "Network interfaces", "netsh", ("interface", "show", "interface"), "Shows Windows network interfaces and their state.", "Pokazuje interfejsy sieciowe Windows i ich stan."),
    CommandSpec("wifi_interfaces", "Network", "Wi-Fi interface status", "netsh", ("wlan", "show", "interfaces"), "Shows current Wi-Fi interface status without revealing saved passwords.", "Pokazuje stan Wi-Fi bez ujawniania zapisanych haseł."),
    CommandSpec("wifi_profiles", "Network", "Saved Wi-Fi profile names", "netsh", ("wlan", "show", "profiles"), "Lists saved Wi-Fi profile names only; it does not request stored keys/passwords.", "Wyświetla tylko nazwy zapisanych profili Wi-Fi; nie pobiera zapisanych kluczy ani haseł."),
    CommandSpec("netbios_names", "Network", "Local NetBIOS names", "nbtstat", ("-n",), "Displays locally registered NetBIOS names.", "Wyświetla lokalnie zarejestrowane nazwy NetBIOS."),
    CommandSpec("firewall_status", "Security", "Firewall profiles", "netsh", ("advfirewall", "show", "allprofiles"), "Shows Windows Firewall profile status and policy.", "Pokazuje stan profili i zasady Zapory Windows."),

    CommandSpec("whoami", "Security", "Identity & privileges", "whoami", ("/all",), "Shows the current identity, groups and enabled privileges.", "Pokazuje bieżącą tożsamość, grupy i uprawnienia."),
    CommandSpec("net_users", "Accounts", "Local/domain users", "net", ("user",), "Lists user accounts visible to the local Windows account.", "Wyświetla konta użytkowników widoczne dla bieżącego konta Windows."),
    CommandSpec("net_localgroups", "Accounts", "Local groups", "net", ("localgroup",), "Lists local groups without changing membership.", "Wyświetla lokalne grupy bez zmiany ich członkostwa."),
    CommandSpec("net_domain_groups", "Accounts", "Domain groups", "net", ("group",), "Lists domain groups when the computer is joined to a domain; otherwise Windows may report that the command is unavailable.", "Wyświetla grupy domenowe, gdy komputer należy do domeny; w innym przypadku Windows może zgłosić brak dostępności."),
    CommandSpec("net_accounts", "Accounts", "Account policy", "net", ("accounts",), "Shows password and logon policy for the local/domain context.", "Pokazuje zasady haseł i logowania dla komputera lub domeny."),
    CommandSpec("net_shares", "Accounts", "Shared resources", "net", ("share",), "Lists Windows shared resources.", "Wyświetla udostępnione zasoby Windows."),
    CommandSpec("net_view", "Network", "Visible Windows computers", "net", ("view",), "Lists visible Windows network computers/resources when discovery is available.", "Wyświetla widoczne komputery/zasoby sieci Windows, jeśli wykrywanie jest dostępne."),
    CommandSpec("net_sessions", "Accounts", "Active SMB sessions", "net", ("session",), "Lists SMB sessions to this computer. Administrator rights are normally required.", "Wyświetla sesje SMB do tego komputera. Zwykle wymagane są uprawnienia administratora.", True),
    CommandSpec("net_open_files", "Accounts", "Open shared files", "net", ("file",), "Lists files opened through Windows file sharing. Administrator rights are normally required.", "Wyświetla pliki otwarte przez udostępnianie Windows. Zwykle wymagane są uprawnienia administratora.", True),

    CommandSpec("tasklist", "Processes", "Running processes", "tasklist", ("/v",), "Shows running processes with verbose metadata.", "Pokazuje uruchomione procesy ze szczegółowymi informacjami."),
    CommandSpec("services", "Processes", "Windows services", "sc", ("query", "type=", "service", "state=", "all"), "Lists Windows services and their state.", "Wyświetla usługi Windows i ich stan."),
    CommandSpec("net_started_services", "Processes", "Started services", "net", ("start",), "Lists services that are currently started.", "Wyświetla usługi, które są obecnie uruchomione."),
    CommandSpec("close_notepad", "Processes", "Close Notepad", "taskkill", ("/IM", "notepad.exe", "/F"), "Force-closes Notepad processes. Unsaved Notepad text can be lost, so confirmation is required.", "Wymusza zamknięcie procesów Notatnika. Niezapisany tekst może zostać utracony, dlatego wymagane jest potwierdzenie.", False, Risk.CHANGE),
    CommandSpec("spooler_status", "Processes", "Print Spooler status", "sc", ("query", "spooler"), "Shows the Print Spooler service state.", "Pokazuje stan usługi Bufor wydruku."),
    CommandSpec("spooler_start", "Service Repair", "Start Print Spooler", "sc", ("start", "spooler"), "Starts the Print Spooler service on the local computer.", "Uruchamia usługę Bufor wydruku na lokalnym komputerze.", True, Risk.CHANGE),
    CommandSpec("spooler_stop", "Service Repair", "Stop Print Spooler", "sc", ("stop", "spooler"), "Stops the Print Spooler service on the local computer.", "Zatrzymuje usługę Bufor wydruku na lokalnym komputerze.", True, Risk.CHANGE),

    CommandSpec("drives", "Storage", "Available drives", "fsutil", ("fsinfo", "drives"), "Lists detected drive letters.", "Wyświetla wykryte litery dysków.", True),
    CommandSpec("bitlocker", "Storage", "BitLocker status", "manage-bde", ("-status",), "Shows BitLocker protection status for local volumes.", "Pokazuje stan ochrony BitLocker dla lokalnych woluminów.", True),

    CommandSpec("power_modes", "Power", "Available sleep states", "powercfg", ("/a",), "Shows sleep states supported by this computer.", "Pokazuje stany uśpienia obsługiwane przez komputer."),
    CommandSpec("power_requests", "Power", "Power requests", "powercfg", ("/requests",), "Shows processes or drivers currently preventing sleep/display idle.", "Pokazuje procesy lub sterowniki blokujące uśpienie albo wygaszanie.", True),
    CommandSpec("battery_report", "Power", "Battery report", "powercfg", ("/batteryreport",), "Generates the standard Windows battery report HTML file and prints its path.", "Generuje standardowy raport baterii Windows w HTML i pokazuje jego ścieżkę.", True, Risk.CHANGE, 180),
    CommandSpec("energy_report", "Power", "Energy efficiency report", "powercfg", ("/energy", "/duration", "10"), "Runs a short Windows energy diagnostic and writes the standard HTML report.", "Uruchamia krótki test energetyczny Windows i zapisuje standardowy raport HTML.", True, Risk.CHANGE, 180),

    CommandSpec("wsl_status", "WSL", "WSL status", "wsl", ("--status",), "Shows Windows Subsystem for Linux configuration.", "Pokazuje konfigurację Windows Subsystem for Linux."),
    CommandSpec("wsl_list", "WSL", "WSL distributions", "wsl", ("--list", "--verbose"), "Lists installed WSL distributions and versions.", "Wyświetla zainstalowane dystrybucje WSL i ich wersje."),
    CommandSpec("wsl_install", "WSL", "Install default WSL distribution", "wsl", ("--install",), "Installs/enables WSL using Microsoft's default flow. This changes Windows features and may require a reboot.", "Instaluje/włącza WSL domyślną metodą Microsoft. Zmienia funkcje Windows i może wymagać restartu.", True, Risk.CHANGE, 1800),
)

CATEGORIES: tuple[str, ...] = tuple(dict.fromkeys(item.category for item in COMMANDS))


def search_catalog(query: str = "", category: str | None = None) -> list[CommandSpec]:
    needle = query.strip().lower()
    result: list[CommandSpec] = []
    for item in COMMANDS:
        if category and category != "All" and item.category != category:
            continue
        haystack = " ".join((item.id, item.title, item.description_en, item.description_pl, item.command_line)).lower()
        if needle and needle not in haystack:
            continue
        result.append(item)
    return result


def get_command(command_id: str) -> CommandSpec | None:
    return next((item for item in COMMANDS if item.id == command_id), None)
