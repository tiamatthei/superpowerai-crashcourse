import asyncio
from pydantic_ai.result import StreamedRunResultSync
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

import logfire

logfire.configure()


if "message_history" not in st.session_state:
    st.session_state.message_history = []


def mostrar_mensajes():
    for message in st.session_state.message_history:
        parts = message.parts
        if isinstance(message, ModelRequest):
            user_parts = [p for p in parts if isinstance(p, UserPromptPart)]
            if not user_parts:
                continue
            with st.chat_message("user"):
                for part in user_parts:
                    c = part.content
                    if isinstance(c, str):
                        st.write(c)
                    else:
                        for item in c:
                            if isinstance(item, str):
                                st.write(item)

        elif isinstance(message, ModelResponse):
            final_parts = [
                p
                for p in parts
                if isinstance(p, ToolCallPart) and p.tool_name == "final_result"
            ]
            if not final_parts:
                continue
            with st.chat_message("assistant"):
                for part in final_parts:
                    args = part.args_as_dict()
                    title = args.get("title", "")
                    description = args.get("description", "")
                    if title:
                        st.write(f"**{title}**")
                    if description:
                        st.write(description)


async def main():
    st.title("Iván Torres del TVN")
    consulta = st.text_input("Hazme una pregunta", value="", key="consulta")

    if "consulta" in st.session_state:
        consulta = st.session_state.consulta
    else:
        consulta = ""

    if consulta:
        with st.spinner("Generando respuesta..."):
            # Aca consulto al agente
            async with ivan_torres.run_stream(consulta, message_history=st.session_state.message_history) as respuesta:
                async for event in respuesta.stream_output(debounce_by=0.2):
                    print(event, flush=True)
                    # st.write(event)

            st.session_state.message_history = respuesta.all_messages()

            mostrar_mensajes()


if __name__ == "__main__":
    asyncio.run(main())
