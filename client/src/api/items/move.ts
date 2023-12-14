import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../api";

export class APIMoveItem {
    private token: string;
  
    constructor(token: string) {
        this.token = token;
    }
  
    public async execute(from: string, to: string, item_id: string): Promise<any> {
        return new Promise((resolve, reject) => {
            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
            };
            
            api.put(
                `${api_v1_safe}/${from}/${to}/item/${item_id}`,
                null,
                {
                    headers: headers,
                }
            )
            .then((response: any) => {
                resolve(response);
            })
            .catch((error) => {
                reject(error.response);
            });
        });
    }
}
