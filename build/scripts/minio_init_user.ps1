if ($args.Count -ne 5) {
    Write-Host "Missing parameters <HOSTNAME> <ROOT_ACCESS_KEY> <ROOT_SECRET_KEY> <USER_ACCESS_KEY> <USER_SECRET_KEY>"
    Exit 1
}

$installPath = Join-Path $env:USERPROFILE "minio"

if (-not (Test-Path $installPath)) {
    New-Item -ItemType Directory -Force -Path $installPath
}

$downloadUrl = "https://dl.min.io/client/mc/release/windows-amd64/mc.exe"
$downloadPath = Join-Path $installPath "mc.exe"

try {
    Invoke-WebRequest $downloadUrl -OutFile $downloadPath -ErrorAction Stop
    Write-Host "mc.exe downloaded successfully."
} catch {
    Write-Host "Failed to download mc.exe: $($_.Exception.Message)"
    Exit 1
}

if (-not ([System.Environment]::GetEnvironmentVariable("Path", "User") -split ";" | Select-String -Pattern [regex]::Escape($installPath))) {
    try {
        [System.Environment]::SetEnvironmentVariable("Path", "$($env:Path);$installPath", "User")
        Write-Host "Path to mc.exe added to user environment variables."
    } catch {
        Write-Host "Failed to add path to mc.exe to user environment variables: $($_.Exception.Message)"
        Exit 1
    }
} else {
    Write-Host "Path to mc.exe already exists in user environment variables."
}

$hostname = $args[0]
$root_access_key = $args[1]
$root_secret_key = $args[2]
$user_access_key = $args[3]
$user_secret_key = $args[4]

try {
    & "$installPath\mc.exe" alias set minioadmin $hostname $root_access_key $root_secret_key
    Write-Host "Alias 'minioadmin' set successfully."
} catch {
    Write-Host "Failed to set alias 'minioadmin': $($_.Exception.Message)"
    Exit 1
}

try {
    & "$installPath\mc.exe" admin user add minioadmin $user_access_key $user_secret_key
    Write-Host "User added successfully."
} catch {
    Write-Host "Failed to add user: $($_.Exception.Message)"
    Exit 1
}

try {
    & "$installPath\mc.exe" admin policy attach minioadmin readwrite --user=$user_access_key
    Write-Host "Policy attached successfully."
} catch {
    Write-Host "Failed to attach policy: $($_.Exception.Message)"
    Exit 1
}
