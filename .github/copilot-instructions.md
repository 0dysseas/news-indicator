## News Indicator — AI coding assistant instructions

Purpose: quick orientation and actionable conventions so an AI agent can be immediately productive working on this repo.

- Project type: small GTK AppIndicator Python app that retrieves news from NewsAPI, displays menu items and desktop notifications. Key runtime deps: `gi` (Gtk), `AppIndicator3`, `notify2`, `requests`, `apscheduler`.

- Quick entry points:
  - `newsindicator/news_indicator.py` — app entry, scheduler setup, UI/menu rendering. Look here to understand how jobs are scheduled and how results are consumed.
  - `newsindicator/get_news.py` — retrieval logic: `DownloadNewsWorker.retrieve_news()` builds a queue of endpoints and spawns `DownloadWorker` threads that call `DownloadWorker._form_news_structure()` and push cleaned items into an output `Queue`.
  - `newsindicator/utils.py` — asset & sources loader. `assets/news_sources.txt` contains lines like `KEY = https://...`.

  1. `news_indicator.main()` scheduled job runs every interval and instantiates `DownloadNewsWorker`.
  2. `DownloadNewsWorker.retrieve_news()` reads `assets/news_sources.txt` (via `get_news_sources_from_file`) and enqueues API URLs (appending `NEWS_API_KEY`).
  3. `DownloadWorker` threads pull from the input queue, HTTP GET each endpoint (`requests.get`), convert JSON via `_form_news_structure()` and push cleaned dicts into an output `Queue`.
  4. Scheduler listener (`listen_for_new_updates`) receives returned list and calls `NewsIndicator.create_and_update_menu()` to render menu & optionally call `show_notifications()`.

- Concurrency & patterns to be aware of:
  - Uses `threading.Thread` + `queue.Queue` for parallel downloads (see `NUM_THREADS` in `get_news.py`). Tests assume synchronous behaviour by calling `_form_news_structure()` directly.
  - Scheduler: `apscheduler.schedulers.background.BlockingScheduler` schedules `main()` job (intervals stored in `about_and_settings_wins.INTERVALS`). Changing intervals calls `scheduler.reschedule_job()`.

- Environment & runtime hints:
  - The app expects `NEWS_API_KEY` in the environment (reads `os.environ['NEWS_API_KEY']`). If missing, `show_alert_notifications()` is invoked and process exits.
  - GTK/notify2 calls require a Linux desktop runtime (X/Wayland + D-Bus). Unit tests run headless and must mock out `gi` and `notify2`.

- Testing & developer workflow (how to run tests reliably):
  - Recommended: create venv, install deps from `requirements.txt`, run `pytest -q` from project root.
  - When running a single test file, set PYTHONPATH so `newsindicator` can be imported: `PYTHONPATH=. pytest -q tests/test_get_news.py`
  - Alternative: install package editable `python -m pip install -e .` so imports work without PYTHONPATH.
  - Tests currently exercise `_form_news_structure()` by instantiating `DownloadWorker` directly — they don't spawn threads or do network calls.

- Project-specific conventions / gotchas (do not change without reason):
  - `utils.get_asset()` returns `assets/news_sources.txt` by default; the sources file uses `key = value` format split with `' = '`.
  - `get_news.py` contains a Python 2/3 compatible `Queue` import fallback. Keep that pattern when adding modules that use `Queue`.
  - UI logic is tightly coupled to synchronous scheduler callbacks and GTK main loop; prefer small, local changes and add unit tests that mock GTK/notify2 when altering UI code.

- Integration points / external dependencies to note:
  - NewsAPI endpoints (in `assets/news_sources.txt`) — code appends `NEWS_API_KEY` to each source before requesting.
  - `requests` used directly (no retry/backoff implemented) — consider adding retries in `DownloadWorker` if making network changes.
  - `notify2` & `gi.repository` are used for notifications and GTK. Tests should mock these modules.

- Useful code examples to copy when coding:
  - Reading & parsing sources: `newsindicator/utils.py:get_news_sources_from_file()` — use this helper instead of re-parsing the file.
  - Normalizing an article (example fields): `_form_news_structure()` should produce dicts with at least `title` and `url` and optionally `source` and `urlToImage`.

- When writing tests:
  - Mock `gi` and `notify2` at import time (or use `tests/conftest.py` to insert mocks into `sys.modules`) so importing `newsindicator.*` doesn't require a desktop runtime.
  - Prefer testing pure functions (for example, `_form_news_structure()`) and avoid starting threads or the scheduler in unit tests.

If any of these items are incomplete or you want more detail for CI setup, debugging tips, or to document additional workflows (packaging, linting), tell me which area to expand.

---
Files referenced: `newsindicator/news_indicator.py`, `newsindicator/get_news.py`, `newsindicator/utils.py`, `newsindicator/about_and_settings_wins.py`, `assets/news_sources.txt`, `tests/test_get_news.py`, `requirements.txt`
