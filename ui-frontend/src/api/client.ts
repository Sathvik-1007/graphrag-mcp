import type {
  GraphResponse,
  EntityResponse,
  SearchResponse,
  StatsResponse,
} from "../types/graph";

const BASE = "/api";

async function request<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

export function fetchGraph(
  limit = 200,
  entityTypes?: string[]
): Promise<GraphResponse> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (entityTypes?.length) {
    params.set("entity_types", entityTypes.join(","));
  }
  return request<GraphResponse>(`/graph?${params}`);
}

export function fetchEntity(name: string): Promise<EntityResponse> {
  return request<EntityResponse>(`/entity/${encodeURIComponent(name)}`);
}

export function fetchSearch(
  query: string,
  limit = 10,
  entityTypes?: string[]
): Promise<SearchResponse> {
  const params = new URLSearchParams({ q: query, limit: String(limit) });
  if (entityTypes?.length) {
    params.set("entity_types", entityTypes.join(","));
  }
  return request<SearchResponse>(`/search?${params}`);
}

export function fetchStats(): Promise<StatsResponse> {
  return request<StatsResponse>("/stats");
}
