@echo off
title Kaosmaskinen (ufarlig)
color 0a

echo Starter ufarlig kaos...
timeout /t 2 >nul

setlocal enabledelayedexpansion

:: Kjør i ca. 40 sekunder
for /l %%i in (1,1,40) do (
    cls

    :: Tilfeldig farge
    set /a f=%random% %% 15
    color 0!f!

    :: Tilfeldig tekst
    echo Kaosnivå %%i
    echo.
    for /l %%x in (1,1,20) do (
        set /a r=%random% %% 255
        echo Tilfeldig verdi: !r!
    )

    :: Litt pip
    echo ^G

    :: Åpne et ekstra CMD-vindu av og til
    if %%i==10 start cmd /c "echo Hei fra et ekstra vindu! & timeout /t 2 >nul"
    if %%i==25 start cmd /c "echo Enda et vindu! & timeout /t 2 >nul"

    :: Meldingsboks av og til
    if %%i==15 powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Alt er ufarlig :)')"
    if %%i==30 powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Snart ferdig!')"

    timeout /t 1 >nul
)

cls
color 07
echo Ferdig! Alt tilbake til normalt.
timeout /t 2 >nul
exit
