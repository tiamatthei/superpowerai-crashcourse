import asyncio
from pydantic_ai import TextPartDelta
from pydantic_ai.result import StreamedRunResultSync
import streamlit as st
from src.agent import ivan_torres, IvanTorresOutput
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartStartEvent,
    PartDeltaEvent,
    ToolCallPart,
    TextPart,
    TextPartDelta,
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
                    st.write(part.content)
                    # args = part.args_as_dict()
                    # title = args.get("title", "")
                    # description = args.get("description", "")
                    # if title:
                    #     st.write(f"**{title}**")
                    # if description:
                    #     st.write(description)


def mostrar_evento(event):
    if isinstance(event, FunctionToolCallEvent):
        st.write("Ejecutando" + event.part.tool_name)
    elif isinstance(event, FunctionToolResultEvent):
        st.write(event.result.tool_name + " ha devuelto " + str(event.result.content))


def mandar_texto_stremeado(event):
    if isinstance(event, PartStartEvent) and isinstance(event.part, TextPart):
        return event.part.content
    elif isinstance(event, PartDeltaEvent) and isinstance(event.delta, TextPartDelta):
        return event.delta.content_delta
    else:
        pass


async def message_manager(consulta):
    with st.spinner("Generando respuesta..."):
        # Aca consulto al agente
        async for event in ivan_torres.run_stream_events(
            consulta, message_history=st.session_state.message_history
        ):
            if isinstance(event, PartStartEvent) :
                if isinstance(event.part, TextPart):
                    yield mandar_texto_stremeado(event)
                    
                if isinstance(event.part, PartDeltaEvent):
                    yield mandar_texto_stremeado(event)
            # else:
            #     mostrar_evento(event)


def main():
    st.title("Iván Torres del TVN")
    consulta = st.text_input("Hazme una pregunta", value="", key="consulta")

    if "consulta" in st.session_state:
        consulta = st.session_state.consulta
    else:
        consulta = ""

    if consulta:
        st.write_stream(message_manager(consulta))


if __name__ == "__main__":
    main()
