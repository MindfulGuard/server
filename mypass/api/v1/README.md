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

  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#sign_up__200) | | |
  | [Service Unavailable](#sign_up__503) | | |
  | [BAD REQUEST](#sign_up__400) | | |
  | [CONFLICT](#sign_up__409) | | |

    ##### sign_up__200
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
    
    ##### sign_up__503
    ```json
    {
      "msg": {
            "de": null,
            "en": "the service is not available",
            "ru": "сервис не доступен"
        },
        "secret_code": null,
        "backup_codes": null
    }
    ```
    
    ##### sign_up__400
    ```json
    {
      "msg": {
            "de": null,
            "en": "the data is not valid",
            "ru": "неправильные данные"
        },
        "secret_code": null,
        "backup_codes": null
    }
  
    ```
    ##### sign_up__409
    ```json
    {
      "msg": {
            "de": null,
            "en": "the user already exists",
            "ru": "пользователь уже существует"
        },
        "secret_code": null,
        "backup_codes": null
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
- ## Sessions
  - ### Request
  
  ```http
  GET /v1/auth/sessions
  ```
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description |
  | - | - | - |
  
  - ### Response
  
  ```json
  {
    "list":[
      {
        "id": "25275093-aa91-4937-941c-1934e0174d2e",
        "first_login": 1695004570,
        "last_login": 1695004570,
        "device": "Chromium/100.0.0 or <Сlient name>/<Version>",
        "last_ip": "127.0.0.1",
        "expiration": 1695004570
      },
      {
        "id": "188da897-a032-4747-bbc7-99c078dd539b",
        "first_login": 1695004574,
        "last_login": 1695004576,
        "device": "Chromium/100.0.0 or <Сlient name>/<Version>",
        "last_ip": "127.0.0.1",
        "expiration": 1695004572
      }
    ],
    "count":2
  }
  ```

- ## Sign out
  - ### Request
  
  ```http
  DELETE /v1/auth/sign_out
  ```
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description |
  | - | - | - |
  | id | string | uuid v4 | |
  
  - ### Response
  
  ```json
  {
    "msg": {
      "de": null,
      "en": "the session token has been deleted",
      "ru": "токен сеанса был удален"
    }
  }
  ```

# Variables
### secret_string
```c
length 128
sha256(login|password|private_string)
```
