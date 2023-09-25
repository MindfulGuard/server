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
    
- ## Get
  - ### Request
  
  ```http
  GET /v1/safe
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
        "authentication": {
            "pbkdf2": {
                "SHA": "sha256",
                "iterations": 10000
            },
            "aes256": {
                "mode": "GCM"
            },
            "password_rule": "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[\\W]).{8,64}$"
        },
        "item": {
            "categories": [
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
            "types": [
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
      "tags":["tag1","tag2","tag3"],
      "favorite":["20228d77-5364-4390-aea7-63bc7d61edfe"],
      "count":2,
      "list":[
        {
          "count":2,
          "safe_id":"df81795d-d39c-4c82-9067-3bb0503847a1",
          "items":[
            {
              "id":"6fff7323-3606-4e2f-8b7e-f0820243f8a0",
              "title":"Title",
              "category":"LOGIN",
              "notes":"There should be notes here",
              "tags":["the values in the tags must be of the string type","tag2"],
              "favorite":false,
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
            },
            {
              "id":"20228d77-5364-4390-aea7-63bc7d61edfe",
              "title":"Title2",
              "category":"LOGIN",
              "notes":"There should be notes here",
              "tags":["the values in the tags must be of the string type","tag2"],
              "favorite":true,
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
          ]
        },
        {
          "count":1,
          "safe_id":"fd2bc249-c560-49b8-b801-3c8b604825a4",
          "items":[
            {
              "id":"5d9aa22d-2797-46d6-b8b7-7c30c3e5a024",
              "title":"Title2",
              "category":"LOGIN",
              "notes":"There should be notes here 2",
              "tags":["the values in the tags must be of the string type","tag2","tag3"],
              "favorite":false,
              "sections":[
                {
                  "section":"INIT",
                  "fields":[
                    {
                      "type":"STRING",
                      "label":"login",
                      "value":"user2"
                    },
                    {
                      "type":"PASSWORD",
                      "label":"password",
                      "value":"123456"
                    }
                  ]
                },
                {
                  "section":"Other sections",
                  "fields":[
                    {
                      "type":"URL",
                      "label":"title",
                      "value":"https://example2.com"
                    },
                    {
                      "type":"EMAIL",
                      "label":"email",
                      "value":"user2@example2.com"
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
  | favorite | array | contains all the UUIDs of favorites from all the safes | &#10007; | |
  | tags | array | shows all existing tags | &#10007; | |

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
      "msg": "ok"
    }
    ```

    ##### item_favorite__500
    ```json
    {
      "msg": {
        "de": null,
        "en": "failed to update favorite",
        "ru": "не удалось обновить фаворита"
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
- #### mode = "" ([can be obtained from the response "authentication.aes256.mode"](#configuration__200))

## Text
```python
private_key = PBKDF2(password, salt = uuid, iterations = 10000, length = 32)
ciphertext = aes256_encrypt(text, private_key, mode)
  #!!!attention, 1 character in unencrypted form is equal to 2 in encrypted!!!
  return (iv(32 bytes).hex+cyphertext.hex+tag(32 bytes).hex).to_string() = "e60c203ae89b8ec4cc3d4917..."
decrypt_text = aes256_decrypt(ciphertext.fromhex, private_key, mode)
```
