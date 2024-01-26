import axios from "axios";

const getDeviceInfo = () => {
    if (typeof window !== 'undefined') {
      const userAgent = window.navigator.userAgent;
      const browserInfoArray = userAgent.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*([\d.]+)/i) || [];
      const browserName = browserInfoArray[1];
      const browserVersion = browserInfoArray[2];
      return {
        deviceName: browserName,
        deviceVersion: browserVersion,
      };
    } else {
      // Handle the case when window is not available (e.g., during server-side rendering)
      return {
        deviceName: 'unknown',
        deviceVersion: 'unknown',
      };
    }
  };
  
export const device = `MindfulGuard Web 0.0.0/${getDeviceInfo().deviceName} ${getDeviceInfo().deviceVersion}`;

console.log(process.env.NEXT_PUBLIC_API_BASE_URL)
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL,
  headers: {
    'Device': device,
  },
});

export const api_v1_auth_sign_up: string = "/v1/auth/sign_up";
export const api_v1_auth_sign_in_basic: string= '/v1/auth/sign_in?type=basic'
export const api_v1_auth_sign_in_backup: string= '/v1/auth/sign_in?type=backup'
export const api_v1_auth_sign_out: string= '/v1/auth/sign_out'
export const api_v1_public_configuration: string = "/v1/public/configuration";
export const api_v1_user = "/v1/user";
export const api_v1_safe = "/v1/safe";