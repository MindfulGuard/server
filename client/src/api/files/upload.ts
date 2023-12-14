import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../api";

export class APIFileUpload {
    private token: string;

    constructor(token: string) {
        this.token = token;
    }

    public async execute(safe_id: string, file: File, config?: any): Promise<any> {
        return new Promise((resolve, reject) => {
            let formData = new FormData();
            formData.append('files', file);

            let headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'multipart/form-data'
            };

            api.post(`${api_v1_safe}/${safe_id}/content`, formData, {
                headers: headers,
                ...config, // Pass the provided config object
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
