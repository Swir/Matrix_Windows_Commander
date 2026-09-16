from matrix_windows_commander.platform_utils import resource_path

def test_resource_path_is_pathlike(): assert resource_path("assets/test.svg").name=="test.svg"
