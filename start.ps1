# Start the course (Windows). Installs uv the first time if it's missing.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$UvVersion = "0.13.5"
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    $env:Path = "$HOME\.local\bin;$env:Path"
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host "First run: installing uv $UvVersion, which sets up Python for this course..."
        powershell -NoProfile -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/$UvVersion/install.ps1 | iex"
        if ($LASTEXITCODE -ne 0) { throw "Installing uv failed." }
    }
}

Write-Host "Preparing the course (the first time can take a few minutes)..."
uv sync --frozen --no-dev --quiet
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
uv run --frozen --no-sync python -m learn_llm.launch @args
exit $LASTEXITCODE
