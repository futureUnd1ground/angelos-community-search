#!/usr/bin/env python3
"""Use Community Store's verified registry reader without installing anything."""
import importlib.util
from pathlib import Path
import sys

path = Path.home() / '.config/angelos/plugins/community-store/scripts/community-store.py'
if not path.is_file():
    print('Установи Community Store 0.9.1 или новее.', file=sys.stderr)
    raise SystemExit(1)
spec = importlib.util.spec_from_file_location('store', path)
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)
raise SystemExit(store.main(['fetch', sys.argv[1]]))
