@echo off
setlocal enabledelayedexpansion

echo 🔍 Searching for Visual Studio Build Tools...

:: Common paths for vcvars64.bat
set "VS_PATHS=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat;C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat;C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat;C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat;C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvars64.bat"

set "FOUND_VS="

for %%P in ("%VS_PATHS:;=" "%") do (
    if exist %%P (
        set "FOUND_VS=%%~P"
        goto :found
    )
)

:found
if not defined FOUND_VS (
    echo ❌ Could not find vcvars64.bat automatically.
    echo Please open "x64 Native Tools Command Prompt" manually and run:
    echo ai-toolkit\venv\Scripts\python.exe -m pip install TTS
    pause
    exit /b 1
)

echo ✅ Found VS Environment: !FOUND_VS!
echo 🚀 Activating Environment and Installing TTS...

call "!FOUND_VS!"

:: Run pip install
echo.
echo 📦 Installing TTS...
ai-toolkit\venv\Scripts\python.exe -m pip install TTS

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ TTS Installation SUCCESSFUL!
) else (
    echo ❌ TTS Installation FAILED.
)
pause
