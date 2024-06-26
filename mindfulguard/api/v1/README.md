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
| [Service Unavailable](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [CONFLICT](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

##### sign_up__200

```json
{
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
| Device | App name version/Device name Version |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| login | string | the length is set in the configuration | &#10007; | |
| secret_string | string | [secret_string](#secret_string) | &#10003; | |
| expiration | int64 | 1 < expiration <= 129600 (90 days), measured in minutes | &#10007; | |
| code | string | the code consists of a 6-digit number, the code can be obtained in the TOTP client or from a backup code | &#10007; | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#sign_in__200) | | |
| [BAD REQUEST](#response-template) | | |
| [NOT_FOUND](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

##### sign_in__200

```json
{
    "token": "b888...length128"
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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [NOT_FOUND](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

## • Administrator

- ## Users Information

- ### Request

```http
GET /v1/admin/users/all?page=1|2|3,...&per_page=2

```

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | application/x-www-form-urlencoded |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Query

| Parameter | Description | Required |
| - | - | - |
| page | Default value 1. | &#10007; |
| per_page | The number of items per page to be returned in the response. Default value 5. | &#10007; |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#admin_get_all_users_200) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [FORBIDDEN](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

##### admin_get_all_users_200

```json
{
    "page": 1,
    "items_per_page": 2,
    "total_pages": 1,
    "total_users": 2,
    "total_storage_size": 0,
    "list": [
        {
            "id": "09c14580-b69e-4292-8a1a-4e88256bd6a3",
            "username": "User423_-",
            "ip": "127.0.0.1",
            "confirm": true,
            "created_at": 1697796126
        },
        {
            "id": "648ac8c5-2c6f-45a8-a855-fa1d0857598c",
            "username": "UFser423534_-",
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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| value | string | | &#10007; | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#admin_search_users_200) | | |
| [NOT_FOUND](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [FORBIDDEN](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

##### admin_search_users_200

```json
{
    "id": "91ac1500-7567-4021-b87a-156f79c45281",
    "username": "User_-12345",
    "ip": "127.0.0.1",
    "confirm": true,
    "created_at": 1698245381
}
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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#admin_get_settings_200) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [FORBIDDEN](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
    "registration": true,
    "scan_time_routines_tokens": 60,
    "scan_time_routines_users": 60,
    "confirmation_period": 604800,
    "disk_space_per_user": 1073741824
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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| value | string |  | &#10007; |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [FORBIDDEN](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

- ## Creating a user by an administrator

- ### Request

```http
POST /v1/admin/users
```

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | application/x-www-form-urlencoded |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#sign_up__200) | | |
| [Service Unavailable](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [CONFLICT](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [FORBIDDEN](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

- ## Delete User

- ### Request

```http
DELETE /v1/admin/users?id=<uuid.v4>
```

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | application/x-www-form-urlencoded |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#user_delete_200) | | |
| [UNAUTHORIZED](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [FORBIDDEN](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#user_info_200) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

##### user_info_200

```json
{
  "tokens":[
    {
      "id": "25275093-aa91-4937-941c-1934e0174d2e",
      "short_hash": "ectcxizeku8nzywkc1j2b7asyok8",
      "first_login": 1695004570,
      "last_login": 1695004570,
      "device": "Chromium/100.0.0 or <Сlient name>/<Version>",
      "last_ip": "127.0.0.1",
      "expiration": 1695004570
    },
    {
      "id": "188da897-a032-4747-bbc7-99c078dd539b",
      "short_hash": "ysvuebx7du1tqfpjietuiyrqml31",
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

| Key | Description |
| --- | ----------- |
| short_hash | The first 28 characters of the token hash `sha256`. |

## • Audit

- ## Get 
- ### Request

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | application/x-www-form-urlencoded |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

```http
GET /v1/user/audit?page=1&per_page=4
```

- Query

| Parameter | Description | Required |
| - | - | - |
| page | Default value 1. | &#10007; |
| per_page | The number of items per page to be returned in the response. Default value 5. | &#10007; |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#user_info_200) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |

```json
{
    "page": 1,
    "total_pages": 1,
    "items_per_page": 4,
    "total_items": 7,
    "list": [
        {
            "id": "e1a85d45-f653-43f6-ba69-fce3124a94d1",
            "created_at": 1709723982,
            "ip": "127.0.0.1",
            "object": "safe",
            "action": "delete",
            "device": "Chromium/100.0.0"
        },
        {
            "id": "5f93cdc3-6ca0-4020-93b3-2e81611ee401",
            "created_at": 1709723960,
            "ip": "127.0.0.1",
            "object": "item",
            "action": "create",
            "device": "Chromium/100.0.0"
        },
        {
            "id": "ca5c4765-8372-493c-9965-61d16d44ccf6",
            "created_at": 1709723952,
            "ip": "127.0.0.1",
            "object": "safe",
            "action": "create",
            "device": "Chromium/100.0.0"
        },
        {
            "id": "3762ed22-f407-4eae-b788-8f1f39072190",
            "created_at": 1709723915,
            "ip": "127.0.0.1",
            "object": "user",
            "action": "sign_in",
            "device": "Chromium/100.0.0"
        }
    ]
}
```

| key | Description |
| --- | ----------- |
| page | Current page. |
| total_pages | Total number of pages. |
| items_per_page | The number of items_per_page contained on a single page. |
| total_items | Total number of items. |
| list.object | Object on which the operation is performed. |
| list.action | Name of action. |

- ## Update `secret_code` or `backup_codes`

- ### Request

```http
PUT /v1/user/settings/auth/one_time_code?type=basic|backup
```

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | application/x-www-form-urlencoded |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| secret_string | string | [secret_string](#secret_string) | &#10003; | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#user_auth_one_time_code_200) | | |
| [UNAUTHORIZED](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

##### user_auth_one_time_code_200

```json
{
  "data":"base32 string for TOTP client",
}

```

##### user_auth_one_time_code_200

```json
{
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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| secret_string | string | [secret_string](#secret_string) | &#10003; | |
| code | string | the code consists of a 6-digit number, the code can be obtained in the TOTP client| &#10007; | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

- ## Update `secret_string`

- ### Request

```http
PUT /v1/user/settings/auth/secret_string
```

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | application/x-www-form-urlencoded |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| old_secret_string | string | [secret_string](#secret_string) | &#10003; | |
| new_secret_string | string | [secret_string](#secret_string) | &#10003; | |
| code | string | the code consists of a 6-digit number, the code can be obtained in the TOTP client| &#10007; | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | All access tokens will be deleted. | |
| [UNAUTHORIZED](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [NOT_FOUND](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| name | string | the length is specified in the configuration | &#10007; | |
| description | string | description<=280  | [&#10003;](#Text) | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| name | string | the length is specified in the configuration | &#10007; | |
| description | string | description<=280 | [&#10003;](#Text) | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [NOT FOUND](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
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
| category | string | The category of the item. One of: • `"LOGIN"`• `"PASSWORD"`• `"SERVER"`• `"DATABASE"`• `"CREDIT_CARD"`• `"MEMBERSHIP"`• `"PASSPORT"`• `"SOFTWARE_LICENSE"`• `"OUTDOOR_LICENSE"`• `"SECURE_NOTE"`• `"WIRELESS_ROUTER"`• `"BANK_ACCOUNT"`• `"DRIVER_LICENSE"`• `"IDENTITY"`• `"REWARD_PROGRAM"`• `"EMAIL_ACCOUNT"`• `"SOCIAL_SECURITY_NUMBER"`• `"MEDICAL_RECORD"`• `"SSH_KEY"`, [can be found on request](#configuration__200) | &#10007; | |
| notes | string | Notes of the item | [&#10003;](#Text) | |
| tags | array | Tags of the item, the elements in the array must be of type string | &#10007; | |
| sections | array | Stores objects in itself | &#10007; | |
| section | string | The name of the section where the records are located. Attention! `"sections"` must contain at least one `"section"` with the `"INIT"` key, since `"INIT"` acts as the main section | &#10007; | |
| fields | array | Contains objects with records | &#10007; | |
| type | string | The category of the field. One of: • `"STRING"`• `"PASSWORD"`• `"EMAIL"`• `"CONCEALED"`• `"URL"`• `"OTP"`• `"DATE"`• `"MONTH_YEAR"`• `"MENU"`• `"FILE"`, [can be found on request](#configuration__200) | &#10007; | |
| label | Label for the field |  | &#10007; | |
| value | The value that is stored in the field |  | [&#10003;](#Text) | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#records_get__200) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
                    ],
                    "created_at": 1707839150,
                    "updated_at": 1707839196
                },
                {
                    "id": "20d9a8c6-5da6-4df1-92c5-defb025e35a9",
                    "title": "Title 22",
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
                    ],
                    "created_at": 1707839150,
                    "updated_at": 1707839196
                }
            ]
        },
        {
            "safe_id": "f8b67b11-dcc6-4c70-b2b0-5299beb0f43d",
            "count": 3,
            "items": [
                {
                    "id": "75622f14-adbd-4a23-b374-2ce9cbb7291b",
                    "title": "Title 44",
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
                            "section": "Other sections 4",
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
                    ],
                    "created_at": 1707839150,
                    "updated_at": 1707839196
                },
                {
                    "id": "86057143-8e30-40c8-aa4d-887a48920cef",
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
                    ],
                    "created_at": 1707839150,
                    "updated_at": 1707839196
                },
                {
                    "id": "cee5638a-5b33-4e57-90ab-0228d1935880",
                    "title": "Title 3",
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
                            "section": "Other sections 3",
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
                    ],
                    "created_at": 1707839150,
                    "updated_at": 1707839196
                }
            ]
        },
        {
            "safe_id": "13a0d3c9-e48c-405c-844c-c6356f29d1d7",
            "count": 1,
            "items": [
                {
                    "id": "eaf7c608-f857-48ff-aec4-9cac14b15b4c",
                    "title": "Title 4",
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
                    ],
                    "created_at": 1707839150,
                    "updated_at": 1707839196
                }
            ]
        }
    ],
    "disk": {
        "total_space": 1073741824,
        "filled_space": 2543
    },
    "files": [
        {
            "safe_id": "5e3965f0-b21f-45bf-a824-fdeee57a7f21",
            "objects": [
                {
                    "id":"aadf327c8267c09d6fffd87a1a80ad3c798469ff332b7a57b9e8c045d46b2af7",
                    "content_path": "safe/5e3965f0-b21f-45bf-a824-fdeee57a7f21/aadf327c8267c09d6fffd87a1a80ad3c798469ff332b7a57b9e8c045d46b2af7/content",
                    "name": "file.txt",
                    "updated_at": 1698693022,
                    "size": 2543
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
| disk | object | contains information about the user's file storage, values are in `bytes` | &#10007; | |
| files | array | contains information about files | &#10007; | |
| safe_id | string | `uuid` of the safe containing the file | &#10007; | |

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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Content-Type | application/json | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Content-Type | application/json | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| body | object | [the request body is the same as when it was created](#item_create) | |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

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
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

| Status code | Description |
| - | - |
| [OK](#response-template) | | |
| [BAD REQUEST](#response-template) | | |
| [UNAUTHORIZED](#response-template) | | |
| [INTERNAL_SERVER_ERROR](#response-template) | | |

## • Files

- ## Upload Files

- ### Request

```http
POST /v1/safe/<safe_id>/content
```

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | multipart/form-data |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| files | file (bytes) | The file name must consist only of characters that are contained in ASCII encoding. | &#10007; | |

- ### Responses

**!!!ATTENTION RESPONSES RETURN ONLY CODE STATUS!!!**

| Status code | Description |
| - | - |
| OK | | |
| BAD REQUEST | | |
| UNAUTHORIZED | | |
| INTERNAL_SERVER_ERROR | | |

- ## Download File

- ### Request

```http
GET /v1/safe/<safe_id>/<file_name>/content
```

[__find out the path to the content here__](#records_get__200)

- Headers

| key | value | Description |
| - | - | - |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body

| Parameters | Type | Description | Encrypt |
| - | - | - | - |

- ### Responses

**!!!ATTENTION RESPONSES RETURN ONLY CODE STATUS OR FILE!!!**

| Status code | Description |
| - | - |
| OK | | |
| BAD REQUEST | | |
| UNAUTHORIZED | | |
| INTERNAL_SERVER_ERROR | | |

- ## Delete Files

- ### Request

```http
DELETE /v1/safe/<safe_id>/content
```

[__all the information you need can be found here__](#records_get__200)

- Headers

| key | value | Description |
| - | - | - |
| Content-Type | application/x-www-form-urlencoded |  | |
| Device | App name version/Device name Version |  | |
| Authorization | Bearer &lt;token> |  | |

- Body
   **!!!ATTENTION "FILES" IS AN ARRAY!!!**

| Parameters | Type | Description | Encrypt |
| - | - | - | - |
| files | string | | &#10007; | |
| files | string | | &#10007; | |
| files | string | | &#10007; | |
| files | string | | &#10007; | |
| files | string | | &#10007; | |

- ### Responses

**!!!ATTENTION RESPONSES RETURN ONLY CODE STATUS!!!**

| Status code | Description |
| - | - |
| OK | | |
| BAD REQUEST | | |
| UNAUTHORIZED | | |
| NOT_FOUND | | |
| INTERNAL_SERVER_ERROR | | |

## • JSON Responses

### Response Template.

```json
{
  "status_code": int
  "description": string
}
```

### *Example.*
```json
{
  "status_code": 200
  "description": "OK"
}
```

### **All http protocol responses can be seen [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).**

# Encryption

## **The "Encryption" section explains how the client should encrypt the data.**

- #### privateKey  = UUIDv4 (stored only on the client, !the uuid must be without hyphens!)

- #### password = @mV3?fsf43vvewqf (must match a [regular expression "authentication.password_rule"](#configuration__200))

### secret_string

```python
length = 128
sha256(login|password|privateKey)
```

- #### iterations = 10000

- #### mode = "GCM"

## Text

```python
cypherKey = PBKDF2(password, salt = privateKey, iterations, length = 32)
ciphertext = aes256_encrypt(text, cypherKey, mode) = (iv(16 bytes)+cyphertext+tag(16 bytes)).hex_encode() = "e60c203ae89b8ec4cc3d4917..."
decrypt_text = aes256_decrypt(ciphertext.hex_decode(), cypherKey, mode)
```
