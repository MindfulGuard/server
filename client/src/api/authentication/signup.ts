import { api, api_v1_auth_sign_up } from "../api";
import { UserSignup } from "@/types/userType";
import { Headers } from "@/types/global";
import { secret_string } from "@/security/security";

export class APISignUp {
  private login: string;
  private password: string;
  private uuid: string;

  constructor(login: string, password: string, uuid: any) {
    this.login = login;
    this.password = password;
    this.uuid = uuid;
  }

    public async execute(): Promise<any> {
        return new Promise((resolve, reject) => {

            let userData: UserSignup = {
                login: this.login,
                secret_string: secret_string(this.login, this.password, this.uuid),
            };
            let headers: Headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            const params: string = new URLSearchParams(Object.entries(userData)).toString();

            api.post(api_v1_auth_sign_up, params, {
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
