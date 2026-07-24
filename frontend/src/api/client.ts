const BASE = 'http://localhost:8000';

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(message: string, status: number, data?: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

function parseErrorMessage(status: number, bodyText: string, path: string): string {
  let detail = '';

  if (bodyText) {
    try {
      const json = JSON.parse(bodyText);
      if (json.detail) {
        if (typeof json.detail === 'string') {
          detail = json.detail;
        } else if (Array.isArray(json.detail)) {
          detail = json.detail.map((err: any) => err.msg || JSON.stringify(err)).join(', ');
        } else {
          detail = JSON.stringify(json.detail);
        }
      } else if (json.message) {
        detail = json.message;
      } else if (json.error) {
        detail = json.error;
      }
    } catch {
      detail = bodyText;
    }
  }

  if (status === 404) {
    const resourceDetail = detail || `Resource at '${path}' was not found.`;
    return `[404 Not Found] ${resourceDetail}`;
  }

  if (status === 500) {
    return `[500 Server Error] ${detail || 'An unexpected internal error occurred in Vivara backend.'}`;
  }

  return detail || `Request failed with status ${status}`;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${BASE}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
  } catch {
    throw new ApiError('Unable to connect to Vivara backend at http://localhost:8000. Please verify backend is running.', 0);
  }

  if (!response.ok) {
    const errorText = await response.text();
    const cleanMsg = parseErrorMessage(response.status, errorText, path);
    throw new ApiError(cleanMsg, response.status, errorText);
  }

  if (response.status === 204) return {} as T;

  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json();
  }
  return (await response.text()) as unknown as T;
}

export async function apiGet<T>(path: string): Promise<T> {
  return request<T>(path);
}

export async function apiPost<T>(path: string, body?: any): Promise<T> {
  return request<T>(path, {
    method: 'POST',
    body: body ? JSON.stringify(body) : undefined,
  });
}

export async function apiPut<T>(path: string, body?: any): Promise<T> {
  return request<T>(path, {
    method: 'PUT',
    body: body ? JSON.stringify(body) : undefined,
  });
}

export async function apiDelete<T = void>(path: string): Promise<T> {
  return request<T>(path, { method: 'DELETE' });
}

export function createSSE(path: string, onMessage: (data: any) => void): EventSource {
  const sse = new EventSource(`${BASE}${path}`);
  sse.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);
      onMessage(data);
    } catch {
      onMessage(e.data);
    }
  };
  return sse;
}
