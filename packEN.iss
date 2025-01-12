[Setup]
AppName=GitHub Labels Manager
AppVersion=develop
VersionInfoVersion=develop
AppPublisher=DuckStudio
VersionInfoCopyright=Copyright (c) 鸭鸭「カモ」
AppPublisherURL=https://duckduckstudio.github.io/yazicbs.github.io/
DefaultDirName={autopf}\GitHub_Labels_Manager
DefaultGroupName=GitHub Labels Manager
UninstallDisplayIcon={app}\glm.exe
OutputDir=.\version\Release\en-US
OutputBaseFilename=GitHub_Labels_Manager_Setup_vdevelop-EN
SetupIconFile=.\ico.ico
LicenseFile=.\LICENSE
Compression=lzma2
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Files]
Source: ".\version\Code\zh-CN\config.json"; DestDir: "{app}"
Source: ".\version\Code\zh-CN\glm.exe"; DestDir: "{app}"
Source: ".\version\Code\zh-CN\LICENSE"; DestDir: "{app}"

[Icons]
Name: "{commonstartmenu}\Programs\GitHub Labels Manager"; Filename: "{app}\glm.exe"; WorkingDir: "{app}"

[Run]
Filename: "{sys}\cmd.exe"; Parameters: "/C setx PATH ""{app};%PATH%"" /M"; Flags: runhidden

[UninstallRun]
Filename: "{sys}\cmd.exe"; Parameters: "/C setx PATH ""%PATH:{app};=%"" /M"; Flags: runhidden; RunOnceId: UninstallSetPath
