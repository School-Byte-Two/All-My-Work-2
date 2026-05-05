@echo off
title Kaosmaskinen 2.0 (ufarlig)
setlocal enabledelayedexpansion

:: Intro
color 0a
echo Starter superkaos...
timeout /t 2 >nul

:: Hovedloop ~50 sek
for /l %%i in (1,1,50) do (
    cls

    :: Tilfeldig farge
    set /a f=%random% %% 15
    color !f!

    echo === KAOS NIVÅ %%i ===
    echo.

    :: Rullende tekst
    for /l %%x in (1,1,10) do (
        set /a r=%random% %% 9999
        echo [%%i:%%x] Data: !r!
    )

    :: Fake loading bar
    set /a bar=%random% %% 30 + 5
    set "load="
    for /l %%b in (1,1,!bar!) do set "load=!load!#"
    echo Laster: !load!

    :: ASCII animasjon
    if %%i==5  echo (>'-')>---  
    if %%i==10 echo <---<('-'<)  
    if %%i==15 echo (>'-')>---  
    if %%i==20 echo <---<('-'<)

    :: Litt pip
    if %%i%%7==0 echo ^G

    :: Åpne små ekstra CMD-vinduer
    if %%i==12 start cmd /c "echo Mini-kaos! & timeout /t 2 >nul"
    if %%i==28 start cmd /c "echo Kaos++ & timeout /t 2 >nul"

    :: Meldingsbokser
    if %%i==18 powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Alt er fortsatt ufarlig!')"
    if %%i==35 powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Kaosmaskinen 2.0 nærmer seg slutten!')"

    :: Åpne Notepad med tull
    if %%i==22 (
        echo Dette er bare tull > temp_kaos.txt
        echo Ingenting farlig skjer >> temp_kaos.txt
        start notepad temp_kaos.txt
    )

    timeout /t 7 >nul
)

:: Avslutning
cls
color 07
echo Kaosmaskinen 2.0 ferdig! Alt tilbake til normalt.
timeout /t 2 >nul
del temp_kaos.txt >nul 2>&1
exit
