# Gera o executavel Windows (dist/CalculadoraPremiacao.exe).
# Uso: .\build.ps1

$ErrorActionPreference = "Stop"

$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Criando ambiente virtual..."
    python -m venv (Join-Path $PSScriptRoot "venv")
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
}

& $venvPython -m PyInstaller --noconfirm --onefile --windowed `
    --name "CalculadoraPremiacao" `
    --icon "assets/icon.ico" `
    --add-data "assets;assets" `
    --collect-all customtkinter `
    main.py

Write-Host ""
Write-Host "Executavel gerado em: dist\CalculadoraPremiacao.exe"
