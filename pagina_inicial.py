import streamlit as st
import pandas as pd
import sqlite3

# ======================== BANCO DE DADOS ========================

def criar_banco():
    conn = sqlite3.connect('usuario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escolhas (
            usuario TEXT,
            aula TEXT,
            dia TEXT,
            horarios TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_escolha(usuario, aula, dia, horarios):
    conn = sqlite3.connect('usuario.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO escolhas (usuario, aula, dia, horarios)
        VALUES (?, ?, ?, ?)
    ''', (usuario, aula, dia, ', '.join(horarios)))
    conn.commit()
    conn.close()

def buscar_aulas(usuario):
    conn = sqlite3.connect('usuario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT aula, dia, horarios FROM escolhas WHERE usuario = ?", (usuario,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# ======================== APP PRINCIPAL ========================

def app():
    criar_banco()

    if "logado" not in st.session_state or not st.session_state.logado:
        st.warning("Você precisa estar logado para acessar esta página.")
        st.stop()

    usuario = st.session_state["usuario"]

    # ============ MENU LATERAL ============
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Escolha uma opção:", ["Cadastrar aula", "Ver minhas aulas"])

    if menu == "Ver minhas aulas":
        st.title("Minhas Aulas")
        resultados = buscar_aulas(usuario)

        if resultados:
            df = pd.DataFrame(resultados, columns=["Aula", "Dia", "Horários"])
            df.index = range(1, len(df) + 1) 
            st.dataframe(df) 
        else:
            st.info("Você ainda não está cadastrado em nenhuma aula.")
        return  


    # ============ CADASTRO DE AULAS ============
    st.title("Cadastro de Aulas :")

    tabela = {
        'Aula': ["Musculação","Muay Thai", "Funcional", "Yoga", "Musculação", "Crossfit", "Zumba", "Pilates", 
                "Musculação", "Muay Thai", "Funcional", "Yoga", "Musculação", "Crossfit", "Zumba", "Pilates", 
                "Musculação", "Muay Thai", "Funcional", "Yoga", "Musculação", "Crossfit", "Zumba", "Funcional", "Fechada"],
        'Horário': ["06h00 - 22h00", "07h00 - 08h00", "19h00 - 20h00", "20h00 - 21h00", "06h00 - 22h00", "07h00 - 08h00", 
                    "18h00 - 19h00", "19h00 - 20h00", "06h00 - 22h00", "07h00 - 08h00", "19h00 - 20h00", "20h00 - 21h00", 
                    "06h00 - 22h00", "07h00 - 08h00", "18h00 - 19h00", "19h00 - 20h00", "06h00 - 22h00", "07h00 - 08h00", 
                    "19h00 - 20h00", "20h00 - 21h00", "08h00 - 14h00", "09h00 - 10h00", "10h00 - 11h00", "10h00 - 11h00", "-"]
    }

    df = pd.DataFrame(tabela, index=[
        "Segunda", "Segunda", "Segunda", "Segunda", "Terça", "Terça", "Terça", "Terça", 
        "Quarta", "Quarta", "Quarta", "Quarta", "Quinta", "Quinta", "Quinta", "Quinta", 
        "Sexta", "Sexta", "Sexta", "Sexta", "Sábado", "Sábado", "Sábado", "Sábado", "Domingo"
    ])

    st.dataframe(df)

    aula = st.selectbox("Selecione a aula:", ["Musculação", "Muay Thai", "Funcional", "Yoga", "Crossfit", "Zumba", "Pilates"])
    dia = None
    horarios = []

    if aula == "Musculação":
        dia = st.selectbox("Selecione o dia:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"])
        horarios = st.multiselect("Escolha os horários:", 
            ["6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", 
             "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
            if dia != "Sábado" else
            ["6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00"])

    elif aula in ["Muay Thai", "Funcional", "Yoga"]:
        dias_validos = {"Muay Thai": ["Segunda", "Quarta", "Sexta"],
                        "Funcional": ["Segunda", "Quarta", "Sexta"],
                        "Yoga": ["Segunda", "Quarta", "Sexta"]}
        horarios_opcao = {"Muay Thai": ["7:00", "8:00"],
                          "Funcional": ["19:00", "20:00"],
                          "Yoga": ["20:00", "21:00"]}
        dia = st.selectbox("Selecione o dia:", dias_validos[aula])
        horarios = st.multiselect("Escolha os horários:", horarios_opcao[aula])

    elif aula == "Crossfit":
        dia = st.selectbox("Selecione o dia:", ["Terça", "Quinta", "Sábado"])
        horarios = st.multiselect("Escolha os horários:", ["7:00", "8:00"] if dia != "Sábado" else ["9:00", "10:00"])

    elif aula == "Zumba":
        dia = st.selectbox("Selecione o dia:", ["Terça", "Quinta", "Sábado"])
        horarios = st.multiselect("Escolha os horários:", ["18:00", "19:00"] if dia != "Sábado" else ["10:00", "11:00"])

    elif aula == "Pilates":
        dia = st.selectbox("Selecione o dia:", ["Terça", "Quinta"])
        horarios = st.multiselect("Escolha os horários:", ["19:00", "20:00"])

    if st.button("Se cadastre"):
        if aula and dia and horarios:
            try:
                salvar_escolha(usuario, aula, dia, horarios)
                st.success("Escolha salva com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.error("Você precisa selecionar a aula, dia e pelo menos um horário.")

