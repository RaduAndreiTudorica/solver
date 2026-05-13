# LeetCode Solver - Setup Script
# Ruleaza o singura data dupa git clone
# Usage: .\setup.ps1

Write-Host "=== LeetCode Solver Setup ===" -ForegroundColor Cyan
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force

# 1. Verifica Python
Write-Host "`n[1/4] Verific Python..." -ForegroundColor Yellow
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} else {
    Write-Host "[EROARE] Python nu e instalat sau nu e in PATH." -ForegroundColor Red
    Write-Host "Descarca de la https://python.org si bifeaza 'Add python.exe to PATH' la instalare." -ForegroundColor Red
    exit 1
}
$version = & $pythonCmd --version
Write-Host "[OK] Gasit: $version (comanda: $pythonCmd)" -ForegroundColor Green

# 2. Creeaza venv
Write-Host "`n[2/4] Creez virtual environment (.venv)..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "[SKIP] .venv exista deja." -ForegroundColor Gray
} else {
    & $pythonCmd -m venv .venv
    Write-Host "[OK] .venv creat." -ForegroundColor Green
}

# 3. Instaleaza dependente
Write-Host "`n[3/4] Instalez dependente din requirements.txt..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
& .\.venv\Scripts\pip.exe install -r requirements.txt
Write-Host "[OK] Dependente instalate." -ForegroundColor Green

# 4. API Key
Write-Host "`n[4/4] Configurez GEMINI_API_KEY..." -ForegroundColor Yellow
$existingKey = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "User")
if ($existingKey) {
    Write-Host "[SKIP] GEMINI_API_KEY e deja setat." -ForegroundColor Gray
} else {
    $apiKey = Read-Host "Introdu GEMINI_API_KEY (de pe https://aistudio.google.com/apikey)"
    if ($apiKey) {
        [Environment]::SetEnvironmentVariable("GEMINI_API_KEY", $apiKey, "User")
        Write-Host "[OK] API key salvat permanent in variabilele de mediu." -ForegroundColor Green
    } else {
        Write-Host "[WARN] API key gol. Seteaza-l manual: `$env:GEMINI_API_KEY='cheia-ta'" -ForegroundColor Yellow
    }
}

# Done
Write-Host "`n=== Setup complet! ===" -ForegroundColor Cyan
Write-Host "Ruleaza scriptul cu:" -ForegroundColor White
Write-Host "  .\run.ps1" -ForegroundColor Green
Write-Host "sau manual:" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "  python script.py" -ForegroundColor Green
Write-Host "`nNota: Ruleaza PowerShell ca Administrator pentru hotkey-uri globale." -ForegroundColor Yellow