@echo off
setlocal

:: Definir la ruta de destino fija
set "dest_path=C:\Users\dicaf\Filmio\FilmioBack\Data\Temp"

:: Verificar que se pasaron los argumentos
if "%~1"=="" (
    echo Uso: unzip.bat ^<ruta_zip^>
    exit /b 1
)

:: Asignar la ruta del archivo ZIP a una variable
set "zip_path=%~1"

:: Comprobar si el archivo ZIP existe
if not exist "%zip_path%" (
    echo El archivo ZIP no existe: %zip_path%
    exit /b 1
)

:: Descomprimir el archivo ZIP usando PowerShell
PowerShell -Command "Expand-Archive -Path '%zip_path%' -DestinationPath '%dest_path%' -Force"

echo Descompresión completada en: %dest_path%

endlocal
