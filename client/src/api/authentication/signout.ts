import { Headers } from "@/types/global";
import { api, api_v1_auth_sign_out } from "../api";

export class APISignOut {
    private token: string
    private token_id: string
  
    constructor(token: string, token_id: string) {
        this.token = token;
        this.token_id = token_id;
    }
  
      public async execute(): Promise<any> {
          return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${this.token}`
            }
  
            api.delete(`${api_v1_auth_sign_out}/${this.token_id}`, {
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