<h1 align="center"><a href="https://github.com/codespearhead/word-to-pdf-api">VisionGUI</a></h1>

<p align="center">
    <br>
  <a href="https://www.flaticon.com/free-icon/binoculars_4695312?related_id=4695227&origin=search">
    <img src="https://cdn-icons-png.flaticon.com/512/4695/4695312.png" width="120px" height="120px"/>
  </a>
  <br><br>
    OpenCV-powered desktop automation tool
  <br>
</p>

<br>


## What's this project?

This is a hard fork of an internal library I created for ScrapeGrid, an internal project which has been in production since September 2025. It was developed to enable ScrapeGrid to interact with SAJ, a desktop application developed by Softplan and one of the main information systems used by the Brazilian Judiciary. However, SAJ presents several issues, such as frequent screen flickering during page rendering that lasts for a few seconds before the interface becomes ready for interaction, which led to the creation of this library. The library itself is system-agnostic and can be used with other desktop applications, as it relies on image recognition rather than direct integration. The only changes in the first commit are to the import statements to make the project standalone, enabling independent evolution and reducing maintenance overhead and complexity in ScrapeGrid.


## Why not use PyAutoGUI?

As of 2026-04-13, [PyAutoGUI](https://github.com/asweigart/pyautogui) has been effectively unmaintained for over 3 years, with many critical bugs still unresolved. It relies on a [fixed US keyboard layout](https://github.com/asweigart/pyautogui/pull/55), meaning you might need to use an incorrect layout to get the typing to work. It also recreates special keys and layout-specific behavior from scratch instead of delegating that complexity to a specialized library, which makes it harder to maintain.


## Common steps

<details>

<summary>Create a Virtual Enviroment and install Poetry</summary>

### Prerequisites

1. Ensure you have the latest stable version of Python installed:

```bash
python --version
```

### Virtual Enviroment creation

1. Create a Virtual Enviroment:

```bash
python -m venv .venv
```

2. Activate the Virtual Enviroment:

```bash
activate_venv() {
    if [[ $(uname) == "Darwin" ]]; then
        source .venv/bin/activate
    elif [[ $(uname) == "Linux" ]]; then
        source .venv/bin/activate
    elif [[ $(uname) == CYGWIN* || $(uname) == MINGW* ]]; then
        source .venv/Scripts/activate
    else
        echo "Unsupported operating system"
    fi
}

activate_venv
```

3. Ensure the Virtual Enviroment is active:

```bash
PYTHON_PATH=$(which python)
if [[ "$PYTHON_PATH" == *".venv"* ]]; then
  echo "Python is using a .venv environment: $PYTHON_PATH"
else
  echo "Python is NOT using a .venv environment: $PYTHON_PATH"
fi
```

### Poetry Installation

```bash
pip install poetry
```
</details>


## Quickstart

1. Create a Virtual Enviroment and install Poetry.

2. Install the project in your existing Poetry project:

```bash
poetry add git+ssh://git@github.com/codespearhead/visiongui.git#f6de75181edca5107097d09754348a3cf4b849ea
```

2. Create a file in the root of your project called "main.py" with the contents of file [./demo/main.py](./demo/main.py).

3. Run that file.

```bash
poetry run python main.py
```

4. For more information on the library's API, read the test suite in [./tests/](./tests/).


## Dev mode

### Local Environment Setup

1. Create a Virtual Enviroment and install Poetry.

2. Install the project dependencies from all dependency groups:

```bash
poetry install --with test,format
```

3. Run the test suite:

```bash
poetry run pytest -rfsxE --capture=no --log-cli-level=DEBUG --maxfail=1 -vv ./tests
```


## Useful commands

#### Code Formatting

```bash
poetry run python ./tasks/format.py
```

#### Code Linting

```bash
poetry run mypy
```
