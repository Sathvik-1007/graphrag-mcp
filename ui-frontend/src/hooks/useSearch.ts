import { useEffect, useRef, useState, useCallback } from "react";
import { fetchSearch } from "../api/client";
import type { SearchResponse } from "../types/graph";

export function useSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout>>(null);

  const search = useCallback((q: string) => {
    setQuery(q);
  }, []);

  const clearSearch = useCallback(() => {
    setQuery("");
    setResults(null);
  }, []);

  useEffect(() => {
    if (timerRef.current) clearTimeout(timerRef.current);

    if (!query.trim()) {
      setResults(null);
      return;
    }

    timerRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await fetchSearch(query.trim());
        setResults(data);
      } catch {
        setResults(null);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [query]);

  return { query, results, loading, search, clearSearch };
}
