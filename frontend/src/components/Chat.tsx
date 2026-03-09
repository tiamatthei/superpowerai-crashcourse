import { useRef, useEffect } from "react";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { useWeatherAgent } from "../hooks/useWeatherAgent";

export function Chat() {
  const { messages, streamingContent, isLoading, error, thinkingStatus, sendMessage, clearMessages } =
    useWeatherAgent();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, streamingContent, thinkingStatus]);

  return (
    <div className="chat">
      <header className="chat__header">
        <div className="chat__header-title">
          <span className="chat__header-icon">W</span>
          <h1>Clima Bot</h1>
        </div>
        <p className="chat__header-subtitle">
          Asistente meteorologico. Pregunta sobre temperatura, humedad o viento en cualquier ciudad.
        </p>
        <button
          type="button"
          className="chat__header-clear"
          onClick={clearMessages}
          aria-label="Limpiar conversacion"
        >
          Limpiar chat
        </button>
      </header>

      <div className="chat__messages" ref={scrollRef}>
        {messages.length === 0 && !streamingContent && (
          <div className="chat__empty">
            <p>Escribe un mensaje para preguntar sobre el clima.</p>
            <p className="chat__empty-hint">Ejemplo: &quot;Cual es la temperatura en Santiago?&quot;</p>
          </div>
        )}
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {thinkingStatus && !streamingContent && (
          <div className="chat-thinking" role="status" aria-live="polite">
            <span className="chat-thinking__dot" />
            <span className="chat-thinking__text">{thinkingStatus}</span>
          </div>
        )}
        {streamingContent && (
          <div className="chat-message chat-message--assistant" data-role="assistant">
            <div className="chat-message__avatar">
              <span className="chat-message__avatar-icon chat-message__avatar-icon--assistant" aria-hidden>W</span>
            </div>
            <div className="chat-message__content">
              <p className="chat-message__text chat-message__text--streaming">{streamingContent}</p>
              <span className="chat-message__cursor" aria-hidden />
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="chat__error" role="alert">
          {error}
        </div>
      )}

      <div className="chat__input-wrapper">
        <ChatInput onSend={sendMessage} disabled={isLoading} placeholder="Pregunta sobre el clima..." />
      </div>
    </div>
  );
}
