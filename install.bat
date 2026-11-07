@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

echo ==============================================================================
echo [SYSTEM] SAORI TACTICAL // AUTOMATED FIELD DEPLOYMENT INSTALLER
echo [NOTICE] DEFENSE-GRADE DEPLOYMENT // ZERO-VRAM ARCHITECTURE
echo ==============================================================================
echo.

:: 1. Verificar Python
echo [1/4] Verificando entorno de ejecucion Python...
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python 3 no fue detectado en PATH.
    echo [ACTION] Instale Python 3.10 o superior desde https://www.python.org/downloads/
    pause
    exit /b 1
)
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Se requiere Python 3.10 o superior.
    pause
    exit /b 1
)
echo [OK] Python detectado correctamente.
echo.

:: 2. Instalar dependencias Python
echo [2/4] Instalando dependencias de Python (requirements.txt)...
python -m pip install --upgrade pip --quiet
python -m pip install -r "%~dp0requirements.txt" --quiet
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Fallo al instalar librerias de requirements.txt.
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas.
echo.

:: 3. Verificar o instalar Ollama
echo [3/4] Verificando motor de inferencia local Ollama...
where ollama >nul 2>&1
if %ERRORLEVEL% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
        set "PATH=%LOCALAPPDATA%\Programs\Ollama;%PATH%"
    ) else (
        echo [INFO] Ollama no encontrado. Intentando instalacion via winget...
        winget install Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements
        set "PATH=%LOCALAPPDATA%\Programs\Ollama;%PATH%"
    )
)

where ollama >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARN] No se pudo instalar Ollama automaticamente.
    echo [ACTION] Descargue e instale Ollama manualmente desde: https://ollama.com/download
) else (
    echo [OK] Motor Ollama verificado.
    echo [INFO] Asegurando que el demonio de Ollama este respondiendo...
    curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        start "" /B ollama serve
        timeout /t 3 /nobreak > nul
    )
    
    echo [INFO] Descargando Flota Multi-Modelo local (requiere ancho de banda)...
    echo.
    echo --- Modelo 1/3: Llama 3.2 3B (Tactical/Supervivencia/Triage) ---
    ollama pull llama3.2:3b
    echo.
    echo --- Modelo 2/3: Qwen 2.5 Coder 3B (SRE Windows/PowerShell) ---
    ollama pull qwen2.5-coder:3b
    echo.
    echo --- Modelo 3/3: DeepSeek R1 1.5B (Analista Logico Deductivo) ---
    ollama pull deepseek-r1:1.5b
    echo.
    echo [OK] Flota Multi-Modelo descargada y verificada en almacenamiento local.
    
    echo [INFO] Purgando VRAM para politica Zero-Hogging (0 MB ocupados)...
    python -c "import urllib.request, json; [urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/generate', data=json.dumps({'model': m, 'keep_alive': 0}).encode(), headers={'Content-Type': 'application/json'})) for m in ['llama3.2:3b','qwen2.5-coder:3b','deepseek-r1:1.5b']]" >nul 2>&1
)
echo.

:: 4. Finalizacion
echo ==============================================================================
echo [SUCCESS] DESPLIEGUE FINALIZADO EXITOSAMENTE
echo.
echo Para iniciar la consola interactiva táctica:
echo   .\saori.bat
echo.
echo Para levantar el servidor web móvil para celulares y tablets:
echo   .\saori.bat web --port 8090
echo ==============================================================================
pause
