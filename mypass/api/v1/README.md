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
  | secret_string | string | length 128 | |
  
  - ### Response
  
  ```json
  {
    "msg": {
          "de": null,
          "en": "registration was successful",
          "ru": "регистрация прошла успешно"
      },
      "secret_code": "base32 string",
      "reserve_codes": [
          111111,
          222222,
          333333,
      ]
  }
  ```
