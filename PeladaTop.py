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
    white-space: nowrap; /* evita quebra de linha */
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

/* Ajuste para alinhar nome + botão na mesma linha */
.player-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
}

/* Layout responsivo para celular */
@media screen and (max-width: 600px) {
    .card {
        font-size: 16px;
        padding: 8px;
    }
    .stButton>button {
        font-size: 14px;
        padding: 6px 12px;
    }
    textarea, input {
        font-size: 15px !important;
    }
}
</style>