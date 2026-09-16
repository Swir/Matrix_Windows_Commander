from matrix_windows_commander.models import CommandSpec, Risk, format_command


def test_format_command_quotes_spaces(): assert format_command("tool.exe",("hello world","/x"))=='tool.exe "hello world" /x'
def test_spec_defaults_to_read_only(): assert CommandSpec("x","Test","Test","echo").risk==Risk.READ_ONLY
