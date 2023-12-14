import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../api";

export class APIGetAllItems {
    private token: string
  
    constructor(token: string) {
        this.token = token;
    }
  
      public async execute(): Promise<any> {
          return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`
            }
            console.log(headers)
            api.get(`${api_v1_safe}/all/item`, {
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