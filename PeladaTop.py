import streamlit as st
import time

# Configurações iniciais (poderiam vir da planilha)
MINUTOS_PARTIDA = 5
EMPATE_PERMITIDO = True
PREFERENCIA_EMPATE = "Time A"  # ou "Time B"

# Estado inicial
if "time_a" not in st.session_state:
    st.session_state.time_a = ["Jg 3", "Jg 4"]
    st.session_state.time_b = ["Jg 5", "Jg 6"]
    st.session_state.fila = ["Jg 1", "Jg 2", "Jg 7", "Jg 8"]
    st.session_state.cronometro = MINUTOS_PARTIDA * 60
    st.session_state.partida_ativa = False

st.title("⚽ App de Partidas Amadoras")

# Mostrar times
st.subheader("Time A")
st.write(st.session_state.time_a)

st.subheader("Time B")
st.write(st.session_state.time_b)

st.subheader("Fila de Espera")
st.write(st.session_state.fila)

# Cronômetro
if st.session_state.partida_ativa:
    st.subheader("⏱️ Cronômetro")
    minutos = st.session_state.cronometro // 60
    segundos = st.session_state.cronometro % 60
    st.write(f"{minutos:02d}:{segundos:02d}")

# Botão iniciar partida
if st.button("Iniciar Partida"):
    st.session_state.partida_ativa = True
    st.session_state.cronometro = MINUTOS_PARTIDA * 60

# Botões de resultado
col1, col2, col3 = st.columns(3)

if col1.button("Time A perdeu"):
    st.session_state.fila.extend(st.session_state.time_a)
    st.session_state.time_a = st.session_state.fila[:len(st.session_state.time_a)]
    st.session_state.fila = st.session_state.fila[len(st.session_state.time_a):]

if col2.button("Time B perdeu"):
    st.session_state.fila.extend(st.session_state.time_b)
    st.session_state.time_b = st.session_state.fila[:len(st.session_state.time_b)]
    st.session_state.fila = st.session_state.fila[len(st.session_state.time_b):]

if col3.button("Empate"):
    if EMPATE_PERMITIDO:
        # Ambos vão para o fim da fila
        st.session_state.fila.extend(st.session_state.time_a)
        st.session_state.fila.extend(st.session_state.time_b)

        # Preferência define quem vai mais para o final
        if PREFERENCIA_EMPATE == "Time A":
            st.session_state.fila.extend(st.session_state.time_a)
        else:
            st.session_state.fila.extend(st.session_state.time_b)

        # Recarregar times
        tamanho_time = len(st.session_state.time_a)
        st.session_state.time_a = st.session_state.fila[:tamanho_time]
        st.session_state.fila = st.session_state.fila[tamanho_time:]

        tamanho_time = len(st.session_state.time_b)
        st.session_state.time_b = st.session_state.fila[:tamanho_time]
        st.session_state.fila = st.session_state.fila[tamanho_time:]