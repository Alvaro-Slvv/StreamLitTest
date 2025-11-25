from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

st.set_page_config(page_title="Saraswati", page_icon="🪷")

col_title, col_config = st.columns([3, 2])

with col_title:
    st.title("Ask Saraswati!")
    st.markdown("Knowledge in one touch")

st.sidebar.header("Configuración del modelo")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        SystemMessage(
            content=(
                "Eres un asistente útil llamado Saraswati. "
                "Responde de forma clara y concisa."
            )
        )
    ]

if "mostrar_sugerencias" not in st.session_state:
    st.session_state.mostrar_sugerencias = True

if "pregunta_desde_sugerencia" not in st.session_state:
    st.session_state.pregunta_desde_sugerencia = None

modelo = st.sidebar.selectbox(
    "Selecciona el modelo",
    [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ],
    index=0,
)

temperatura = st.sidebar.slider(
    "Temperatura",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.05,
    help="Valores bajos = respuestas más deterministas; valores altos = más creativas",
)

if st.sidebar.button("🧹 Borrar conversación"):
    st.session_state.mensajes = [
        SystemMessage(
            content=(
                "Eres un asistente útil llamado Saraswati. "
                "Responde de forma clara y concisa."
            )
        )
    ]
    st.session_state.mostrar_sugerencias = True
    st.session_state.pregunta_desde_sugerencia = None
    st.rerun()

with col_config:
    st.markdown(
        f"""
        <div style="text-align: right; font-size: 0.9rem; opacity: 0.8;">
            <b>Modelo:</b> {modelo}<br>
            <b>Temperatura:</b> {temperatura}
        </div>
        """,
        unsafe_allow_html=True,
    )

chat_model = ChatGoogleGenerativeAI(
    model=modelo,
    temperature=temperatura,
)

for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue  

    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.session_state.mostrar_sugerencias:
    st.caption("Sugerencias:")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💡 Fotosíntesis"):
            st.session_state.pregunta_desde_sugerencia = (
                "Explícame la fotosíntesis como si tuviera 10 años."
            )
            st.session_state.mostrar_sugerencias = False
            st.rerun()

    with col2:
        if st.button("💻 Ayúdame con Python"):
            st.session_state.pregunta_desde_sugerencia = (
                "Enséñame un ejemplo simple de función en Python."
            )
            st.session_state.mostrar_sugerencias = False
            st.rerun()

    with col3:
        if st.button("📚 ¿Puedes resumir un texto?"):
            st.session_state.pregunta_desde_sugerencia = (
                "¿Puedes resumir un texto si te lo pego?"
            )
            st.session_state.mostrar_sugerencias = False
            st.rerun()

pregunta_input = st.chat_input("Escribe tu mensaje:")

pregunta = None
if st.session_state.pregunta_desde_sugerencia is not None:
    pregunta = st.session_state.pregunta_desde_sugerencia
    st.session_state.pregunta_desde_sugerencia = None
elif pregunta_input:
    pregunta = pregunta_input

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            respuesta = chat_model.invoke(st.session_state.mensajes)
            st.markdown(respuesta.content)

    st.session_state.mensajes.append(respuesta)
