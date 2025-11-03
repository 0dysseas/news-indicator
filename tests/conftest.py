import sys
import types

# Mock top-level imports used by the module under test
sys.modules['gi'] = types.SimpleNamespace(require_version=lambda *a, **k: None)
sys.modules['notify2'] = types.SimpleNamespace(
    init=lambda *a, **k: None,
    Notification=lambda *a, **k: types.SimpleNamespace(
        set_urgency=lambda *a, **k: None,
        set_timeout=lambda *a, **k: None,
        update=lambda *a, **k: None,
        show=lambda *a, **k: None
    ),
    URGENCY_NORMAL=None
)

# Provide a stub for the package-local utils module so relative import succeeds
sys.modules['newsindicator.utils'] = types.SimpleNamespace(
    get_news_sources_from_file=lambda: {},
    delete_redundant_items=lambda x: x
)