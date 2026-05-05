@echo off
title Kaosmaskinen 3.0 ULTRA (ufarlig)
setlocal enabledelayedexpansion

color 0a
echo Initialiserer kaos...
timeout /t 2 >nul

:: Hovedloop ~60 sek
for /l %%i in (1,1,60) do (
    cls

    :: Tilfeldig farge
    set /a f=%random% %% 15
    color !f!

    echo === KAOSMASKINEN 3.0 – SYKLUS %%i ===
    echo.

    :: MATRIX-REGN
    for /l %%m in (1,1,20) do (
        set /a r=%random% %% 2
        if !r!==0 (
            echo 0101010101010101010101010101010101010101
        ) else (
            echo 1010101010101010101010101010101010101010
        )
    )

    echo.
    echo Skanner systemfiler...
    set /a scan=%random% %% 100
    echo Fremdrift: !scan!%%

    :: Fake feilmelding
    if %%i==15 echo FEIL: Uventet stabilitet oppdaget!
    if %%i==16 echo Løser problemet...
    if %%i==17 echo Problem løst. Kaos gjenopprettet.

    :: ASCII-animasjon
    if %%i==10 echo [■□□□□□□□□□]
    if %%i==11 echo [■■□□□□□□□□]
    if %%i==12 echo [■■■□□□□□□□]
    if %%i==13 echo [■■■■□□□□□□]
    if %%i==14 echo [■■■■■□□□□□]
    if %%i==15 echo [■■■■■■□□□□]
    if %%i==16 echo [■■■■■■■□□□]
    if %%i==17 echo [■■■■■■■■□□]
    if %%i==18 echo [■■■■■■■■■□]
    if %%i==19 echo [■■■■■■■■■■]

    :: Pip
    if %%i%%8==0 echo ^G

    :: Ekstra CMD-vinduer
    if %%i==20 start cmd /c "echo Ekstra vindu aktivert! & timeout /t 2 >nul"
    if %%i==40 start cmd /c "echo Kaosnivå maks! & timeout /t 2 >nul"

    :: Meldingsbokser
    if %%i==25 powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Systemet ditt er 100% trygt :)')"
    if %%i==50 powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('Kaosmaskinen 3.0 nærmer seg slutten!')"

    :: Notepad-spam
    if %%i==30 (
        echo Dette er fortsatt bare tull > kaos_temp.txt
        echo Ingenting farlig skjer her >> kaos_temp.txt
        echo Kaosnivå: %%i >> kaos_temp.txt
        start notepad kaos_temp.txt
    )

    timeout /t 1 >nul
)

:: Avslutning
cls
color 07
echo Kaosmaskinen 3.0 ULTRA ferdig! Alt tilbake til normalt.
timeout /t 2 >nul
del kaos_temp.txt >nul 2>&1
exit
