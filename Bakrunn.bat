@echo off
setlocal enabledelayedexpansion

:: Sett mappen der bakgrunnene ligger
set "C:\Users\toeka002\OneDrive - Osloskolen\Bilder\Bakrunner"

:: Tell antall filer
set count=0
for %%f in ("%folder%\*.*") do (
    set /a count+=1
    set "file[!count!]=%%f"
)

:: Velg et tilfeldig tall mellom 1 og count
set /a rand=%random% %% count + 1

:: Hent filen
set "chosen=!file[%rand%]!"

echo Valgt bakgrunn: %chosen%

:: Sett bakgrunn via PowerShell
powershell -command "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class W { [DllImport(\"user32.dll\", SetLastError=true)] public static extern bool SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni); }'; [W]::SystemParametersInfo(20,0,'%chosen%',3)"

exit