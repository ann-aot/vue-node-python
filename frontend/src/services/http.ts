import { API_BASE } from '../constants';

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

export async function http<T = unknown>(
  path: string,
  options?: { method?: HttpMethod; body?: unknown; headers?: Record<string, string> },
): Promise<T> {
  const { method = 'GET', body, headers = {} } = options ?? {};
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status} ${res.statusText}${text ? `: ${text}` : ''}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}
