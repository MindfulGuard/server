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
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | login | string | the length is set in the configuration | &#10007; | |
  | secret_string | string | [secret_string](#secret_string) | &#10003; | |

  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#sign_up__200) | | |
  | [Service Unavailable](#503) | | |
  | [BAD REQUEST](#400) | | |
  | [CONFLICT](#sign_up__409) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

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
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | login | string | the length is set in the configuration | &#10007; | |
  | secret_string | string | [secret_string](#secret_string) | &#10003; | |
  | expiration | int64 | 1 < expiration < sizeof(int64) | &#10007; | |
  | code | string | the code consists of a 6-digit number, the code can be obtained in the TOTP client or from a backup code | &#10007; | |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#sign_in__200) | | |
  | [BAD REQUEST](#400) | | |
  | [NOT_FOUND](#sign_in__404) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |
  
    ##### sign_in__200
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
    
    ##### sign_in__404
    ```json
    {
        "msg": {
            "de": null,
            "en": "user not found",
            "ru": "пользователь не найден"
        }
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
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#sessions__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### sessions__200
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
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | id | string | uuid v4 | &#10007; | |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#sign_out__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [NOT_FOUND](#sign_out__404) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### sign_out__200
    ```json
    {
      "msg": {
        "de": null,
        "en": "the session token has been deleted",
        "ru": "токен сеанса был удален"
      }
    }
    ```

    ##### sign_out__404
    ```json
    {
      "msg": {
            "de": null,
            "en": "failed to delete token",
            "ru": "не удалось удалить токен"
        },
    }
    ```

## • Safe

- ## Create
  - ### Request
  
  ```http
  POST /v1/safe/create
  ```
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | name | string | the length is specified in the configuration | &#10007; | |
  | description | string | the length is specified in the configuration | [&#10003;](#Text) | |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#create__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#create__500) | | |

    ##### create__200
    ```json
    {
      "msg": {
            "de": null,
            "en": "the safe was successfully created",
            "ru": "сейф удачно создан"
        },
    }
    ```

    ##### create__500
    ```json
    {
      "msg": {
            "de": null,
            "en": "failed to create a safe",
            "ru": "не удалось создать сейф"
        },
    }
    ```
    
- ## Get
  - ### Request
  
  ```http
  GET /v1/safe/get
  ```
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#get__200) | list[N].discription, [watch text encryption](#Text) | |
  | [BAD REQUEST](#400) | | |
  | [NOT_FOUND](#get__404) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### get__200
    ```json
    {
      "list": [
            {
                "id": "00538bc9-dedc-401a-ab1a-a4a024906784",
                "name": "hello_user2 mew",
                "description": "Encrypted string",
                "created_at": 1695044525,
                "updated_at": 1695044525
            },
            {
                "id": "77ab76fe-47dd-4bac-9d12-d9fc2c93de0c",
                "name": "hello_user3 mew",
                "description": "Encrypted string",
                "created_at": 1695044539,
                "updated_at": 1695044539
            }
        ],
        "count": 2
    }
    ```

    ##### get__404
    ```json
    {
      "msg": [],
      "count": 0
    }
    ```

- ## Update
  - ### Request
  
  ```http
  PUT /v1/safe/update
  ```
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | id | string | uuid v4 | &#10007; | |
  | name | string | the length is specified in the configuration | &#10007; | |
  | description | string | the length is specified in the configuration | [&#10003;](#Text) | |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#update__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#update__500) | | |

    ##### update__200
    ```json
    {
      "msg": {
            "de": null,
            "en": "the safe was successfully updated",
            "ru": "сейф успешно обновлен"
        },
    }
    ```

    ##### update__500
    ```json
    {
        "msg": {
            "de": null,
            "en": "failed to update the safe",
            "ru": "не удалось обновить сейф"
        }
    }
    ```

- ## Delete
  - ### Request
  
  ```http
  DELETE /v1/safe/delete
  ```
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | id | string | uuid v4 | &#10007; | |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#delete__200) | | |
  | [BAD REQUEST](#400) | | |
  | [NOT FOUND](#delete__404) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### delete__200
    ```json
    {
        "msg": {
            "de": null,
            "en": "the safe has been successfully deleted",
            "ru": "сейф был успешно удален"
        }
    }
    ```

    ##### delete__404
    ```json
    {
        "msg": {
            "de": null,
            "en": "failed to delete the safe",
            "ru": "не удалось удалить сейф"
        }
    }
    ```

## • Public

- ## Configuration
  - ### Request
  
  ```http
  GET /v1/public/configuration
  ```
  - Headers
  
  | key | value | Description |
  | - | - | - |
  
  - Body
  
  | Parameters | Type | Description |
  | - | - | - |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#configuration__200) | | |

    ##### configuration__200
    ```json
    {
        "authentication": {
            "pbkdf2": {
                "SHA": "sha256",
                "iterations": 10000
            },
            "aes256": {
                "mode": "GCM"
            },
            "password_rule": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[\\W]).{8,64}$"
        }
    }
    ```
    
## • JSON Responses
-
  ### *401*
  ```json
  {
    "msg": {
      "de": null,
      "en": "unauthorized",
      "ru": "не авторизован"
    }
  }
  ```
-
  ### *400*
  ```json
  {
    "msg": {
      "de": null,
      "en": "failed to delete the safe",
      "ru": "не удалось удалить сейф"
    }
  }
  ```

-
  ### *503*
  ```json
  {
      "msg": {
        "de": null,
        "en": "the service is not available",
        "ru": "сервис недоступен"
      },
  }
  ```

-
  ### *500*
  ```json
  {
    "msg": {
      "de": null,
      "en": "server error",
      "ru": "ошибка сервера"
    },
  }
  ```

# Encryption
## **The "Encryption" section explains how the client should encrypt the data.**

- #### uuid  = UUIDv4 (stored only on the client)
- #### password = @mV3?fsf43vvewqf (must match a [regular expression "authentication.password_rule"](#configuration__200))

### secret_string
```python
length = 128
sha256(login|password|uuid)
```

- #### iterations = 100000 ([can be obtained from the response "authentication.pbkdf2.iterations"](#configuration__200)) *(Abandoned)*
- #### mode = "" ([can be obtained from the response "authentication.aes256.mode"](#configuration__200))

## Text
```python
private_key = PBKDF2(password, salt = uuid, iterations = 10000, length = 64)[:32]
ciphertext = aes256_encrypt(text, private_key, mode) return iv(16 bytes)+cyphertext+tag(16 bytes).hex.to_string() = "e60c203ae89b8ec4cc3d4917..."
aes256_decrypt(ciphertext.fromhex, private_key, mode)
```
