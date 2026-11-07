#!/usr/bin/env bash
# ==============================================================================
# SAORI TACTICAL // Automated Deployment Script (Linux / Termux / macOS)
# Defense-Grade Sovereign Emergency System // Zero-VRAM Architecture
# ==============================================================================

set -e

echo "=============================================================================="
echo "[SYSTEM] SAORI TACTICAL // AUTOMATED DEPLOYMENT INSTALLER"
echo "[NOTICE] DEFENSE-GRADE DEPLOYMENT // ZERO-VRAM ARCHITECTURE"
echo "=============================================================================="
echo ""

# 1. Comprobar Python
echo "[1/4] Verificando entorno Python..."
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 no encontrado en el sistema."
    echo "[ACTION] Instale Python 3.10 o superior (ej: apt install python3 python3-pip)"
    exit 1
fi
echo "[OK] Python 3 detectado."
echo ""

# 2. Instalar dependencias
echo "[2/4] Instalando requerimientos Python..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r "$(dirname "$0")/requirements.txt" --quiet
echo "[OK] Dependencias instaladas."
echo ""

# 3. Comprobar Ollama
echo "[3/4] Verificando motor de inferencia local Ollama..."
if ! command -v ollama &>/dev/null; then
    echo "[WARN] Ollama no encontrado en PATH."
    echo "[ACTION] Instale Ollama con: curl -fsSL https://ollama.com/install.sh | sh"
else
    echo "[OK] Ollama detectado."
    echo "[INFO] Descargando Flota Multi-Modelo local..."
    ollama pull llama3.2:3b || true
    ollama pull qwen2.5-coder:3b || true
    ollama pull deepseek-r1:1.5b || true
    echo "[OK] Modelos descargados."
fi
echo ""

# 4. Finalizacion
echo "=============================================================================="
echo "[SUCCESS] INSTALACION FINALIZADA"
echo "Para ejecutar la consola interactiva:"
echo "  python3 saori_tactical.py"
echo ""
echo "Para iniciar el servidor web táctico:"
echo "  python3 saori_tactical.py web --port 8090"
echo "=============================================================================="
