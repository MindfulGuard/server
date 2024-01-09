import { Headers } from "@/types/global";
import { api, api_v1_user } from "../api";
import { secret_string } from "@/security/security";

export class APIUserUpdateSecretString{
    private token: string
    private login: string
    private old_secret_string: string
    private new_secret_string: string
    private private_string: string
    private one_time_code: string
  
    constructor(token: string, login: string, old_secret_string: string, private_string: string, new_secret_string: string, one_time_code: string) {
        this.token = token;
        this.login = login
        this.old_secret_string = old_secret_string;
        this.private_string = private_string
        this.new_secret_string = new_secret_string
        this.one_time_code = one_time_code
    }
  
      public async execute(): Promise<any> {
          return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            let body = {
                old_secret_string: secret_string(this.login, this.old_secret_string, this.private_string),
                new_secret_string: secret_string(this.login, this.new_secret_string, this.private_string),
                code: this.one_time_code
            }
            const params: string = new URLSearchParams(Object.entries(body)).toString();
            console.log(headers)
            api.put(`${api_v1_user}/settings/auth/secret_string`,
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