import { Headers } from "@/types/global";
import { api, api_v1_user } from "../api";

export class APIUserGet {
    private token: string;
  
    constructor(token: string) {
        this.token = token;
    }

    public async execute(): Promise<any> {
        return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Authorization':`Bearer ${this.token}`,
            }
  
            api.get(api_v1_user, {
                headers: headers,
                })
                .then((response: any) => {
                resolve(response);
                })
                .catch((error :any) => {
                reject(error.response);
            });
          });
      }
  }