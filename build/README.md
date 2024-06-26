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

## Сhanges to files named
   ```bash
   nano docker/.SERVER.env
   ```

### Variable `MINDFULGUARD_ARGS` in `docker/.SERVER.env` file.

| Argument | Description | Type |
| -------- | -------- | --- |
| --LOG-TO-CONSOLE | Enable logging to console | Bool |
| --LOG-TO-FILE | Enable logging to file  | Bool |
| --LOG-FILE-PATH | Path to the log file  | String |
| --LOG-ROTATION-SIZE | Size limit for log file rotation  | String |
| --LOG-LEVEL | Set the logging level  | String |
| --LOG-RETENTION-PERIOD | Duration to retain log files  | String |

## Initial setup

   ```bash
   docker-compose -f docker/docker-compose-dev.yml up -d
   ```

   - ENV_FILE - path to the settings file.
   - POSTGRES_HOST - the host on which the database is running.
   - MINIO_HOSTNAME - the host running s3 storage.
   - ADMIN_LOGIN - name for the administrator.
   - ADMIN_PASSWORD - administrator password.
     
  ```bash
  chmod +x build/init.sh
  ```
  ```bash
  ./build/init.sh <ENV_FILE> <POSTGRES_HOST> <MINIO_HOSTNAME> <ADMIN_LOGIN> <ADMIN_PASSWORD>
  ```

  #### Example.
  ```bash
  ./build/init.sh docker/.SERVER.env localhost "http://localhost:9000" "Admin" "AdminPassword1!"
  ```
### If the service has been configured successfully, then the `build/admin_data.json` file will be created, which will contain the admin data for logging into the account.
