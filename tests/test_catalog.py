from matrix_windows_commander.catalog import CATEGORIES, COMMANDS, get_command, search_catalog
from matrix_windows_commander.models import Risk


def test_command_ids_are_unique():
    ids = [item.id for item in COMMANDS]
    assert len(ids) == len(set(ids))
    assert len(ids) >= 45


def test_catalog_has_multiple_categories():
    assert len(CATEGORIES) >= 8


def test_search_finds_command_and_category():
    assert get_command("systeminfo").executable == "systeminfo"
    assert any(item.id == "netstat" for item in search_catalog("connection", "Network"))
    assert any(item.id == "wifi_profiles" for item in search_catalog("Wi-Fi", "Network"))


def test_admin_repair_commands_are_marked():
    item = get_command("dism_restore")
    assert item and item.admin_required and item.risk == Risk.REPAIR
    ip_reset = get_command("ip_stack_reset")
    assert ip_reset and ip_reset.admin_required and ip_reset.risk == Risk.REPAIR


def test_restored_legacy_diagnostics_are_available_in_safe_forms():
    expected = {
        "hostname",
        "ip_release",
        "ip_renew",
        "pathping_cloudflare",
        "wifi_profiles",
        "netbios_names",
        "reg_software",
        "event_logs",
        "scheduled_tasks",
        "bcd_enum",
        "net_users",
        "net_localgroups",
        "net_accounts",
        "net_shares",
        "net_view",
        "spooler_status",
        "battery_report",
        "energy_report",
        "wsl_install",
    }
    assert expected.issubset({item.id for item in COMMANDS})


def test_network_and_service_changes_require_confirmation_risk():
    for command_id in ("ip_release", "ip_renew", "spooler_start", "spooler_stop", "wsl_install"):
        item = get_command(command_id)
        assert item is not None
        assert item.risk == Risk.CHANGE


def test_wifi_profile_command_never_requests_saved_keys():
    item = get_command("wifi_profiles")
    assert item is not None
    line = item.command_line.lower()
    assert "key=clear" not in line
    assert " key " not in f" {line} "


def test_dangerous_legacy_one_click_actions_removed():
    lines = "\n".join(item.command_line.lower() for item in COMMANDS)
    forbidden = (
        "format a:",
        "diskpart",
        "reg delete",
        "shutdown /s",
        "shutdown /r",
        "wsl --unregister",
        "rd c:\\",
        "del /s",
    )
    for value in forbidden:
        assert value not in lines
