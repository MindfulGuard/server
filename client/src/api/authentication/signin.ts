import { UserSignin } from "@/types/userType";
import { api, api_v1_auth_sign_in_backup, api_v1_auth_sign_in_basic } from "../api";
import { secret_string } from "@/security/security";
import { Headers } from "@/types/global";

export class APISignIn{
    private login: string;
    private password: string;
    private uuid: string;
    private one_time_code: string;
    private expiration: string;
    private user_agent: string;

    constructor(login: string, password: string, uuid: any, one_time_code: string, expiration: string, user_agent: string) {
        this.login = login;
        this.password = password;
        this.uuid = uuid;
        this.one_time_code = one_time_code;
        this.expiration = expiration;
        this.user_agent = user_agent;
    }

    public execute(one_time_code_type: string|'basic'|'backup'): Promise<any>{
        return new Promise((resolve, reject) => {

            let userData: UserSignin = {
                login: this.login,
                secret_string: secret_string(this.login, this.password, this.uuid),
                expiration: this.expiration,
                code: this.one_time_code
            };
            
            let headers: Headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            };
            
            let api_path:string = one_time_code_type == 'backup'?api_v1_auth_sign_in_backup:api_v1_auth_sign_in_basic;
            const params: string = new URLSearchParams(Object.entries(userData)).toString();
            console.log(this.user_agent);
            api.post(api_path, params, {
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