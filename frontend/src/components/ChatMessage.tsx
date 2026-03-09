import type { ChatMessage as ChatMessageType } from "../types/chat";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`chat-message ${isUser ? "chat-message--user" : "chat-message--assistant"}`}
      data-role={message.role}
    >
      <div className="chat-message__avatar">
        {isUser ? (
          <span className="chat-message__avatar-icon" aria-hidden>U</span>
        ) : (
          <span className="chat-message__avatar-icon chat-message__avatar-icon--assistant" aria-hidden>W</span>
        )}
      </div>
      <div className="chat-message__content">
        <p className="chat-message__text">{message.content}</p>
      </div>
    </div>
  );
}
