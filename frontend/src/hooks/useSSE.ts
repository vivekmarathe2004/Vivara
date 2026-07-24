import { useEffect, useState, useRef } from 'react';
import { createSSE } from '../api/client';

export function useSSE(url: string | null, onMessage: (data: any) => void) {
  const [connected, setConnected] = useState(false);
  const sseRef = useRef<EventSource | null>(null);
  const callbackRef = useRef(onMessage);

  useEffect(() => {
    callbackRef.current = onMessage;
  }, [onMessage]);

  useEffect(() => {
    if (!url) {
      if (sseRef.current) {
        sseRef.current.close();
        sseRef.current = null;
      }
      setConnected(false);
      return;
    }

    let isMounted = true;
    let sse: EventSource | null = null;

    const connect = () => {
      if (!isMounted) return;
      sse = createSSE(url, (data) => {
        if (callbackRef.current) {
          callbackRef.current(data);
        }
      });
      sseRef.current = sse;

      sse.onopen = () => {
        if (isMounted) setConnected(true);
      };

      sse.onerror = () => {
        if (isMounted) setConnected(false);
      };
    };

    connect();

    return () => {
      isMounted = false;
      if (sse) {
        sse.close();
      }
      setConnected(false);
    };
  }, [url]);

  return { connected };
}
