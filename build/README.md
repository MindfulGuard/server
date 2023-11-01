# Build Instructions

## Download

  ```bash
  wget https://github.com/MindfulGuard/server/releases/download/main/build-release.tar.gz
  ```

  ```bash
  tar -xzvf build-release.tar.gz
  ```

  ```bash
  cd build-release
  ```

## Set environments
   ```bash
   nano ~/.bashrc
   ```

  - Add the variables to the file, replacing the values with your values
   ```bash
   export DATABASE_PORT=5432
   export DATABASE_USER="mindfulguard"
   export DATABASE_HOST="postgresql"
   export DATABASE_PASSWORD="root_password"
   export MINIO_HOSTNAME="http://localhost:9000"
   export MINIO_ROOT_ACCESS_KEY="rootuser123"
   export MINIO_ROOT_SECRET_KEY="rootpassword123"
   export MINIO_USER_ACCESS_KEY="useruser123"
   export MINIO_USER_SECRET_KEY="userpassword123"
   ```

 - To apply the new environment variables, restart your shell or run this command
  ```bash
  source ~/.bashrc
  ```
    
## Initial setup

   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```
   - LOGIN - must contain no less than 2 and no more than 50 characters, may contain Latin characters, digits, hyphen and underscore
   - PASSWORD - not less than 8 and not more than 64 characters, must have 1 upper case character, 1 lower case character, 1 special character and 1 digit.
   - **IT IS STRONGLY RECOMMENDED TO STORE "LOGIN" AND "PASSWORD" IN A SAFE PLACE AND NOT IN THE ENVIRONMENT.**
     
   ```bash
   make -f build/Makefile init admin_login=LOGIN admin_password=PASSWORD minio_hostname="$MINIO_HOSTNAME" minio_root_access_key="$MINIO_ROOT_ACCESS_KEY" minio_root_secret_key="$MINIO_ROOT_SECRET_KEY" minio_user_access_key="$MINIO_USER_ACCESS_KEY" minio_user_secret_key="$MINIO_USER_SECRET_KEY"
   ```
   - Response
   ```bash
   Login: your_login
   Password: your_password
   Salt: salt_value
   Secret code: secret_code_value
   Backup codes: backup_codes_value
   ```