import { Headers } from "@/types/global";
import { api, api_v1_user } from "../api";
import { secret_string } from "@/security/security";

export class APIUserUpdateSecretOrBackupCode{
    private token: string
    private login: string
    private secret_string: string
    private private_string: string
  
    constructor(token: string, login: string, secret_string: string, private_string: string) {
        this.token = token;
        this.login = login
        this.secret_string = secret_string;
        this.private_string = private_string
    }
  
      public async execute(code_type: 'basic' | 'backup'): Promise<any> {
          return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            let body = {
                secret_string: secret_string(this.login, this.secret_string, this.private_string),
            }
            const params: string = new URLSearchParams(Object.entries(body)).toString();
            console.log(headers)
            api.put(`${api_v1_user}/settings/auth/one_time_code?type=${code_type}`,
                params,
                {
                headers: headers,
                })
                .then((response: any) => {
                resolve(response);
                })
                .catch((error) => {
                reject(error.response);
            });
        });
    }
}