if ($args.Count -ne 5){
    Write-Host "Missing parameters <ENV_FILE> <POSTGRES_HOST> <MINIO_HOSTNAME> <ADMIN_LOGIN> <ADMIN_PASSWORD>"
    Exit 1
}

$envfile = $args[0]
$pghost = $args[1]
$miniohost = $args[2]
$adminlogin = $args[3]
$adminpassword = $args[4]

try {
    $envContent = Get-Content $envfile
    foreach ($line in $envContent) {
        $name, $value = $line.Split('=')
        Set-Item -Path "env:\$name" -Value $value
    }
} catch {
    Write-Host "Error reading environment file: $_"
    Exit 1
}

try {
    make -f build/Makefile init `
        admin_login="$adminlogin" `
        admin_password="$adminpassword" `
        database_host="$pghost" `
        database_port="$env:POSTGRES_PORT" `
        database_user="$env:POSTGRES_USER" `
        database_password="$env:POSTGRES_PASSWORD" `
        minio_hostname="$miniohost" `
        minio_root_access_key="$env:MINIO_ROOT_USER" `
        minio_root_secret_key="$env:MINIO_ROOT_PASSWORD" `
        minio_user_access_key="$env:MINIO_USER_ACCESS_KEY" `
        minio_user_secret_key="$env:MINIO_USER_SECRET_KEY"
} catch {
    Write-Host "Error executing Makefile: $_"
    Exit 1
}
