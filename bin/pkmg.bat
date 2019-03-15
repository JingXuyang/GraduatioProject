@echo off

set CURRENT_DIR=%cd%

cd /d %~dp0
cd ..

set PKMG_ROOT_PATH=%cd%
set PKMG_THIRDPARTY_PATH=%PKMG_ROOT_PATH%\thirdparty
set PROJECT_ROOT_PATH=C:\projects

cd /d %CURRENT_DIR%

set DATABASE=CGTeamwork
rem set DATABASE=LocalCGTeamwork

set PLTK_LANGUAGE=Chinese

set PYTHONPATH=%PKMG_ROOT_PATH%;%PKMG_ROOT_PATH%\main;%PKMG_THIRDPARTY_PATH%

%~sdp0\python.bat %PKMG_ROOT_PATH%\main\pkmg %*