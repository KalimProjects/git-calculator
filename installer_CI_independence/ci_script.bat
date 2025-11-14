@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ЗАПУСК CI СКРИПТА ДЛЯ GIT CALCULATOR
echo ============================================================

:: Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python не установлен или не найден в PATH
    exit /b 1
)

:: Проверяем наличие PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не установлен
    exit /b 1
)

:: Проверяем наличие Inno Setup
where iscc >nul 2>&1
if errorlevel 1 (
    echo Inno Setup не установлен или не найден в PATH
    exit /b 1
)

:: ===== КОНФИГУРАЦИЯ =====
set "REPO_URL=https://github.com/KalimProjects/git-calculator"
set "PROJECT_NAME=Git Calculator"
set "PROJECT_VERSION=1.1"
set "SCRIPT_DIR=%~dp0"
set "TEMP_DIR=%SCRIPT_DIR%ci_build"
set "MAIN_BRANCH=main"
set "TEST_BRANCH=test"
set "RELEASE_BRANCH=releases"

echo.
echo ===================================================
echo 1. ЗАГРУЗКА АКТУАЛЬНОГО СОСТОЯНИЯ С СЕРВЕРА
echo ===================================================

echo Создаем временную директорию: %TEMP_DIR%
if exist "%TEMP_DIR%" (
    echo Удаляем старую директорию
    rmdir /s /q "%TEMP_DIR%" >nul 2>&1
)

mkdir "%TEMP_DIR%" 2>nul
if errorlevel 1 (
    echo Ошибка создания временной директории
    goto :cleanup
)

:: Скачиваем файлы из main ветки
echo Загружаем файлы из ветки %MAIN_BRANCH%
cd /d "%TEMP_DIR%"

:: Скачиваем отдельные файлы через raw ссылки
echo Скачиваем main.py
curl -s -L -o "main.py" "https://raw.githubusercontent.com/KalimProjects/git-calculator/main/main.py"
if not exist "main.py" (
    echo Не удалось скачать main.py
    goto :cleanup
)

echo Скачиваем functions.py
curl -s -L -o "functions.py" "https://raw.githubusercontent.com/KalimProjects/git-calculator/main/functions.py"
if not exist "functions.py" (
    echo Не удалось скачать functions.py
    goto :cleanup
)

echo Скачиваем icon.ico
curl -s -L -o "icon.ico" "https://raw.githubusercontent.com/KalimProjects/git-calculator/main/icon.ico"
if not exist "icon.ico" (
    echo Не удалось скачать icon.ico
    goto :cleanup
)

:: Скачиваем LICENSE.txt
echo Скачиваем LICENSE.txt
curl -s -L -o "LICENSE.txt" "https://raw.githubusercontent.com/KalimProjects/git-calculator/main/LICENSE.txt"
if not exist "LICENSE.txt" (
    echo Не удалось скачать LICENSE.txt
    goto :cleanup
)

echo Файлы из ветки %MAIN_BRANCH% загружены

:: Скачиваем тесты из test ветки
echo.
echo Загружаем тесты из ветки %TEST_BRANCH%
mkdir tests 2>nul

:: Ищем тестовые файлы в ветке test
echo Скачиваем test_calc.py
curl -s -L -o "tests\test_calc.py" "https://raw.githubusercontent.com/KalimProjects/git-calculator/test/tests/test_calc.py"
if exist "tests\test_calc.py" (
    echo test_calc.py загружен
) else (
    echo test_calc.py не найден
)

echo Скачиваем test_functions.py
curl -s -L -o "tests\test_functions.py" "https://raw.githubusercontent.com/KalimProjects/git-calculator/test/tests/test_functions.py"
if exist "tests\test_functions.py" (
    echo test_functions.py загружен
) else (
    echo test_functions.py не найден
)

:: Скачиваем оригинальный скрипт установщика из ветки releases
echo.
echo Загружаем скрипт установщика из ветки %RELEASE_BRANCH%
curl -s -L -o "installer.iss" "https://raw.githubusercontent.com/KalimProjects/git-calculator/releases/installer_creation/installer.iss"
if not exist "installer.iss" (
    echo Не удалось скачать installer.iss
    goto :cleanup
)

:: Создаем исправленную версию скрипта
echo Исправляем пути в скрипте установщика
(
  for /f "tokens=1* delims=:" %%a in ('findstr /n "^" installer.iss') do (
    set "line=%%b"
    if defined line (
      set "line=!line:#define OutputDir "..\installer"=#define OutputDir "installer"!"
      set "line=!line:#define IconNameSource "..\icon.ico"=#define IconNameSource "icon.ico"!"
      set "line=!line:Source: "{#ExeName}"=Source: "dist\main.exe"; DestName: "{#ExeName}"!"
      echo(!line!
    ) else echo(
  )
) > installer_fixed.iss

move /y installer_fixed.iss installer.iss >nul
echo Скрипт установщика исправлен и готов

echo.
echo ===================================================
echo 2. ВЫПОЛНЕНИЕ UNITTEST
echo ===================================================

set "TESTS_PASSED=1"
set "TEST_COUNT=0"

:: Создаем __init__.py в папке tests для правильного импорта
echo. > tests\__init__.py

:: Запускаем все найденные тесты через прямое выполнение файлов
for %%f in (tests\test_*.py) do (
    if exist "%%f" (
        set /a TEST_COUNT+=1
        echo Запуск тестов: %%~nf
        
        :: Запускаем тесты через прямое выполнение Python файла
        python "%%f"
        if errorlevel 1 (
            echo Тесты %%~nf не прошли
            set "TESTS_PASSED=0"
        ) else (
            echo Тесты %%~nf прошли успешно
        )
    )
)

if "!TEST_COUNT!"=="0" (
    echo Тестовые файлы не найдены
    set "TESTS_PASSED=0"
)

if "!TESTS_PASSED!"=="0" (
    echo.
    echo CI прерван: не все тесты прошли
    goto :cleanup
)

echo.
echo ===================================================
echo 3. СБОРКА ПРОЕКТА
echo ===================================================

echo Сборка с PyInstaller
pyinstaller --onefile --windowed --icon="icon.ico" --add-data="icon.ico;." main.py functions.py

if not exist "dist\main.exe" (
    echo Ошибка сборки: EXE файл не создан
    goto :cleanup
)

echo Проект успешно собран

echo.
echo ===================================================
echo 4. СОЗДАНИЕ УСТАНОВЩИКА
echo ===================================================

echo Создание установщика с Inno Setup
iscc "installer.iss" >nul 2>&1

if not exist "installer\GitCalculatorSetup.exe" (
    echo Ошибка создания установщика
    goto :cleanup
)

echo Установщик создан в installer\GitCalculatorSetup.exe

:: Создаем папку installer на одном уровне с ci_build
echo Создаем папку installer
if not exist "%SCRIPT_DIR%installer" (
    mkdir "%SCRIPT_DIR%installer" 2>nul
    if errorlevel 1 (
        echo Ошибка создания директории installer
    ) else (
        echo Директория installer создана
    )
) else (
    echo Директория installer уже существует
)

:: Переносим установщик из ci_build/installer в новую директорию installer
echo Переносим установщик в папку installer
if exist "%TEMP_DIR%\installer\GitCalculatorSetup.exe" (
    move "%TEMP_DIR%\installer\GitCalculatorSetup.exe" "%SCRIPT_DIR%installer\" >nul
    if exist "%SCRIPT_DIR%installer\GitCalculatorSetup.exe" (
        echo Установщик перенесен в %SCRIPT_DIR%installer\
    ) else (
        echo Ошибка переноса установщика
    )
) else (
    echo Файл установщика не найден в %TEMP_DIR%\installer\
)

:: Очищаем и удаляем ci_build
echo Очищаем и удаляем папку ci_build
if exist "%TEMP_DIR%" (
    rmdir /s /q "%TEMP_DIR%" >nul 2>&1
    if exist "%TEMP_DIR%" (
        echo Папка очищена, но не удалена полностью
    ) else (
        echo Папка ci_build удалена
    )
) else (
    echo Папка ci_build не существует
)

echo.
echo ===================================================
echo 5. УСТАНОВКА ПРИЛОЖЕНИЯ
echo ===================================================

if exist "%SCRIPT_DIR%installer\GitCalculatorSetup.exe" (
    echo Запуск установки Git Calculator...
    "%SCRIPT_DIR%installer\GitCalculatorSetup.exe" /SILENT /NORESTART
    if errorlevel 1 (
        echo Ошибка установки приложения
    ) else (
        echo Приложение успешно установлено
    )
) else (
    echo Файл установщика не найден: %SCRIPT_DIR%installer\GitCalculatorSetup.exe
)

echo.
echo ===================================================
echo ВСЕ ЭТАПЫ CI УСПЕШНО ЗАВЕРШЕНЫ
echo ===================================================
echo.

echo Приложение готово к работе.
echo Установщик приложения сохранён (доступен в директории installer, созданной на уровне местоположения текущего скрипта).
pause