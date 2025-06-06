import streamlit as st
import sqlite3
import bdados as bd


def app():

    conn = sqlite3.connect("bcodds.db")

    cursor = conn.cursor()

    bd.cria_db()


    st.set_page_config(page_icon=("🏋🏼‍♀️"),page_title=("Academia"))

    st.title("Olá, Seja bem vindo a ACADEMIA")
    st.write("Esse é a melhor academia que você vai ver")

    if "usuarios" not in st.session_state:
        st.session_state.usuarios = {"admin": "1234"}

    # salvar o login
    if "logado" not in st.session_state:
        st.session_state.logado = False

    # login
    def login():
        st.title("Login")

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        

        if st.button("Entrar"):
            if bd.verificar_login(usuario, senha):
                st.session_state.logado = True
                st.session_state["usuario"]  =  usuario  
                st.success(f"Bem-vindo, {usuario}!")
                st.session_state["pagina"] = "pagina_inicial"  # redireciona pra página inicial
            else:
                st.error("Usuário ou senha inválidos.")

        st.markdown("---")
        if st.button("Criar Usuário"):
            st.session_state["pagina"] = "cadastro"
            return usuario

    # cadastro
    def cadastro():        

        st.title("Cadastro")

        novo_usuario = st.text_input("Novo usuário")
        nova_senha = st.text_input("Nova senha", type="password")

        if st.button("Cadastrar"):
            if novo_usuario in st.session_state.usuarios:
                st.warning("Usuário já existe!")                
            else:
                conn = sqlite3.connect("bcodds.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (novo_usuario, nova_senha))
                conn.commit()
                conn.close()
                st.session_state.usuarios[novo_usuario] = nova_senha
                st.success("Cadastro realizado com sucesso!")
                st.session_state["pagina"] = "login"
            
        st.markdown("---")
        if st.button("Voltar para Login"):
            st.session_state["pagina"] = "login"

    # mudar de pg
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "login"
        st.switch_page("main.py")

    if not st.session_state.logado:
        if st.session_state["pagina"] == "login":
            login()
        else:
            cadastro()
    else:
        st.title("Área Logada")
        st.write("Você está logado no sistema.")
        if st.button("Sair"):
            st.session_state.logado = False
            st.session_state.pagina = "login"
