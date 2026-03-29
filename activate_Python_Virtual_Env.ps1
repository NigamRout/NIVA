<#
.SYNOPSIS
    Activates a Python virtual environment.

.DESCRIPTION
    This script checks for the existence of a specified Python virtual environment
    and activates it if found. It's the PowerShell equivalent of the batch file
    for activating the environment in the current session.
#>

Set-ExecutionPolicy RemoteSigned -Scope Process

# Define variables using PowerShell syntax
$vEnv_Base = "D:\apps\Projects\GitHub\NIVA" 
$vEnv_Name = ".venv"

# Use Join-Path for robust path handling
$vEnv_Path = Join-Path -Path $vEnv_Base -ChildPath $vEnv_Name

# Check if the directory exists
if (Test-Path -Path $vEnv_Path -PathType Container) {
    # Use the dot-sourcing operator (.) to run the script in the current session
    . "$vEnv_Path\Scripts\Activate.ps1"

    Write-Host "Virtual Env: [$vEnv_Path] activated with Python Version [$(python --version)]"
    
} else {
    # Warn the user if the virtual environment is not found
    Write-Host "Warning: Virtual Env NOT found at: $vEnv_Path" -ForegroundColor Yellow
}



# python -m pip install --upgrade --force-reinstall pip 