@echo off
title KAOSMASKINEN 6.0 - STABLE SPAM EDITION
setlocal enabledelayedexpansion

:: Avoid encoding issues
chcp 437 >nul

echo Press ESC at any time to stop the chaos.
echo.

:: ESC detection
:loop
timeout /t 0 >nul
if exist stop.flag del stop.flag >nul

:: Start ESC listener in background
start "" /b cmd /c "choice /c E /n >nul & echo STOP > stop.flag"

:: Main chaos loop
for /l %%i in (1,1,9999) do (

    if exist stop.flag goto END

    cls
    set /a f=%random% %% 15
    color !f!

    echo === CHAOS CYCLE %%i ===
    echo.

    :: TERMINAL SPAM
    if %%i%%2==0 start cmd /c "echo TERMINAL SPAM! & timeout /t 1 >nul"
    if %%i%%3==0 start cmd /c "echo MORE TERMINAL SPAM! & timeout /t 1 >nul"

    :: POPUP SPAM (GUI)
    for /l %%p in (1,1,3) do (
        start powershell -command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('POPUP SPAM! %%i - %%p')"
    )

    :: Fake errors
    if %%i%%5==0 echo ERROR: Not enough chaos detected!
    if %%i%%5==1 echo FIXING: Increasing chaos level...

    :: Beep
    if %%i%%4==0 echo ^G

    timeout /t 1 >nul
)

:END
cls
color 07
echo CHAOS STOPPED BY ESC.
echo Everything is back to normal.
timeout /t 2 >nul
exit
