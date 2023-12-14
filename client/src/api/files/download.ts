import { Headers } from "@/types/global";
import { api, api_v1_safe } from "../api";

export class APIFileDownload {
  private token: string;

  constructor(token: string) {
    this.token = token;
  }

  public async execute(fileObject: any): Promise<void> {
    try {
      const headers: Headers = {
        'Authorization': `Bearer ${this.token}`,
      };

      const response = await api.get(
        `/v1/${fileObject.content_path}`,
        {
          headers: headers,
          responseType: 'blob',
        }
      );

      // Extract filename from the object
      const filename = fileObject.name;

      // Create a blob from the response data
      const blob = new Blob([response.data], { type: response.headers['content-type'] });

      // Create a link element and trigger a click to start the download
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();

      // Clean up resources
      document.body.removeChild(link);
      window.URL.revokeObjectURL(link.href);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  }
}
