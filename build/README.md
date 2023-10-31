# Build Instructions

## Download

  ```bash
  curl -O https://github.com/MindfulGuard/server/releases/download/main/build-release.tar.gz
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
   export DATABASE_PORT = 5432
   export DATABASE_USER = mindfulguard
   export DATABASE_HOST = postgresql
   export DATABASE_PASSWORD = root_password
   export MINIO_HOSTNAME = http://localhost:9000
   export MINIO_USER_ACCESS_KEY = useruser123
   export MINIO_USER_SECRET_KEY = userpassword123
   ```
## Initial setup

   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

   ```bash
   make -f build/Makefile init
   ```
