import ky from 'ky';
import type { PurchaseInvoice } from './invoiceTypes';
import { validatePurchaseInvoice } from './invoiceTypes';

interface SiigoConfig {
  baseURL: string;
  apiBaseURL: string;
  username: string;
  accessKey: string;
  partnerId: string;
  accessToken?: string;
}

class ApiRequester {
  private config: SiigoConfig;

  constructor(config: SiigoConfig) {
    this.config = config;
  }

  private getAuthHeaders() {
    return {
      'Content-Type': 'application/json',
      'Partner-Id': this.config.partnerId,
    };
  }

  private getHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.config.accessToken}`,
      'Partner-Id': this.config.partnerId,
    };
  }

  async authenticate(): Promise<void> {
    try {
      const response = await ky.post(`${this.config.baseURL}/auth`, {
        json: {
          username: this.config.username,
          access_key: this.config.accessKey,
        },
        headers: this.getAuthHeaders(),
      }).json();
      this.config.accessToken = (response as any).access_token;
      console.log('✅ Authentication successful');
    } catch (error) {
      throw new Error(`Authentication failed: ${error}`);
    }
  }

  async get(endpoint: string, params?: Record<string, any>): Promise<any> {
    try {
      const url = new URL(endpoint, this.config.apiBaseURL);
      if (params) {
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
      }
      return await ky.get(url.toString(), { headers: this.getHeaders() }).json();
    } catch (error) {
      throw new Error(`GET request failed: ${error}`);
    }
  }

  async post(endpoint: string, data: any): Promise<any> {
    try {
      return await ky.post(`${this.config.apiBaseURL}${endpoint}`, {
        json: data,
        headers: this.getHeaders(),
      }).json();
    } catch (error) {
      throw new Error(`POST request failed: ${error}`);
    }
  }

  async put(endpoint: string, data: any): Promise<any> {
    try {
      return await ky.put(`${this.config.apiBaseURL}${endpoint}`, {
        json: data,
        headers: this.getHeaders(),
      }).json();
    } catch (error) {
      throw new Error(`PUT request failed: ${error}`);
    }
  }

  async delete(endpoint: string): Promise<any> {
    try {
      return await ky.delete(`${this.config.apiBaseURL}${endpoint}`, {
        headers: this.getHeaders(),
      }).json();
    } catch (error) {
      throw new Error(`DELETE request failed: ${error}`);
    }
  }

  async createPurchaseInvoice(invoiceData: unknown): Promise<any> {
    try {
      const validatedData = validatePurchaseInvoice(invoiceData);
      return await ky.post(`${this.config.baseURL}/v1/purchases`, {
        json: validatedData,
        headers: this.getHeaders(),
      }).json();
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Failed to create purchase invoice: ${error.message}`);
      }
      throw new Error(`Failed to create purchase invoice: ${error}`);
    }
  }
}

export default ApiRequester;
