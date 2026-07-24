import { useEffect, useState, useRef } from 'react';
import { createSSE } from '../api/client';

export function useSSE(url: string | null, onMessage: (data: any) => void) {
  const [connected, setConnected] = useState(false);
  const sseRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!url) {
      if (sseRef.current) {
        sseRef.current.close();
        sseRef.current = null;
      }
      setConnected(false);
      return;
    }

    const sse = createSSE(url, onMessage);
    sseRef.current = sse;

    sse.onopen = () => setConnected(true);
    sse.onerror = () => {
      setConnected(false);
      sse.close();
    };

    return () => {
      sse.close();
      setConnected(false);
    };
  }, [url]);

  return { connected };
}
