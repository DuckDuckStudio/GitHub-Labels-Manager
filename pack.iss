[Setup]
AppName=GitHub Labels Manager
AppVersion=v1.1
VersionInfoVersion=1.1
AppPublisher=DuckStudio
VersionInfoCopyright=Copyright (c) 鸭鸭「カモ」
AppPublisherURL=https://github.com/DuckDuckStudio/GitHub-Labels-Manager/releases
DefaultDirName={autopf}\GitHub_Labels_Manager
DefaultGroupName=GitHub Labels Manager
UninstallDisplayIcon={app}\glm.exe
OutputDir=D:\Duckhome\projects\MSVS\Source\Repos\GitHub-Labels-Manager\version
OutputBaseFilename=GitHub_Labels_Manager_Setup_v1.1
SetupIconFile=D:\Duckhome\projects\MSVS\Source\Repos\GitHub-Labels-Manager\ico.ico
LicenseFile=D:\Duckhome\projects\MSVS\Source\Repos\GitHub-Labels-Manager\LICENSE
Compression=lzma2
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Files]
Source: "D:\Duckhome\projects\MSVS\Source\Repos\GitHub-Labels-Manager\version\GitHub-Labels-Manager-v1.1\*"; DestDir: "{app}"

[Icons]
Name: "{commonstartmenu}\Programs\GitHub Labels Manager"; Filename: "{app}\glm.exe"; WorkingDir: "{app}"

[Run]
Filename: "{sys}\cmd.exe"; Parameters: "/C setx PATH ""{app};%PATH%"" /M"; Flags: runhidden

[UninstallRun]
Filename: "{sys}\cmd.exe"; Parameters: "/C setx PATH ""%PATH:{app};=%"" /M"; Flags: runhidden; RunOnceId: UninstallSetPath
