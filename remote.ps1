# Set error action preference to stop on errors
$ErrorActionPreference = "Stop"

# Define the GitHub repository URL and the branch or release tag
$GitHubRepoURL = "https://github.com/natanrauber/klebertibiabot"
$BranchOrTag = "master" # or whatever branch or tag you want to download

# Define the temporary folder path
$TempFolder = "$env:TEMP\kleber"

# Create the temporary folder if it doesn't exist
if (-not (Test-Path $TempFolder)) {
    New-Item -ItemType Directory -Path $TempFolder | Out-Null
}

# Download the contents of the GitHub repository to the temporary folder
git clone --single-branch --branch $BranchOrTag $GitHubRepoURL $TempFolder

# Change directory to the temporary folder
Set-Location $TempFolder

# Run install dependencies
python -m pip install -r .\requirements.txt

# Run compiler
python .\compiler.py

# Get uid from uid.txt
$uid = Get-Content -Path ".\uid.txt"

# Run the executable with the generated uid
Start-Process -FilePath ".\dist\$uid.exe" -Wait

# Wait for uid.exe to finish before deleting uid.txt
do {
Start-Sleep -Seconds 1
} until (-not (Get-Process -Name "$uid" -ErrorAction SilentlyContinue))

# Delete uid.txt
Remove-Item -Path ".\uid.txt" -ErrorAction SilentlyContinue

# Change directory back to the original directory
Set-Location ..

# Remove the temporary folder and its contents
Remove-Item -Path $TempFolder -Recurse -Force
