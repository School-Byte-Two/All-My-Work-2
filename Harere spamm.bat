@echo off
title KAOSMASKINEN 7.0 - INSANITY OVERDRIVE
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

    echo === INSANITY OVERDRIVE CYCLE %%i ===
    echo.

    :: TERMINAL SPAM WAVES
    if %%i%%2==0 start cmd /c "echo TERMINAL WAVE! & timeout /t 1 >nul"
    if %%i%%3==0 start cmd /c "echo TERMINAL BLAST! & timeout /t 1 >nul"
    if %%i%%5==0 start cmd /c "echo TERMINAL SHOCKWAVE! & timeout /t 1 >nul"

    :: POPUP SPAM WAVES
    for /l %%p in (1,1,5) do (
        start powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('POPUP STORM! %%i - %%p')"
    )

    :: INSANITY MODE (after cycle 50)
    if %%i geq 50 (
        for /l %%x in (1,1,10) do (
            start powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('INSANITY MODE!!!')"
        )
    )

    :: ASCII GLITCH
    if %%i%%4==0 (
        echo [GL1TCH] ##########%%%%%%%##########%%%%%%%##########
        echo [GL1TCH] @@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%@@@@@@@@@@@@
    )

    :: FAKE MELTDOWN
    if %%i==100 (
        echo SYSTEM MELTDOWN DETECTED!!!
        echo ATTEMPTING TO CONTAIN CHAOS...
        timeout /t 2 >nul
    )

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
