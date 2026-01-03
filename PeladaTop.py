import streamlit as st
import random
import datetime
from zoneinfo import ZoneInfo

# ---- CSS customizado para layout ----
st.markdown(
    """
    <style>
/* Fundo geral */
.stApp {
    background-color: #f5f5f5;
}

/* Títulos e textos */
h1, h2, h3, p, label, .stMarkdown {
    color: #212121 !important;
    font-family: 'Arial', sans-serif;
}

/* Caixas de texto e área de texto */
textarea, input {
    background-color: #eeeeee !important; /* fundo cinza claro */
    color: #212121 !important;            /* texto digitado */
    border-radius: 6px !important;
    border: 1px solid #ccc !important;
    padding: 8px !important;
    font-size: 16px !important;
}

/* Botões */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #388E3C;
    color: #fff;
}

/* Cartões de times e fila */
.card {
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 10px;
    font-size: 18px;
    line-height: 1.6;
}
.timeA { background-color: #E8F5E9; } /* verde claro */
.timeB { background-color: #E3F2FD; } /* azul claro */
.fila  { background-color: #eeeeee; } /* cinza claro */

/* Mensagens de sucesso e alerta */
.stSuccess {
    background-color: #C8E6C9;
    color: #1B5E20;
    border-radius: 5px;
    padding: 8px;
}
.stWarning {
    background-color: #FFF9C4;
    color: #F57F17;
    border-radius: 5px;
    padding: 8px;
}

/* Layout responsivo para celular */
@media screen and (max-width: 600px) {
    .card {
        font-size: 16px;
        padding: 8px;
    }
    .stButton>button {
        width: 100%;
        margin-top: 5px;
    }
    textarea, input {
        font-size: 15px !important;
    }
}
</style>
    """,
    unsafe_allow_html=True
)

# ------------------ Estado inicial ------------------
def init_state():
    defaults = {
        "tela": 1,
        "jogadores": [],
        "qtd_por_time": 4,
        "minutos_partida": 7,
        "fila": [],
        "time_a": [],
        "time_b": [],
        "inicio_partida": None,
        "fim_partida": None,
        "partida_ativa": False,
        "confirm_remove": None,
        "confirm_team": None,
        "confirm_index": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ------------------ Utilidades ------------------
def distribuir_inicial():
    jogadores = st.session_state.jogadores.copy()
    random.shuffle(jogadores)
    st.session_state.fila = jogadores
    q = st.session_state.qtd_por_time
    st.session_state.time_a = st.session_state.fila[:q]
    st.session_state.fila = st.session_state.fila[q:]
    st.session_state.time_b = st.session_state.fila[:q]
    st.session_state.fila = st.session_state.fila[q:]

def repor_time_from_fila(time_key, index=None):
    if st.session_state.fila:
        substituto = st.session_state.fila.pop(0)
        if index is not None:
            st.session_state[time_key][index] = substituto
        else:
            q = st.session_state.qtd_por_time
            bloco = st.session_state.fila[:q]
            st.session_state.fila = st.session_state.fila[q:]
            st.session_state[time_key] = bloco

# ------------------ Tela 1 ------------------
if st.session_state.tela == 1:
    st.title("⚽ Organizar Futebol")

    novo = st.text_input("Nome do jogador")
    if st.button("➕ Adicionar jogador") and novo:
        st.session_state.jogadores.append(novo)
        st.success(f"{novo} adicionado!")

    lista = st.text_area("Ou cole uma lista de jogadores (um por linha)")
    if st.button("📥 Importar lista") and lista:
        nomes = [n.strip() for n in lista.split("\n") if n.strip()]
        st.session_state.jogadores.extend(nomes)
        st.success("Lista importada com sucesso!")

    st.subheader("Jogadores cadastrados")
    if st.session_state.jogadores:
        for i, j in enumerate(st.session_state.jogadores):
            c1, c2 = st.columns([3,1])
            c1.write(j)
            if c2.button("➖", key=f"rm_{i}"):
                st.session_state.jogadores.pop(i)
                st.rerun()
    else:
        st.info("Nenhum jogador cadastrado ainda.")

    st.session_state.qtd_por_time = st.number_input(
        "Quantidade de jogadores por time", min_value=1, max_value=11, value=4
    )
    st.session_state.minutos_partida = st.number_input(
        "Tempo da partida (minutos)", min_value=1, max_value=90, value=7
    )

    if st.button("⚽ Organizar Futebol"):
        distribuir_inicial()
        st.session_state.tela = 2
        st.rerun()

# ------------------ Tela 2 ------------------
elif st.session_state.tela == 2:
    st.title("🏟️ Partida em andamento")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card timeA">', unsafe_allow_html=True)
        st.subheader("Time A")
        for i, jogador in enumerate(st.session_state.time_a):
            c1, c2 = st.columns([3,1])
            c1.write(jogador)
            if c2.button("➖", key=f"rm_timea_{i}"):
                st.session_state.confirm_remove = jogador
                st.session_state.confirm_team = "time_a"
                st.session_state.confirm_index = i
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card timeB">', unsafe_allow_html=True)
        st.subheader("Time B")
        for i, jogador in enumerate(st.session_state.time_b):
            c1, c2 = st.columns([3,1])
            c1.write(jogador)
            if c2.button("➖", key=f"rm_timeb_{i}"):
                st.session_state.confirm_remove = jogador
                st.session_state.confirm_team = "time_b"
                st.session_state.confirm_index = i
        st.markdown('</div>', unsafe_allow_html=True)

    # Confirmação de remoção
    if st.session_state.confirm_remove:
        st.warning(f"Remover {st.session_state.confirm_remove} da partida?")
        c1, c2 = st.columns(2)
        if c1.button("✅ Confirmar remoção"):
            st.session_state.fila.append(st.session_state.confirm_remove)
            repor_time_from_fila(st.session_state.confirm_team, st.session_state.confirm_index)
            st.success("Substituição realizada com sucesso!")
            st.session_state.confirm_remove = None
            st.session_state.confirm_team = None
            st.session_state.confirm_index = None
            st.rerun()
        if c2.button("❌ Cancelar"):
            st.session_state.confirm_remove = None
            st.session_state.confirm_team = None
            st.session_state.confirm_index = None
            st.rerun()

    # Informativo de tempo
    st.subheader("⏱️ Tempo da partida")
    if st.button("▶️ Iniciar Partida"):
        st.session_state.partida_ativa = True
        st.session_state.inicio_partida = datetime.datetime.now(ZoneInfo("America/Sao_Paulo"))
        st.session_state.fim_partida = st.session_state.inicio_partida + datetime.timedelta(
            minutes=st.session_state.minutos_partida
        )

    if st.session_state.inicio_partida:
        st.write(f"🕒 Início: {st.session_state.inicio_partida.strftime('%H:%M')}")
        st.write(f"⏰ Fim previsto: {st.session_state.fim_partida.strftime('%H:%M')}")
        if datetime.datetime.now(ZoneInfo("America/Sao_Paulo")) >= st.session_state.fim_partida:
            st.markdown(
                """
                <audio autoplay>
                    <source src="https://www.soundjay.com/button/beep-07.wav" type="audio/wav">
                </audio>
                """,
                unsafe_allow_html=True,
            )
            st.warning("⏰ Tempo da partida encerrado!")

    if st.button("⏹️ Encerrar"):
        st.session_state.partida_ativa = False
        st.session_state.tela = 3
        st.rerun()

    # ➕ Adicionar novos jogadores durante a partida
    st.subheader("➕ Adicionar jogador à fila")
    novo_jogador = st.text_input("Nome do novo jogador", key="novo_jogador_fila")
    if st.button("➕ Adicionar na fila"):
        if novo_jogador:
            st.session_state.fila.append(novo_jogador)
            st.success(f"{novo_jogador} entrou na fila!")

    # 🔄 Fila dos próximos em blocos com opção de remover
    st.subheader("🔄 Fila de próximos jogadores")
    st.markdown('<div class="card fila">', unsafe_allow_html=True)
    q = st.session_state.qtd_por_time
    fila = st.session_state.fila
    blocos = [fila[i:i+q] for i in range(0, len(fila), q)]

    for idx, bloco in enumerate(blocos):
        st.markdown(f"**{idx+1}º Próximos:**")
        if bloco:
            for j, jogador in enumerate(bloco):
                c1, c2 = st.columns([3,1])
                c1.write(jogador)
                if c2.button("➖", key=f"rmfila_{idx}_{j}"):
                    st.session_state.fila.remove(jogador)
                    st.success(f"{jogador} removido da fila!")
                    st.rerun()

    st.markdown(f"**Total na fila: {len(fila)} jogadores**")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ Tela 3 ------------------
elif st.session_state.tela == 3:
    st.title("📊 Resultado da Partida")

    empate = st.radio("Deu empate?", ["Sim", "Não"])

    if empate == "Sim":
        preferencia = st.radio("Qual a preferência?", ["Time A", "Time B"])
        if st.button("✅ Confirmar Empate"):
            q_total = st.session_state.qtd_por_time * 2
            fila_disponivel = len(st.session_state.fila)

            if fila_disponivel < q_total:
                if preferencia == "Time A":
                    st.session_state.fila.extend(st.session_state.time_b)
                    repor_time_from_fila("time_b")
                else:
                    st.session_state.fila.extend(st.session_state.time_a)
                    repor_time_from_fila("time_a")
            else:
                st.session_state.fila.extend(st.session_state.time_a)
                st.session_state.fila.extend(st.session_state.time_b)
                if preferencia == "Time A":
                    st.session_state.fila.extend(st.session_state.time_b)
                else:
                    st.session_state.fila.extend(st.session_state.time_a)
                repor_time_from_fila("time_a")
                repor_time_from_fila("time_b")

            st.success("Empate registrado e times atualizados!")
            st.session_state.tela = 2
            st.rerun()

    else:
        perdedor = st.radio("Quem perdeu?", ["Time A", "Time B"])
        if st.button("✅ Confirmar Resultado"):
            if perdedor == "Time A":
                st.session_state.fila.extend(st.session_state.time_a)
                repor_time_from_fila("time_a")
            else:
                st.session_state.fila.extend(st.session_state.time_b)
                repor_time_from_fila("time_b")

            st.success("Resultado registrado e times atualizados!")
            st.session_state.tela = 2
            st.rerun()

    if st.button("⏹️ Encerrar Futebol"):
        for k in ["tela","time_a","time_b","fila","inicio_partida","fim_partida","partida_ativa",
                  "confirm_remove","confirm_team","confirm_index"]:
            st.session_state[k] = 1 if k=="tela" else (False if k=="partida_ativa" else None if "confirm" in k else [])
        st.session_state.jogadores = []
        st.success("⚽ Futebol encerrado! Tudo pronto para começar de novo.")
        st.rerun()