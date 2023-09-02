# Image Meta Cleaner

Utility for extracting location info and cleaning meta data of images.

Creating in strange purposes of security and privacy.

## Usage

1. Download executable from last [release](https://github.com/butvinm/ImageMetaCleaner/releases)
2. Put `imc.exe` somewhere
3. Create `run.bat` with following content:
    ```bat
    @echo off
    imc.exe <path to images directory> <delay in seconds>
    ```
    Example:
    ```bash
    @echo off
    "C:\Program Files\Imc\imc.exe" "C:\Users\belk1\Downloads" 60
    ```

4. Add `run.bat` to autostart

## Develop

1. Python 3.11
2. Poetry
   - See [Poetry installation guide for you platform](https://python-poetry.org/docs/)
3. Install dependencies
    ```bash
    poetry install
    ```
4. Activate virtual environment
    ```bash
    poetry shell
    ```

## Build

1. Install pyinstaller
    ```bash
    poetry shell
    pip install pyinstaller
    ```
2. Build
    ```bash
    pyinstaller ./main.spec
    ```

## Attribution

Project uses [Clean icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/clean)
