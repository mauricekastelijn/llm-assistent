@echo off
setlocal enabledelayedexpansion

REM capture the directory where this script is located
set SCRIPT_PATH=%~dp0

REM Get the current working directory
set CWD=%cd%

REM Check if any arguments are passed
if "%~1"=="" (
    set ROOT_PATH=%CWD%
) else (
    for %%I in ("%~1") do set ROOT_PATH=%%~fI
)
echo Using code base root path %ROOT_PATH%

REM swap \ for / in the path
REM because docker likes it that way in volume mounting
set ROOT_PATH=%ROOT_PATH:\=/%

REM also change drive
set ROOT_PATH=%ROOT_PATH:C:=//c%
set ROOT_PATH=%ROOT_PATH:D:=//d%
set ROOT_PATH=%ROOT_PATH:E:=//e%
set ROOT_PATH=%ROOT_PATH:F:=//f%

docker compose -f %SCRIPT_PATH%\docker-compose-dev.yml build backend
docker compose -f %SCRIPT_PATH%\docker-compose-dev.yml run -it --rm ^
    --env OLLAMA_ENDPOINT="http://host.docker.internal:11434" ^
    -p 8000:8000 ^
    -v "%ROOT_PATH%/backend/backend/:/home/backend" ^
    -v "%ROOT_PATH%/secrets/backend/.env:/home/backend/secrets/.env" ^
    backend

endlocal
