import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../../api";

export class APISafeDelete{
    private token: string
  
    constructor(token: string) {
        this.token = token;
    }
  
      public async execute(safe_id: string): Promise<any> {
          return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            api.delete(`${api_v1_safe}/${safe_id}`,
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