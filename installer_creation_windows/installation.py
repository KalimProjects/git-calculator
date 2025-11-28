import os, subprocess, shutil
from pathlib import Path

def build_calculator():
    """Скрипт сборки с очисткой лишних директорий и файлов, образовавшихся во время сборки"""
    
    # 0. Определяем текущую директорию скрипта
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    icon_absolute = project_root / "icon.ico"
    
    if not icon_absolute.exists():
        print(f"Файл иконки {icon_absolute} не найден!")
        return
    
    print(f"Иконка найдена")
    
    # 1. PyInstaller (запускаем из корня проекта)
    print("Сборка EXE с PyInstaller...")
    os.chdir(project_root)
    
    py_cmd = f'pyinstaller --onefile --windowed --icon="{icon_absolute}" --add-data=icon.ico:. main.py functions.py'
    subprocess.run(py_cmd, shell=True)
    
    # 2. Переименовываем и перемещаем EXE файл
    exe_source = project_root / "dist" / "main.exe"
    exe_dest = script_dir / "calculator.exe"
    
    if not exe_source.exists():
        print("dist/main.exe отсутствует!")
        return

    shutil.move(str(exe_source), str(exe_dest))
    print("EXE-файл перемещён в installer_creation_windows/")
        
    # 3. Inno Setup
    print("Сборка установщика с Inno Setup...")
    iss_file = script_dir / "installer.iss"
    iss_cmd = f'iscc "{iss_file}"'
    subprocess.run(iss_cmd, shell=True)
    
    # 4. Очистка временных файлов
    print("Очистка временных файлов...")
    folders_to_remove = ["build", "dist"]
    files_to_remove = ["main.spec"]
    
    for folder in folders_to_remove:
        folder_path = project_root / folder
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"Удалена директория: {folder}")
        else:
            print(f"Директория {folder} уже не существует")
    
    for file in files_to_remove:
        file_path = project_root / file
        if file_path.exists():
            os.remove(file_path)
            print(f"Удален файл: {file}")
        else:
            print(f"Файл {file} уже не существует")
    
    print("Сборка EXE-файла и установщика успешно завершена!")

if __name__ == "__main__":
    build_calculator()