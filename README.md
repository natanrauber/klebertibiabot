# Kleber Tibia Bot

![System](https://img.shields.io/badge/windows-blue.svg)
![Repo size](https://img.shields.io/github/repo-size/natanrauber/klebertibiabot)
[![License](https://img.shields.io/github/license/natanrauber/klebertibiabot)](https://github.com/natanrauber/klebertibiabot/blob/master/LICENSE)
    
## Dependencies
[![Python 3.10.11](https://img.shields.io/badge/python-3.10.11-blue.svg)](https://www.python.org/downloads/release/python-31011/)

## Features
- Attack
- Heal
- Loot
- Drop unwanted items
- Eat food
- Walk on waypoints

## How to use it?

### Method 1 - PowerShell (Recommended)
- Open PowerShell or Terminal (Not CMD).
- Copy and paste the following code into PowerShell or Terminal and press Enter to run the bot:
  ```
  irm https://raw.githubusercontent.com/natanrauber/klebertibiabot/master/run1.ps1 | iex
  ```
  - `irm`: This command fetches the file/script from the specified URL. `irm` is an alias for Invoke-RestMethod;
  - `iex`: This command executes the script passed to it from the previous command. `iex` is an alias for Invoke-Expression.

- Alternatively, you can use this option with a shortened url:
  ```
  irm tinyurl.com/kleber-start | iex
  ```
- You can also use this option to compile the bot before running it:
  ```
  irm https://raw.githubusercontent.com/natanrauber/klebertibiabot/master/run2.ps1 | iex
  ```

### Method 2 - Traditional
- Download this repository
- Run the file `runner.py`

## Dev Related
[![pytest 8.2.0](https://img.shields.io/badge/pytest-8.2.0-blue.svg)](https://pypi.org/project/pytest/8.2.0/)
[![pipreqs 0.5.0](https://img.shields.io/badge/pipreqs-0.5.0-blue.svg)](https://pypi.org/project/pipreqs/0.5.0/)
