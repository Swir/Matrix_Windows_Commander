from matrix_windows_commander.catalog import CATEGORIES, COMMANDS, get_command, search_catalog
from matrix_windows_commander.models import Risk


def test_command_ids_are_unique():
    ids=[item.id for item in COMMANDS]; assert len(ids)==len(set(ids)); assert len(ids)>=20

def test_catalog_has_multiple_categories(): assert len(CATEGORIES)>=6

def test_search_finds_command_and_category():
    assert get_command("systeminfo").executable=="systeminfo"; assert any(item.id=="netstat" for item in search_catalog("connection","Network"))

def test_admin_repair_commands_are_marked():
    item=get_command("dism_restore"); assert item and item.admin_required and item.risk==Risk.REPAIR

def test_dangerous_legacy_one_click_actions_removed():
    lines="\n".join(item.command_line.lower() for item in COMMANDS); forbidden=("format a:","diskpart","reg delete","shutdown /s","shutdown /r","wsl --unregister","rd c:\\")
    for value in forbidden: assert value not in lines
