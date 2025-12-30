$ErrorActionPreference = 'Stop'

Write-Host "Checking for Python 3.10..." -ForegroundColor Cyan

# Try to find Python 3.10 launcher
try {
    # Use single quotes to prevent PowerShell from interpreting the semicolon
    $py_path = py -3.10 -c 'import sys; print(sys.executable)'
    Write-Host "Python 3.10 found at: $py_path" -ForegroundColor Green
}
catch {
    Write-Host "Python 3.10 NOT found!" -ForegroundColor Red
    Write-Host "FATAL ERROR: The AI libraries (Torch) do not support your current Python version (3.14)."
    Write-Host "Please install Python 3.10 from here: https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    exit 1
}

$repo_dir = 'ai-toolkit'
$venv_dir = 'ai-toolkit\venv'

# Create Directory if needed
if (-not (Test-Path $repo_dir)) {
    Write-Host "Cloning AI-Toolkit..."
    git clone https://github.com/ostris/ai-toolkit.git
}

# Create Venv
Write-Host "Creating Virtual Env with Python 3.10..."
py -3.10 -m venv $venv_dir

# Activate and Install
Write-Host "Installing Dependencies (this will take a while)..."
# We use the pip inside the venv directly
& "$venv_dir\Scripts\python" -m pip install --upgrade pip
& "$venv_dir\Scripts\pip" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
& "$venv_dir\Scripts\pip" install -r "$repo_dir\requirements.txt"

Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "To train, use:   $venv_dir\Scripts\python run.py config_lena.yaml"
