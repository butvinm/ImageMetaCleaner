# Image Meta Cleaner

**Overview:**
Image Meta Cleaner is a utility designed for extracting location information and cleaning metadata from images. It was created with the primary goal of enhancing security and privacy when working with images.

## Installation

1. **Download the Executable:**
   - Start by downloading the latest release of Image Meta Cleaner from the official repository on [GitHub](https://github.com/butvinm/ImageMetaCleaner/releases).

2. **Place the Executable:**
   - Once the download is complete, place the `imc.exe` executable file in a directory of your choice.

3. **Create a Batch File:**
   - Create a `run.bat` batch file with the following content:

   ```batch
   @echo off
   imc.exe <path to images directory> <delay in seconds>
   ```

   - Replace `<path to images directory>` with the actual path to the directory containing your images.
   - Set `<delay in seconds>` to the desired delay between cleaning operations.

   **Example:**

   ```batch
   @echo off
   "C:\Program Files\ImageMetaCleaner\imc.exe" "C:\Users\<your username>\Downloads" 60
   ```

4. **Add to Autostart:**
   - To automate the cleaning process, add the `run.bat` file to your computer's autostart programs.

## Development Environment

If you wish to contribute to the development of Image Meta Cleaner, here are the steps to set up the development environment:

1. **Requirements:**
   - Python 3.11
   - Poetry (Install using [Poetry installation guide for your platform](https://python-poetry.org/docs/))

2. **Install Dependencies:**
   - Navigate to the project directory and install the required dependencies using Poetry:

   ```bash
   poetry install
   ```

3. **Activate Virtual Environment:**
   - Activate the virtual environment created by Poetry:

   ```bash
   poetry shell
   ```

## Building from Source

To build the project from source code, follow these steps:

1. **Install PyInstaller:**
   - While in the Poetry virtual environment, install PyInstaller:

   ```bash
   poetry shell
   pip install pyinstaller
   ```

2. **Build the Executable:**
   - Build the executable using PyInstaller:

   ```bash
   pyinstaller ./main.spec
   ```

## Attribution

This project makes use of clean icons created by Freepik and available on Flaticon. You can find these icons [here](https://www.flaticon.com/free-icons/clean).

With these instructions, users should be able to easily install, use, and even contribute to Image Meta Cleaner.

## Russian Translation

**Обзор:**
Image Meta Cleaner - это утилита, предназначенная для извлечения информации о местоположении и удаления метаданных из изображений.

## Установка

1. **Скачайте исполняемый файл:**
   - Исполняемый файл закреплен в последнем релизе на [GitHub](https://github.com/butvinm/ImageMetaCleaner/releases).

2. **Разместите исполняемый файл:**
   - После завершения загрузки поместите исполняемый файл `imc.exe` в выбранную вами директорию.

3. **Создайте скрипт для запуска (batch file):**
   - Создайте файл пакетной обработки `run.bat` с следующим содержанием:

   ```batch
   @echo off
   imc.exe <путь к директории с изображениями> <задержка в секундах>
   ```

   - Замените `<путь к директории с изображениями>` на фактический путь к директории с вашими изображениями.
   - Установите `<задержка в секундах>` в желаемое значение задержки между операциями очистки.

   **Пример:**

   ```batch
   @echo off
   "C:\Program Files\ImageMetaCleaner\imc.exe" "C:\Users\belk1\Downloads" 60
   ```

4. **Добавьте в автозагрузку:**
   - Чтобы автоматизировать процесс очистки, добавьте файл `run.bat` в автозагрузку через Диспетчер задач.

## Среда разработки

Если вы хотите внести вклад в развитие Image Meta Cleaner, следуйте этим шагам для настройки среды разработки:

1. **Требования:**
   - Python 3.11
   - Poetry (Установите с помощью [руководства по установке Poetry для вашей платформы](https://python-poetry.org/docs/))

2. **Установка зависимостей:**
   - Перейдите в директорию проекта и установите необходимые зависимости с помощью Poetry:

   ```bash
   poetry install
   ```

3. **Активация виртуальной среды:**
   - Активируйте виртуальную среду, созданную Poetry:

   ```bash
   poetry shell
   ```

## Сборка из исходного кода

Чтобы собрать проект из исходного кода, выполните следующие шаги:

1. **Установите PyInstaller:**
   - Находясь в виртуальной среде Poetry, установите PyInstaller:

   ```bash
   poetry shell
   pip install pyinstaller
   ```

2. **Сборка исполняемого файла:**
   - Соберите исполняемый файл с помощью PyInstaller:

   ```bash
   pyinstaller ./main.spec
   ```

## Атрибуция

Этот проект использует иконки "Clean", созданные Freepik и доступные на Flaticon. Вы можете найти эти иконки [здесь](https://www.flaticon.com/free-icons/clean).
