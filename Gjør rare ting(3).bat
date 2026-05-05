@echo off
title KAOSMASKINEN 8.0 - APOCALYPSE PRIME
setlocal enabledelayedexpansion

:: Avoid encoding issues
chcp 437 >nul

echo PRESS ESC ANYTIME TO STOP THE CHAOS.
echo.

:: ESC detection flag
if exist stop.flag del stop.flag >nul

:: Start ESC listener
start "" /b cmd /c "choice /c E /n >nul & echo STOP > stop.flag"

:: MAIN LOOP
for /l %%i in (1,1,999999) do (

    if exist stop.flag goto END

    cls
    set /a f=%random% %% 15
    color !f!

    echo === APOCALYPSE PRIME CYCLE %%i ===
    echo.

    :: TERMINAL SPIRAL SPAM
    if %%i%%2==0 start cmd /c "echo SPIRAL NODE A & timeout /t 1 >nul"
    if %%i%%3==0 start cmd /c "echo SPIRAL NODE B & timeout /t 1 >nul"
    if %%i%%4==0 start cmd /c "echo SPIRAL NODE C & timeout /t 1 >nul"
    if %%i%%5==0 start cmd /c "echo SPIRAL NODE D & timeout /t 1 >nul"

    :: POPUP STORM WAVES
    for /l %%p in (1,1,6) do (
        start powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('APOCALYPSE POPUP! %%i - %%p')"
    )

    :: OVERDRIVE MODE (after cycle 100)
    if %%i geq 100 (
        for /l %%x in (1,1,12) do (
            start powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('OVERDRIVE!!!')"
        )
    )

    :: ASCII GLITCH STORM
    if %%i%%6==0 (
        echo [CORRUPTION] %%%%%%%%########@@@@@@@@@@########%%%%%%%%
        echo [CORRUPTION] @@@@@@@@%%%%%%%%########%%%%%%%%@@@@@@@@@
        echo [CORRUPTION] ########@@@@@@@@@@%%%%%%%%@@@@@@@@@@######
    )

    :: FAKE SYSTEM REBOOT
    if %%i==150 (
        echo SYSTEM REBOOT INITIATED...
        timeout /t 1 >nul
        echo SHUTTING DOWN CHAOS MODULES...
        timeout /t 1 >nul
        echo REBOOT FAILED. CHAOS LEVEL TOO HIGH.
        timeout /t 2 >nul
    )

    :: AI GLITCH TEXT
    if %%i%%7==0 echo [AI ERROR] Logic overflow detected.
    if %%i%%7==1 echo [AI ERROR] Attempting self‑repair...
    if %%i%%7==2 echo [AI ERROR] Repair failed. Chaos increasing.

    :: BEEP
    if %%i%%3==0 echo ^G

    timeout /t 1 >nul
)

:END
cls
color 07
echo CHAOS TERMINATED BY ESC.
echo SYSTEM RESTORED TO NORMAL.
timeout /t 2 >nul
exit
