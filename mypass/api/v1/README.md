# API

## • Authentication

- ## Sign up
  - ### Request
  
  ```http
  POST /v1/auth/sign_up
  ```
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  
  - Body
  
  | Parameters | Type | Description |
  | - | - | - |
  | login | string | the length is set in the configuration | |
  | secret_string | string | [secret_string](#secret_string) | |
  
  - ### Response
  
  ```json
  {
    "msg": {
          "de": null,
          "en": "registration was successful",
          "ru": "регистрация прошла успешно"
      },
      "secret_code": "base32 string for TOTP client",
      "backup_codes": [
          111111,
          222222,
          333333,
      ]
  }
  ```

- ## Sign in
  - ### Request
  
  ```http
  POST /v1/auth/sign_in?type=basic|backup
  ```
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  
  - Body
  
  | Parameters | Type | Description |
  | - | - | - |
  | login | string | the length is set in the configuration | |
  | secret_string | string | [secret_string](#secret_string) | |
  | expiration | int64 | 1 < expiration < sizeof(int64) | |
  | code | string | the code consists of a 6-digit number, the code can be obtained in the TOTP client or from a backup code | |
  
  - ### Response
  
  ```json
  {
      "msg": {
          "de": null,
          "en": "successful login",
          "ru": "удачный вход в систему"
      },
      "token": "b888...128bytes"
  }
  ```
# Variables
### secret_string
```c
length 128
sha256(login|password|private_string)
```
