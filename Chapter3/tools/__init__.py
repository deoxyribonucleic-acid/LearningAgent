from importlib import import_module
from pathlib import Path

_current_dir = Path(__file__).parent

for py in _current_dir.glob("*.py"):
    if py.name == "tool_registry.py" or py.name.startswith("_"):
        continue
    module_name = f"{__package__}.{py.stem}"
    import_module(module_name)