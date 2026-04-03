import { useEffect, useRef, useState, useCallback } from "react";
import { fetchSearch } from "../api/client";
import type { SearchResponse } from "../types/graph";

export function useSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout>>(null);
  const abortRef = useRef<AbortController | null>(null);

  const search = useCallback((q: string) => {
    setQuery(q);
  }, []);

  const clearSearch = useCallback(() => {
    setQuery("");
    setResults(null);
    // Cancel in-flight request
    if (abortRef.current) {
      abortRef.current.abort();
      abortRef.current = null;
    }
  }, []);

  useEffect(() => {
    if (timerRef.current) clearTimeout(timerRef.current);

    if (!query.trim()) {
      setResults(null);
      setLoading(false);
      return;
    }

    // Debounce 150ms (reduced from 300 — local results show instantly anyway)
    timerRef.current = setTimeout(async () => {
      // Cancel previous in-flight request
      if (abortRef.current) abortRef.current.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      setLoading(true);
      try {
        const data = await fetchSearch(query.trim());
        // Only update if this request wasn't aborted
        if (!controller.signal.aborted) {
          setResults(data);
        }
      } catch {
        if (!controller.signal.aborted) {
          setResults(null);
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }, 150);

    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [query]);

  return { query, results, loading, search, clearSearch };
}
