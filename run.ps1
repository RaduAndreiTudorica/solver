# LeetCode Solver - Run Script
# Usage: .\run.ps1

# Verifica venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "[EROARE] .venv nu exista. Ruleaza mai intai: .\setup.ps1" -ForegroundColor Red
    exit 1
}

# Verifica API key
$apiKey = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "User")
if (-not $apiKey) {
    Write-Host "[EROARE] GEMINI_API_KEY nu e setat. Ruleaza mai intai: .\setup.ps1" -ForegroundColor Red
    exit 1
}

# Seteaza API key in sesiunea curenta (pentru procese child)
$env:GEMINI_API_KEY = $apiKey

# Ruleaza
Write-Host "Pornind LeetCode Solver..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe script.py