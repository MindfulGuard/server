import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../../api";

export class APISafeCreate {
    private token: string
    private name: string
    private description: string
  
    constructor(token: string, name: string, description: string) {
        this.token = token;
        this.name = name;
        this.description = description;
    }
  
      public async execute(): Promise<any> {
          return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            let body: Safe = {
                name: this.name,
                description: this.description
            }
            const params: string = new URLSearchParams(Object.entries(body)).toString();
            console.log(headers)
            api.post(`${api_v1_safe}`,
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