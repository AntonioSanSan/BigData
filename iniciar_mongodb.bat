@echo off
REM Ruta personalizada a la base de datos de MongoDB
SET DBPATH=%~dp0db_temp

REM Crear la carpeta si no existe
IF NOT EXIST "%DBPATH%" (
    mkdir "%DBPATH%"
    echo Carpeta db_temp creada en: %DBPATH%
)

REM Iniciar MongoDB con esa ruta
echo Iniciando MongoDB en %DBPATH% ...
mongod --dbpath "%DBPATH%"
pause
