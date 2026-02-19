import streamlit as st
from src.agent import ivan_torres, IvanTorresOutput
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    FinalResultEvent,
)
from pydantic_ai.agent import (
    AgentRunResult,
)


if "message_history" not in st.session_state:
    st.session_state.message_history = []


def mostrar_mensajes():
    for message in st.session_state.message_history:
        parts = message.parts
        if isinstance(message, ModelRequest):
            with st.chat_message("user"):
                for part in parts:
                    if isinstance(part, UserPromptPart):
                        st.write(part)
                        
        elif isinstance(message, ModelResponse):
            with st.chat_message("assistant"):
                for part in parts:
                    if part.tool_name == "final_result":
                        st.write(part.args['title'])


def main():
    st.title("Iván Torres del TVN")
    consulta = st.text_input("Hazme una pregunta", value="", key="consulta")

    if "consulta" in st.session_state:
        consulta = st.session_state.consulta
    else:
        consulta = ""

    if consulta:
        with st.spinner("Generando respuesta..."):
            # Aca consulto al agente
            respuesta: AgentRunResult[IvanTorresOutput] = ivan_torres.run_sync(
                consulta,
                message_history=st.session_state.message_history,
            )

            st.session_state.message_history = respuesta.all_messages()
            
            mostrar_mensajes()


if __name__ == "__main__":
    main()
