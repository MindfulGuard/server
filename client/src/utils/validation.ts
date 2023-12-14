import { APISettings } from "@/api/settings";

export class Validation{
    public async is_password(text: string): Promise<boolean> {
        try {
            let api_settings = new APISettings();
            const apiResponse = await api_settings.response;
            
            console.log(apiResponse && apiResponse.data);
            
            return apiResponse && apiResponse.status === 200
                ? new RegExp(apiResponse.data.password_rule).test(text)
                : false;
        } catch (error: any) {
            console.error("API error:", error);
            return false;
        }
    }
    
    public is_number(str: string): boolean{
        return /^\d+$/.test(str);
    }

    public is_empty(str: string) {
        if (str.trim() == '') 
          return true;
          
        return false;
      }
}