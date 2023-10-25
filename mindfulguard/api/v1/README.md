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
  | expiration | int64 | 1 < expiration < sizeof(int64), measured in minutes | &#10007; | |
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

- ## Sign out
  - ### Request
  
  ```http
  DELETE /v1/auth/sign_out/{token_id}
  ```
  
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | token_id | string | uuid v4, [id of the token that can be obtained from sessions](#sessions__200) | &#10007; | |
  
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

## • Administrator

- ## Users Information
  - ### Request
  
  ```http
  GET /v1/admin/users/all?page=1|2|3,...
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
  | [OK](#admin_get_all_users_200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [FORBIDDEN](#403) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### admin_get_all_users_200
    ```json
    {
        "page": 1,
        "total_pages": 1,
        "total_users": 2,
        "list": [
            {
                "id": "09c14580-b69e-4292-8a1a-4e88256bd6a3",
                "login": "User423_-",
                "ip": "127.0.0.1",
                "confirm": true,
                "created_at": 1697796126
            },
            {
                "id": "648ac8c5-2c6f-45a8-a855-fa1d0857598c",
                "login": "UFser423534_-",
                "ip": "127.0.0.1",
                "confirm": false,
                "created_at": 1697794266
            }
        ]
    }
    ```

  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | page | integer | displays the current page | &#10007; | |
  | count_pages | integer | displays the total number of pages | &#10007; | |
  | count_users | integer | displays the total number of users | &#10007; | |
  | list | array | the array contains 10 users per page | &#10007; | |

- ## Search Users
  - ### Request
  
  ```http
  GET /v1/admin/users/search?by=id|username
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
  | [OK](#admin_search_users_200) | | |
  | [NOT_FOUND](#admin_search_users_404) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [FORBIDDEN](#403) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### admin_search_users_200
    ```json
    {
        "id": "91ac1500-7567-4021-b87a-156f79c45281",
        "login": "User_-12345",
        "ip": "127.0.0.1",
        "confirm": true,
        "created_at": 1698245381
    }
    ```

    ##### admin_search_users_404
    ```json
    {}
    ```

- ## Get Settings
  - ### Request
  
  ```http
  GET /v1/admin/settings
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
  | [OK](#admin_get_settings_200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [FORBIDDEN](#403) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### admin_get_settings_200
    ```json
    {
        "password_rule": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[\\W]).{8,64}$",
        "item_categories": [
            "LOGIN",
            "PASSWORD",
            "API_CREDENTIAL",
            "SERVER",
            "DATABASE",
            "CREDIT_CARD",
            "MEMBERSHIP",
            "PASSPORT",
            "SOFTWARE_LICENSE",
            "OUTDOOR_LICENSE",
            "SECURE_NOTE",
            "WIRELESS_ROUTER",
            "BANK_ACCOUNT",
            "DRIVER_LICENSE",
            "IDENTITY",
            "REWARD_PROGRAM",
            "DOCUMENT",
            "EMAIL_ACCOUNT",
            "SOCIAL_SECURITY_NUMBER",
            "MEDICAL_RECORD",
            "SSH_KEY"
        ],
        "item_types": [
            "STRING",
            "PASSWORD",
            "EMAIL",
            "CONCEALED",
            "URL",
            "OTP",
            "DATE",
            "MONTH_YEAR",
            "MENU",
            "FILE"
        ],
        "registration_status": true,
        "scan_time_routines_tokens": 60,
        "scan_time_routines_users": 60,
        "confirmation_period": 604800
    }
    ```

- ## Update Settings
  - ### Request
  
  ```http
  PUT /v1/admin/settings?key=<str>
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
  | value |  |  | &#10007; |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#admin_update_settings_200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [FORBIDDEN](#403) | | |
  | [INTERNAL_SERVER_ERROR](#admin_update_settings_500) | | |

    ##### admin_update_settings_200
    ```json
    {
      "msg": {
            "de": null,
            "en": "the settings have been successfully updated",
            "ru": "настройки были успешно обновлены"
        }
    }
    ```

    ##### admin_update_settings_500
    ```json
    {
      "msg": {
            "de": null,
            "en": "failed to update settings",
            "ru": "не удалось обновить настройки"
        }
    }
    ```

- ## Creating a user by an administrator
  - ### Request
  
  ```http
  POST /v1/admin/users
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
  | [OK](#sign_up__200) | | |
  | [Service Unavailable](#503) | | |
  | [BAD REQUEST](#400) | | |
  | [CONFLICT](#sign_up__409) | | |
  | [UNAUTHORIZED](#401) | | |
  | [FORBIDDEN](#403) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

- ## Delete User
  - ### Request
  
  ```http
  DELETE /v1/admin/users?id=<uuid.v4>
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
  | [OK](#user_delete_200) | | |
  | [UNAUTHORIZED](#401) | | |
  | [BAD REQUEST](#400) | | |
  | [FORBIDDEN](#403) | | |
  | [INTERNAL_SERVER_ERROR](#user_delete_500) | | |

## • User

- ## User Information
  - ### Request
  
  ```http
  GET /v1/user
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
  | [OK](#user_info_200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### user_info_200
    ```json
    {
      "tokens":[
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
      "count_tokens":2,
      "information": {
          "username": "User_-12345",
          "created_at": 1697560563,
          "ip": "127.0.0.1"
      }
    }
    ```

- ## Update `secret_code` or `backup_codes`
  - ### Request
  
  ```http
  PUT /v1/user/settings/auth/one_time_code?type=basic|backup
  ```
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | secret_string | string | [secret_string](#secret_string) | &#10003; | |

  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#user_auth_one_time_code_200) | | |
  | [UNAUTHORIZED](#401) | | |
  | [BAD REQUEST](#400) | | |
  | [INTERNAL_SERVER_ERROR](#user_auth_one_time_code_500) | | |

    ##### user_auth_one_time_code_200
    ```json
    {
      "msg": {
            "de": null,
            "en": "successfully updated",
            "ru": "успешно обновлено"
        }
      "data":"base32 string for TOTP client",
    }
    ```

    ##### user_auth_one_time_code_200
    ```json
    {
      "msg": {
            "de": null,
            "en": "successfully updated",
            "ru": "успешно обновлено"
        }
      "data":[534543,123456]
    }
    ```

- ## Delete User
  - ### Request
  
  ```http
  DELETE /v1/user/settings
  ```
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | login | string | the length is set in the configuration | &#10007; | |
  | secret_string | string | [secret_string](#secret_string) | &#10003; | |
  | code | string | the code consists of a 6-digit number, the code can be obtained in the TOTP client| &#10007; | |

  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#user_delete_200) | | |
  | [UNAUTHORIZED](#401) | | |
  | [BAD REQUEST](#400) | | |
  | [INTERNAL_SERVER_ERROR](#user_delete_500) | | |

    ##### user_delete_200
    ```json
    {
      "msg": {
            "de": null,
            "en": "the user has been successfully deleted",
            "ru": "пользователь успешно удален"
        }
    }
    ```
    
    ##### user_delete_500
    ```json
    {
      "msg": {
            "de": null,
            "en": "не удалось удалить пользователя",
            "ru": "failed to delete user"
        }
    }
    ```

- ## Update `secret_string`
  - ### Request
  
  ```http
  PUT /v1/user/settings/auth/secret_string
  ```
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/x-www-form-urlencoded |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | login | string | | &#10007; | |
  | old_secret_string | string | [secret_string](#secret_string) | &#10003; | |
  | new_secret_string | string | [secret_string](#secret_string) | &#10003; | |
  | code | string | the code consists of a 6-digit number, the code can be obtained in the TOTP client| &#10007; | |

  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#user_update_secret_string_200) | | |
  | [UNAUTHORIZED](#401) | | |
  | [BAD REQUEST](#400) | | |
  | [NOT_FOUND](#user_update_secret_string_404) | | |
  | [INTERNAL_SERVER_ERROR](#user_update_secret_string_500) | | |

    ##### user_update_secret_string_200
    ```json
    {
      "msg": {
            "de": null,
            "en": "successfully updated",
            "ru": "успешно обновлено"
        }
    }
    ```

    ##### user_update_secret_string_404
    ```json
    {
      "msg": {
            "de": null,
            "en": "failed to update",
            "ru": "не удалось обновить"
        }
    }
    ```
    
    ##### user_update_secret_string_500
    ```json
    {
      "msg": {
            "de": null,
            "en": "failed to update",
            "ru": "не удалось обновить"
        }
    }
    ```

## • Safe

- ## Create
  - ### Request
  
  ```http
  POST /v1/safe
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
  | description | string | description<=280  | [&#10003;](#Text) | |
  
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

- ## Update
  - ### Request
  
  ```http
  PUT /v1/safe/{safe_id}
  ```
  
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | safe_id | string | uuid v4 | &#10007; | |
  
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
  | description | string | description<=280 | [&#10003;](#Text) | |
  
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
  DELETE /v1/safe/{safe_id}
  ```
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | safe_id | string | uuid v4 | &#10007; | |

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
        "password_rule": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[\\W]).{8,64}$",
        "item_categories": [
            "LOGIN",
            "PASSWORD",
            "API_CREDENTIAL",
            "SERVER",
            "DATABASE",
            "CREDIT_CARD",
            "MEMBERSHIP",
            "PASSPORT",
            "SOFTWARE_LICENSE",
            "OUTDOOR_LICENSE",
            "SECURE_NOTE",
            "WIRELESS_ROUTER",
            "BANK_ACCOUNT",
            "DRIVER_LICENSE",
            "IDENTITY",
            "REWARD_PROGRAM",
            "DOCUMENT",
            "EMAIL_ACCOUNT",
            "SOCIAL_SECURITY_NUMBER",
            "MEDICAL_RECORD",
            "SSH_KEY"
        ],
        "item_types": [
            "STRING",
            "PASSWORD",
            "EMAIL",
            "CONCEALED",
            "URL",
            "OTP",
            "DATE",
            "MONTH_YEAR",
            "MENU",
            "FILE"
        ]
    }
    ```

## • Records

- ## Create
  - ### Request
  
  ```http
  POST /v1/safe/{safe_id}/item
  ```
  
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | safe_id | string | uuid v4 | &#10007; | |

  - Headers
  
  | key | value | Description |
  | - | - | - |
  | Content-Type | application/json | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  - ##### item_create
  ```json
  {
    "title":"Title",
    "category":"LOGIN",
    "notes":"There should be notes here",
    "tags":["the values in the tags must be of the string type","tag2"],
    "sections":[
      {
        "section":"INIT",
        "fields":[
          {
            "type":"STRING",
            "label":"login",
            "value":"user1"
          },
          {
            "type":"PASSWORD",
            "label":"password",
            "value":"12345"
          }
        ]
      },
      {
        "section":"Other sections",
        "fields":[
          {
            "type":"URL",
            "label":"title",
            "value":"https://example.com"
          },
          {
            "type":"EMAIL",
            "label":"email",
            "value":"user@example.com"
          }
        ]
      }
    ]
  }
  ```

  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | safe_id | string | UUID4, id of the safe in which the item will be recorded | &#10007; | |
  | title | string | The title of the item | &#10007; | |
  | category | string | The category of the item. One of: <br>• `"LOGIN"`<br>• `"PASSWORD"`<br>• `"SERVER"`<br>• `"DATABASE"`<br>• `"CREDIT_CARD"`<br>• `"MEMBERSHIP"`<br>• `"PASSPORT"`<br>• `"SOFTWARE_LICENSE"`<br>• `"OUTDOOR_LICENSE"`<br>• `"SECURE_NOTE"`<br>• `"WIRELESS_ROUTER"`<br>• `"BANK_ACCOUNT"`<br>• `"DRIVER_LICENSE"`<br>• `"IDENTITY"`<br>• `"REWARD_PROGRAM"`<br>• `"EMAIL_ACCOUNT"`<br>• `"SOCIAL_SECURITY_NUMBER"`<br>• `"MEDICAL_RECORD"`<br>• `"SSH_KEY"`, [can be found on request](#configuration__200) | &#10007; | |
  | notes | string | Notes of the item | [&#10003;](#Text) | |
  | tags | array | Tags of the item, the elements in the array must be of type string | &#10007; | |
  | sections | array | Stores objects in itself | &#10007; | |
  | section | string | The name of the section where the records are located. Attention! `"sections"` must contain at least one `"section"` with the `"INIT"` key, since `"INIT"` acts as the main section | &#10007; | |
  | fields | array | Contains objects with records | &#10007; | |
  | type | string | The category of the field. One of: <br>• `"STRING"`<br>• `"PASSWORD"`<br>• `"EMAIL"`<br>• `"CONCEALED"`<br>• `"URL"`<br>• `"OTP"`<br>• `"DATE"`<br>• `"MONTH_YEAR"`<br>• `"MENU"`<br>• `"FILE"`, [can be found on request](#configuration__200) | &#10007; | |
  | label | Label for the field |  | &#10007; | |
  | value | The value that is stored in the field |  | [&#10003;](#Text) | |

  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#item_create__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#item_create__500) | | |

    ##### item_create__200
    ```json
    {
      "msg": {
        "de": null,
        "en": "the item was successfully created",
        "ru": "элемент был успешно создан"
      }
    }
    ```
    
    ##### item_create__500
    ```json
    {
      "msg": {
        "de": null,
        "en": "failed to create item",
        "ru": "не удалось создать элемент"
      }
    }
    ```
    
- ## Get
  - ### Request
  
  ```http
  GET /v1/safe/all/item
  ```
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | all | string | selects all safes | &#10007; | |
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#records_get__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#500) | | |

    ##### records_get__200
    ```json
    {
        "safes": [
            {
                "id": "13a0d3c9-e48c-405c-844c-c6356f29d1d7",
                "name": "safe 1",
                "description": "descrip. 1",
                "created_at": 1695750016,
                "updated_at": 1695820640,
                "count_items": 1
            },
            {
                "id": "4607459b-404e-4048-b5d7-40ab296fc2bf",
                "name": "safe 2",
                "description": "descrip. 2",
                "created_at": 1695750022,
                "updated_at": 1695750154,
                "count_items": 2
            },
            {
                "id": "f8b67b11-dcc6-4c70-b2b0-5299beb0f43d",
                "name": "safe 3",
                "description": "descrip. 3",
                "created_at": 1695750025,
                "updated_at": 1695750196,
                "count_items": 3
            }
        ],
        "count": 3,
        "tags": [
            "the values in the tags must be of the string type",
            "tag2",
            "tag3",
            "tag65"
        ],
        "favorites": [
            "eaf7c608-f857-48ff-aec4-9cac14b15b4c",
            "cee5638a-5b33-4e57-90ab-0228d1935880"
        ],
        "list": [
            {
                "safe_id": "4607459b-404e-4048-b5d7-40ab296fc2bf",
                "count": 2,
                "items": [
                    {
                        "id": "b6637471-653e-4ab8-861f-5e029dc7a9bc",
                        "title": "Title",
                        "category": "LOGIN",
                        "notes": "There should be notes here",
                        "tags": [
                            "the values in the tags must be of the string type",
                            "tag2"
                        ],
                        "favorite": false,
                        "sections": [
                            {
                                "section": "INIT",
                                "fields": [
                                    {
                                        "type": "STRING",
                                        "label": "login",
                                        "value": "user1"
                                    },
                                    {
                                        "type": "PASSWORD",
                                        "label": "password",
                                        "value": "12345"
                                    }
                                ]
                            },
                            {
                                "section": "Other sections",
                                "fields": [
                                    {
                                        "type": "URL",
                                        "label": "title",
                                        "value": "https://example.com"
                                    },
                                    {
                                        "type": "EMAIL",
                                        "label": "email",
                                        "value": "user@example.com"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "20d9a8c6-5da6-4df1-92c5-defb025e35a9",
                        "title": "Title 2",
                        "category": "LOGIN",
                        "notes": "There should be notes here",
                        "tags": [
                            "the values in the tags must be of the string type",
                            "tag2"
                        ],
                        "favorite": false,
                        "sections": [
                            {
                                "section": "INIT",
                                "fields": [
                                    {
                                        "type": "STRING",
                                        "label": "login",
                                        "value": "user1"
                                    },
                                    {
                                        "type": "PASSWORD",
                                        "label": "password",
                                        "value": "12345"
                                    }
                                ]
                            },
                            {
                                "section": "Other sections 2",
                                "fields": [
                                    {
                                        "type": "URL",
                                        "label": "title",
                                        "value": "https://example.com"
                                    },
                                    {
                                        "type": "EMAIL",
                                        "label": "email",
                                        "value": "user@example.com"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "safe_id": "f8b67b11-dcc6-4c70-b2b0-5299beb0f43d",
                "count": 3,
                "items": [
                    {
                        "id": "75622f14-adbd-4a23-b374-2ce9cbb7291b",
                        "title": "Title mew",
                        "category": "LOGIN",
                        "notes": "There should be notes here",
                        "tags": [
                            "the values in the tags must be of the string type",
                            "tag2"
                        ],
                        "favorite": false,
                        "sections": [
                            {
                                "section": "INIT",
                                "fields": [
                                    {
                                        "type": "STRING",
                                        "label": "login",
                                        "value": "user1"
                                    },
                                    {
                                        "type": "PASSWORD",
                                        "label": "password",
                                        "value": "12345"
                                    }
                                ]
                            },
                            {
                                "section": "Other sections f",
                                "fields": [
                                    {
                                        "type": "URL",
                                        "label": "title",
                                        "value": "https://example.com"
                                    },
                                    {
                                        "type": "EMAIL",
                                        "label": "email",
                                        "value": "user@example.com"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "86057143-8e30-40c8-aa4d-887a48920cef",
                        "title": "Title mew",
                        "category": "LOGIN",
                        "notes": "There should be notes here",
                        "tags": [
                            "the values in the tags must be of the string type",
                            "tag2"
                        ],
                        "favorite": false,
                        "sections": [
                            {
                                "section": "INIT",
                                "fields": [
                                    {
                                        "type": "STRING",
                                        "label": "login",
                                        "value": "user1"
                                    },
                                    {
                                        "type": "PASSWORD",
                                        "label": "password",
                                        "value": "12345"
                                    }
                                ]
                            },
                            {
                                "section": "Other sections f",
                                "fields": [
                                    {
                                        "type": "URL",
                                        "label": "title",
                                        "value": "https://example.com"
                                    },
                                    {
                                        "type": "EMAIL",
                                        "label": "email",
                                        "value": "user@example.com"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "cee5638a-5b33-4e57-90ab-0228d1935880",
                        "title": "Title mew",
                        "category": "LOGIN",
                        "notes": "There should be notes here",
                        "tags": [
                            "the values in the tags must be of the string type",
                            "tag2"
                        ],
                        "favorite": true,
                        "sections": [
                            {
                                "section": "INIT",
                                "fields": [
                                    {
                                        "type": "STRING",
                                        "label": "login",
                                        "value": "user1"
                                    },
                                    {
                                        "type": "PASSWORD",
                                        "label": "password",
                                        "value": "12345"
                                    }
                                ]
                            },
                            {
                                "section": "Other sections f",
                                "fields": [
                                    {
                                        "type": "URL",
                                        "label": "title",
                                        "value": "https://example.com"
                                    },
                                    {
                                        "type": "EMAIL",
                                        "label": "email",
                                        "value": "user@example.com"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "safe_id": "13a0d3c9-e48c-405c-844c-c6356f29d1d7",
                "count": 1,
                "items": [
                    {
                        "id": "eaf7c608-f857-48ff-aec4-9cac14b15b4c",
                        "title": "Title mew",
                        "category": "LOGIN",
                        "notes": "There should be notes here",
                        "tags": [
                            "tag3",
                            "tag65"
                        ],
                        "favorite": true,
                        "sections": [
                            {
                                "section": "INIT",
                                "fields": [
                                    {
                                        "type": "STRING",
                                        "label": "login",
                                        "value": "user1"
                                    },
                                    {
                                        "type": "PASSWORD",
                                        "label": "password",
                                        "value": "12345"
                                    }
                                ]
                            },
                            {
                                "section": "Other sections f",
                                "fields": [
                                    {
                                        "type": "URL",
                                        "label": "title",
                                        "value": "https://example.com"
                                    },
                                    {
                                        "type": "EMAIL",
                                        "label": "email",
                                        "value": "user@example.com"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | list | array | Contains an array with items distributed across safes | &#10007; | |
  | items | array | [A description of the other parameters can be found here](#item_create) | &#10007; | |
  | id | string | UUID4, "id" is the item ID | &#10007; | |
  | count | int | number of safes | &#10007; | |
  | list[N].count | int | number of items in the safe | &#10007; | |
  | favorite | bool | indicates whether an item is a favorite] | &#10007; | |
  | favorites | array | contains all the UUIDs of favorites from all the safes | &#10007; | |
  | tags | array | shows all existing tags | &#10007; | |
  | safes | array | contain information about safes | &#10007; | |

- ## Move
  - ### Request
  
  ```http
  PUT /v1/safe/{from}/{to}/item/{item_id}
  ```
  
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | from | string | uuid v4, `id` of the safe from which to move the items | &#10007; | |
  | to | string | uuid v4, `id` of the safe to move the items to | &#10007; | |
  | item_id | string | uuid v4, the `id` of the item you want to move | &#10007; | |
  
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
  | [OK](#safe_move__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#safe_move__500) | | |

    ##### safe_move__200
    ```json
    {
      "msg": {
            "de": null,
            "en": "the item was successfully moved to the safe",
            "ru": "элемент был успешно перемещен в сейф"
        },
    }
    ```

    ##### safe_move__500
    ```json
    {
        "msg": {
            "de": null,
            "en": "failed to move item to safe",
            "ru": "не удалось переместить элемент в сейф"
        }
    }
    ```

- ## Set favorite
  - ### Request
  
  ```http
  PUT /v1/safe/{safe_id}/item/{item_id}/favorite
  ```
  
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | safe_id | string | uuid v4, id of the safe that contains the item | &#10007; | |
  | item_id | string | uuid v4, id of the item to be changed in the safe | &#10007; | |
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Content-Type | application/json | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#item_favorite__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#item_favorite__500) | | |

    ##### item_favorite__200
    ```json
    {
      "msg": {
        "de": null,
        "en": "the item was successfully added to favorites",
        "ru": "элемент успешно добавлен в избранное"
      }
    }
    ```

    ##### item_favorite__500
    ```json
    {
      "msg": {
        "de": null,
        "en": "couldn't add item to favorites",
        "ru": "не удалось добавить элемент в избранное"
      }
    }
    ```

- ## Update
  - ### Request
  
  ```http
  PUT /v1/safe/{safe_id}/item/{item_id}
  ```
  
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | safe_id | string | uuid v4, id of the safe that contains the item | &#10007; | |
  | item_id | string | uuid v4, id of the item to be changed in the safe | &#10007; | |
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Content-Type | application/json | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | body | object | [the request body is the same as when it was created](#item_create) | |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#item_update__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#item_update__500) | | |

    ##### item_update__200
    ```json
    {
      "msg": {
        "de": null,
        "en": "the item was successfully updated",
        "ru": "элемент был успешно обновлен"
      }
    }
    ```

    ##### item_update__500
    ```json
    {
      "msg": {
        "de": null,
        "en": "failed to update the item",
        "ru": "не удалось обновить элемент"
      }
    }
    ```

- ## Delete
  - ### Request
  
  ```http
  DELETE /v1/safe/{safe_id}/item/{item_id}
  ```
  
  - Params
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  | safe_id | string | uuid v4, id of the safe that contains the item | &#10007; | |
  | item_id | string | uuid v4, id of the item to be changed in the safe | &#10007; | |
  
  - Headers
  
  | key | value | Description |
  | - | - | - |
  | User-Agent | Chromium/100.0.0 or <Сlient name>/&lt;Version> |  | |
  | Authorization | Bearer &lt;token> |  | |
  
  - Body
  
  | Parameters | Type | Description | Encrypt |
  | - | - | - | - |
  
  - ### Responses

  | Status code | Description |
  | - | - |
  | [OK](#item_delete__200) | | |
  | [BAD REQUEST](#400) | | |
  | [UNAUTHORIZED](#401) | | |
  | [INTERNAL_SERVER_ERROR](#item_delete__500) | | |

    ##### item_delete__200
    ```json
    {
      "msg": {
        "de": null,
        "en": "the item was successfully deleted",
        "ru": "элемент был успешно удален"
      }
    }
    ```

    ##### item_delete__500
    ```json
    {
      "msg": {
        "de": null,
        "en": "не удалось удалить элемент",
        "ru": "failed to delete item"
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
  ### *403*
  ```json
  {
    "msg": {
      "de": null,
      "en": "отказано в доступе",
      "ru": "access denied"
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

- #### uuid  = UUIDv4 (stored only on the client, !the uuid must be without hyphens!)
- #### password = @mV3?fsf43vvewqf (must match a [regular expression "authentication.password_rule"](#configuration__200))

### secret_string
```python
length = 128
sha256(login|password|uuid)
```

- #### iterations = 100000 ([can be obtained from the response "authentication.pbkdf2.iterations"](#configuration__200)) *(Abandoned)*
- #### mode = "GCM" ([can be obtained from the response "authentication.aes256.mode"](#configuration__200))

## Text
```python
private_key = PBKDF2(password, salt = uuid, iterations = 10000, length = 32)
ciphertext = aes256_encrypt(text, private_key, mode)
  #!!!attention, 1 character in unencrypted form is equal to 2 in encrypted!!!
  return (iv(32 bytes).hex+cyphertext.hex+tag(32 bytes).hex).to_string() = "e60c203ae89b8ec4cc3d4917..."
decrypt_text = aes256_decrypt(ciphertext.fromhex, private_key, mode)
```
