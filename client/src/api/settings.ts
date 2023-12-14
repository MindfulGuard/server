import { api, api_v1_public_configuration } from "./api";

export class APISettings{
    public get response(): Promise<any> {
        return new Promise((resolve, reject) => {
            api.get(api_v1_public_configuration)
                .then((response: any) => {
                resolve(response);
                })
                .catch((error) => {
                reject(error.response);
            });
        });
    }
}
