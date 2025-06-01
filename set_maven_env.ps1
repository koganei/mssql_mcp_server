# Set Maven environment variables
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Parent $scriptPath
$mavenBaseDir = $scriptDir

# Set environment variables
$env:MAVEN_BASEDIR = $mavenBaseDir
Write-Host "MAVEN_BASEDIR set to $mavenBaseDir"

# Check for JAVA_HOME
if (-not $env:JAVA_HOME) {
    Write-Host "WARNING: JAVA_HOME not set. Maven might not work properly."
    Write-Host "Please set JAVA_HOME environment variable to the location of your Java installation."
}

Write-Host "Maven environment variables set successfully."
Write-Host "You can now run mvnw.cmd or mvnw.py from any directory."
