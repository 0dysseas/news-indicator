# Application Indicator for Ubuntu Unity / Gnome / Xfce

Application Indicator (system tray icon) that accesses, retrieves and displays the latest news from top media outlets.

News sources and blogs can be found/updated at the `/assets/news_sources.txt file`.

[![final_notification.png](https://s13.postimg.org/j15fgsfav/final_notification.png)](https://postimg.org/image/caoy7cs4z/)

Main features:

- Displays latest news via a notification message
- Allows setting the news retrieval interval (10, 15, 20, 30 and 60 minutes)
- Allows setting the notifications display ON or OFF

# Usage

**Install**:

    - Grab a NewsAPI key from https://newsapi.org/
    - Navigate to your ~/.profile file and add the key as follows: export NEWS_API_KEY="your_api_key"
    - Log out and log back in, in order for the changes to take effect
    - sudo pip install git+https://github.com/0dysseas/news-indicator.git
    - Run the "News Application Indicator" from your menu or system utilities.

**Uninstall**:

    - sudo pip uninstall newsindicator

# Screenshots
**(Theme may vary based on your installed desktop theme. I'm using the Mint-Y-Dark)**
[![final_menu.png](https://s13.postimg.org/ylct75hnr/final_menu.png)](https://postimg.org/image/iacpau55v/)
[![settings_mastered.png](https://s13.postimg.org/a9tt8lbp3/settings_mastered.png)](https://postimg.org/image/utyn72rg3/)

# Attributions

Powered by https://newsapi.org/
Icon made by Freepik from [www.flaticon.com](http://www.flaticon.com)


# News Indicator

## Running the test suite

1. Create and activate a virtual environment (recommended)
    
    python3 -m venv .venv
    source .venv/bin/activate

2. Install dependencies

    python3 -m pip install -r requirements.txt

3. Run all tests

    pytest -q

Notes
- If you run a single test file and see "ModuleNotFoundError: No module named 'newsindicator'", run pytest with the project root on PYTHONPATH:
    
    PYTHONPATH=. pytest -q tests/test_get_news.py

- Alternatively, install the package in editable mode (requires setup/pyproject):

    python3 -m pip install -e .
    pytest -q


## Running the test suite

1. Create and activate a virtual environment (recommended)
    
    python3 -m venv .venv
    source .venv/bin/activate

2. Install dependencies

    python3 -m pip install -r requirements.txt

3. Run all tests

    pytest -q
