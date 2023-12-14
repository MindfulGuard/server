import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../api";

export class APIFileDelete{
    private token: string
  
    constructor(token: string) {
        this.token = token;
    }
  
      public async execute(safe_id: string, file_id: string): Promise<any> {
          return new Promise((resolve, reject) => {
            let formData = new FormData();
            formData.append('files', file_id);

            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            };

            api.delete(`${api_v1_safe}/${safe_id}/content`, {
                data: formData,
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