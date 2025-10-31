; ===== ПЕРЕМЕННЫЕ =====
#define AppName "Git Calculator"
#define AppVersion "1.1"
#define AppPublisher "KalimProjects"
#define AppPublisherURL "https://github.com/KalimProjects"
#define AppSupportURL "https://github.com/KalimProjects/git-calculator"
#define AppUpdatesURL "https://github.com/KalimProjects/git-calculator/releases"
#define AppCopyright "Copyright © 2025 KalimProjects & KitsuruDev"
; ===== ДЛЯ УНИКАЛЬНОСТИ И ОБНОВЛЕНИЙ ПРОШЛЫХ УСТАНОВЛЕННЫХ ВЕРСИЙ =====
#define AppID "19D003DA-67D2-4835-965C-0FF5145F708C"
#define DefaultDirName "Git Calculator"
#define OutputDir "..\installer"
#define OutputBaseFilename "GitCalculatorSetup"
#define ExeName "calculator.exe"
#define IconName "icon.ico"
#define IconNameSource "..\icon.ico"
#define LicenseFile "LICENSE.txt"

; ===== ПАРАМЕТРЫ УСТАНОВКИ =====
[Setup]
DisableWelcomePage=no
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppPublisherURL}
AppSupportURL={#AppSupportURL}
AppUpdatesURL={#AppUpdatesURL}
AppCopyright={#AppCopyright}
AppID={#AppID}
DefaultDirName={autopf}\{#DefaultDirName}
DefaultGroupName={#DefaultDirName}
OutputDir={#OutputDir}
OutputBaseFilename={#OutputBaseFilename}
SetupIconFile={#IconNameSource}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
LicenseFile={#LicenseFile}
WizardImageFile=compiler:WizClassicImage-IS.bmp
WizardSmallImageFile=compiler:WizClassicSmallImage-IS.bmp

; ===== ЯЗЫКИ УСТАНОВКИ =====
[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

; ===== СООБЩЕНИЯ ДЛЯ ОКНА ПРИВЕТСТВИЯ =====
[Messages]
russian.WelcomeLabel1=Добро пожаловать в мастер установки {#AppName}
russian.WelcomeLabel2=Этот мастер установит {#AppName} {#AppVersion} на ваш компьютер.%n%nРекомендуется закрыть все другие приложения перед продолжением.

; ===== СООБЩЕНИЯ ДЛЯ СОЗДАНИЯ ИКОНКИ НА РАБОЧЕМ СТОЛЕ И ЗАПУСКА ПРОГРАММЫ =====
[CustomMessages]
russian.CreateDesktopIcon=Создать ярлык на рабочем столе
russian.LaunchProgram=Запустить {#AppName}
english.CreateDesktopIcon=Create a desktop icon
english.LaunchProgram=Launch {#AppName}

; ===== КАКИЕ ФАЙЛЫ БУДУТ ИСПОЛЬЗОВАТЬСЯ ДЛЯ СОЗДАНИЯ УСТАНОВЩИКА =====
[Files]
Source: "{#ExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#IconNameSource}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#LicenseFile}"; DestDir: "{app}"; Flags: ignoreversion

; ===== ИКОНКА В МЕНЮ ПУСК И ЯРЛЫК НА РАБОЧЕМ СТОЛЕ (где, на что ссылается, иконка) =====
[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#ExeName}"; IconFilename: "{app}\{#IconName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#ExeName}"; IconFilename: "{app}\{#IconName}";

; ===== ВЫВОД ОПЦИИ "СОЗДАТЬ ЯРЛЫК НА РАБОЧЕМ СТОЛЕ" =====
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

; ===== ЗАПУСК ПРОГРАММЫ ПОСЛЕ УСТАНОВКИ =====
[Run]
Filename: "{app}\{#ExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent unchecked