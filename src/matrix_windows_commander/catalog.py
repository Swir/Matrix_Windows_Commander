from __future__ import annotations

from .models import CommandSpec, Risk


COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec("systeminfo", "System", "System information", "systeminfo", description_en="Detailed Windows version, hardware and hotfix information.", description_pl="Szczegółowe informacje o Windows, sprzęcie i poprawkach."),
    CommandSpec("sfc_verify", "System", "SFC verify", "sfc", ("/verifyonly",), "Checks protected system files without repairing them.", "Sprawdza chronione pliki systemowe bez naprawiania.", True),
    CommandSpec("sfc_scan", "Repair", "SFC scan & repair", "sfc", ("/scannow",), "Scans protected system files and repairs detected corruption.", "Skanuje chronione pliki systemowe i naprawia wykryte uszkodzenia.", True, Risk.REPAIR, 1800),
    CommandSpec("dism_check", "System", "DISM CheckHealth", "DISM", ("/Online", "/Cleanup-Image", "/CheckHealth"), "Quickly checks whether the Windows image is marked as corrupted.", "Szybko sprawdza, czy obraz Windows jest oznaczony jako uszkodzony.", True),
    CommandSpec("dism_scan", "System", "DISM ScanHealth", "DISM", ("/Online", "/Cleanup-Image", "/ScanHealth"), "Performs a deeper Windows component-store health scan.", "Wykonuje dokładniejsze skanowanie magazynu składników Windows.", True, Risk.READ_ONLY, 900),
    CommandSpec("dism_restore", "Repair", "DISM RestoreHealth", "DISM", ("/Online", "/Cleanup-Image", "/RestoreHealth"), "Repairs the Windows component store. This can take a long time.", "Naprawia magazyn składników Windows. Operacja może potrwać długo.", True, Risk.REPAIR, 1800),
    CommandSpec("ip_all", "Network", "IP configuration", "ipconfig", ("/all",), "Shows detailed adapter, DHCP, DNS and address information.", "Pokazuje szczegółowe informacje o kartach, DHCP, DNS i adresach."),
    CommandSpec("ping_cloudflare", "Network", "Connectivity test", "ping", ("1.1.1.1", "-n", "4"), "Sends four ICMP probes to Cloudflare DNS to test connectivity.", "Wysyła cztery pakiety ICMP do Cloudflare DNS, aby sprawdzić połączenie."),
    CommandSpec("tracert_cloudflare", "Network", "Network route", "tracert", ("-d", "1.1.1.1"), "Shows the network path without slow reverse-DNS lookups.", "Pokazuje trasę sieciową bez powolnego odwrotnego DNS.", timeout_seconds=180),
    CommandSpec("dns_lookup", "Network", "DNS lookup", "nslookup", ("example.com",), "Tests DNS resolution using a harmless example domain.", "Testuje rozwiązywanie DNS na bezpiecznej domenie przykładowej."),
    CommandSpec("netstat", "Network", "Connections & listeners", "netstat", ("-ano",), "Lists active TCP/UDP endpoints and owning process IDs.", "Wyświetla aktywne połączenia TCP/UDP i identyfikatory procesów."),
    CommandSpec("interfaces", "Network", "Network interfaces", "netsh", ("interface", "show", "interface"), "Shows Windows network interfaces and their state.", "Pokazuje interfejsy sieciowe Windows i ich stan."),
    CommandSpec("wifi_interfaces", "Network", "Wi-Fi interface status", "netsh", ("wlan", "show", "interfaces"), "Shows current Wi-Fi interface status without revealing saved passwords.", "Pokazuje stan Wi-Fi bez ujawniania zapisanych haseł."),
    CommandSpec("firewall_status", "Security", "Firewall profiles", "netsh", ("advfirewall", "show", "allprofiles"), "Shows Windows Firewall profile status and policy.", "Pokazuje stan profili i zasady Zapory Windows."),
    CommandSpec("whoami", "Security", "Identity & privileges", "whoami", ("/all",), "Shows the current identity, groups and enabled privileges.", "Pokazuje bieżącą tożsamość, grupy i uprawnienia."),
    CommandSpec("tasklist", "Processes", "Running processes", "tasklist", ("/v",), "Shows running processes with verbose metadata.", "Pokazuje uruchomione procesy ze szczegółowymi informacjami."),
    CommandSpec("services", "Processes", "Windows services", "sc", ("query", "type=", "service", "state=", "all"), "Lists Windows services and their state.", "Wyświetla usługi Windows i ich stan."),
    CommandSpec("drivers", "System", "Installed drivers", "driverquery", ("/v",), "Lists installed Windows drivers with verbose details.", "Wyświetla zainstalowane sterowniki Windows ze szczegółami."),
    CommandSpec("disk_check", "Storage", "Check C: filesystem", "chkdsk", ("C:",), "Checks the C: filesystem without requesting repair.", "Sprawdza system plików C: bez żądania naprawy.", True, Risk.READ_ONLY, 600),
    CommandSpec("drives", "Storage", "Available drives", "fsutil", ("fsinfo", "drives"), "Lists detected drive letters.", "Wyświetla wykryte litery dysków.", True),
    CommandSpec("bitlocker", "Storage", "BitLocker status", "manage-bde", ("-status",), "Shows BitLocker protection status for local volumes.", "Pokazuje stan ochrony BitLocker dla lokalnych woluminów.", True),
    CommandSpec("power_modes", "Power", "Available sleep states", "powercfg", ("/a",), "Shows sleep states supported by this computer.", "Pokazuje stany uśpienia obsługiwane przez komputer."),
    CommandSpec("power_requests", "Power", "Power requests", "powercfg", ("/requests",), "Shows processes or drivers currently preventing sleep/display idle.", "Pokazuje procesy lub sterowniki blokujące uśpienie albo wygaszanie.", True),
    CommandSpec("wsl_status", "WSL", "WSL status", "wsl", ("--status",), "Shows Windows Subsystem for Linux configuration.", "Pokazuje konfigurację Windows Subsystem for Linux."),
    CommandSpec("wsl_list", "WSL", "WSL distributions", "wsl", ("--list", "--verbose"), "Lists installed WSL distributions and versions.", "Wyświetla zainstalowane dystrybucje WSL i ich wersje."),
    CommandSpec("flush_dns", "Repair", "Flush DNS cache", "ipconfig", ("/flushdns",), "Clears the local DNS resolver cache.", "Czyści lokalną pamięć podręczną resolvera DNS.", True, Risk.CHANGE),
    CommandSpec("gpupdate", "Repair", "Refresh Group Policy", "gpupdate", ("/force",), "Refreshes local/domain Group Policy. Use on computers you administer.", "Odświeża lokalne/domenowe zasady grupy. Używaj na komputerach, którymi administrujesz.", True, Risk.CHANGE, 600),
    CommandSpec("winsock_reset", "Repair", "Reset Winsock", "netsh", ("winsock", "reset"), "Resets the Winsock catalog. A reboot may be required afterwards.", "Resetuje katalog Winsock. Później może być wymagany restart.", True, Risk.CHANGE),
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
