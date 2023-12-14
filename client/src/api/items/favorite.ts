import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../api";

export class APIFavorite {
    private token: string;

    constructor(token: string) {
        this.token = token;
    }

    public async execute(safe_id: string, item_id: string): Promise<any> {
        try {
            const headers: Headers = {
                'Authorization': `Bearer ${this.token}`,
            };

            // Assuming an empty object {} as the request body
            const response = await api.put(`${api_v1_safe}/${safe_id}/item/${item_id}/favorite`, {}, { headers });

            return response.data; // Assuming you want to return the data from the response
        } catch (error: any) {
            throw error.response || error; // Throw the response if available, otherwise throw the error
        }
    }
}
