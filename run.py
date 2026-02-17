import streamlit as st
from src import llamar_ivan
from langchain.messages import HumanMessage, AIMessage


if "message_history" not in st.session_state:
    st.session_state.message_history = []


def mostrar_mensajes():
    for message in st.session_state.message_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)


def main():
    st.title("Iván Torres del TVN")
    consulta = st.text_input("Hazme una pregunta", value="", key="consulta")
    
    if "consulta" in st.session_state:
        consulta = st.session_state.consulta
    else:
        consulta = ""

    
    if consulta:
        st.session_state.message_history.append(HumanMessage(content=consulta))
        
        with st.spinner("Generando respuesta..."):
            respuesta = llamar_ivan(consulta, message_history=st.session_state.message_history)
            data = respuesta["messages"][-1]
            content = data.content
            texto = content[0]["text"] if isinstance(content, list) else None
            if isinstance(content, list):
                texto = content[0]["text"]
            else:
                texto = content
            
            st.session_state.message_history.append(AIMessage(content=texto))
            mostrar_mensajes()
    
if __name__ == "__main__":
    main()









