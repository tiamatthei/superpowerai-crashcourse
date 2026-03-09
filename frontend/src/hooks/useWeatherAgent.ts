import { useCallback, useRef, useState } from "react";
import { HttpAgent } from "@ag-ui/client";
import type { ChatMessage } from "../types/chat";

const AGENT_URL = "http://localhost:8000/weather-agent";

function createAgent() {
  return new HttpAgent({
    url: AGENT_URL,
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
  });
}

const TOOL_LABELS: Record<string, string> = {
  get_temperature: "temperatura",
  get_humidity: "humedad",
  get_wind_speed: "viento",
};

function toolLabel(name: string): string {
  return TOOL_LABELS[name] ?? name;
}

export function useWeatherAgent() {
  const agentRef = useRef<HttpAgent | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [streamingContent, setStreamingContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [thinkingStatus, setThinkingStatus] = useState<string | null>(null);

  const getAgent = useCallback(() => {
    if (!agentRef.current) {
      agentRef.current = createAgent();
    }
    return agentRef.current;
  }, []);

  const sendMessage = useCallback(
    async (userContent: string) => {
      if (!userContent.trim() || isLoading) return;

      setError(null);
      setIsLoading(true);
      setStreamingContent("");
      setThinkingStatus(null);

      const agent = getAgent();
      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: userContent.trim(),
      };
      setMessages((prev) => [...prev, userMessage]);

      const agMessages = [
        ...messages.map((m) => ({
          id: m.id,
          role: m.role,
          content: m.content,
        })),
        { id: userMessage.id, role: "user" as const, content: userContent.trim() },
      ];

      agent.setMessages(agMessages);

      try {
        await agent.runAgent(
          undefined,
          {
            onRunStartedEvent: () => {
              setThinkingStatus("Pensando...");
            },
            onToolCallStartEvent: ({ event }) => {
              const name = (event as { toolCallName?: string }).toolCallName;
              setThinkingStatus(name ? `Consultando ${toolLabel(name)}...` : "Pensando...");
            },
            onToolCallResultEvent: () => {
              setThinkingStatus("Procesando resultados...");
            },
            onTextMessageStartEvent: () => {
              setThinkingStatus(null);
            },
            onTextMessageContentEvent: ({ textMessageBuffer }) => {
              setStreamingContent(textMessageBuffer);
            },
            onTextMessageEndEvent: ({ textMessageBuffer }) => {
              setStreamingContent("");
              setMessages((prev) => [
                ...prev,
                {
                  id: crypto.randomUUID(),
                  role: "assistant",
                  content: textMessageBuffer,
                },
              ]);
            },
            onRunErrorEvent: ({ event }) => {
              const errMsg =
                typeof (event as { message?: string }).message === "string"
                  ? (event as { message: string }).message
                  : "Error desconocido";
              setError(errMsg);
            },
          }
        );
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Error de conexion con el agente";
        setError(msg);
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: "assistant",
            content: `Error: ${msg}. Verifica que el backend este corriendo en http://localhost:8000`,
          },
        ]);
      } finally {
        setIsLoading(false);
        setStreamingContent("");
        setThinkingStatus(null);
      }
    },
    [getAgent, isLoading, messages]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setStreamingContent("");
    setError(null);
    setThinkingStatus(null);
  }, []);

  return {
    messages,
    streamingContent,
    isLoading,
    error,
    thinkingStatus,
    sendMessage,
    clearMessages,
  };
}
